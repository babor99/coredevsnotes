# Generated by Django 3.2.5 on 2021-07-12 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes_app', '0003_remove_subscription_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='subscription_type',
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='price',
            field=models.PositiveIntegerField(default=23),
            preserve_default=False,
        ),
    ]
