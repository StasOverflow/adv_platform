# Generated by Django 2.1.7 on 2019-03-25 14:31

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('adv_board', '0004_announcement_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='category',
        ),
        migrations.AddField(
            model_name='announcement',
            name='category',
            field=mptt.fields.TreeForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='works', to='adv_board.Category', verbose_name='parent category'),
            preserve_default=False,
        ),
    ]
