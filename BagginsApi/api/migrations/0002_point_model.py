# Generated by Django 4.2.10 on 2024-05-19 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='model',
            field=models.FileField(default=1, upload_to='upload_files/'),
            preserve_default=False,
        ),
    ]