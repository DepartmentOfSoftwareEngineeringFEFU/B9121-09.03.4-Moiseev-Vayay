# Generated by Django 5.1.3 on 2025-04-01 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("arbitrage", "0001_initial"),
        ("brokers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="exchanges",
            field=models.ManyToManyField(blank=True, to="brokers.exchange"),
        ),
    ]
