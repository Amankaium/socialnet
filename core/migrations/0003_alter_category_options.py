# Generated by Django 4.2.3 on 2023-08-02 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_category_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
    ]
