# Generated by Django 5.0.1 on 2024-01-30 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0004_remove_obrigacao_abril_remove_obrigacao_agosto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='obrigacao',
            name='empresa',
        ),
        migrations.AddField(
            model_name='competencia',
            name='obs',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='obrigacao',
            name='empresas',
            field=models.ManyToManyField(related_name='obrigacoes', through='controle.Competencia', to='controle.empresa'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='nome',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='obrigacao',
            name='nome',
            field=models.CharField(max_length=50),
        ),
    ]
