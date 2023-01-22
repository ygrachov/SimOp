# Generated by Django 4.1.4 on 2023-01-16 23:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0006_remove_createinput_number_jf_agents_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createinput',
            name='reach_rate_h',
            field=models.FloatField(default=0.5, help_text='highest percentage of customers who answered the call out of those who received it', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='createinput',
            name='reach_rate_l',
            field=models.FloatField(default=0.01, help_text='lowest percentage of customers who answered the call out of those who received it', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='createinput',
            name='reach_rate_m',
            field=models.FloatField(default=0.3, help_text='average percentage of customers who answered the call out of those who received it', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='createinput',
            name='unreachable_h',
            field=models.FloatField(default=0.3, help_text='maximum percentage of unsuccessful attempts in a batch', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='createinput',
            name='unreachable_l',
            field=models.FloatField(default=0.1, help_text='minimum percentage of unsuccessful attempts in a batch', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='createinput',
            name='unreachable_m',
            field=models.FloatField(default=0.2, help_text='average percentage of unsuccessful attempts in a batch', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]