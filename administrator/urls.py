from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.halamanlogin, name='halamanlogin'),
    path('administrator/', views.berandaadmin, name='berandaadmin'),
    
    path('tahun-pelajaran/', views.tahunpelajaran, name='tahunpelajaran'),
    path('form-tahun-pelajaran/', views.formtahunadmin, name='formtahunadmin'),
    path('edit-tahun-pelajaran/<str:pk>', views.edittahunadmin, name='edittahunadmin'),
    path('delete-tahun-pelajaran/<str:pk>', views.deletetahunadmin, name='deletetahunadmin'),


    path('wilayah/', views.wilayah, name='wilayah'),
    path('form-wilayah/', views.formwilayah, name='formwilayah'),
    path('edit-wilayah/<str:pk>', views.editwilayah, name='editwilayah'),
    path('delete-wilayah/<str:pk>', views.deletewilayah, name='deletewilayah'),
    
    path('jenis/', views.jenis, name='jenis'),
    path('form-jenis/', views.formjenis, name='formjenis'),
    path('edit-jenis/<str:pk>', views.editjenis, name='editjenis'),
    path('delete-jenis/<str:pk>', views.deletejenis, name='deletejenis'),
    
    path('bank/', views.bank, name='bank'),
    path('form-bank/', views.formbank, name='formbank'),
    path('edit-bank/<str:pk>', views.editbank, name='editbank'),
    path('delete-bank/<str:pk>', views.deletebank, name='deletebank'),
    
    path('bendahara-admin/', views.bendaharaadmin, name='bendaharaadmin'),
    path('form-bendahara-admin/', views.formbendaharaadmin, name='formbendaharaadmin'),
    path('form-edit-bendahara-admin/<str:pk>', views.editbendaharaadmin, name='editbendaharaadmin'),
    path('delete-bendahara-admin/<str:pk>', views.deletebendaharaadmin, name='deletebendaharaadmin'),
    
    path('santri-admin/', views.santriadmin, name='santriadmin'),
    path('form-santri-admin/', views.formsantriadmin, name='formsantriadmin'),
     path('form-edit-santri-admin/<str:pk>', views.editsantriadmin, name='editsantriadmin'),
      path('detail-pembayaran-admin/<str:pk>', views.detailpembayaranadmin, name='detailpembayaranadmin'),
      
      
    path('tabelnominal/', views.tabelnominal, name='tabelnominal'),
    path('hapusdetailadmin/', views.hapusdetailadmin, name='hapusdetailadmin'),
    path('cekjenispembayaran/', views.cekjenispembayaran, name='cekjenispembayaran'),
    path('simpanjenisplotingadmin/', views.simpanjenisplotingadmin, name='simpanjenisplotingadmin'),
    
    path('delete-santri-admin/<str:pk>', views.deletesantriadmin, name='deletesantriadmin'),
    path('data-pembayaran-admin/', views.datapembayaranadmin, name='datapembayaranadmin'),
    path('logout/', views.logoutPage, name='logout'),
  
]