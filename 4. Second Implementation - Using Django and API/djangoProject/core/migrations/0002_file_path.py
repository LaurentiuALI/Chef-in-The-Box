# Generated by Django 4.0.1 on 2022-01-25 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='path',
            field=models.CharField(default='yes', max_length=256),
            preserve_default=False,
        ),
    ]