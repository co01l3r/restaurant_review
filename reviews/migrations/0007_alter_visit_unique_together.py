# Generated by Django 4.2.7 on 2023-11-16 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_review_rating_alter_review_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='visit',
            unique_together=set(),
        ),
    ]