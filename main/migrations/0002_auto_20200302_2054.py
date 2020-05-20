# Generated by Django 2.1.2 on 2020-03-02 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30, unique=True)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=12)),
            ],
        ),
        migrations.AlterModelOptions(
            name='trajectorydata',
            options={'ordering': ['datetime']},
        ),
        migrations.AlterField(
            model_name='trajectorydata',
            name='trajectoryRecordId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TrajectoryRecord', verbose_name='记录ID'),
        ),
    ]
