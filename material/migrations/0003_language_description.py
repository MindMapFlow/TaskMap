# Generated by Django 5.2 on 2025-05-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_alter_theory_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='description',
            field=models.TextField(default='описание отсутвует'),
            preserve_default=False,
        ),
    ]
