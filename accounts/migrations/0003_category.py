# Generated by Django 2.2.2 on 2020-11-12 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_city_country_service_state_timestampmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('categoryId', models.AutoField(primary_key=True, serialize=False)),
                ('categoryName', models.CharField(blank=True, max_length=255, null=True)),
                ('serviceName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Service')),
            ],
            options={
                'verbose_name_plural': 'Category',
            },
        ),
    ]
