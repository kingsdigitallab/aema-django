# Atlantic Europe in the Metal Ages (AEMA) 

This repository contains the latest version of the software code
running the [AEMA online resource](www.aemap.ac.uk).

* Principal Investigator: John Thomas Kock
* Lead developer: Neil Jakeman

# Change log

* May 2021: Converted from SVN, Django 1.5, Python 2 to Github and Django 1.8 and Python 3.6
by Geoffroy Noel, and instance migrated to new virtual machine aema2.  

# Setup

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

# update haystack index

`python manage.py rebuild_index`

