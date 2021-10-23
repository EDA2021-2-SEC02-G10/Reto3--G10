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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
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
    return analyzer


# Funciones para agregar informacion al catalogo


def addUfo(analyzer, datetime, city, state, country, shape,
           durationSec, durationHoursMin, dateposted, latitude, longitude):

    dictUfo = {}
    dictUfo['Datetime'] = datetime
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
        dictCity['Datetime'] = datetime
        dictCity['Country'] = country
        dictCity['Shape'] = shape
        dictCity['DurationSec'] = durationSec
        lt.addLast(lstCity, dictCity)
        om.put(analyzer['cityIndex'], city, lstCity)
    else:
        cityEntry = om.get(analyzer['cityIndex'], city)
        cityList = me.getValue(cityEntry)
        dictCity = {}
        dictCity['Datetime'] = datetime
        dictCity['Country'] = country
        dictCity['Shape'] = shape
        dictCity['DurationSec'] = durationSec
        lt.addLast(cityList, dictCity)

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareCity(city1, city2):
    """
    Compara dos fechas
    """
    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1


# Funciones de ordenamiento
