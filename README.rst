==============
eo-tilematcher
==============

Tools to quickly find the Sentinel2, Landsat5, and Landsat8 tiles that a given region
of interest.

Basically the library returns:
- __geometry__: is the requested geometry to be matched against satellite tiles
- __match_polygon__: is the intersection/contains WKT geometry (string) that matches each satellite tile 
- __match__: partial/total (str). total indicates a _contains_ conditition.
- __TILE__ ( __PATH#ROW__): the satellite tile (path,row) matched in __match__ condition (Sentinel/Landsat convention)

Installation
============

You can install the from PyPI by simply running::

    pip install eo_tilematcher


Installation from sources
-------------------------

To install the package, from the project root run::

    pip install .  # Regular installation
    pip install -e .  # Install in development mode


Usage
=====

Basic library usage
--------------------

    > from eo_tilematcher import intersects
    > geo_match = intersects(spacecraft,ROI)

Where
- ROI=geopandas geodataframe
- spacecraft ={sentinel2,landsat8,landsat5}


Check the [eo-tilematcher-101](./notebooks/eo-tilematcher-101.ipynb) tutorial notebook to see some plots.

Basic command line usage
------------------------

Just tiles display no write to file:

    > python eo_tilematcher.py /path/to/ROI --spacecraft spacecraft 

Where:
- /path/to/ROI is the path to any kind of file that fiona could open (shp,gpkg,geojson,...)
- spacecraft ={sentinel2,landsat8,landsat5} (default sentinel2 no input required).

With dump:

    > python eo_tilematcher.py /path/to/ROI --spacecraft spacecraft  --dump 

to current dir (as a geodataframe, "./geom_match.gpkg")

    > python eo_tilematcher.py /path/to/ROI --spacecraft spacecraft  --dump --dump_file /any/dir/file
    
to dump geodataframe in /any/dir/file