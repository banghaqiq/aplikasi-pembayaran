from django.urls import path
from . import views

urlpatterns = [
   
   
    path('', views.berandabendahara, name='berandabendahara'),
     path('data-pembayaran-bendahara/', views.datapembayaranabendahara, name='datapembayaranabendahara'),
     
     
      path('setting-pembayaran', views.setting, name='setting'),
    path('simpansettingpembayaran', views.simpansettingpembayaran, name='simpansettingpembayaran'),
    
    path('ubah-status-pembayaran/<str:pk>', views.ubahstatusbayar, name='ubahstatusbayar'),
    # path('delete-data-bayar-bendahara/<str:pk>', views.deletedatabayarbendahara, name='deletedatabayarbendahara'),
   
    
]