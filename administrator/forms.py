from django import forms
from django.forms import ModelForm
from .models import SettingPembayaran, Tahun_pelajaran, Detail_nominal_santri, Santri, Bendahara, Jenis_pembayaran, Wilayah,Bank
from django.contrib.auth.models import User

class TahunForm(ModelForm):
    class Meta:
        model = Tahun_pelajaran
        fields=['nama','aktif']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control','placeholder':'Tahun Pelajaran'}),
            
            }
class UbahSetting(ModelForm):
    class Meta:
        model = SettingPembayaran
        fields=['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
           
            
            }
class BuktiSetting(ModelForm):
    class Meta:
        model = SettingPembayaran
        fields=['file_bukti']
        widgets = {
            'file_bukti': forms.FileInput(attrs={'class': 'form-control'}),
            # 'file_bukti': forms.FileInput(attrs={'class': 'form-control','OnChange':'unggahpengajuanpdf(this.value)'}),
            
           
            
            }
        
class WilayahForm(ModelForm):
    class Meta:
        model = Wilayah
        fields=['nama_wilayah','chat_id','aktif']
        widgets = {
            'nama_wilayah': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nama Wilayah'}),
            'chat_id': forms.TextInput(attrs={'class': 'form-control','placeholder':'Chat ID Telegram'}),
        }
        
class JenisForm(ModelForm):
    class Meta:
        model = Jenis_pembayaran
        fields=['nama_pembayaran','nominal','aktif']
        widgets = {
            'nama_pembayaran': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nama Pembayaran'}),
            'nominal': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nominal','type':'number'}),
           

        }
class BankForm(ModelForm):
    class Meta:
        model = Bank
        fields=['nama_bank','atas_nama','nomor_rekening','aktif']
        widgets = {
            'nama_bank': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nama Bank'}),
            'atas_nama': forms.TextInput(attrs={'class': 'form-control','placeholder':'Atas Nama'}),
            'nomor_rekening': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nomor Rekening','type':'number'}),
        }
        
class BendaharaForm(ModelForm):
    class Meta:
        model = Bendahara
        fields=['nama_bendahara','jenis_kelamin','alamat','no_hp','chat_id']
        widgets = {
            'nama_bendahara': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nama Bendahara'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control','placeholder':'Alamat'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control','type':'number','placeholder':'628xxxxxxxxxx'}),
             'chat_id': forms.TextInput(attrs={'class': 'form-control','placeholder':'Chat ID Telegram'}),

        }


class UserForm(ModelForm):
    class Meta:
        model= User
        fields =['username']
        help_texts ={
            'username':''
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
        }
        labels = {
            'username': 'Username*',
        }
class SantriForm(ModelForm):
    class Meta:
        model = Santri
        fields=['nama_santri','wilayah','jenis_kelamin','alamat','no_hp','chat_id']
        widgets = {
            'nama_santri': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nama Santri'}),
            'wilayah': forms.Select(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'alamat': forms.TextInput(attrs={'class': 'form-control','placeholder':'Alamat'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control','type':'number','placeholder':'628xxxxxxxxxx'}),
             'chat_id': forms.TextInput(attrs={'class': 'form-control','placeholder':'Chat ID Telegram'}),

        }