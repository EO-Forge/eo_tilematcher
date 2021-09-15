import os
from pathlib import Path
import argparse
import pandas as pd
import geopandas as gpd


####
parser = argparse.ArgumentParser(description="EO-tilematcher")
# mandatory
parser.add_argument(
    "roi", type=str, help="ROI FILE (any file that fiona/geopandas could open)"
)
# optional
parser.add_argument(
    "--spacecraft",
    type=str,
    help="satellite (landsat5,landsat8,sentinel2)",
    default="sentinel2",
)
parser.add_argument(
    "--verbose", help="To display results (if any)", action="store_true"
)
parser.add_argument(
    "--dump", help="To dump results (if any) to file", action="store_true"
)
parser.add_argument(
    "--dump_file",
    type=str,
    help="To leave dump results path (default current dir)",
    default="./geom_match.gpkg",
)
#


def _db_loader(file_name):
    data_dir = Path(__file__).parent
    subdir = file_name.split("_")[0]
    tiles_db = pd.read_pickle(os.path.join(data_dir, "./data", subdir, file_name))
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


def get_contains_intersect_on_tiles(gpd_to_match, gpd_tiles, gpd_tiles_col):
    """get if contains or intersects (but not contains) shape on sat tiles
    Parameters
    ----------
        gpd_to_match: geodataframe
            roi to be intersected by tiles
        gpd_tiles: geodataframe
            geodataframe of sat tiles or path#rows
        gpd_tiles_col: str
            tiles/pathrow column on gpd_tiles

    Returns
    -------
        geodataframe that matches shapes to tiles (either contains or
        intersects)
    """
    contains_ = []
    intersects_ = []
    tile_name_out = gpd_tiles_col
    for i, r in gpd_to_match.iterrows():
        # get those that contains geom
        flag_cont = gpd_tiles.geometry.contains(r["geometry"])
        flag_int = gpd_tiles.geometry.intersects(r["geometry"])
        if any(flag_cont):
            # any contains
            gpd_tf = gpd_tiles[flag_cont]
            for it, rt in gpd_tf.iterrows():
                gpd_ = gpd_to_match.iloc[[i]].copy()
                gpd_["match_polygon"] = (
                    rt["geometry"].intersection(r["geometry"]).to_wkt()
                )
                gpd_["match"] = "total"
                gpd_[tile_name_out] = rt[gpd_tiles_col]
                contains_.append(gpd_)
        elif any(flag_int):
            gpd_tf = gpd_tiles[flag_int]
            for it, rt in gpd_tf.iterrows():
                gpd_ = gpd_to_match.iloc[[i]].copy()
                gpd_["match_polygon"] = (
                    rt["geometry"].intersection(r["geometry"]).to_wkt()
                )
                gpd_["match"] = "partial"
                gpd_[tile_name_out] = rt[gpd_tiles_col]
                intersects_.append(gpd_)
        else:
            # switch to overlay
            gpd_test = gpd_to_match.iloc[[i]].copy()
            gpd_over = gpd.overlay(gpd_test, gpd_tiles)
            for io, ro in gpd_over.iterrows():
                gpd_tf = gpd_tiles[gpd_tiles[gpd_tiles_col] == ro[gpd_tiles_col]]
                for it, rt in gpd_tf.iterrows():
                    gpd_ = gpd_to_match.iloc[[i]]
                    # by construction
                    if rt["geometry"].contains(r["geometry"]):
                        gpd_["match_polygon"] = (
                            rt["geometry"].intersection(r["geometry"]).to_wkt()
                        )
                        gpd_["match"] = "total-overlay"
                        gpd_[tile_name_out] = rt[gpd_tiles_col]
                        contains_.append(gpd_)
                    elif rt["geometry"].intersects(r["geometry"]):
                        gpd_["match_polygon"] = (
                            rt["geometry"].intersection(r["geometry"]).to_wkt()
                        )
                        gpd_["match"] = "partial-overlay"
                        gpd_[tile_name_out] = rt[gpd_tiles_col]
                        intersects_.append(gpd_)
                    else:
                        raise ("Could not make any match")
    #
    if len(contains_) and len(intersects_):
        gpd_contains_, gpd_intersects_ = pd.concat(
            contains_, ignore_index=True
        ), pd.concat(intersects_, ignore_index=True)
        gpd_contains_intersects_ = pd.concat(
            [gpd_contains_, gpd_intersects_], ignore_index=True
        )
        return gpd_contains_intersects_
    elif len(contains_) > 0:
        gpd_contains_ = pd.concat(contains_, ignore_index=True)
        return gpd_contains_
    elif len(intersects_) > 0:
        gpd_intersects_ = pd.concat(intersects_, ignore_index=True)
        return gpd_intersects_
    else:
        return gpd.GeoDataFrame()


def intersects(spacecraft, gpd_roi):
    """
    Returns the names and the geometries of the tiles that intersects a given
    Region of Interest (ROI).
    """
    selected_db = get_spacecraft_db(spacecraft)
    if spacecraft == "sentinel2":
        gpd_col = "TILE"
    else:
        gpd_col = "PATH#ROW"
    # get roi
    gpd_to_match = gpd_roi.copy()

    return get_contains_intersect_on_tiles(gpd_to_match, selected_db, gpd_col)


if __name__ == "__main__":
    m, _ = parser.parse_known_args()
    bbox = gpd.read_file(m.roi)
    tiles_match = intersects(m.spacecraft, bbox)
    if m.verbose:
        if tiles_match.shape[0] > 0:
            print(tiles_match)
        else:
            print("Could not find any intersection")
    if m.dump:
        if tiles_match.shape[0] > 0:
            tiles_match.to_file(m.dump_file, driver="GPKG")
