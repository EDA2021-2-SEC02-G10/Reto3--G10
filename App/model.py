"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from datetime import datetime
from os import pardir
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    analyzer = {'ufos': None,
                'cityIndex': None
                }

    analyzer['UFOS'] = lt.newList('ARRAY_LIST')
    analyzer['cityIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareCity)
    analyzer['secondsIndex'] = om.newMap(omaptype='RBT',
                                         comparefunction=compareDurationSec)
    analyzer['hourIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDurationHour)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDate)
    analyzer['longitudeIndex'] = om.newMap(omaptype='RBT',
                                           comparefunction=compareLongitude)

    return analyzer


# Funciones para agregar informacion al catalogo


def addUfo(analyzer, Datetime, city, state, country, shape,
           durationSec, durationHoursMin, dateposted, latitude, longitude):

    dictUfo = {}
    dictUfo['Datetime'] = Datetime
    dictUfo['City'] = city
    dictUfo['State'] = state
    dictUfo['Country'] = country
    dictUfo['Shape'] = shape
    dictUfo['DurationSec'] = durationSec
    dictUfo['DurationHM'] = durationHoursMin
    dictUfo['DatePosted'] = dateposted
    dictUfo['Latitude'] = latitude
    dictUfo['Longitude'] = longitude
    lt.addLast(analyzer['UFOS'], dictUfo)

    # Creacion arbol por ciudad
    if om.contains(analyzer['cityIndex'], city) is False:
        dictCity = {}
        lstCity = lt.newList('ARRAY_LIST')
        dictCity['Datetime'] = Datetime
        dictCity['Country'] = country
        dictCity['Shape'] = shape
        dictCity['DurationSec'] = durationSec
        lt.addLast(lstCity, dictCity)
        om.put(analyzer['cityIndex'], city, lstCity)
    else:
        cityEntry = om.get(analyzer['cityIndex'], city)
        cityList = me.getValue(cityEntry)
        dictCity = {}
        dictCity['Datetime'] = Datetime
        dictCity['Country'] = country
        dictCity['Shape'] = shape
        dictCity['DurationSec'] = durationSec
        lt.addLast(cityList, dictCity)

    # Creacion de arbol por duracion (Segundos)
    if om.contains(analyzer['secondsIndex'], durationSec) is False:
        dictCitySecs = {}
        lstCitySecs = lt.newList('ARRAY_LIST')
        dictCitySecs['Datetime'] = Datetime
        dictCitySecs['Country'] = country
        dictCitySecs['City'] = city
        dictCitySecs['Shape'] = shape
        dictCitySecs['DurationSec'] = durationSec
        lt.addLast(lstCitySecs, dictCity)
        om.put(analyzer['secondsIndex'], durationSec, lstCitySecs)
    else:
        durationSecsEntry = om.get(analyzer['secondsIndex'], durationSec)
        durationSecsList = me.getValue(durationSecsEntry)
        dictCitySecs = {}
        dictCitySecs['Datetime'] = Datetime
        dictCitySecs['Country'] = country
        dictCitySecs['City'] = city
        dictCitySecs['Shape'] = shape
        dictCitySecs['DurationSec'] = durationSec
        lt.addLast(durationSecsList, dictCitySecs)

    # Creacion indice de hora/minuto
    hourList = Datetime.split(' ')
    finalHourList = hourList[1]
    # datetime_object = datetime.strptime(finalHourList, '%H:%M:%S')
    if om.contains(analyzer['hourIndex'], finalHourList) is False:
        dictCityHour = {}
        lstCityHour = lt.newList('ARRAY_LIST')
        dictCityHour['Datetime'] = Datetime
        dictCityHour['Country'] = country
        dictCityHour['City'] = city
        dictCityHour['Shape'] = shape
        dictCityHour['DurationSec'] = durationSec
        lt.addLast(lstCityHour, dictCityHour)
        om.put(analyzer['hourIndex'], finalHourList, lstCityHour)
    else:
        durationHourEntry = om.get(analyzer['hourIndex'], finalHourList)
        durationHourList = me.getValue(durationHourEntry)
        dictCityHour = {}
        dictCityHour['Datetime'] = Datetime
        dictCityHour['Country'] = country
        dictCityHour['City'] = city
        dictCityHour['Shape'] = shape
        dictCityHour['DurationSec'] = durationSec
        lt.addLast(durationHourList, dictCityHour)

    # Creacion indice fecha
    date = hourList[0]
    if om.contains(analyzer['dateIndex'], date) is False:
        dictDate = {}
        dateLst = lt.newList('ARRAY_LIST')
        dictDate['Datetime'] = Datetime
        dictDate['Country'] = country
        dictDate['City'] = city
        dictDate['Shape'] = shape
        dictDate['DurationSec'] = durationSec
        lt.addLast(dateLst, dictDate)
        om.put(analyzer['dateIndex'], date, dateLst)
    else:
        dateEntry = om.get(analyzer['dateIndex'], date)
        dateLst = me.getValue(dateEntry)
        dictDate = {}
        dictDate['Datetime'] = Datetime
        dictDate['Country'] = country
        dictDate['City'] = city
        dictDate['Shape'] = shape
        dictDate['DurationSec'] = durationSec
        lt.addLast(dateLst, dictDate)

    # Creacion de indice de longitud
    if om.contains(analyzer['longitudeIndex'], longitude) is False:
        dictLongitude = {}
        longitudeLst = lt.newList('ARRAY_LIST')
        dictLongitude['Datetime'] = Datetime
        dictLongitude['Country'] = country
        dictLongitude['City'] = city
        dictLongitude['Shape'] = shape
        dictLongitude['DurationSec'] = durationSec
        dictLongitude['Latitude'] = latitude
        lt.addLast(longitudeLst, dictLongitude)
        om.put(analyzer['longitudeIndex'], longitude, longitudeLst)
    else:
        longitudeEntry = om.get(analyzer['longitudeIndex'], longitude)
        longitudeLst = me.getValue(longitudeEntry)
        dictLongitude = {}
        dictLongitude['Datetime'] = Datetime
        dictLongitude['Country'] = country
        dictLongitude['City'] = city
        dictLongitude['Shape'] = shape
        dictLongitude['DurationSec'] = durationSec
        dictLongitude['Latitude'] = latitude
        lt.addLast(longitudeLst, dictLongitude)

# Funciones para creacion de datos

# Funciones de consulta


def findSightingsCity(analyzer, city):

    lstCities = lt.newList('ARRAY_LIST')
    cities = om.keySet(analyzer['cityIndex'])
    totalCities = 0
    for cityT in lt.iterator(cities):
        if om.contains(analyzer['cityIndex'], cityT):
            dictTotal = {}
            cityLstEntry = om.get(analyzer['cityIndex'], cityT)
            cityLst = me.getValue(cityLstEntry)
            if lt.size(cityLst) != 0:
                totalCities += 1
            dictTotal[cityT] = lt.size(cityLst)
            lt.addLast(lstCities, dictTotal)

    sorted_list = ms.sort(lstCities, cmpCitiesBySightings)

    cityEntry = om.get(analyzer['cityIndex'], city)
    cityList = me.getValue(cityEntry)
    totalCitySightings = lt.size(cityList)
    sortCity = cityList.copy()
    sorted_city = ms.sort(sortCity, cmpByDatetime)

    return totalCities, sorted_list, totalCitySightings, sorted_city


# Funciones utilizadas para comparar elementos dentro de una lista


def compareCity(city1, city2):

    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1


def compareDurationSec(city1, city2):

    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1


def compareDurationHour(city1, city2):

    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1


def compareDate(city1, city2):

    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1


def compareLongitude(city1, city2):

    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1

# Funciones de ordenamiento


def cmpCitiesBySightings(city1, city2):

    city1F = (list(city1.values()))[0]
    city2F = (list(city2.values()))[0]
    r = True
    if city1F > city2F:
        r = False

    return r


def cmpByDatetime(city1, city2):

    date1 = city1['Datetime']
    datetime_object1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    date2 = city2['Datetime']
    datetime_object2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
    if datetime_object1 > datetime_object2:
        return False
    else:
        return True
