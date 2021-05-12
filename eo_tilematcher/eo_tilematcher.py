import os
import pickle
import numpy as np
import pygeos
from pathlib import Path
import argparse

#
parser=argparse.ArgumentParser(description= "EO-tilematcher")
# mandatory
parser.add_argument("roi",type=str,help="ROI WKT (currently only wkt is supported)")
#optional
parser.add_argument('--spacecraft',type=str,help= "satellite (landsat5,landsat8,sentinel2)",default="sentinel2")
parser.add_argument('--op',type=str,help= "match task (intersection,contains)",default="intersection")
parser.add_argument("--dump",help="To dump results (if any) to file",action="store_true")
parser.add_argument("--dump_full",help="To dump just tiles to dump also geoms",action="store_true")
parser.add_argument("--dump_file",type=str,help="To leave dump results path (default current dir)",default="./test.txt")
#

def _db_loader(file_name):
    tiles_db = dict()
    data_dir = Path(__file__).parent
    subdir = file_name.split("_")[0]
    tmp = pickle.load(open(os.path.join(data_dir, "./data", subdir, file_name), "rb"))
    tiles_db["geometry"] = pygeos.creation.polygons(
        [pygeos.creation.linearrings(pol) for _, pol in tmp]
    ).squeeze()
    tiles_db["tile"] = np.array([tile for tile, _ in tmp])
    return tiles_db


def _sentinel2_db_loader():
    return _db_loader("sentinel2_tiles.pkl")


def _landsat_db_loader():
    return _db_loader("landsat_tiles.pkl")


SPACECRAFTS_DB = dict(
    sentinel2=None,
    landsat5=None,
    landsat8=None,
)

SPACECRAFTS_LOADERS = dict(
    sentinel2=_sentinel2_db_loader,
    landsat5=_landsat_db_loader,
    landsat8=_landsat_db_loader,
)


def get_spacecraft_db(spacecraft):
    spacecraft = spacecraft.lower()
    if spacecraft not in SPACECRAFTS_DB:
        raise ValueError(
            f"Spacecraft '{spacecraft}' not supported.\n"
            f"Allowed values: {str(list(SPACECRAFTS_DB.keys()))}"
        )

    if SPACECRAFTS_DB[spacecraft] is None:
        SPACECRAFTS_DB[spacecraft] = SPACECRAFTS_LOADERS[spacecraft]()
    return SPACECRAFTS_DB[spacecraft]


def intersects(spacecraft, roi):
    """
    Returns the names and the geometries of the tiles that intersects a given
    Region of Interest (ROI).
    """
    selected_db = get_spacecraft_db(spacecraft)
    matches = pygeos.predicates.intersects(selected_db["geometry"], roi)
    return selected_db["tile"][matches], selected_db["geometry"][matches]

def write_tiles_geoms(tiles,geoms=None,file_dump='./test.txt'):
       
    if geoms is None:
        with open(file_dump,'w+') as f:
            for t in tiles:
                f.write('{} \n'.format(t))
    else:
        with open(file_dump,'w+') as f:
            for t,g in zip(tiles,geoms):
                f.write('{} , {}\n'.format(t,g))


if __name__ == '__main__':
    m,_=parser.parse_known_args()
    box=pygeos.io.from_wkt(m.roi)
    if m.op =='intersection':
        tiles,geoms=intersects(m.spacecraft,box)
    print(tiles)
    if m.dump:
        if len(tiles)>0:
            if not m.dump_full:
                write_tiles_geoms(tiles,None,m.dump_file)
            else:
                write_tiles_geoms(tiles,geoms,m.dump_file)