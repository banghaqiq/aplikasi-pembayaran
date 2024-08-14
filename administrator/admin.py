from django.contrib import admin
from .models import SettingPembayaran,Wilayah, Santri, Bendahara, Detail_nominal_santri, Jenis_pembayaran,Bank

admin.site.register(Wilayah)
admin.site.register(Santri)
admin.site.register(Bendahara)
admin.site.register(Detail_nominal_santri)
admin.site.register(Jenis_pembayaran)
admin.site.register(SettingPembayaran)
admin.site.register(Bank)
# Register your models here.