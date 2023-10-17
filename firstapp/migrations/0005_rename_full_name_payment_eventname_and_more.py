# Generated by Django 4.2.3 on 2023-09-29 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='full_name',
            new_name='eventname',
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]