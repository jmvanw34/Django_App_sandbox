# Generated by Django 2.2.5 on 2021-03-24 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GifsQuestionMark', '0002_auto_20210324_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotes',
            name='quote_content',
            field=models.TextField(max_length=600),
        ),
    ]
