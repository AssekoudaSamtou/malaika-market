# Generated by Django 2.1.5 on 2019-02-19 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20190217_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='est_suppr',
            field=models.BooleanField(default=False, verbose_name='Commande supprimée ?'),
        ),
    ]
