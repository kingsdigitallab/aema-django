from django import forms
from django.utils.safestring import mark_safe

class MflcLinkWidget(forms.Widget):
    '''This widget adds a link, to edit the current inline, after the inline form fields.'''
    def __init__(self, obj, attrs=None):
        self.object = obj
        super(MflcLinkWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if self.object.pk:
            return mark_safe('<a onclick="return showRelatedObjectLookupPopup(this);" href="../../../%s/%s/%s/">%s</a>' % \
                             (self.object._meta.app_label, self.object._meta.object_name.lower(), self.object.pk, self.object))
        else:
            return mark_safe('')

class MflcForm(forms.ModelForm):
    '''This form renders the Feature model and adds a link to edit the Feature. This is useful for \ 
    inline editing when the nested inline fields are not displayed.'''
    # required=False is essential because we don't render input tag so there will be no value submitted.
    edit_link = forms.CharField(label='Edit', required=False)



    def __init__(self, *args, **kwargs):
        super(MflcForm, self).__init__(*args, **kwargs)
        # instance is always available, it just does or doesn't have pk.
        self.fields['edit_link'].widget = MflcLinkWidget(self.instance)
