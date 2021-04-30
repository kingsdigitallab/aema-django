# Setup

## Local settings

The secret, instance-specific settings should be palced in a file called:

`local_settings.py`

Keep this file out of the repository.

## Install js packages

`npm ci`

## Install the python packages

First create a python virtual environment and activate it.

```bash
# this project uses pip-tools
pip install pip-tools
# install the packages from the requirements.txt
pip-sync
```

# update haystack index

`python manage.py rebuild_index`

