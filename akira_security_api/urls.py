from django.urls import path
from akira_security_api import views

urlpatterns = [
    path('getMetaData/<str:MetaKey>/<str:EncryptedMetaKey>/', views.IndexView.as_view(), name='index'),
]