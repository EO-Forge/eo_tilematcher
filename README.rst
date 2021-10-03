==============
eo-tilematcher
==============

Tools to quickly find the Sentinel2, Landsat5, and Landsat8 tiles that a given region
of interest.

Basically, the library returns a geodataframe with:

* **geometry**: is the requested geometry to be matched against satellite tiles

* **match_polygon**: is the intersection/contains WKT geometry (string) that matches each satellite tile

* **match**: partial/total (str). total indicates a *contains* conditition.

* **TILE** (Sentinel2) or **PATH#ROW** (Landsat): the satellite tile (path,row) matched in **match** condition (Sentinel/Landsat convention)

Usage
=====

Basic library usage
-------------------

For this case, import the library::

    from eo_tilematcher import intersects

and run::

    geo_match = intersects(spacecraft,ROI)

Where

- ROI=geopandas geodataframe
- spacecraft ={sentinel2,landsat8,landsat5}


Check the `eo-tilematcher-101 <./examples/eo-tilematcher-101.ipynb>`_ tutorial notebook to see some plots.

Command-line usage
----------------------

1. Print the tiles intersecting a Region Of Interest (ROI) for a given satellite::

    python -m eo_tilematcher /path/to/ROI --spacecraft spacecraft

or::

    eo_tilematcher /path/to/ROI --spacecraft spacecraft

Where:
- /path/to/ROI is the path to any kind of file that `fiona` could open (shp,gpkg,geojson,...)
- spacecraft ={sentinel2,landsat8,landsat5} (default sentinel2 no input required).

2. Find and save to a file the tiles intersecting a Region Of Interest (ROI) for a given satellite
With dump::

    python -m eo_tilematcher /path/to/ROI --spacecraft spacecraft  --output my_ouput.gpkg

or::

    eo_tilematcher /path/to/ROI --spacecraft spacecraft  --output my_ouput.gpkg



Installation
============

You can install them from PyPI by simply running::

    pip install eo_tilematcher


Installation from sources
-------------------------

To install the package, from the project root run::

    pip install .  # Regular installation
    pip install -e .  # Install in development mode
