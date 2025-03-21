# Generated by Django 5.1.5 on 2025-02-25 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guitar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=20)),
                ('pickups', models.CharField(max_length=5)),
                ('model', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('image', models.URLField()),
                ('description', models.TextField()),
                ('shape', models.CharField(max_length=30)),
            ],
        ),
    ]
