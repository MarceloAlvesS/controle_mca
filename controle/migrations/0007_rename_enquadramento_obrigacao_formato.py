# Generated by Django 5.0.1 on 2024-02-13 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0006_rename_formato_obrigacao_enquadramento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='obrigacao',
            old_name='enquadramento',
            new_name='formato',
        ),
    ]
