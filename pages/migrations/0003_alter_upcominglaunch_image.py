# Generated by Django 4.1.2 on 2022-10-21 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_upcominglaunch_stream_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upcominglaunch',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]