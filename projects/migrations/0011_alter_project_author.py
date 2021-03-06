# Generated by Django 3.2.4 on 2021-09-28 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210928_2202'),
        ('projects', '0010_auto_20210928_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Projects authors'),
        ),
    ]
