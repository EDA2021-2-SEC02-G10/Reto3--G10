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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos


def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    ufosfile = cf.data_dir + 'UFOS-utf8-small.csv'
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"))
    for row in input_file:
        model.addUfo(analyzer, row['datetime'], row['city'], row['state'], row['country'], row['shape'],
                     (row['duration (seconds)']), row['duration (hours/min)'],
                     row['date posted'], float(row['latitude']), float(row['longitude']))

    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def findSightingsCity(analyzer, city):

    return model.findSightingsCity(analyzer, city)


def Sightingsbyseconds(analyzer, secondsmin,secondsmax):

    return model.Sightingsbyseconds(analyzer,secondsmin,secondsmax)


def countSightingsByHour(analyzer, li, lf):

    return model.countSightingsByHour(analyzer, li, lf)


def Sightingsbydate (analyzer,date1,date2):

    return model.Sightingsbydate (analyzer,date1,date2)


def findSightingsByRegion(analyzer, loni, lonf, lati, latf):

    return model.findSightingsByRegion(analyzer, loni, lonf, lati, latf)


def seeSightingsByRegion(analyzer, loni, lonf, lati, latf):

    return model.seeSightingsByRegion(analyzer, loni, lonf, lati, latf)
