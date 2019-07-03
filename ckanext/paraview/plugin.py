import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import os

def add_link (resource_id):
    # CANNOT just rename the file - then CKAN can't find it
    # also cannot just symlink; pvw won't open it
    try:
        f = open("/var/lib/ckan/default/pvw/" + \
                resource_id + ".stl")
        f.close()
        return resource_id[0:3] + "/" + resource_id[3:6] + "/" + \
            resource_id[6:] + " symlink exists"
    except IOError:

        src = "/var/lib/ckan/default/resources/" + resource_id[0:3] + \
            "/" + resource_id[3:6] + "/" + resource_id[6:]
        dst = "/var/lib/ckan/default/pvw/" + resource_id + ".stl"

        os.link(src, dst)

        return resource_id[0:3] + "/" + resource_id[3:6] + "/" + \
            resource_id[6:] + " symlink created"


class ParaviewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)
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
        resource = data_dict["resource"]
        return (resource.get('format', '').lower() in ['stl', 'dcm'])

    # TODO: implement setup_template_variables?
    # this is probably where you'll pass the file to open
    # what exactly is this supposed to return
    def setup_template_variables(self, context, data_dict):
        return data_dict

    def view_template(self, context, data_dict):
        return "pvw_view.html"

    # ITemplateHelpers
    def get_helpers(self):
        return {"paraview_add_link": add_link}
