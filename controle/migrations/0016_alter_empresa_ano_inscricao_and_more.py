# Generated by Django 5.0.1 on 2025-02-14 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0015_alter_empresa_ano_inscricao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='ano_inscricao',
            field=models.CharField(default='2024', max_length=4),
        ),
        migrations.AlterField(
            model_name='obrigacao',
            name='ano_inscricao',
            field=models.CharField(default='2024', max_length=4),
        ),
    ]
