# Generated by Django 4.1.3 on 2022-12-15 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('featured', models.BooleanField()),
                ('administrator', models.CharField(max_length=75, null=True)),
                ('type', models.CharField(max_length=75, null=True)),
                ('country_code', models.CharField(max_length=25)),
                ('abbreviation', models.CharField(max_length=25)),
                ('description', models.TextField(null=True)),
                ('founding_year', models.CharField(max_length=4, null=True)),
                ('launchers', models.CharField(max_length=75, null=True)),
                ('spacecrafts', models.CharField(max_length=75, null=True)),
                ('total_launches', models.IntegerField()),
                ('successful_launches', models.IntegerField()),
                ('consecutive_successful_launches', models.IntegerField()),
                ('failed_launches', models.IntegerField()),
                ('pending_launches', models.IntegerField()),
                ('home_webpage', models.URLField(null=True)),
                ('wiki_page', models.URLField(null=True)),
                ('nation_image', models.ImageField(null=True, upload_to='')),
                ('logo', models.ImageField(null=True, upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Agencies',
            },
        ),
        migrations.CreateModel(
            name='Astronaut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('nationality', models.CharField(max_length=75)),
                ('agency', models.CharField(blank=True, max_length=75, null=True)),
                ('status', models.CharField(max_length=75)),
                ('bio', models.TextField()),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='UpcomingLaunch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('launch_provider', models.CharField(max_length=75)),
                ('launch_provider_abbrev', models.CharField(max_length=75)),
                ('launch_location', models.CharField(max_length=75)),
                ('launch_date_time', models.CharField(max_length=75)),
                ('launch_status', models.CharField(max_length=75)),
                ('stream_url', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Launches',
            },
        ),
    ]
