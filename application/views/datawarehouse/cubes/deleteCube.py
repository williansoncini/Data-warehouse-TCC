from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect

from application.models import ColumnsDatawarehouse, CubeColumnsDatawarehouse, CubeDatawarehouse
from application.services.database.datawarehouse import deleteView, selectDataFromView

class DeleteCube(View):
    def get(self, request, cube_id):
        cube = CubeDatawarehouse.objects.get(pk=cube_id)
        
        factTable = cube.factTable
        firstDimension = cube.firstDimension
        secondDimension = cube.secondDimension
        thirdDimension = cube.thirdDimension
        fourthDimension = cube.fourthDimension
              
        tables = []
        tables.append(factTable)
        tables.append(firstDimension)
        tables.append(secondDimension)
        tables.append(thirdDimension)
        tables.append(fourthDimension)

        tableAndColumns = []
        for table in tables:
            columns = ColumnsDatawarehouse.objects.filter(table=table)
            data = {
                'table': table,
                'columns': columns
            }
            tableAndColumns.append(data)

        data = selectDataFromView(cube.name)

        return render(request,'application/datawarehouse/cubes/deleteCube.html',{
            'cube':cube,
            'tableAndColumns':tableAndColumns,
            'data':data
        })

    def post(self, request, cube_id):
        cube = CubeDatawarehouse.objects.get(pk=cube_id)
        deleteView(cube.name)
        print(cube.name)
        cube.delete()

        messages.success(request,'The cube was successfully deleted!!')
        return redirect('application:datawarehouse-cubes')

