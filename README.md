## Introduction

**Made by CHENNAUD Emmanuel, ELOY Typhenn, LAMBERT Vincent, SOULLARD Thomas, TOURNEUR Hugo.**

Tutored project following work by UIT Informatique students for the NATUITUION company. The purpose of this project is to be able to collect information on the direction of a robot thanks to its gps position and send it to a postgres database.

## Installation & Dependencies
This driver depends on:

* [Adafruit_CircuitPython_ADS1x15](https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15)
* [Psycopg2](https://pypi.org/project/psycopg2/)
* [Requests](https://requests-fr.readthedocs.io/en/latest/)

Please ensure all dependencies are available on the CircuitPython filesystem.

## Installing from PyPI

To install and be able to use your project please follow the instructions below :

``` 
git clone https://forge.iut-larochelle.fr/echenuau/pts3-pts4.git 
cd pts3-pts4/src/ 
python3 -m venv .env
source .env/bin/activate 
pip3 install adafruit-circuitpython-ads1x15
pip3 install psycopg2
pip3 install requests
```
## Configuration

To configure our project we created a config.data file to be able to enter multiple information such as database identifiers for example.

## Database
To create the database we have made available to you sql files with the creation execution orders.
You must have the extension [postgis](https://postgis.net/) on your [postgresql](https://www.postgresql.org/) database to operate the link of the information collected with the display on the [QGIS](https://www.qgis.org/fr/site/index.html) software.
