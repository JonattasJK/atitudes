# Generated by Django 4.2 on 2024-02-07 11:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('breed', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
                ('score', models.IntegerField(default=0)),
                ('credits', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('stars', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('stage', models.IntegerField(default=1)),
                ('bookTitle', models.CharField(max_length=100, null=True)),
                ('continues', models.CharField(default='abertura1', max_length=20)),
                ('answerable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='livro1.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testimony', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=50)),
                ('date', models.DateField(default=datetime.datetime(2024, 2, 7, 8, 48, 49, 153375, tzinfo=datetime.timezone.utc))),
                ('address', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('cnpj', models.CharField(max_length=50)),
                ('foundation_date', models.DateTimeField(default=datetime.datetime(2024, 2, 7, 8, 48, 49, 146379, tzinfo=datetime.timezone.utc))),
                ('address', models.CharField(max_length=255)),
                ('accession', models.IntegerField(default=0)),
                ('log', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('relationship', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_number', models.CharField(max_length=5)),
                ('class_year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WishingRegistred',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StickerBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stickers', to='livro1.profile')),
            ],
        ),
        migrations.CreateModel(
            name='SavedBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livro1.profile')),
            ],
        ),
        migrations.CreateModel(
            name='QuestText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questNumber', models.CharField(max_length=25)),
                ('text', models.CharField(max_length=255)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questText', to='livro1.profile')),
            ],
        ),
        migrations.CreateModel(
            name='QuestConclude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questNumber', models.CharField(max_length=25)),
                ('score', models.IntegerField(default=0)),
                ('credits', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quests', to='livro1.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='related_school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='livro1.school'),
        ),
        migrations.AddField(
            model_name='profile',
            name='sponsor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='livro1.sponsor'),
        ),
        migrations.AddField(
            model_name='profile',
            name='student',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='livro1.student'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Discovery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('text', models.CharField(max_length=255)),
                ('sort', models.CharField(max_length=25)),
                ('found', models.ManyToManyField(to='livro1.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_ref', models.CharField(max_length=100)),
                ('paymentID', models.CharField(max_length=100)),
                ('mp_status', models.CharField(default='refused', max_length=100)),
                ('paid', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkout', to='livro1.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paragraph', models.CharField(max_length=255)),
                ('chapter', models.IntegerField(default=0)),
                ('style', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=12)),
                ('position', models.CharField(max_length=15)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paragraphs', to='livro1.profile')),
            ],
        ),
        migrations.CreateModel(
            name='AvatarHub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.CharField(default='/img/avatars/default.jpg', max_length=255)),
                ('background', models.CharField(default='/img/avatars/0/1.jpg', max_length=255)),
                ('acquired', models.ManyToManyField(to='livro1.avatar')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to='livro1.profile')),
            ],
        ),
    ]
