# Generated by Django 3.2.13 on 2022-07-08 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20220708_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerequest',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customerrs', to='core.customuserregistration'),
        ),
    ]
