import io
from typing import Callable, Self

import numpy as np
import pandas as pd
import requests
import geopandas as gpd

from se_deep_coral_communities.data_loading.context_source import ContextSource


class BioOracleTemperatureSource(ContextSource):
    _BASE_URL = (
        "https://erddap.bio-oracle.org/erddap/griddap"
        "/thetao_baseline_2000_2019_depthmean.csv"
    )
    _GRID_STEP = 0.05
    _GRID_ORIGIN_LAT = -89.975
    _GRID_ORIGIN_LON = -179.975
    _TIME_START = "2000-01-01T00:00:00Z"
    _TIME_END = "2010-01-01T00:00:00Z"

    def __init__(self) -> None:
        self._grid: gpd.GeoDataFrame | None = None

    @property
    def required_columns(self) -> frozenset[str]:
        return frozenset({"lat", "lon"})

    def fetch(self, df: pd.DataFrame) -> Self:
        self._validate(df)
        lat_min = self._snap(df["lat"].min(), self._GRID_ORIGIN_LAT, np.floor)
        lat_max = self._snap(df["lat"].max(), self._GRID_ORIGIN_LAT, np.ceil)
        lon_min = self._snap(df["lon"].min(), self._GRID_ORIGIN_LON, np.floor)
        lon_max = self._snap(df["lon"].max(), self._GRID_ORIGIN_LON, np.ceil)

        url = (
            f"{self._BASE_URL}"
            f"?thetao_mean[({self._TIME_START}):({self._TIME_END})]"
            f"[({lat_min}):({lat_max})][({lon_min}):({lon_max})]"
        )

        response = requests.get(url, timeout=600)
        response.raise_for_status()

        raw = pd.read_csv(
            io.StringIO(response.text),
            skiprows=[1],
            parse_dates=["time"],
        )
        latest = (
            raw.dropna(subset=["thetao_mean"])
            .loc[lambda d: d["time"] == d["time"].max()]
            .drop(columns=["time"])
        )

        self._grid = gpd.GeoDataFrame(
            latest[["thetao_mean"]],
            geometry=gpd.points_from_xy(latest["longitude"], latest["latitude"]),
            crs="EPSG:4326",
        ).to_crs("EPSG:3395")

        return self

    def join(self, df: pd.DataFrame) -> pd.DataFrame:
        self._validate(df)
        if self._grid is None:
            raise RuntimeError("Call fetch() before join().")

        coral_gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df["lon"], df["lat"]),
            crs="EPSG:4326",
        ).to_crs("EPSG:3395")

        joined = gpd.sjoin_nearest(coral_gdf, self._grid, how="left").to_crs("EPSG:4326")
        return pd.DataFrame(joined.drop(columns=["geometry", "index_right"]))

    def _snap(self, value: float, origin: float, fn: Callable) -> float:
        return round(fn((value - origin) / self._GRID_STEP) * self._GRID_STEP + origin, 10)
