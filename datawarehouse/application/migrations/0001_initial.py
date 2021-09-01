# Generated by Django 3.2.4 on 2021-08-31 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnStagingArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('typeColumn', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CsvFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('size', models.FloatField()),
                ('uploadDate', models.DateTimeField(auto_now_add=True)),
                ('withHeader', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Datamart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('incative', 'Inactive')], default='Active', max_length=20)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='TableStagingArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tableName', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('filePath', models.TextField()),
                ('size', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeSimple', models.CharField(choices=[('text', 'TEXT'), ('text(#)', 'TEXT(#)'), ('number', 'NUMBER'), ('number(#,#)', 'NUMBER(#,#)')], max_length=50)),
                ('typeDataBase', models.CharField(choices=[('int', 'INT'), ('varchar(250)', 'VARCHAR(250)'), ('varchar(#)', 'VARCHAR(#)'), ('char(1)', 'CHAR(1)'), ('double(14,4)', 'DOUBLE(14,4)'), ('double(#,#)', 'DOUBLE(#,#)')], max_length=50)),
            ],
            options={
                'ordering': ('-typeSimple',),
            },
        ),
        migrations.CreateModel(
            name='TableDataMart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='Active', max_length=20)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('datamart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_datamart', to='application.datamart')),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='ExpressionColumnStagingArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.TextField()),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stagingarea_column_expression', to='application.columnstagingarea')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stagingarea_table_expression', to='application.tablestagingarea')),
            ],
        ),
        migrations.AddField(
            model_name='columnstagingarea',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stagingarea_table_column', to='application.tablestagingarea'),
        ),
        migrations.CreateModel(
            name='ColumnDataMart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column_datamart', to='application.tabledatamart')),
                ('typeSimple', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column_typeSimple', to='application.typedata')),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
    ]
