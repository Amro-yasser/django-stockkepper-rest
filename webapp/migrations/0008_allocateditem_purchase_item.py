# Generated by Django 2.0 on 2018-01-28 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_allocateditem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocateditem',
            name='purchase_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.PurchaseItem'),
            preserve_default=False,
        ),
    ]
