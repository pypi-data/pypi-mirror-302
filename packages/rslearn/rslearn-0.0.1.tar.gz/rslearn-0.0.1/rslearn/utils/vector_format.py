"""Classes for writing vector data to a UPath."""

import json
from typing import Any

import numpy as np
import shapely
from class_registry import ClassRegistry
from upath import UPath

from rslearn.config import VectorFormatConfig
from rslearn.const import WGS84_PROJECTION

from .feature import Feature
from .geometry import PixelBounds, Projection, STGeometry

VectorFormats = ClassRegistry()


class VectorFormat:
    """An abstract class for writing vector data.

    Implementations of VectorFormat should support reading and writing vector data in
    a UPath. Vector data is a list of GeoJSON-like features.
    """

    def encode_vector(
        self, path: UPath, projection: Projection, features: list[Feature]
    ) -> None:
        """Encodes vector data.

        Args:
            path: the directory to write to
            projection: the projection of the raster data
            features: the vector data
        """
        raise NotImplementedError

    def decode_vector(self, path: UPath, bounds: PixelBounds) -> list[Feature]:
        """Decodes vector data.

        Args:
            path: the directory to read from
            bounds: the bounds of the vector data to read

        Returns:
            the vector data
        """
        raise NotImplementedError


@VectorFormats.register("tile")
class TileVectorFormat(VectorFormat):
    """TileVectorFormat stores data in GeoJSON files corresponding to grid cells.

    A tile size defines the grid size in pixels. One file is created for each grid cell
    containing at least one feature. Features are written to all grid cells that they
    intersect.
    """

    def __init__(self, tile_size: int = 512):
        """Initialize a new TileVectorFormat instance.

        Args:
            tile_size: the tile size (grid size in pixels), default 512
        """
        self.tile_size = tile_size

    def encode_vector(
        self, path: UPath, projection: Projection, features: list[Feature]
    ) -> None:
        """Encodes vector data.

        Args:
            path: the directory to write to
            projection: the projection of the raster data
            features: the vector data
        """
        tile_data = {}
        for feat in features:
            if not feat.geometry.shp.is_valid:
                continue
            bounds = feat.geometry.shp.bounds
            start_tile = (
                int(bounds[0]) // self.tile_size,
                int(bounds[1]) // self.tile_size,
            )
            end_tile = (
                int(bounds[2]) // self.tile_size + 1,
                int(bounds[3]) // self.tile_size + 1,
            )
            for col in range(start_tile[0], end_tile[0]):
                for row in range(start_tile[1], end_tile[1]):
                    cur_shp = feat.geometry.shp.intersection(
                        shapely.box(
                            col * self.tile_size,
                            row * self.tile_size,
                            (col + 1) * self.tile_size,
                            (row + 1) * self.tile_size,
                        )
                    )
                    cur_shp = shapely.transform(
                        cur_shp,
                        lambda array: array
                        - np.array([[col * self.tile_size, row * self.tile_size]]),
                    )
                    cur_feat = Feature(
                        STGeometry(projection, cur_shp, None), feat.properties
                    )
                    try:
                        cur_geojson = cur_feat.to_geojson()
                    except Exception as e:
                        print(e)
                        continue
                    tile = (col, row)
                    if tile not in tile_data:
                        tile_data[tile] = []
                    tile_data[tile].append(cur_geojson)

        path.mkdir(parents=True, exist_ok=True)
        for (col, row), geojson_features in tile_data.items():
            fc = {
                "type": "FeatureCollection",
                "features": [geojson_feat for geojson_feat in geojson_features],
                "properties": projection.serialize(),
            }
            with (path / f"{col}_{row}.geojson").open("w") as f:
                json.dump(fc, f)

    def decode_vector(self, path: UPath, bounds: PixelBounds) -> list[Feature]:
        """Decodes vector data.

        Args:
            path: the directory to read from
            bounds: the bounds of the vector data to read

        Returns:
            the vector data
        """
        start_tile = (bounds[0] // self.tile_size, bounds[1] // self.tile_size)
        end_tile = (
            (bounds[2] - 1) // self.tile_size + 1,
            (bounds[3] - 1) // self.tile_size + 1,
        )
        features = []
        for col in range(start_tile[0], end_tile[0]):
            for row in range(start_tile[1], end_tile[1]):
                cur_fname = path / f"{col}_{row}.geojson"
                if not cur_fname.exists():
                    continue
                with cur_fname.open("r") as f:
                    fc = json.load(f)
                if "properties" in fc and "crs" in fc["properties"]:
                    projection = Projection.deserialize(fc["properties"])
                else:
                    projection = WGS84_PROJECTION

                for feat in fc["features"]:
                    shp = shapely.geometry.shape(feat["geometry"])
                    shp = shapely.transform(
                        shp,
                        lambda array: array
                        + np.array([[col * self.tile_size, row * self.tile_size]]),
                    )
                    feat["geometry"] = json.loads(shapely.to_geojson(shp))
                    features.append(Feature.from_geojson(projection, feat))
        return features

    @staticmethod
    def from_config(name: str, config: dict[str, Any]) -> "TileVectorFormat":
        """Create a TileVectorFormat from a config dict.

        Args:
            name: the name of this format
            config: the config dict

        Returns:
            the TileVectorFormat
        """
        return TileVectorFormat(tile_size=config.get("tile_size", 512))


@VectorFormats.register("geojson")
class GeojsonVectorFormat(VectorFormat):
    """A vector format that uses one big GeoJSON."""

    fname = "data.geojson"

    def encode_vector(
        self, path: UPath, projection: Projection, features: list[Feature]
    ) -> None:
        """Encodes vector data.

        Args:
            path: the directory to write to
            projection: the projection of the raster data
            features: the vector data
        """
        path.mkdir(parents=True, exist_ok=True)
        with (path / self.fname).open("w") as f:
            json.dump(
                {
                    "type": "FeatureCollection",
                    "features": [feat.to_geojson() for feat in features],
                    "properties": projection.serialize(),
                },
                f,
            )

    def decode_vector(self, path: UPath, bounds: PixelBounds) -> list[Feature]:
        """Decodes vector data.

        Args:
            path: the directory to read from
            bounds: the bounds of the vector data to read

        Returns:
            the vector data
        """
        with (path / self.fname).open("r") as f:
            fc = json.load(f)
        if "properties" in fc and "crs" in fc["properties"]:
            projection = Projection.deserialize(fc["properties"])
        else:
            projection = WGS84_PROJECTION
        return [Feature.from_geojson(projection, feat) for feat in fc["features"]]

    @staticmethod
    def from_config(name: str, config: dict[str, Any]) -> "GeojsonVectorFormat":
        """Create a GeojsonVectorFormat from a config dict.

        Args:
            name: the name of this format
            config: the config dict

        Returns:
            the GeojsonVectorFormat
        """
        return GeojsonVectorFormat()


def load_vector_format(config: VectorFormatConfig) -> VectorFormat:
    """Loads a VectorFormat from a VectorFormatConfig.

    Args:
        config: the VectorFormatConfig configuration object specifying the
            VectorFormat.

    Returns:
        the loaded VectorFormat implementation
    """
    cls = VectorFormats.get_class(config.name)
    return cls.from_config(config.name, config.config_dict)
