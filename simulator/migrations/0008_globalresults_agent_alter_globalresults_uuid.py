# Generated by Django 4.1.4 on 2023-01-29 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0007_alter_createinput_reach_rate_h_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalresults',
            name='agent',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='globalresults',
            name='uuid',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
