# Generated by Django 4.0.3 on 2022-05-20 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_user_followcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likedchirps',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
