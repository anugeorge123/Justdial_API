# Generated by Django 2.2.2 on 2020-11-23 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_rp_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rating',
            new_name='comment',
        ),
    ]
