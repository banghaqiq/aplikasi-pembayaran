# Generated by Django 5.0.7 on 2024-07-16 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0002_alter_settingpembayaran_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingpembayaran',
            name='file_bukti',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to='arsip/file_bukti'),
        ),
    ]
