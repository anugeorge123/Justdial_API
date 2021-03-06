# Generated by Django 2.2.2 on 2020-11-12 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryName', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name_plural': 'Country',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('serviceId', models.AutoField(primary_key=True, serialize=False)),
                ('serviceName', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Service',
            },
        ),
        migrations.CreateModel(
            name='TimeStampModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stateName', models.CharField(blank=True, max_length=30, null=True)),
                ('countryName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Country')),
            ],
            options={
                'verbose_name_plural': 'State',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cityName', models.CharField(blank=True, max_length=30, null=True)),
                ('stateName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.State')),
            ],
            options={
                'verbose_name_plural': 'City',
            },
        ),
    ]
