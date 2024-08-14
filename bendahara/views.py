from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from administrator.decorators import ijinkan_pengguna
from django.http import JsonResponse
from administrator.models import Wilayah, Tahun_pelajaran, Detail_nominal_santri, SettingPembayaran, Santri, Jenis_pembayaran
import uuid
from administrator.telegram_utill import send_telegram_message
from django.contrib.humanize.templatetags.humanize import intcomma

from django.contrib.sites.shortcuts import get_current_site
from administrator.forms import UbahSetting



@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['bendahara'])
def berandabendahara(request):
    jmlSantriPa= Santri.objects.filter(jenis_kelamin='Laki-laki').count()
    jmlSantriPi= Santri.objects.filter(jenis_kelamin='Perempuan').count()
    jmlWilayah= Wilayah.objects.all().count()
    jmlbelumbayar= SettingPembayaran.objects.filter(status='Belum Lunas').count()
    jmlbayar= SettingPembayaran.objects.filter(status='Lunas').count()
    context = {
        'judul': 'Halaman Bendahara',
        'menu': 'bendaharaadmin',
        'nama': 'Bendahara',
           'jmlSantriPa':jmlSantriPa,
        'jmlSantriPi':jmlSantriPi,
        'jmlWilayah':jmlWilayah,
        'jmlbelumbayar':jmlbelumbayar,
        'jmlbayar':jmlbayar,
      
    }
    return render(request, 'berandabendahara.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['bendahara'])
def datapembayaranabendahara(request):
    wilayah_filter = request.GET.get('wilayah')
    tahun_filter = request.GET.get('tahun')
    bulan_filter = request.GET.get('bulan')
    current_site = get_current_site(request)
    domain = current_site.domain
    
    bayar = SettingPembayaran.objects.all()
    
    if wilayah_filter:
        bayar = bayar.filter(santri__wilayah__id=wilayah_filter)
    
    if tahun_filter:
        bayar = bayar.filter(tahun=tahun_filter)
    
    if bulan_filter:
        bayar = bayar.filter(bulan=bulan_filter)
        
    bayar = bayar.annotate(total=Sum('santri__detail_nominal_santri__jenis_pembayaran__nominal')).order_by('-id')
    
    wilayah_list = Wilayah.objects.all()
    tahun_list = SettingPembayaran.objects.values_list('tahun', flat=True).distinct()
    bulan_list = SettingPembayaran.objects.values_list('bulan', flat=True).distinct()
    
    context = {
        'judul': 'Halaman Data Pembayaran',
        'menu': 'datapembayaranabendahara',
        'nama': 'Pembayaran',
        'bayar': bayar,
        'wilayah_list': wilayah_list,
        'tahun_list': tahun_list,
        'bulan_list': bulan_list,
        'domain':domain
    }
    return render(request, 'databayarbendahara.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['bendahara'])
def setting(request):
    santri = Santri.objects.all().annotate(total=Sum('detail_nominal_santri__jenis_pembayaran__nominal')).order_by('-id')
    tahun = Tahun_pelajaran.objects.all().order_by('-id')
    wilayah = Wilayah.objects.all().filter(aktif=True).order_by('-id')

    context = {
        'judul': 'Halaman Setting Pembayaran',
        'menu': 'settingbendahara',
        'nama': 'Setting Pembayaran',
        'santri': santri,
        'tahun': tahun,
        'wilayah': wilayah,
        # 'selected_wilayah': selected_wilayah,
        # 'search_query': search_query,
    }
    return render(request, 'settingbendahara.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['bendahara'])
def simpansettingpembayaran(request):
    if request.method == "POST":
        idsantri = request.POST.getlist('id[]')
        bulan = request.POST.get('bulan')
        tahun = request.POST.get('tahun')
        token_dasar = str(uuid.uuid4())
       
        for row in idsantri:
            iddetailsantri= Santri.objects.get(pk=row)
            # detail = Detail_nominal_santri.objects.all().filter(santri__id=iddetailsantri.id)
            bayar = Detail_nominal_santri.objects.values('jenis_pembayaran__nominal').filter(santri__id=iddetailsantri.id).order_by('id')
            total = 0
            
            total_nominal = Detail_nominal_santri.objects.filter(santri__id=iddetailsantri.id).aggregate(Sum('jenis_pembayaran__nominal'))
            total_nominal_value = total_nominal['jenis_pembayaran__nominal__sum'] or 0  # Handle None value
            grantotal_formatted = f"Rp. {intcomma(total_nominal_value)}"
            if iddetailsantri.chat_id:
                message =f"Assalamualaikum Wr Wb,\n\n<b>Tagihan</b> Pembayaran Bulan: <b>{bulan}</b> \n Atas Nama : <b>{iddetailsantri.nama_santri}</b> \nTahun: <b>{tahun} </b>\nSejumlah: : <b>{grantotal_formatted}</b>\n\n\nTerimakasih, Salam Hormat Yayasan AR-ROHMAH Patokan Kraksaan \n Wssalamualaikum Wr Wb."
                send_telegram_message(iddetailsantri.chat_id, message)
            
            
            
            for rw in bayar:
                jml = rw['jenis_pembayaran__nominal']
                total += jml
            simpan = SettingPembayaran.objects.create(status='Belum Lunas')
            simpan.santri = iddetailsantri
            simpan.wilayah = iddetailsantri.wilayah
            simpan.biaya = total
            simpan.tahun = tahun
            simpan.bulan = bulan
            simpan.save()
        return JsonResponse({'status': 'Save' })
    else:
        return JsonResponse({'status' : 0})

# @login_required(login_url='halamanlogin')
# @ijinkan_pengguna(yang_diizinkan=['bendahara'])
# def deletedatabayarbendahara(request, pk):
#     hapus = SettingPembayaran.objects.get(id=pk)
    
#     if request.method == 'POST':
       
#         hapus.delete()
       
       
#         return redirect('datapembayaranbendahara')
#     context = {
#        'judul': 'Halaman Data Pembayaran',
#         'menu': 'datapembayaranbendahara',
#         'hapus':hapus,  
#     }
#     return render(request, 'hapusbayarbendahara.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['bendahara'])
def ubahstatusbayar(request, pk):
    setting = SettingPembayaran.objects.get(id=pk)
    form = UbahSetting(instance=setting)
    if request.method == 'POST':
        formsimpan = UbahSetting(request.POST, instance=setting)
        if formsimpan.is_valid():
            formsimpan.save()
            santri = Santri.objects.get(id=setting.santri.id)
            
            grantotal_formatted = f"Rp. {intcomma(setting.biaya)}"
            if santri.chat_id:
                message =f"Assalamualaikum Wr Wb,\n\nPembayaran Bulan: <b>{setting.bulan}</b>\n Atas Nama : <b>{santri.nama_santri}</b> \nTahun: <b>{setting.tahun} </b>\nSejumlah: : <b>{grantotal_formatted}</b>\nStatus: <b>{setting.status}</b>\n\n\nTerimakasih, Salam Hormat Yayasan AR-ROHMAH Patokan Kraksaan \n Wssalamualaikum Wr Wb."
                send_telegram_message(santri.chat_id, message)
            
            return redirect('datapembayaranabendahara')
            
        

        
            

    context = {
        'judul': 'Ubah Data Pembayaran',
        'menu': 'datapembayaranabendahara',
        'nama': 'Ubah Pembayaran',
        'form':form
    }
    return render(request, 'ubahstatus.html', context)