# Generated by Django 2.2.2 on 2019-11-26 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resdig', '0002_auto_20190511_0358'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Errotable',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='cpu',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='cpufrom',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='memory',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='memoryfrom',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='motherboard',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='motherboardfrom',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='power',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='powerfrom',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='storage',
        ),
        migrations.RemoveField(
            model_name='etable',
            name='storagefrom',
        ),
        migrations.AlterField(
            model_name='appversiontable',
            name='updatetime',
            field=models.FloatField(default=1574772761.819489),
        ),
        migrations.AlterField(
            model_name='broadcasttable',
            name='casttime',
            field=models.FloatField(default=1574772761.8197346),
        ),
        migrations.AlterField(
            model_name='donatetable',
            name='donatetime',
            field=models.FloatField(default=1574772761.8200426, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='feedbacktable',
            name='time',
            field=models.FloatField(default=1574772761.8189123),
        ),
        migrations.AlterField(
            model_name='keywordtable',
            name='lastdigtime',
            field=models.FloatField(default=1574772761.8184438),
        ),
        migrations.AlterField(
            model_name='messagetable',
            name='time',
            field=models.FloatField(default=1574772761.819204),
        ),
        migrations.AlterField(
            model_name='resourcetable',
            name='scantime',
            field=models.FloatField(default=1574772761.818151),
        ),
    ]
