# Generated by Django 5.0.1 on 2025-02-13 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0013_alter_competencia_ano'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='ano_inscricao',
            field=models.CharField(default='2024', max_length=4),
        ),
        migrations.AddField(
            model_name='obrigacao',
            name='ano_inscricao',
            field=models.CharField(default='2024', max_length=4),
        ),
    ]
