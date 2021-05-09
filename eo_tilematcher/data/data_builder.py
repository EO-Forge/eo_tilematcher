"""
Script used to build the tiles databases for the Sentinel2,
Landsat5, and Landsat8 spacecrafts.
"""
import fiona
import os
import pickle
import shutil
import tempfile
import zipfile
from pathlib import Path


def unzip_file(file):
    """Unzip a file in a temporary directory."""
    dirtmp = tempfile.mkdtemp()
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(dirtmp)
    return dirtmp


def build_sentinel2_db():
    """Extract the Sentinel2 tiles information and store it in pickle format."""
    data_dir = Path(__file__).parent
    wrs_dir = unzip_file(
        os.path.join(data_dir, "./sentinel2/sentinel2_tiles_world.zip")
    )
    shp_polygons = [
        (pol["properties"]["Name"], pol["geometry"]["coordinates"])
        for pol in fiona.open(os.path.join(wrs_dir, "sentinel2_tiles_world.shp"))
    ]
    pickle.dump(
        shp_polygons,
        open(os.path.join(data_dir, "sentinel2/sentinel2_tiles.pkl"), "wb"),
    )

    shutil.rmtree(wrs_dir)


def build_lansat_db():
    """Extract the Landsat tiles (path/row) information and store it in pickle format."""
    data_dir = Path(__file__).parent
    wrs_dir = unzip_file(os.path.join(data_dir, "landsat/WRS2_descending_0.zip"))
    tile_name_ftm = "PATH:{path},ROW:{row}"
    shp_data = [
        entry for entry in fiona.open(os.path.join(wrs_dir, "WRS2_descending.shp"))
    ]
    for entry in shp_data:
        points = entry["geometry"]["coordinates"][0]
        if not isinstance(points[0], tuple):
            points = points[0]
        entry["geometry"]["coordinates"] = [[(b, a, 0) for a, b in points]]

    shp_polygons = [
        (
            tile_name_ftm.format(
                path=entry["properties"]["PATH"], row=entry["properties"]["ROW"]
            ),
            entry["geometry"]["coordinates"],
        )
        for entry in shp_data
    ]
    pickle.dump(
        shp_polygons, open(os.path.join(data_dir, "landsat/landsat_tiles.pkl"), "wb")
    )
    shutil.rmtree(wrs_dir)


if __name__ == "__main__":
    build_sentinel2_db()
    build_lansat_db()
