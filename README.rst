==============
eo-tilematcher
==============

Tools to quickly find the Sentinel2, Landsat5, and Landsat8 tiles that a given region
of interest.

Basic command line usage
------------------------


Just tiles display no write to file:

    > python eo_tilematcher.py --spacecraft spacecraft 'POLYGON ((-65 -26, -65 -25, -64 -25, -64 -26, -65 -26))'

spacecraft ={sentinel2,landsat8,landsat5} (default sentinel2 no input required)


With dump:

    > python eo_tilematcher.py 'POLYGON ((-65 -26, -65 -25, -64 -25, -64 -26, -65 -26))' --dump 

to current dir (just tiles)

    > python eo_tilematcher.py 'POLYGON ((-65 -26, -65 -25, -64 -25, -64 -26, -65 -26))' --dump --dump_full --dump_file /any/dir/file
    
to dump tiles and geometries in /any/dir/file