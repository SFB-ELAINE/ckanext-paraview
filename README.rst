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
slightly different configurations will not work correctly.


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
