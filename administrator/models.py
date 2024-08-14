from django.db import models
from django.contrib.auth.models import User


class Bendahara(models.Model):
    Jk=(
        ('Laki-laki','Laki-laki'),
        ('Perempuan','Perempuan')
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nama_bendahara = models.CharField(max_length=200, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=200, blank=True, null=True, choices=Jk)
    alamat = models.TextField (blank=True, null=True)
    chat_id =  models.CharField(max_length=100, blank=True, null=True)
    no_hp =  models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama_bendahara
    class Meta:
        verbose_name_plural ="Bendahara"


class Tahun_pelajaran(models.Model):
    nama = models.CharField(max_length=200, blank=False, null=True)
    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural ="Tahun Pelajaran"
        
class Bank(models.Model):
    nama_bank = models.CharField(max_length=200, blank=False, null=True)
    atas_nama= models.CharField(max_length=200, blank=False, null=True)
    nomor_rekening= models.CharField(max_length=200, blank=False, null=True)
    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_bank
    class Meta:
        verbose_name_plural ="Tahun Pelajaran"
        
class Wilayah(models.Model):
    nama_wilayah = models.CharField(max_length=200, blank=False, null=True)
    chat_id =  models.CharField(max_length=100, blank=True, null=True)
    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_wilayah
    class Meta:
        verbose_name_plural ="wilayah"

class Jenis_pembayaran(models.Model):
    nama_pembayaran = models.CharField(max_length=200, blank=False, null=True)
    nominal = models.PositiveIntegerField(blank=False, null=True)
    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_pembayaran
    class Meta:
        verbose_name_plural ="Jenis Pembayaran"

class Santri(models.Model):
    Jk=(
        ('Laki-laki','Laki-laki'),
        ('Perempuan','Perempuan')
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nama_santri = models.CharField(max_length=200, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=200, blank=True, null=True, choices=Jk)
    alamat = models.TextField (blank=True, null=True)
    no_hp =  models.CharField(max_length=100, blank=True, null=True)
    chat_id =  models.CharField(max_length=100, blank=True, null=True)
    wilayah = models.ForeignKey(Wilayah, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nama_santri
    class Meta:
        verbose_name_plural ="santri"

class Detail_nominal_santri(models.Model):
    santri = models.ForeignKey(Santri, null=True, blank=True, on_delete=models.SET_NULL)
    jenis_pembayaran = models.ForeignKey(Jenis_pembayaran, null=True, blank=True, on_delete=models.SET_NULL)
    

    def __str__(self):
        return self.santri.nama_santri
    class Meta:
        verbose_name_plural ="Detail Nominal santri"

class SettingPembayaran(models.Model):
    STATUS=(
        ('Belum Lunas', 'Belum Lunas'),
        ('Lunas' , 'Lunas'),
      
    )

   
    tahun = models.CharField(max_length=200, blank=False, null=True)
    santri = models.ForeignKey(Santri, null=True, blank=True, on_delete=models.SET_NULL)
    wilayah = models.ForeignKey(Wilayah, null=True, blank=True, on_delete=models.SET_NULL)
    bulan = models.CharField(max_length=200, blank=False, null=True)
    status = models.CharField(max_length=200, blank=False, null=True, choices=STATUS)
    biaya = models.CharField(max_length=200, blank=False, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    file_bukti = models.FileField(upload_to='arsip/file_bukti',blank=True, null=True,max_length=300)

    def __str__(self):
        return self.bulan

    def __str__(self):
        if not self.santri:
           return ""
        return str(f"{self.tahun} ({self.bulan}) {self.santri}")
    class Meta:
        verbose_name_plural ="Setting Pembayaran"

