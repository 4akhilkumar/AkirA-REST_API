from django.urls import path
from . import views

urlpatterns = [
    path('fetchKey/', views.fetchKey, name='fetchKey'),
    path('getEncryptionData/<str:MetaKey>/', views.CustomEncryption.as_view()),
    path('getDecryptionData/<str:EncryptedMetaData>/', views.CustomDecryption.as_view()),
    path('getEmail/<str:email>/', views.isSensibleEmail.as_view()),
]