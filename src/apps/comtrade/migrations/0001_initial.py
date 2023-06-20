# Generated by Django 4.2.2 on 2023-06-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.TextField(blank=True, max_length=255)),
                ('iso_alpha3_code', models.CharField(blank=True, max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='HSCode',
            fields=[
                ('id', models.CharField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField(blank=True, max_length=255)),
            ],
        ),
    ]
