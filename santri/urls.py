from django.urls import path
from . import views

urlpatterns = [
    path('', views.berandasantri, name='berandasantri'),
    path('tagihan-pembayaran', views.tagihanpembayaran, name='tagihanpembayaran'),
     path('bukti-pembayaran/<str:pk>', views.buktibayar, name='buktibayar'),
   
]