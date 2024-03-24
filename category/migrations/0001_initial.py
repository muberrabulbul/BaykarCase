# Generated by Django 4.2.11 on 2024-03-23 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=225)),
                ('text', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
    ]
