from django.urls import re_path as url
from EntiretyApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    url(r'^user$',views.userRegistrationApi),
    url(r'^user/([0-9]+)$',views.userRegistrationApi),

    url(r'^products$',views.productsApi),
    url(r'^products/([0-9]+)$',views.productsApi),

    url(r'^productuser$',views.userProductMapApi),
    url(r'^productuser/([0-9]+)$',views.userProductMapApi),
    url(r'^productuser/([0-9]+)/([0-9]+)$',views.userProductMapApi),

    url(r'^userrole/([0-9]+)$',views.userRoleMapApi),

    url(r'^productusercheck/([0-9]+)/([0-9]+)$',views.userProductMapCheckApi),

    url(r'^login$',views.userLoginApi)
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)