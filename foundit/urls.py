from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from founditapi.models import *
from founditapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'items', Items, 'item')
router.register(r'categories', Categories, 'category')
router.register(r'organizers', Organizers, 'organizer')
router.register(r'users', UserViewSet, 'user')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
]