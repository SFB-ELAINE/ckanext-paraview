.. image:: https://travis-ci.org/SFB-ELAINE/ckanext-paraview.svg?branch=master
    :target: https://travis-ci.org/SFB-ELAINE/ckanext-paraview

.. image:: https://coveralls.io/repos/SFB-ELAINE/ckanext-paraview/badge.svg
  :target: https://coveralls.io/r/SFB-ELAINE/ckanext-paraview

.. image:: https://pypip.in/download/ckanext-paraview/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-paraview/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-paraview/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-paraview/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-paraview/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-paraview/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-paraview/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-paraview/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-paraview/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-paraview/
    :alt: License

=====================
ckanext-paraview
=====================

This is an extension for CKAN that uses the ParaViewWeb Visualizer to provide views
for STL files. In the future, it will also provide views for DICOM files (and
hopefully other types as well).

This extension is designed to be used jointly with a ParaViewWeb server running
in a container built from the Dockerfile here: https://gitlab.elaine.uni-rostock.de/hl201/paraview-docker.
This server is configured to work with this extension, and another server with
slightly different configurations will not work correctly. It is also designed
to be run from a CKAN instance in a Docker container built from the Dockerfile here:
https://gitlab.elaine.uni-rostock.de/INF/datahub/datahub-docker and run using the
``startckan`` script in that repository. This will set up the Docker volumes correctly
for files to be shared between the CKAN and ParaViewWeb containers, which is necessary
for the ParaViewWeb server to render files stored in the CKAN datahub instance.


------------
Requirements
------------

Tested with CKAN 2.8.2.

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-paraview:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-paraview Python package into your virtual environment::

     pip install -e pip install -e git+https://github.com/SFB-ELAINE/ckanext-paraview.git#egg=ckanext-paraview

3. Add ``paraview`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Add ``paraview`` to the ``ckan.views.default_views`` setting located in the same
   config file.

5. For CKAN to recognize STL files, add the following line to the list of allowed
   resource formats in `ckan/config/resource_formats.json``::

    ["STL", "Stereolithography", "model/stl", []]


6. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

---------------------------
Using the Extension
---------------------------

This extensions embeds a ParaViewWeb Visualizer in a CKAN resource's webpage using an HTML `iframe`.
It assumes that the ParaViewWeb server is running at the IP address 172.17.0.3 (which is a private IP
on the same host machine). If that is not where the server is running, this address must be changed
in ``paraview/templates/pvw_view.html``. There are also several locations in the ParaViewWeb server's
settings where the IP address must be set - see
https://gitlab.elaine.uni-rostock.de/hl201/paraview-docker#dockerfile-for-a-paraviewweb-server.

The CKAN instance and the ParaViewWeb server work closely together in order to display the
ParaViewWeb Visualizer as a view for files. Both CKAN and ParaViewWeb must have access to files
that have been uploaded to the CKAN instance. If you have set up a CKAN instance image from
https://gitlab.elaine.uni-rostock.de/INF/datahub/datahub-docker and a ParaViewWeb server image
from https://gitlab.elaine.uni-rostock.de/hl201/paraview-docker, these files can be shared
by mounting the ``ckan_storage`` volume (created while setting up the CKAN image) to
``/pvw-data/pvw/data`` when running a container for a ParaViewWeb server. This will put all files
exactly where both containers expect them to be, and no further configuration should be needed.

The ParaViewWeb Visualizer application, which is embedded in the CKAN instance to provide the
ParaView view, does not allow users to manually select the file format they are viewing. It decides
a file's format and how it will be displayed based on the file's extension; thus, all files must
have correct extensions in order for the Visualizer to display them correctly. Since CKAN stores files
only using their resource ID number without a file extension, we must add an extension before
the Visualizer will display files uploaded to CKAN. The extension does this by creating hard links to
displayable files (currently only STL files) in a dataset when a user attempts to use the Visualizer to
view one. These hard links have a .stl extension and thus can be opened by the Visualizer. When a resource
or dataset is deleted, these hard links are also automatically deleted. Hard links to
resources in the same dataset are all kept in the same directory, identified by
the dataset's randomly-generated ID.

A user can view any resource that works with this extension (currently just STL
files) from another resource in the same dataset's view. They can also use the
viewer to display multiple resources from the same dataset in the Visualizer
simultaneously. To prevent users from viewing files outside of the same dataset,
the CKAN instance sends the ID of the dataset containing the viewed resource to the
ParaViewWeb server. The ParaViewWeb server uses the ID to start a Visualizer process
with that dataset's directory of hard-linked files as the top-level directory, which
prevents users from accessing any other directories while allowing them to open any
viewable file from the same dataset.
