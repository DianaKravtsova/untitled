# Generated by Django 3.0.3 on 2020-03-12 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20200313_0217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='filmmaker',
        ),
        migrations.AddField(
            model_name='film',
            name='filmmaker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='filmmaker', to='movies.Filmmaker', verbose_name='режиссер'),
        ),
    ]
