from django.conf.urls import include, url
#from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'luces_pinguino.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'luces_pinguino.views.home', name='home'),
    url(r'^acerca/', 'luces_pinguino.views.acerca', name='acerca'),
]
