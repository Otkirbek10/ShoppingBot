# Generated by Django 4.1.6 on 2023-02-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=150, null=True, verbose_name='Tg user_name'),
        ),
    ]
