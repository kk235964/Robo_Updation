# Generated by Django 3.1.5 on 2021-05-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210316_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='regnum',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]