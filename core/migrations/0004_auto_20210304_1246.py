# Generated by Django 2.2 on 2021-03-04 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210304_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_from', models.CharField(max_length=255)),
                ('email_to', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('sending', 'Enviando'), ('sended', 'Enviado'), ('error', 'Error'), ('cancel', 'Cancelado')], default='pending', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='core.Template')),
            ],
        ),
        migrations.DeleteModel(
            name='Email',
        ),
    ]