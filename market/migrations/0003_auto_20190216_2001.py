# Generated by Django 2.1.5 on 2019-02-16 20:01

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('market', '0002_auto_20190213_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('telephone', models.CharField(max_length=100)),
                ('lieux_livraison', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=1, null=True)),
                ('est_paye', models.BooleanField(default=False, verbose_name='Commande payée ?')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Client')),
            ],
        ),
        migrations.AlterModelOptions(
            name='categorie',
            options={'verbose_name': 'Categorie Produit'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Image'},
        ),
        migrations.AlterModelOptions(
            name='produit',
            options={'ordering': ['date_ajout'], 'verbose_name': 'Produit'},
        ),
        migrations.AlterModelOptions(
            name='produitimage',
            options={'ordering': ['produit'], 'verbose_name': 'Produit  avec des images'},
        ),
        migrations.AddField(
            model_name='commande',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Produit'),
        ),
        migrations.AddField(
            model_name='client',
            name='panier',
            field=models.ManyToManyField(related_name='_client_panier_+', through='market.Commande', to='market.Produit'),
        ),
    ]
