# Generated by Django 4.0.4 on 2022-06-04 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0005_remove_authorprofile_profile_pic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='authorprofile',
            name='tagline',
            field=models.CharField(blank=True, default='I am blog user', max_length=200, null=True),
        ),
    ]
