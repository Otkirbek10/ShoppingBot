# Generated by Django 4.1.6 on 2023-02-16 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0002_alter_user_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField()),
                ('product', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
