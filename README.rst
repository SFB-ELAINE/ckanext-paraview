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

This extension is NOT finished and should not yet be installed with a production instance of CKAN.


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

4. For CKAN to recognize STL files, add the following line to the list of allowed
resource formats in `ckan/config/resource_formats.json`::

    ["STL", "Stereolithography", "model/stl", []]


5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload



---------------
Config Settings
---------------

Document any optional config settings here. For example::

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    ckanext.paraview.some_setting = some_default_value

------------------------
Development Installation
------------------------

To install ckanext-paraview for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/SFB-ELAINE/ckanext-paraview.git
    cd ckanext-paraview
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.paraview --cover-inclusive --cover-erase --cover-tests


--------------------------------------
Registering ckanext-paraview on PyPI
--------------------------------------

ckanext-paraview should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-paraview. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


---------------------------------------------
Releasing a New Version of ckanext-paraview
---------------------------------------------

ckanext-paraview is availabe on PyPI as https://pypi.python.org/pypi/ckanext-paraview.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
