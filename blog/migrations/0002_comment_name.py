# Generated by Django 3.2.6 on 2021-08-11 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(default='Someone', max_length=80),
            preserve_default=False,
        ),
    ]