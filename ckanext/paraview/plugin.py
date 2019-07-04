import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import os

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

    #TODO: update for DICOM

    # dictionary with metadata about the package
    pkg_dict = toolkit.get_action('package_show')({}, {'id': package_id})
    # list of dictionaries of metadata about each resource in the package
    resources = pkg_dict['resources']

    # iterate through the list of resources and create the .stl links if they
    # don't exist yet
    for resource in resources:
        # check if the file is actually an STL file; only process it if it is
        if resource['format'] == 'STL':
            resource_id = resource["id"]
            try:
                f = open("/var/lib/ckan/default/pvw/" + package_id + "/" + \
                        resource_id + ".stl")
                f.close()
            except IOError:
                # create the link if it doesn't exist
                src = "/var/lib/ckan/default/resources/" + resource_id[0:3] + \
                    "/" + resource_id[3:6] + "/" + resource_id[6:]
                dst = "/var/lib/ckan/default/pvw/" + package_id + "/" + resource_id + ".stl"
                try:
                    os.link(src, dst)
                except OSError:
                    # sometimes we have to create the dataset directory to contain
                    # the .stl resource files
                    os.mkdir("/var/lib/ckan/default/pvw/" + package_id)
                    os.link(src, dst)
    return ""

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
        # TODO: add DICOM files
        resource = data_dict["resource"]
        return (resource.get('format', '').lower() in ['stl'])

    # TODO: implement setup_template_variables?
    # this is probably where you'll pass the file to open
    # what exactly is this supposed to return
    def setup_template_variables(self, context, data_dict):
        return data_dict

    def view_template(self, context, data_dict):
        return "pvw_view.html"

    # IResourceController

    def before_delete(self, context, resource, resources):
        '''
        If a file has been opened with the PVW Visualizer, an extra file has
        been created with a file extension allowing the Visualizer to
        recognize its type. This function deletes that extra file when the
        original resource is deleted.
        '''
        filename = resource["id"] + ".stl"
        path = ""
        # we don't know the package ID of the dataset the resource belongs to,
        # so we need to manually find the name ofthe directory that contains
        # the .stl file
        for dirname, dirs, files in os.walk("/var/lib/ckan/default/pvw/"):
            if filename in files:
                path = os.path.join(dirname, filename)
        # TODO: update for DICOM
        try:
            os.remove(path)
        except:
            pass

    # IPackageController

    def after_delete(self, context, pkg_dict):
        '''
        If any files in this dataset have been opened with the PVW Visualizer,
        then a directory was created to hold their .stl openable files. This
        function deletes that directory (and any files in it) when the dataset
        is deleted.
        '''
        path = "/var/lib/ckan/default/pvw/" + pkg_dict["id"]
        try:
            os.system("rm -rf " + path)
            return pkg_dict
        except:
            return pkg_dict

    # ITemplateHelpers

    def get_helpers(self):
        return {"paraview_add_links": add_links}
