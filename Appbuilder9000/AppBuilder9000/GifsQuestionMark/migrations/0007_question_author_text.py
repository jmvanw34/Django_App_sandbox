# Generated by Django 2.2.5 on 2021-05-18 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GifsQuestionMark', '0006_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='author_text',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
