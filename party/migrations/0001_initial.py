# Generated by Django 3.0.6 on 2020-05-31 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('party_id', models.UUIDField(primary_key=True, serialize=False, verbose_name='party UUID')),
                ('maps', models.TextField(verbose_name='selected maps list')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.UUIDField(primary_key=True, serialize=False, verbose_name='client steam auth id')),
                ('party_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='party.Party')),
            ],
        ),
    ]
