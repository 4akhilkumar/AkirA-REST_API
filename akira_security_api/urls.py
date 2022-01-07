from django.urls import path
from akira_security_api import views

urlpatterns = [
    path('getMetaData/<str:MetaKey>/<str:EncryptedMetaKey>/', views.IndexView.as_view(), name='index'),
    path('getEncryptionData/<str:MetaKey>/', views.CustomEncryption.as_view()),
    path('getDecryptionData/<str:EncryptedMetaData>/', views.CustomDecryption.as_view()),
]