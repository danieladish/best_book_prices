# Generated by Django 4.1.6 on 2023-08-22 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_rename_user_userprofile_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='username',
            new_name='user',
        ),
    ]