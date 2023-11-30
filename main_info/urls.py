from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from distribution.views import ClientViewSet, MailingViewSet, MessageViewSet
from main_info.svag import swaggerurlpatterns
from user_backend.views import RegistrationView, LogInView, AccessTokenView, ActivationView

router = routers.DefaultRouter()
router.register(r"clients", ClientViewSet, basename='client')
router.register(r"messages", MessageViewSet, basename='message')
router.register(r"mailings", MailingViewSet, basename='mailing')
router.register(r"signup/", RegistrationView, basename='reg')
router.register(r"activate_account/", ActivationView, basename='active')
router.register(r"signin/", LogInView, basename='log')
router.register(r"access_/", AccessTokenView, basename='access_')


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('api/login/', include("rest_framework.urls"))
]


urlpatterns += swaggerurlpatterns