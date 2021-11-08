# Generated by Django 3.2.4 on 2021-11-07 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnsDatawarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('id',),
            },
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
                ('database', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('host', models.CharField(max_length=20)),
                ('port', models.IntegerField()),
                ('localdatabase', models.BooleanField(default='0')),
            ],
            options={
                'ordering': ('-updated',),
            },
        ),
        migrations.CreateModel(
            name='ExtractConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('database', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('host', models.CharField(max_length=20)),
                ('port', models.IntegerField()),
                ('localdatabase', models.BooleanField(default='0')),
            ],
        ),
        migrations.CreateModel(
            name='TableDatawarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-updated',),
            },
        ),
        migrations.CreateModel(
            name='TableStagingArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tableName', models.CharField(max_length=250)),
                ('statementCreateTable', models.TextField(null=True)),
                ('statementSelect', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('filePath', models.TextField()),
            ],
            options={
                'ordering': ('name',),
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
                'ordering': ('-updated',),
            },
        ),
        migrations.CreateModel(
            name='importationDatamart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datamart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='importation_datamart', to='application.datamart')),
                ('tableDatamart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='importation_tableDatamart', to='application.tabledatamart')),
            ],
        ),
        migrations.CreateModel(
            name='CubeDatawarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('factTable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cube_fact_tableDatawarehouse', to='application.tabledatawarehouse')),
                ('firstDimension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cube_first_dimension_tableDatawarehouse', to='application.tabledatawarehouse')),
                ('fourthDimension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cube_fourth_dimension_tableDatawarehouse', to='application.tabledatawarehouse')),
                ('secondDimension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cube_second_dimension_tableDatawarehouse', to='application.tabledatawarehouse')),
                ('thirdDimension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cube_third_dimension_tableDatawarehouse', to='application.tabledatawarehouse')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CubeColumnsDatawarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cube', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cube_cube_columns', to='application.cubedatawarehouse')),
                ('dimension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dimention_column_id', to='application.columnsdatawarehouse')),
                ('fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fact_column_id', to='application.columnsdatawarehouse')),
            ],
        ),
        migrations.CreateModel(
            name='ColumnStagingArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('typeColumn', models.CharField(choices=[('INT', 'INT'), ('VARCHAR', 'VARCHAR'), ('FLOAT', 'FLOAT')], max_length=30)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stagingarea_table_column', to='application.tablestagingarea')),
            ],
        ),
        migrations.AddField(
            model_name='columnsdatawarehouse',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column_datawarehouse', to='application.tabledatawarehouse'),
        ),
        migrations.CreateModel(
            name='ColumnDataMart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column_datamart', to='application.tabledatamart')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
