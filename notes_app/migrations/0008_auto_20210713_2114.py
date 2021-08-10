# Generated by Django 3.2.5 on 2021-07-13 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes_app', '0007_profile_is_subscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptiontype',
            name='day_limit',
        ),
        migrations.RemoveField(
            model_name='subscriptiontype',
            name='price',
        ),
        migrations.AddField(
            model_name='subscription',
            name='day_limit',
            field=models.PositiveIntegerField(default=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='price',
            field=models.PositiveIntegerField(default=456),
            preserve_default=False,
        ),
    ]