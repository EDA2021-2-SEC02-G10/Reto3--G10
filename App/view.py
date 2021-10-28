"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
from DISClib.ADT import orderedmap as om
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printFindCitySightings(result):

    print('Hay ' + str(result[0]) + ' ciudades con avistamientos de UFOS')
    sorted_list = result[1]
    print('Las 5 ciudades con mas avistamientos son: ')
    print(lt.getElement(sorted_list, lt.size(sorted_list)))
    print(lt.getElement(sorted_list, -1))
    print(lt.getElement(sorted_list, -2))
    print(lt.getElement(sorted_list, -3))
    print(lt.getElement(sorted_list, -4))
    print('---------------------------------------------------------------------------------------------------')
    print('Hay ' + str(result[2]) + ' avistamientos en la ciudad pedida')
    print('Los primeros y ultimos 3 avistamientos cronologicamente son: ')
    finalList = result[3]
    print(lt.getElement(finalList, 1))
    print(lt.getElement(finalList, 2))
    print(lt.getElement(finalList, 3))
    print(lt.getElement(finalList, (lt.size(finalList)-2)))
    print(lt.getElement(finalList, (lt.size(finalList)-1)))
    print(lt.getElement(finalList, (lt.size(finalList)-0)))


def printCountSightingsByHour(result):

    print('Hay ' + str(result[0]) + ' horas de avistamientos diferentes registradas')
    lst1 = result[1]
    lst2 = result[3]
    print('Las ultimas 5 horas de avistamientos y su numero de avistamientos asociados son: ')
    print(lt.getElement(lst1, 1))
    print(lt.getElement(lst1, 2))
    print(lt.getElement(lst1, 3))
    print(lt.getElement(lst1, 4))
    print(lt.getElement(lst1, 5))

    print('-----------------------------------------------------------------------------------------------------------------------')
    print('En el rango dado el total de avistamientos es: ' + str(result[2]))
    print('Los primeros y ultimos 3 avistamientos cronologicamente de el rango de horas dadas son: ')
    print(lt.getElement(lst2, 1))
    print(lt.getElement(lst2, 2))
    print(lt.getElement(lst2, 3))
    print(lt.getElement(lst2, -2))
    print(lt.getElement(lst2, -1))
    print(lt.getElement(lst2, lt.size(lst2)))


def printSightingsByRegion(result):

    print('En la region geografica hay ' + str(result[0]) + ' avistamientos')
    lst = result[1]
    print('Los primeros y ultimos 3 avistamientos en orden de ubicacion cronologico son: ')
    print(lt.getElement(lst, 1))
    print(lt.getElement(lst, 2))
    print(lt.getElement(lst, 3))
    print(lt.getElement(lst, -2))
    print(lt.getElement(lst, -1))
    print(lt.getElement(lst, lt.size(lst)))


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Contar los avistamientos en una ciudad")
    print("3- Contar los avistamientos por duracion")
    print("4- Contar los avistamientos por hora/minuto del dia")
    print("5- Contar losa avistamientos en un rango de fechas")
    print("6- Contar los avistamientos en una zona geografica")
    print("7- Visualizar los avistamientos de una zona geográfica")


analyzer = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        analyzer = controller.init()
        controller.loadData(analyzer)
        print('Se cargaron un total de ' + str(lt.size(analyzer['UFOS'])) + ' avistamientos')
        print('Los primeros y ultimos 3 avistamientos cargados son: ')
        print(lt.getElement(analyzer["UFOS"], 1))
        print(lt.getElement(analyzer["UFOS"], 2))
        print(lt.getElement(analyzer["UFOS"], 3))
        print(lt.getElement(analyzer["UFOS"], -1))
        print(lt.getElement(analyzer["UFOS"], -2))
        print(lt.getElement(analyzer["UFOS"], -3))

    elif int(inputs[0]) == 2:

        inputCity = input('Digite el nombre de la ciudad de la cual desea consultar los avistamientos: ')
        result = controller.findSightingsCity(analyzer, inputCity)
        printFindCitySightings(result)

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:

        li = input('Limite inicial de formato HH:MM : ')
        lf = input('LImite final de formato HH:MM : ')
        result = controller.countSightingsByHour(analyzer, li, lf)
        printCountSightingsByHour(result)

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:

        loni = float(input('Limite minimo de longitud: '))
        lonf = float(input('Limite maximo de longitud: '))
        lati = float(input('Limite minimo de latitud: '))
        latf = float(input('Limite maximo de latitud: '))
        result = controller.findSightingsByRegion(analyzer, loni, lonf, lati, latf)
        printSightingsByRegion(result)

    elif int(inputs[0]) == 7:

        result = controller.seeSightingsByRegion(analyzer, loni, lonf, lati, latf)
        printSightingsByRegion(result)

    else:
        sys.exit(0)
sys.exit(0)
