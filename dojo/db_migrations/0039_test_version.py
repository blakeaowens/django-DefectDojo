# Generated by Django 2.2.12 on 2020-04-24 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0038_timezone_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='version',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
