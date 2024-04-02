# Generated by Django 5.0.1 on 2024-03-16 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0008_alter_empresa_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='enquadramento',
            field=models.CharField(blank=True, choices=[('', '____________'), ('s-m', 'Simples Matriz'), ('s-f', 'Simples Filial'), ('l-m', 'Lucro Real Matriz'), ('l-f', 'Lucro Real Filial'), ('p-m', 'Presumido Matriz'), ('p-f', 'Presumido Filial'), ('t', 'Terceiro Setor')], default='', max_length=3),
        ),
    ]
