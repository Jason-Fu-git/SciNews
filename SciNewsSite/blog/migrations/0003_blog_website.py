# Generated by Django 3.2.20 on 2023-08-26 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20230826_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='website',
            field=models.CharField(default='', max_length=20),
        ),
    ]
