# Generated by Django 4.1.6 on 2023-02-24 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0004_alter_cart_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('phone', models.IntegerField()),
                ('product', models.CharField(max_length=255, verbose_name='Product nomi')),
            ],
        ),
    ]