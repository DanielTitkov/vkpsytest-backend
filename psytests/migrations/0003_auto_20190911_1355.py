# Generated by Django 2.2.5 on 2019-09-11 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psytests', '0002_mockuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psytests.Scale')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psytests.MockUser')),
            ],
        ),
        migrations.CreateModel(
            name='Norm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(default='ALL', max_length=50)),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psytests.Scale')),
            ],
        ),
    ]
