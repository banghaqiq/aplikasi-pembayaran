from django.http import HttpResponse
from django.shortcuts import redirect

def tolakhalaman_ini(fungsi_awal):
    def perubahan_halaman(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('berandaadmin')
        else:
            return fungsi_awal(request, *args, **kwargs)
    return perubahan_halaman

def ijinkan_pengguna(yang_diizinkan=[]):
    def aturan(fungsi_awal):
        def perubahan_halaman(request, *args, **kwargs):
            # print('Nama User', yang_diizinkan )
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in yang_diizinkan :
                return fungsi_awal(request, *args, **kwargs)
            else:
                return HttpResponse('<h2><center>Anda Tidak Dijikankan Ke Tampilan ini</center></h2>')
        return perubahan_halaman
    return aturan

def pilihan_login(fungsi_awal):
    def perubahan_halaman(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'bendahara' :
            return redirect('berandabendahara')
       
        if group == 'santri' :
            return redirect('berandasantri')

        if group == 'administrator' :
            return fungsi_awal(request, *args, **kwargs)
            
    return perubahan_halaman
