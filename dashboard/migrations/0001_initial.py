# Generated by Django 2.2.26 on 2022-03-14 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('type', models.CharField(choices=[('Web', 'Web'), ('Mobile', 'Mobile')], max_length=16, verbose_name='Type')),
                ('framework', models.CharField(choices=[('Django', 'Django'), ('React Native', 'React Native')], max_length=16, verbose_name='Framework')),
                ('domain_name', models.CharField(max_length=50, verbose_name='Domain Name')),
                ('screenshot', models.URLField(blank=True, verbose_name='Screenshot')),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, verbose_name='Updated at')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Price')),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, verbose_name='Updated at')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(verbose_name='Active')),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, verbose_name='Updated at')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.App')),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Plan')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
