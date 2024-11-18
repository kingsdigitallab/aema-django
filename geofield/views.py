from django.shortcuts import render


def geofield_js(request, field):
    context = {}
    context['geofield_js'] = field
    return render(
        request, 'geofield_js.js',
        context, content_type='application/javascript'
    )
