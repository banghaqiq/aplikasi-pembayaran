from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import ijinkan_pengguna, pilihan_login, tolakhalaman_ini
from .models import SettingPembayaran, Tahun_pelajaran, Detail_nominal_santri, Santri, Bendahara, Jenis_pembayaran, Wilayah,Bank
from django.http import JsonResponse
from .forms import TahunForm, WilayahForm, JenisForm, BankForm,BendaharaForm,UserForm, SantriForm
from django.contrib.auth.forms import AuthenticationForm


@tolakhalaman_ini
def halamanlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'Username Tidak ditemukan')
            return redirect('halamanlogin')
        cocokan = authenticate(request, username=username, password=password)
        if cocokan is None:
            messages.success(request, 'Password salah')
            return redirect('halamanlogin')
        if cocokan is not None:
            login(request, cocokan)
            return redirect('berandaadmin')
    context = {
        'judul': 'Halaman Login',
    }
    return render(request, 'halamanlogin.html', context)

def logoutPage(request):
    logout(request)
    return redirect('halamanlogin')

@login_required(login_url='halamanlogin')
@pilihan_login
def berandaadmin(request):
    jmlSantriPa= Santri.objects.filter(jenis_kelamin='Laki-laki').count()
    jmlSantriPi= Santri.objects.filter(jenis_kelamin='Perempuan').count()
    jmlWilayah= Wilayah.objects.all().count()
    jmlbelumbayar= SettingPembayaran.objects.filter(status='Belum Lunas').count()
    jmlbayar= SettingPembayaran.objects.filter(status='Lunas').count()
    context = {
        'judul': 'Halaman Beranda',
        'menu': 'berandaadmin',
         'jmlSantriPa':jmlSantriPa,
        'jmlSantriPi':jmlSantriPi,
        'jmlWilayah':jmlWilayah,
        'jmlbelumbayar':jmlbelumbayar,
        'jmlbayar':jmlbayar,
     
    }
    return render(request, 'beranda_admin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def tahunpelajaran(request):
    tahun = Tahun_pelajaran.objects.all().order_by('-id')
    context = {
        'judul': 'Halaman Tahun Pelajaran',
        'menu': 'berandatahunpelajaran',
        'nama': 'Tahun Pelajaran',
        'data':tahun,
    }
    return render(request, 'tahunpelajaran_admin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formtahunadmin(request):
    form = TahunForm()
    if request.method == 'POST':
        formsimpan = TahunForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('tahunpelajaran')
    context = {
        'judul': 'Form Tahun Pelajaran',
        'menu': 'berandatahunpelajaran',
        'nama': 'Tahun Pelajaran',
        'form':form
    }
    return render(request, 'formtahunadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def edittahunadmin(request, pk):
    tahun = Tahun_pelajaran.objects.get(id=pk)
    form = TahunForm(instance=tahun)
    if request.method == 'POST':
        formsimpan = TahunForm(request.POST, instance=tahun)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('tahunpelajaran')
    context = {
        'judul': 'Formedit Tahun Pelajaran',
        'menu': 'berandatahunpelajaran',
        'nama': 'Tahun Pelajaran',
        'form':form
    }
    return render(request, 'formtahunadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletetahunadmin(request, pk):
    hapus = Tahun_pelajaran.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('tahunpelajaran')

    context = {
        'judul': 'Hapus Tahun Pelajaran',
        'menu': 'berandatahunpelajaran',
        'nama': 'Tahun Pelajaran',
        'hapus':hapus  
    }
    return render(request, 'hapustahunadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def wilayah(request):
    wilayah = Wilayah.objects.all().order_by('-id')
    context = {
        'judul': 'Halaman Wilayah',
        'menu': 'wilayahadmin',
        'nama': 'Tahun Wilayah',
        'data':wilayah,
    }
    return render(request, 'wilayah_admin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formwilayah(request):
    form = WilayahForm()
    if request.method == 'POST':
        formsimpan = WilayahForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('wilayah')
    context = {
       'judul': 'Form Wilayah',
        'menu': 'wilayahadmin',
        'nama': 'Tahun Wilayah',
        'form':form
    }
    return render(request, 'formwilayah.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editwilayah(request, pk):
    wilayah = Wilayah.objects.get(id=pk)
    form = WilayahForm(instance=wilayah)
    if request.method == 'POST':
        formsimpan = WilayahForm(request.POST, instance=wilayah)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('wilayah')
    context = {
       'judul': 'Formedit Wilayah',
        'menu': 'wilayahadmin',
        'nama': 'Tahun Wilayah',
        'form':form
    }
    return render(request, 'formwilayah.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletewilayah(request, pk):
    hapus = Wilayah.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('wilayah')

    context = {
       'judul': 'Hapus Wilayah',
        'menu': 'wilayahadmin',
        'nama': 'Wilayah',
        'hapus':hapus  
    }
    return render(request, 'hapuswilayah.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def jenis(request):
    jenis = Jenis_pembayaran.objects.all().order_by('-id')
    context = {
        'judul': 'Halaman Jenis',
        'menu': 'jenisadmin',
        'nama': 'Tahun Jenis',
        'data':jenis,
    }
    return render(request, 'jenis_admin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formjenis(request):
    form = JenisForm()
    if request.method == 'POST':
        formsimpan = JenisForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('jenis')
    context = {
       'judul': 'Form Jenis',
        'menu': 'jenisadmin',
        'nama': 'Tahun Jenis',
        'form':form
    }
    return render(request, 'formjenis.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editjenis(request, pk):
    jenis = Jenis_pembayaran.objects.get(id=pk)
    form = JenisForm(instance=jenis)
    if request.method == 'POST':
        formsimpan = JenisForm(request.POST, instance=jenis)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('jenis')
    context = {
       'judul': 'Formedit Jenis',
        'menu': 'jenisadmin',
        'nama': 'Tahun Jenis',
        'form':form
    }
    return render(request, 'formjenis.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletejenis(request, pk):
    hapus = Jenis_pembayaran.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('jenis')

    context = {
       'judul': 'Hapus Jenis',
        'menu': 'jenisadmin',
        'nama': 'Jenis',
        'hapus':hapus  
    }
    return render(request, 'hapusjenis.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def bank(request):
    bank = Bank.objects.all().order_by('-id')
    context = {
        'judul': 'Halaman Bank',
        'menu': 'bankadmin',
        'nama': 'Tahun Bank',
        'data':bank,
    }
    return render(request, 'bank_admin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formbank(request):
    form = BankForm()
    if request.method == 'POST':
        formsimpan = BankForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('bank')
    context = {
       'judul': 'Form Bank',
        'menu': 'bankadmin',
        'nama': 'Tahun Bank',
        'form':form
    }
    return render(request, 'formbank.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editbank(request, pk):
    bank = Bank.objects.get(id=pk)
    form = BankForm(instance=bank)
    if request.method == 'POST':
        formsimpan = BankForm(request.POST, instance=bank)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('bank')
    context = {
       'judul': 'Formedit Bank',
        'menu': 'bankadmin',
        'nama': 'Tahun Bank',
        'form':form
    }
    return render(request, 'formbank.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletebank(request, pk):
    hapus = Bank.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('bank')

    context = {
       'judul': 'Hapus Bank',
        'menu': 'bankadmin',
        'nama': 'Bank',
        'hapus':hapus  
    }
    return render(request, 'hapusbank.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def bendaharaadmin(request):
    bendahara = Bendahara.objects.all()
    context = {
        'data': bendahara,
        'judul': 'Halaman Bendahara',
        'menu': 'bendaharaadmin',
        'nama': 'Bendahara',
    }
    return render(request, 'bendaharaadmin.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formbendaharaadmin(request):
    form = BendaharaForm()
    formuser = UserForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       

        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.is_active = True
        user.save()

        akses = Group.objects.get(name='bendahara')
        user.groups.add(akses)

        formsimpan = BendaharaForm(request.POST)
        if formsimpan.is_valid():
            data = formsimpan.save()
            data.user = user
            data.save()
            return redirect('bendaharaadmin')
    context = {
        'judul': 'Form Bendahara',
        'menu': 'bendaharaadmin',
        'nama': 'Bendahara',
        'form':form,
        'formuser':formuser
    }
    return render(request, 'formbendaharaadmin.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editbendaharaadmin(request, pk):
    bendahara = Bendahara.objects.get(id=pk)
    user = User.objects.get(id=bendahara.user.id)
    form = BendaharaForm(instance=bendahara)
    formuser = UserForm(instance=user)
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        if password:
            formsimpan = BendaharaForm(request.POST,request.FILES, instance=bendahara)
            simpanuser = User.objects.get(id=bendahara.user.id)
            simpanuser.set_password(password)
            simpanuser.username = username
            simpanuser.save()
            if formsimpan.is_valid():
                formsimpan.save()
                return redirect('bendaharaadmin')
        else:
            formsimpan = BendaharaForm(request.POST,request.FILES, instance=bendahara)
            simpanuser = User.objects.get(id=bendahara.user.id)
            simpanuser.username = username
            simpanuser.save()
            if formsimpan.is_valid():
                formsimpan.save()
                return redirect('bendaharaadmin')
    context = {
        'judul': 'Formedit Bendahara',
        'menu': 'bendaharaadmin',
        'nama': 'Bendahara',
        'form':form,
        'formuser':formuser,
        'id': bendahara,
    }
    return render(request, 'formeditbendaharaadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletebendaharaadmin(request, pk):
    hapus = Bendahara.objects.get(id=pk)
    user = User.objects.get(id=hapus.user.id)
    if request.method == 'POST':
        hapus.delete()
        user.delete()
        return redirect('bendaharaadmin')
    context = {
       'judul': 'Hapus Bendahara',
        'menu': 'bendahharaadmin',
        'nama': 'Bendahara',
        'hapus':hapus,  
    }
    return render(request, 'hapusbendaharaadmin.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def santriadmin(request):
    selected_wilayah = request.GET.get('wilayah', None)
    
    if selected_wilayah:
        santri = Santri.objects.filter(wilayah__id=selected_wilayah).annotate(total=Sum('detail_nominal_santri__jenis_pembayaran__nominal')).order_by('-id')
    else:
        santri = Santri.objects.all().annotate(total=Sum('detail_nominal_santri__jenis_pembayaran__nominal')).order_by('-id')
        
    wilayah = Wilayah.objects.filter(aktif=True)
    
    context = {
        'data': santri,
        'judul': 'Halaman Santri',
        'menu': 'santriadmin',
        'nama': 'Santri',
        'wilayah': wilayah,
        'selected_wilayah': selected_wilayah
    }
    return render(request, 'santriadmin.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formsantriadmin(request):
    form = SantriForm()
    formuser = UserForm()
    jenis = Jenis_pembayaran.objects.all().filter(aktif=True).order_by('-id')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.is_active = True
        user.save()

        akses = Group.objects.get(name='santri')
        user.groups.add(akses)

        formsimpan = SantriForm(request.POST)
        if formsimpan.is_valid():
            jenisnominal = request.POST.getlist('jenis[]')
            data = formsimpan.save()
            data.user = user
            data.save()
            for row in jenisnominal:
                iddetailjenis= Jenis_pembayaran.objects.get(pk=row)
                simpan = Detail_nominal_santri.objects.create(santri=data)
                simpan.jenis_pembayaran = iddetailjenis
                simpan.save()
            return redirect('santriadmin')
    context = {
         'judul': 'Form Santri',
        'menu': 'santriadmin',
        'nama': 'Santri',
        'form':form,
        'formuser':formuser,
        'jenis':jenis
    }
    return render(request, 'formsantriadmin.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editsantriadmin(request, pk):
    santri = Santri.objects.get(id=pk)
    user = User.objects.get(id=santri.user.id)
    form = SantriForm(instance=santri)
    formuser = UserForm(instance=user)
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        if password:
            formsimpan = SantriForm(request.POST,request.FILES, instance=santri)
            simpanuser = User.objects.get(id=santri.user.id)
            simpanuser.set_password(password)
            simpanuser.username = username
            simpanuser.save()
            if formsimpan.is_valid():
                formsimpan.save()
                return redirect('santriadmin')
        else:
            formsimpan = SantriForm(request.POST,request.FILES, instance=santri)
            simpanuser = User.objects.get(id=santri.user.id)
            simpanuser.username = username
            simpanuser.save()
            if formsimpan.is_valid():
                formsimpan.save()
                return redirect('santriadmin')
    context = {
         'judul': 'Formedit Santri',
        'menu': 'santriadmin',
        'nama': 'Santri',
        'form':form,
        'formuser':formuser,
        'id': santri,
    }
    return render(request, 'formeditsantriadmin.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def detailpembayaranadmin(request, pk):
    santri = Santri.objects.get(id=pk)
    jenis = Jenis_pembayaran.objects.all().filter(aktif=True).order_by('-id')
    
    context = {
        'judul': 'Detail Pembayaran Santri',
        'menu': 'santriadmin',
        'nama': 'Santri',
        'santri':santri,
        'jenis':jenis,
        
    }
    return render(request, 'detailpembayaransantriadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def tabelnominal(request):
    idsantri = request.POST.get('idsantri')

    detail = Detail_nominal_santri.objects.all().filter(santri__id=idsantri).order_by('-id')
  
    context = {
        'detail':detail
    }
    return render(request, 'detailnominaladmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def hapusdetailadmin(request):
    if request.method == "POST":
        id = request.POST.get('id')

        pus = Detail_nominal_santri.objects.get(pk=id)
        pus.delete()

        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])   
def cekjenispembayaran(request):
    idjenis = request.GET.get('idjenis', None)
    jenis = Jenis_pembayaran.objects.get(id=idjenis)
    idsantri = request.GET.get('idsantri', None)
    santri = Santri.objects.get(id=idsantri)
    
    data = {
        'is_taken': Detail_nominal_santri.objects.filter(jenis_pembayaran__id=jenis.id, santri__id=santri.id).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Jenis Pembayaran tersebut sudah terploting'
    return JsonResponse(data)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def simpanjenisplotingadmin(request):
    if request.method == "POST":
        idsantri = request.POST.get('idsantri')
        idjenis = request.POST.get('jenis_pembayaran')
        jenis = Jenis_pembayaran.objects.get(id=idjenis)
        santri = Santri.objects.get(id=idsantri)
        simpan = Detail_nominal_santri.objects.create(santri=santri)
        simpan.jenis_pembayaran =jenis
        simpan.save()

        
        return JsonResponse({'status': 'Save' })
    else:
        return JsonResponse({'status' : 0})
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])  
def deletesantriadmin(request, pk):
    hapus = Santri.objects.get(id=pk)
    user = User.objects.get(id=hapus.user.id)
    if request.method == 'POST':
        Detail_nominal_santri.objects.filter(santri__id=pk).delete()
        hapus.delete()
        user.delete()
       
        return redirect('santriadmin')
    context = {
         'judul': 'Hapus Data Santri',
        'menu': 'santriadmin',
        'nama': 'Santri',
        'hapus':hapus,  
    }
    return render(request, 'hapussantriadmin.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def datapembayaranadmin(request):
    wilayah_filter = request.GET.get('wilayah')
    tahun_filter = request.GET.get('tahun')
    bulan_filter = request.GET.get('bulan')
    
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
        'menu': 'pembayaranadmin',
        'nama': 'Pembayaran',
        'bayar': bayar,
        'wilayah_list': wilayah_list,
        'tahun_list': tahun_list,
        'bulan_list': bulan_list,
    }
    return render(request, 'databayaradmin.html', context)







