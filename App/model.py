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
from os import pardir, truncate
from DISClib.DataStructures.bst import maxKey, maxKeyNode
from DISClib.DataStructures.rbt import maxKeyTree
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf
import folium 
import webbrowser

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
        lstCitySecs = lt.newList('ARRAY_LIST')
        dictCitySecs = {}
        dictCitySecs['Datetime'] = Datetime
        dictCitySecs['City'] = city
        dictCitySecs['Country'] = country
        dictCitySecs['DurationSec'] = durationSec
        dictCitySecs['Shape'] = shape
        lt.addLast(lstCitySecs, dictCitySecs)
        ms.sort(lstCitySecs,cmpByPlace)
        om.put(analyzer['secondsIndex'], durationSec, lstCitySecs)

    else:
        durationSecsEntry = om.get(analyzer['secondsIndex'], durationSec)
        durationSecsList = me.getValue(durationSecsEntry)
        dictCitySecs = {}
        dictCitySecs['Datetime'] = Datetime
        dictCitySecs['City'] = city
        dictCitySecs['Country'] = country
        dictCitySecs['DurationSec'] = durationSec
        dictCitySecs['Shape'] = shape
        lt.addLast(durationSecsList, dictCitySecs)
        ms.sort(durationSecsList,cmpByPlace)

    # Creacion indice de hora/minuto
    hourList = Datetime.split(' ')
    finalHourList = hourList[1]
    # datetime_object = datetime.strptime(finalHourList, '%H:%M:%S')
    if om.contains(analyzer['hourIndex'], finalHourList) is False:
        dictCityHour = {}
        lstCityHour = lt.newList('ARRAY_LIST')
        dictCityHour['Datetime'] = Datetime
        dictCityHour['Country'] = country
        dictCityHour['State'] = state
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
        dictCityHour['State'] = state
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
        dictDate['City'] = city
        dictDate['Country'] = country
        dictDate['DurationSec'] = durationSec
        dictDate['Shape'] = shape
        lt.addLast(dateLst, dictDate)
        om.put(analyzer['dateIndex'], date, dateLst)
    else:
        dateEntry = om.get(analyzer['dateIndex'], date)
        dateLst = me.getValue(dateEntry)
        dictDate = {}
        dictDate['Datetime'] = Datetime
        dictDate['City'] = city
        dictDate['Country'] = country
        dictDate['DurationSec'] = durationSec
        dictDate['Shape'] = shape
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


def Sightingsbyseconds(analyzer, secondsmin, secondsmax):
    total_avistamientos = 0
    duracion_mas_larga = om.maxKey(analyzer['secondsIndex'])
    valoresmaximo = om.get(analyzer['secondsIndex'],duracion_mas_larga)
    valoresmaximo2 = me.getValue(valoresmaximo)
    total_avistamientos_maximo = lt.size(valoresmaximo2)

    intervalo =om.values(analyzer['secondsIndex'],secondsmin,secondsmax)
    lista_avistamientos = lt.newList('ARRAY_LIST')
    for x in lt.iterator(intervalo):
        total_avistamientos += lt.size(x)
        for y in lt.iterator(x):
            lt.addLast(lista_avistamientos,y)
    return(duracion_mas_larga,total_avistamientos_maximo,lista_avistamientos,total_avistamientos)


def countSightingsByHour(analyzer, li, lf):

    totalTimes = om.keySet(analyzer['hourIndex'])
    timesCounter = 0
    lstTimes = lt.newList('ARRAY_LIST')
    for time in lt.iterator(totalTimes):
        dictTemp = {}
        entryTime = om.get(analyzer['hourIndex'], time)
        timeList = me.getValue(entryTime)
        if lt.size(timeList) > 0:
            timesCounter += 1
            dictTemp[time] = lt.size(timeList)
            lt.addLast(lstTimes, dictTemp)

    sorted_list = ms.sort(lstTimes, cmpHourBySightings)

    ch = lf[4]
    chf = str(int(lf[4])+1)
    lff = lf[:4]+chf
    print(lff)
    rangeKeys = om.keys(analyzer['hourIndex'], li, lff)
    totalRangeSightings = 0
    lstRange = lt.newList('ARRAY_LIST')
    for key in lt.iterator(rangeKeys):
        entryKey = om.get(analyzer['hourIndex'], key)
        lstKey = me.getValue(entryKey)
        if lt.size(lstKey) > 0:
            totalRangeSightings += lt.size(lstKey)
            for element in lt.iterator(lstKey):
                dictTemp = {}
                dictTemp['HH:MM'] = key
                dictTemp['Datetime'] = element['Datetime']
                dictTemp['City'] = element['City']
                dictTemp['State'] = element['State']
                dictTemp['Shape'] = element['Shape']
                dictTemp['DurationSec'] = element['DurationSec']
                lt.addLast(lstRange, dictTemp)

    finalList = ms.sort(lstRange, cmpByHour)

    return timesCounter, sorted_list, totalRangeSightings, finalList


def Sightingsbydate (analyzer, date1, date2):
    total_avistamientos = 0
    fecha_mas_pequeña = om.minKey(analyzer['dateIndex'])
    fechaminima = om.get(analyzer['dateIndex'],fecha_mas_pequeña)
    fechaminima2 = me.getValue(fechaminima)
    total_avistamientos_minimo = lt.size(fechaminima2)
    
    intervalofechas = om.values(analyzer['dateIndex'],date1,date2)
    lista_avistamientos = lt.newList('ARRAY_LIST')
    for x in lt.iterator(intervalofechas):
        total_avistamientos += lt.size(x)
        for y in lt.iterator(x):
            lt.addLast(lista_avistamientos,y)

    return (fecha_mas_pequeña,total_avistamientos_minimo,lista_avistamientos,total_avistamientos)


def findSightingsByRegion(analyzer, loni, lonf, lati, latf):

    # Creacion de lista de avisamientos en la region
    longitudeValues = om.keys(analyzer['longitudeIndex'], float(loni), float(lonf))
    lstRangeElements = lt.newList('ARRAY_LIST')
    for longitude in lt.iterator(longitudeValues):
        longitudeEntry = om.get(analyzer['longitudeIndex'], longitude)
        longitudeLst = me.getValue(longitudeEntry)
        for element in lt.iterator(longitudeLst):
            if (element['Latitude']) >= (lati) and (element['Latitude']) <= (latf):
                dictTemp = {}
                dictTemp['Longitude'] = longitude
                dictTemp['Latitude'] = element['Latitude']
                dictTemp['Datetime'] = element['Datetime']
                dictTemp['Country'] = element['Country']
                dictTemp['City'] = element['City']
                dictTemp['DurationSec'] = element['DurationSec']
                dictTemp['Shape'] = element['Shape']
                lt.addLast(lstRangeElements, dictTemp)

    sightingsRange = lt.size(lstRangeElements)
    sorted_list = ms.sort(lstRangeElements, cmpByDatetime)

    return sightingsRange, sorted_list


def seeSightingsByRegion(analyzer, loni, lonf, lati, latf):

    result = findSightingsByRegion(analyzer, loni, lonf, lati, latf)

    midpointLon = (loni + lonf)/2
    midpointLat = (lati + latf)/2
    myMap = folium.Map(location=[midpointLat, midpointLon], zoom_start=7)
    for sighting in lt.iterator(result[1]):
        lat = int(sighting['Latitude'])
        lon = int(sighting['Longitude'])
        folium.Marker([lat, lon], popup="UFO").add_to(myMap)

    myMap.save("map.html")
    webbrowser.open("map.html")

    return result[0], result[1]
# Funciones utilizadas para comparar elementos dentro de una lista


def compareCity(city1, city2):

    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1


def compareDurationSec(city1 , city2):
    a = float(city1)
    b = float(city2)
    if (a == b):
        return 0
    elif (a > b):
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


def cmpByHour(hour1, hour2):

    hour1Lst = hour1['HH:MM'].split(':')
    h1 = hour1Lst[0]
    m1 = hour1Lst[1]
    hour2Lst = hour2['HH:MM'].split(':')
    h2 = hour2Lst[0]
    m2 = hour2Lst[1]
    if h1 > h2:
        r = False
    elif h1 < h2:
        r = True
    elif m1 > m2:
        r = False
    elif m1 < m2:
        r = True
    else:
        r = True

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


def cmpHourBySightings(hour1, hour2):

    hour1F = (list(hour1.keys()))[0]
    hour2F = (list(hour2.keys()))[0]
    r = True
    if hour1F > hour2F:
        r = True
    else:
        r = False
    return r


def cmpByLocation(loc1, loc2):

    if loc1['Longitude'] > loc2['Longitude']:
        r = True

    elif loc1['Longitude'] == loc2['Longitude']:
        if loc1['Latitude'] > loc2['Latitude']:
            r = True

        else:
            r = False
    else:
        r = False

    return r

def cmpByPlace(place1, place2):

    if place1['City'] < place2['City']:
        r = True

    elif place1['City'] == place2['City']:
        if place1['Country'] < place2['Country']:
            r = True

        else:
            r = False
    else:
        r = False

    return r
