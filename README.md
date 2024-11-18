# Atlantic Europe in the Metal Ages (AEMA) 

This repository contains the latest version of the software code
running the [AEMA online resource](www.aemap.ac.uk).

* Principal Investigator: John Thomas Kock
* Lead developer: Neil Jakeman

# Change log

* May 2021: Converted from SVN, Django 1.5, Python 2 to Github and Django 1.8 and Python 3.6
by Geoffroy Noel, and instance migrated to new virtual machine aema2.  
* 2016: Software maintained by KDL
* 2013-2016: Software development

# Setup

## Install system packages

[Geospatial libraries for Django](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/)

`sudo apt-get install binutils libproj-dev gdal-bin`

## Local settings

The secret, instance-specific settings should be placed in a local file called:

`local_settings.py`

Keep this file out of the repository. It should be in the same folder as manage.py.

## Install js packages

`npm ci`

## Install the python packages

First create a python virtual environment and activate it.

```bash
# this project uses pip-tools
pip install pip-tools
# install the packages from requirements.txt
pip-sync
```

## Update search index

`python manage.py rebuild_index`

