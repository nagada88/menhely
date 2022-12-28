# Generated by Django 4.0.3 on 2022-12-20 22:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_menhely', '0002_alter_allat_eletkor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bemutatkozas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cim', models.CharField(max_length=200)),
                ('tartalom', models.TextField()),
                ('bemutatkozas_main_img', models.ImageField(upload_to='app_menhely/img/photos')),
                ('priority', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
            ],
        ),
    ]
