# Generated by Django 2.2.4 on 2019-10-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_admin', '0003_auto_20191016_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slo',
            name='slo_code',
            field=models.CharField(max_length=10),
        ),
    ]