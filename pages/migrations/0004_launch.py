# Generated by Django 4.1.2 on 2022-10-21 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_upcominglaunch_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Launch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('launch_provider', models.CharField(max_length=75)),
                ('launch_location', models.CharField(max_length=75)),
                ('launch_date_time', models.CharField(max_length=75)),
                ('launch_status', models.CharField(max_length=75)),
                ('stream_url', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]