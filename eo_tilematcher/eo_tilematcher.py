import numpy as np
import os
import pickle
import pygeos
from pathlib import Path


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
