# Generated by Django 4.1.6 on 2023-02-21 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0003_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.IntegerField(),
        ),
    ]
