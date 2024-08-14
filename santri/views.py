from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from administrator.decorators import ijinkan_pengguna
from django.http import JsonResponse
from administrator.models import Wilayah, Tahun_pelajaran, Detail_nominal_santri, SettingPembayaran, Santri, Jenis_pembayaran,Bendahara
import uuid
from django.contrib.sites.shortcuts import get_current_site
from administrator.forms import BuktiSetting
from administrator.telegram_utill import send_telegram_message
from django.contrib.humanize.templatetags.humanize import intcomma

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['santri'])
def berandasantri(request):
   
    context = {
        'judul': 'Halaman Santri',
        'menu': 'santriadmin',
        'nama': 'Santri',
      
    }
    return render(request, 'berandasantri.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['santri'])
def tagihanpembayaran(request):
    current_site = get_current_site(request)
    domain = current_site.domain
    santri = request.user.santri.id
    bayar = SettingPembayaran.objects.filter(santri__id=santri).annotate(total=Sum('santri__detail_nominal_santri__jenis_pembayaran__nominal')).order_by('-id')
    context = {
        'judul': 'Halaman Tagihan Pembayaran',
        'menu': 'tagihanpembayaran',
        'nama': 'Tagihan Pembayaran',
        'bayar':bayar,
        'domain':domain
      
    }
    return render(request, 'tagihanpembayaran.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['santri'])
def buktibayar(request, pk):
    setting = SettingPembayaran.objects.get(id=pk)
    form = BuktiSetting(instance=setting)
    if request.method == 'POST':
        formsimpan = BuktiSetting(request.POST,request.FILES, instance=setting)
        if formsimpan.is_valid():
            formsimpan.save()
            chats = Bendahara.objects.all()
            for chat in chats:
                grantotal_formatted = f"Rp. {intcomma(setting.biaya)}"
                message =f"Assalamualaikum Wr Wb,\n\nPembayaran Bulan: <b>{setting.bulan} {setting.tahun}</b> \n Atas Nama : <b>{setting.santri.nama_santri}</b> \nPesan: <b>Sudah melakukan pembayaran Silakan dicek di Aplikasi </b>\nSejumlah: : <b>{grantotal_formatted}</b>\n\n\nTerimakasih, Salam Hormat Yayasan AR-ROHMAH Patokan Kraksaan \n Wssalamualaikum Wr Wb."
                send_telegram_message(chat.chat_id, message)
            
            return redirect('tagihanpembayaran')
    context = {
       'judul': 'Upload Bukti Tagihan Pembayaran',
        'menu': 'tagihanpembayaran',
        'nama': 'Bukti Pembayaran',
        'form':form
    }
    return render(request, 'buktibayar.html', context)