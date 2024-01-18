# Generated by Django 5.0.1 on 2024-01-03 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebpageSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('link', models.URLField()),
                ('snapshot', models.ImageField(upload_to='webpage_snapshots/')),
            ],
        ),
    ]