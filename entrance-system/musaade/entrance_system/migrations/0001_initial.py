# Generated by Django 4.0 on 2022-01-18 21:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import entrance_system.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssid', models.CharField(max_length=32, verbose_name='SSID')),
                ('password', models.CharField(max_length=64, verbose_name='Password')),
            ],
            options={
                'verbose_name': 'Access Point',
                'verbose_name_plural': 'Access Points',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='Name')),
                ('qr_code_type', models.CharField(choices=[('1', 'Personnel'), ('2', 'HES')], max_length=16, verbose_name='QR Code Type')),
                ('last_activity', models.DateTimeField(default=None, null=True, verbose_name='Last Activity')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('api_token', models.CharField(default=entrance_system.utils.api_token, max_length=96, unique=True, verbose_name='API Token')),
                ('access_point', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='entrance_system.accesspoint', verbose_name='Access Point')),
                ('departments', models.ManyToManyField(blank=True, default=None, to='entrance_system.Department', verbose_name='Departments')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('national_id', models.PositiveBigIntegerField(unique=True, verbose_name='National ID')),
                ('first_name', models.CharField(max_length=16, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=16, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='Email')),
                ('last_activity', models.DateTimeField(default=None, null=True, verbose_name='Last Activity')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('secret_token', models.CharField(default=entrance_system.utils.secret_token, max_length=16, unique=True, verbose_name='Secret Token')),
                ('qr_code_data', models.CharField(max_length=128, unique=True, verbose_name='QR Code Data')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entrance_system.department', verbose_name='Department')),
            ],
            options={
                'verbose_name': 'Personnel',
                'verbose_name_plural': 'Personnel',
            },
        ),
        migrations.CreateModel(
            name='PersonnelActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time')),
                ('result', models.BooleanField(default=False, verbose_name='Result')),
                ('message', models.CharField(default='', max_length=256, verbose_name='Message')),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='entrance_system.location', verbose_name='Location')),
                ('personnel', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='entrance_system.personnel', verbose_name='Personnel')),
            ],
            options={
                'verbose_name': 'Personnel Activity',
                'verbose_name_plural': 'Personnel Activity',
            },
        ),
        migrations.CreateModel(
            name='HESActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=16, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=16, verbose_name='Last Name')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time')),
                ('result', models.BooleanField(default=False, verbose_name='Result')),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='entrance_system.location', verbose_name='Location')),
            ],
            options={
                'verbose_name': 'HES Activity',
                'verbose_name_plural': 'HES Activity',
            },
        ),
    ]
