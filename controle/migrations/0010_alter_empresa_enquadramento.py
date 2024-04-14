# Generated by Django 5.0.1 on 2024-04-14 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0009_alter_empresa_enquadramento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='enquadramento',
            field=models.CharField(blank=True, choices=[('', '____________'), ('l-m', 'Lucro Real Matriz'), ('l-f', 'Lucro Real Filial'), ('m', 'Mei'), ('p-m', 'Presumido Matriz'), ('p-f', 'Presumido Filial'), ('s-m', 'Simples Matriz'), ('s-f', 'Simples Filial'), ('t', 'Terceiro Setor')], default='', max_length=3),
        ),
    ]