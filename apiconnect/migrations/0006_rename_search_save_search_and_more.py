# Generated by Django 4.2.4 on 2023-09-18 22:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apiconnect', '0005_share_study_share_search'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Search',
            new_name='Save_Search',
        ),
        migrations.RenameModel(
            old_name='SingleResult',
            new_name='Save_Study',
        ),
    ]
