# Generated by Django 2.1.7 on 2019-03-25 21:07

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('adv_board', '0006_auto_20190325_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d')),
                ('url', models.URLField(max_length=400)),
            ],
        ),
        migrations.AlterField(
            model_name='announcement',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='adv_board.Category', verbose_name='parent category'),
        ),
        migrations.AddField(
            model_name='imagefile',
            name='announcement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='adv_board.Announcement'),
        ),
    ]