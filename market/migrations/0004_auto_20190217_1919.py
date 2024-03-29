# Generated by Django 2.1.5 on 2019-02-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20190216_2001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Client'},
        ),
        migrations.AlterModelOptions(
            name='produit',
            options={'ordering': ['publie_le'], 'verbose_name': 'Produit'},
        ),
        migrations.AddField(
            model_name='commande',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='client',
            name='panier',
            field=models.ManyToManyField(related_name='_client_panier_+', through='market.Commande', to='market.Produit', verbose_name='Commandes'),
        ),
    ]
