from django.conf.urls import patterns, include, url
from django.contrib import admin
from fs_renderer import views as fs_renderer_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fs_proj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^althtml/(\w+)/(\w+)/(\w+)', csrf_exempt(fs_renderer_views.AltHTMLView.as_view())),
    url(r'^althtml/(\w+)/(\w+)', csrf_exempt(fs_renderer_views.AltHTMLView.as_view())),
    url(r'^althtml/(\w+)', csrf_exempt(fs_renderer_views.AltHTMLView.as_view())),
    url(r'^althtml/', csrf_exempt(fs_renderer_views.AltHTMLView.as_view())),
)
