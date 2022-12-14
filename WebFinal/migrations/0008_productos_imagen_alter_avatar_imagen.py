# Generated by Django 4.1.2 on 2022-11-25 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebFinal', '0007_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='avatares/'),
        ),
    ]
