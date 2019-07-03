import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import os

def add_link (resource_id):
    '''
    Called in pvw_view.html to add a file extension to a file that is about to
    be rendered with the PVW Visualizer (because the Visualizer won't open
    files that do not have a file extension, since it can't tell how it should
    render them). Checks if a file with the extension exists; if it doesn't,
    creates a hard link to a new file with the extension. A hard link is
    deleted when the associated resource is deleted.

    :param resource_id: the ID of the resource to be opened; provides us with
    the path to the resource's file
    :type resource_id: string

    :returns: None
    '''
    # TODO: this could probably be done in IResourecController after_create()
    # TODO: update for DICOM
    try:
        f = open("/var/lib/ckan/default/pvw/" + \
                resource_id + ".stl")
        f.close()
        return ""
    except IOError:
        src = "/var/lib/ckan/default/resources/" + resource_id[0:3] + \
            "/" + resource_id[3:6] + "/" + resource_id[6:]
        dst = "/var/lib/ckan/default/pvw/" + resource_id + ".stl"
        os.link(src, dst)
        return ""

class ParaviewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)
    plugins.implements(plugins.IResourceController)
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

    def before_create(self, context, resource):
        pass

    def after_create(self, context, resource):
        pass

    def before_update(self, context, current, resource):
        pass

    def after_update(self, context, resource):
        pass

    def before_delete(self, context, resource, resources):
        '''
        If a file has been opened with the PVW Visualizer, an extra file has
        been created with a file extension allowing the Visualizer to
        recognize its type. This function deletes that extra file when the
        original resource is deleted.
        '''
        # TODO: update for DICOM
        path = "/var/lib/ckan/default/pvw/" + resource["id"] + ".stl"
        try:
            os.remove(path)
        except:
            pass


    def after_delete(self, context, resources):
        pass

    def before_show(self, resource_dict):
        pass


    # ITemplateHelpers

    def get_helpers(self):
        return {"paraview_add_link": add_link}
