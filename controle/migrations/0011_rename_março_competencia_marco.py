# Generated by Django 5.0.1 on 2024-04-16 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0010_alter_empresa_enquadramento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competencia',
            old_name='março',
            new_name='marco',
        ),
    ]
