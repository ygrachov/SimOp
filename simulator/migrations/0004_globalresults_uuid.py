# Generated by Django 4.0.2 on 2023-01-12 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0003_alter_globalresults_shift_finished_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalresults',
            name='uuid',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
