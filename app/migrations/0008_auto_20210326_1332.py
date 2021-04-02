# Generated by Django 3.1.5 on 2021-03-26 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210326_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('TopWears', 'Top Wears'), ('FrontWears', 'Front Wears'), ('Stationary', 'Stationary'), ('Electronics', 'Electronics'), ('DailyNeeds', 'Daily needs'), ('Services', 'services'), ('Fashion', 'Fashion'), ('Mobiles', 'Mobiles'), ('Laptop', 'Laptop')], max_length=20),
        ),
    ]
