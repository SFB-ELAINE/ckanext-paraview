import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import os
import re

def add_links (package_id):
    '''
    Called in pvw_view.html when a user tries to open a resource using this view.
    The PVW Visualizer only displays files whose types it can recognize, so
    this function creates hard links for the resources in the same dataset as the
    viewed resource to file names with .stl extensions, which allows the
    Visualizer to open the files in the view. Since a user might want to view
    more than one file at once, all files in the dataset are processed and
    put into the same directory where they are all accessible from any
    resource's view. Each time the view is opened, we check to make sure that all
    resources in the dataset have been processed, since more may have been added
    since the last time someone viewed the dataset.

    :returns: None
    '''

    #TODO: update for other file types
    # get dictionary with metadata about the package
    pkg_dict = toolkit.get_action('package_show')({}, {'id': package_id})
    # list of dictionaries of metadata about each resource in the package
    resources = pkg_dict['resources']

    # iterate through the list of resources and create the .stl links if they
    # don't exist yet
    for resource in resources:
        # check if the file is actually an STL file; only process it if it is
        # TODO: update for other file formats
        if resource['format'] == 'STL':
            resource_id = resource["id"]
            resource_name = resource["name"]

            # TODO: update for other file formats
            # check whether the resource name ends with the correct file extension
            pattern = r".*\.stl$"
            regexp = re.compile(pattern)
            result = regexp.search(resource_name)
            # if no match, add the file extension to the resource name
            if (result == None):
                resource_name += ".stl"

            # attempt to open the file - if this fails, then the file doesn't exist
            # and we need to create it
            try:
                f = open("/var/lib/ckan/default/pvw/" + package_id + "/" + resource_name)
                f.close()
            except IOError:
                # create the link if it doesn't exist
                src = "/var/lib/ckan/default/resources/" + resource_id[0:3] + \
                    "/" + resource_id[3:6] + "/" + resource_id[6:]
                dst = "/var/lib/ckan/default/pvw/" + package_id + "/" + resource_name
                # try to create the link - this may fail if the dataset directory for links
                # doesn't exist yet
                try:
                    os.link(src, dst)
                except OSError:
                    # create the directory to hold links to files in this dataset
                    # and then create the link
                    os.makedirs("/var/lib/ckan/default/pvw/" + package_id)
                    os.link(src, dst)
    return ""

def delete_resource_link(resource):
    '''
    If a file has been opened with the PVW Visualizer, an extra file has
    been created with a file extension allowing the Visualizer to
    recognize its type. This function deletes that extra file when the
    original resource is deleted.
    '''
    # TODO: update for other file types

    # get the human-readable name of the file
    resource_dict = toolkit.get_action("resource_show")({}, {"id": resource["id"]})
    filename = resource_dict["name"]
    path = ""

    # check whether the resource name ends with the correct file extension
    pattern = r".*\.stl$"
    regexp = re.compile(pattern)
    result = regexp.search(filename)
    # if no match, add the file extension to the resource name
    if (result == None):
        filename += ".stl"

    # we don't know the package ID of the dataset the resource belongs to,
    # so we need to manually find the name of the directory that contains
    # the .stl file
    for dirname, dirs, files in os.walk("/var/lib/ckan/default/pvw/"):
        if filename in files:
            path = os.path.join(dirname, filename)

    try:
        os.remove(path)
    except:
        pass

class ParaviewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'paraview')

    # IResourceView

    def info(self):
        return { "name": "paraview",
            "title": toolkit._("ParaView Visualizer"),
            "icon": "cube",
            "default_title": toolkit._("ParaView Visualizer"),
            "iframed": False
        }

    def can_view(self, data_dict):
        # right now, we can only view STL files with the extension
        # TODO: update for other file types
        resource = data_dict["resource"]
        return (resource.get('format', '').lower() in ['stl'])

    def setup_template_variables(self, context, data_dict):
        return data_dict

    def view_template(self, context, data_dict):
        return "pvw_view.html"

    # IResourceController

    def before_delete(self, context, resource, resources):
        delete_resource_link(resource)

    def before_update(self, context, current, resource):
        delete_resource_link(current)

    # IPackageController

    def after_delete(self, context, pkg_dict):
        '''
        If any files in this dataset have been opened with the PVW Visualizer,
        then a directory was created to hold their .stl openable files. This
        function deletes that directory (and any files in it) when the dataset
        is deleted.
        '''
        path = ""
        # try to create the path to the directory to delete
        # if we don't get passed the correct thing, this will fail -
        # in that case, just return the pkg_dict
        try:
            path = "/var/lib/ckan/default/pvw/" + pkg_dict["id"]
        except TypeError:
            return pkg_dict

        # if it didn't fail, try to delete the directory (and just exit if
        # this fails too)
        try:
            os.system("rm -rf " + path)
        except:
            pass
        return pkg_dict

    # ITemplateHelpers

    def get_helpers(self):
        return {"paraview_add_links": add_links}
