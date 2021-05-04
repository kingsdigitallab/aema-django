from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def str_replace(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

def str_in(value,arg):
    return arg in value

register.filter('str_replace', str_replace)
register.filter('str_in', str_in)
	
@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

@register.filter(name='arrayIndex')    
def arrayIndex(value, arg):
    return value[arg]

#To deal with none Type iterators
@register.filter(name='iterable')
def iterable(value):
    try:
        test = value.all()
        test.all()
        print(value.all())
        return 'true'
    except Exception:
        return 'false'

@register.filter
def divide(value, arg): return int(value) / int(arg)	

@register.filter
def fix_media_path(value):
    # media used to be placed within /static
    # before we migrated to django 1.8
    return mark_safe(value.replace('/static/media/', '/media/'))
