# Generated by Django 5.0.1 on 2024-02-13 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0004_alter_competencia_abril_alter_competencia_agosto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competencia',
            name='formato',
        ),
        migrations.AddField(
            model_name='obrigacao',
            name='formato',
            field=models.CharField(choices=[('M', 'Mensal'), ('A', 'Anual')], default='M', max_length=1),
        ),
    ]
