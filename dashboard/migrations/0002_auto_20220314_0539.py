# Generated by Django 2.2.26 on 2022-03-14 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='app',
            name='updated_at',
            field=models.DateTimeField(null=True, verbose_name='Updated at'),
        ),
    ]