# Generated by Django 5.0.1 on 2024-02-08 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='enquadramento',
            field=models.CharField(blank=True, choices=[('', '____________'), ('s-m', 'Simples Matrix'), ('s-f', 'Simples Filial'), ('l-m', 'Lucro Real Matrix'), ('l-f', 'Lucro Real Filial'), ('p-m', 'Presumido Matrix'), ('p-f', 'Presumido Filial'), ('t', 'Terceiro Setor')], default='', max_length=3),
        ),
    ]
