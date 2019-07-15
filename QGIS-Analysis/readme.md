# Analyzing your Meteobike Data in QGIS

[QGIS](https://qgis.org) is a free and open-source Geographic Information System (GIS) that allows us to perform advanced geographical analysis of the data obtained from one or multiple Meteobike systems. It runs on Linux, Mac OSX, Windows and other systems. 

## Installing QGIS

Download [QGIS](https://qgis.org) and follow installation instructions, incluing the correct Python version.

## Importing and map Meteobike data in QGIS

In a first step we would like to import and map your meteobike dataset.

### Set-up OSM as background map in QGIS

Open [QGIS](https://qgis.org) and create a new project using `Project` > `New` >. Save the new project under `Project` > `Save As...`. 

In the 'Browser', click on `XYZ Tiles` and double click `OpenStreetMap`. Open Street Map tiles will be shown. Navigate to Freiburg.

![Images/QGIS_OSMFull.png](Images/QGIS_OSMFull.png)

### Importing Meteobike data to QGIS

You can import any .csv file into QGIS. Use Menu `Layer` > `Add Layer` > `Add Delimited Text Layer...`:

![Images/QGIS_CSVImport.png](Images/QGIS_CSVImport.png)

Choose the file of your system (by clicking on the `...`-button in the upper right). Alternatively, you can also select the compiled file (`ALL-SYSTEMS-2019-06-26.csv`) with all systems and corrected for cooling. 

 Under 'File Format' select `CSV (comma separated values)`, under 'Record and Field Options' select `First record has field names` and `Detect field types`. Under 'Geometry Definition' it should automatically select 'Longitude' as `x field` and 'Latitude' as `y field`. 'Sample Data' displays your measurement dataset. Click `Add`.

Your trace will be displayed as single measurement points. Right click on the new layer and select `Properties...`. You can display the measured values as numeric labels. Under 'Labels' you can for example select the 'Temperature' field:

![Images/QGIS_LayerOptions.png](Images/QGIS_LayerOptions.png)

Each point is now geo-referenced and displays the measured temperatures:

![Images/QGIS_Labels.png](Images/QGIS_Labels.png)

## Create spatial operations in QGIS

### Select temperatures based on a specific subset.