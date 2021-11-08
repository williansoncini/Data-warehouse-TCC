from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from application.models import ColumnsDatawarehouse, CubeColumnsDatawarehouse, CubeDatawarehouse, TableDatawarehouse
from application.services.database.datawarehouse import createViewWithStatement, selectDataFromView


class SelectColumns(View):
    def get(self, request):
        factTable = request.session['factTable']
        firstDimension = request.session['firstDimension']
        secondDimension = request.session['secondDimension']
        thirdDimension = request.session['thirdDimension']
        fourthDimension = request.session['fourthDimension']

        factTableDatawarehouse = TableDatawarehouse.objects.get(name=factTable)
        firstDimensionTableDatawarehouse = TableDatawarehouse.objects.get(name=firstDimension)
        secondDimensionTableDatawarehouse = TableDatawarehouse.objects.get(name=secondDimension)
        thirdDimensionTableDatawarehouse = TableDatawarehouse.objects.get(name=thirdDimension)
        fourthDimensionTableDatawarehouse = TableDatawarehouse.objects.get(name=fourthDimension)

        columnsFactTable = ColumnsDatawarehouse.objects.filter(table=factTableDatawarehouse.id)
        columnsFirstDimension = ColumnsDatawarehouse.objects.filter(table=firstDimensionTableDatawarehouse.id)
        columnsSecondDimension = ColumnsDatawarehouse.objects.filter(table=secondDimensionTableDatawarehouse.id)
        columnsThirdDimension = ColumnsDatawarehouse.objects.filter(table=thirdDimensionTableDatawarehouse.id)
        columnsFourthDimension = ColumnsDatawarehouse.objects.filter(table=fourthDimensionTableDatawarehouse.id)

        return render(request, 'application/datawarehouse/cubes/create/selectColumnsCube.html', {
            'factTableDatawarehouse':factTableDatawarehouse,
            'firstDimensionTableDatawarehouse':firstDimensionTableDatawarehouse,
            'secondDimensionTableDatawarehouse':secondDimensionTableDatawarehouse,
            'thirdDimensionTableDatawarehouse':thirdDimensionTableDatawarehouse,
            'fourthDimensionTableDatawarehouse':fourthDimensionTableDatawarehouse,
            'columnsFactTable': columnsFactTable,
            'columnsFirstDimension': columnsFirstDimension,
            'columnsSecondDimension': columnsSecondDimension,
            'columnsThirdDimension': columnsThirdDimension,
            'columnsFourthDimension': columnsFourthDimension
        })

    def post(self, request):
        factTable = request.session['factTable']
        firstDimension = request.session['firstDimension']
        secondDimension = request.session['secondDimension']
        thirdDimension = request.session['thirdDimension']
        fourthDimension = request.session['fourthDimension']

        factTableDatawarehouse = TableDatawarehouse.objects.get(name=factTable)
        firstDimensionTableDatawarehouse = TableDatawarehouse.objects.get(name=firstDimension)
        secondDimensionTableDatawarehouse = TableDatawarehouse.objects.get(name=secondDimension)
        thirdDimensionTableDatawarehouse = TableDatawarehouse.objects.get(name=thirdDimension)
        fourthDimensionTableDatawarehouse = TableDatawarehouse.objects.get(name=fourthDimension)

        firstColumnFactDimensionId = request.POST.get('first-fact-column-dimension')
        secondColumnFactDimensionId = request.POST.get('second-fact-column-dimension')
        thirdColumnFactDimensionId = request.POST.get('third-fact-column-dimension')
        fourthColumnFactDimensionId = request.POST.get('fourth-fact-column-dimension')

        firstColumnDimensionId = request.POST.get('first-column-dimension')
        secondColumnDimensionId = request.POST.get('second-column-dimension')
        thirdColumnDimensionId = request.POST.get('third-column-dimension')
        fourthColumnDimensionId = request.POST.get('fourth-column-dimension')

        firstColumnFactDimension = ColumnsDatawarehouse.objects.get(pk=firstColumnFactDimensionId)
        secondColumnFactDimension = ColumnsDatawarehouse.objects.get(pk=secondColumnFactDimensionId)
        thirdColumnFactDimension = ColumnsDatawarehouse.objects.get(pk=thirdColumnFactDimensionId)
        fourthColumnFactDimension = ColumnsDatawarehouse.objects.get(pk=fourthColumnFactDimensionId)

        firstColumnDimension = ColumnsDatawarehouse.objects.get(pk=firstColumnDimensionId)
        secondColumnDimension = ColumnsDatawarehouse.objects.get(pk=secondColumnDimensionId)
        thirdColumnDimension = ColumnsDatawarehouse.objects.get(pk=thirdColumnDimensionId)
        fourthColumnDimension = ColumnsDatawarehouse.objects.get(pk=fourthColumnDimensionId)

        cubeName = request.POST.get('cube-name')
        existsCube = CubeDatawarehouse.objects.filter(name=cubeName).first()
        if existsCube != None:
            messages.warning(request,'Nome de cube já existente!')
            return redirect('application:datawarehouse-cubes-select-tables-cubes')
            
        cubeDatawarehouse = CubeDatawarehouse(
            name=cubeName,
            factTable = factTableDatawarehouse,
            firstDimension = firstDimensionTableDatawarehouse,
            secondDimension = secondDimensionTableDatawarehouse,
            thirdDimension = thirdDimensionTableDatawarehouse,
            fourthDimension = fourthDimensionTableDatawarehouse
        )
        cubeDatawarehouse.save()

        
        firstDimensionCube = CubeColumnsDatawarehouse(cube=cubeDatawarehouse, fact=firstColumnFactDimension, dimension=firstColumnDimension)
        secondDimensionCube = CubeColumnsDatawarehouse(cube=cubeDatawarehouse, fact=secondColumnFactDimension, dimension=secondColumnDimension)
        thirdimensionCube = CubeColumnsDatawarehouse(cube=cubeDatawarehouse, fact=thirdColumnFactDimension, dimension=thirdColumnDimension)
        fourthDimensionCube = CubeColumnsDatawarehouse(cube=cubeDatawarehouse, fact=fourthColumnFactDimension, dimension=fourthColumnDimension)

        firstDimensionCube.save()
        secondDimensionCube.save()
        thirdimensionCube.save()
        fourthDimensionCube.save()

        tables = []
        tables.append(factTableDatawarehouse)
        tables.append(firstDimensionTableDatawarehouse)
        tables.append(secondDimensionTableDatawarehouse)
        tables.append(thirdDimensionTableDatawarehouse)
        tables.append(fourthDimensionTableDatawarehouse)

        factTablesJoin = []
        factTablesJoin.append(firstColumnFactDimension)
        factTablesJoin.append(secondColumnFactDimension)
        factTablesJoin.append(thirdColumnFactDimension)
        factTablesJoin.append(fourthColumnFactDimension)
        
        dimensionsJoin = []
        dimensionsJoin.append(firstColumnDimension)
        dimensionsJoin.append(secondColumnDimension)
        dimensionsJoin.append(thirdColumnDimension)
        dimensionsJoin.append(fourthColumnDimension)
        
        select = self.makeSelectWithTables(tables)
        joins = self.makeJoinsWithTables(factTablesJoin,dimensionsJoin)

        statementView = (select + joins)
        print(statementView)
        createViewWithStatement(cubeName, statementView)
        # allData = selectDataFromView(cubeName)
        # for row in allData:
        #     print(row)

        messages.success(request, 'successfully created cube')
        return redirect('application:datawarehouse-cubes')

    def makeSelectWithTables(self, tables):
        select = 'select '
        for table in tables:
            columns = ColumnsDatawarehouse.objects.filter(table=table)
            for column in columns:
                select += ('{}.{} as {}_{},'.format(column.table,column.name, column.table,column.name))
        select = select[:-1]
        select += ' from {}'.format(tables[0].name)
        return select
        
    def makeJoinsWithTables(self, factJoin, dimensionJoin):
        join = ' '
        for i in range(4):
            factColumn = ColumnsDatawarehouse.objects.get(pk=factJoin[i].id)
            dimensionColum = ColumnsDatawarehouse.objects.get(pk=dimensionJoin[i].id)
            join += 'inner join {} on {}.{} = {}.{} '.format(dimensionColum.table, factColumn.table, factColumn.name, dimensionColum.table, dimensionColum.name)
        return join
