import io
from typing import Self

import geopandas as gpd
import pandas as pd
import requests

from se_deep_coral_communities.data_loading.context_source import ContextSource

_ERDDAP_BASE = "https://www.ncei.noaa.gov/erddap/tabledap/IMLGS_Marine_Geology.csv"


class IMLGSSubstrateSource(ContextSource):
    """Primary seafloor lithology from the NOAA/NCEI Index to Marine and Lacustrine
    Geological Samples (IMLGS).

    Each coral event is assigned the LITH1 classification of the nearest physical
    geological sample with water depth >= 50 m. The output column ``lith1`` contains
    the raw IMLGS category string (e.g. "terrigenous", "calcareous, biogenic").
    """

    _MIN_DEPTH_M = 50
    _BBOX_BUFFER_DEG = 1.0

    def __init__(self) -> None:
        self._samples: gpd.GeoDataFrame | None = None

    @property
    def required_columns(self) -> frozenset[str]:
        return frozenset({"lat", "lon"})

    def fetch(self, df: pd.DataFrame) -> Self:
        self._validate(df)
        lat_min = df["lat"].min() - self._BBOX_BUFFER_DEG
        lat_max = df["lat"].max() + self._BBOX_BUFFER_DEG
        lon_min = df["lon"].min() - self._BBOX_BUFFER_DEG
        lon_max = df["lon"].max() + self._BBOX_BUFFER_DEG

        url = (
            f"{_ERDDAP_BASE}"
            f"?latitude,longitude,WATER_DEPTH,LITH1"
            f"&latitude>={lat_min}&latitude<={lat_max}"
            f"&longitude>={lon_min}&longitude<={lon_max}"
            f"&WATER_DEPTH>={self._MIN_DEPTH_M}"
        )

        response = requests.get(url, timeout=120)
        response.raise_for_status()

        raw = pd.read_csv(io.StringIO(response.text), skiprows=[1])
        samples = raw.dropna(subset=["LITH1"]).copy()
        samples = samples.rename(columns={"LITH1": "lith1"})

        self._samples = gpd.GeoDataFrame(
            samples[["lith1"]],
            geometry=gpd.points_from_xy(samples["longitude"], samples["latitude"]),
            crs="EPSG:4326",
        ).to_crs("EPSG:3395")

        return self

    def join(self, df: pd.DataFrame) -> pd.DataFrame:
        self._validate(df)
        if self._samples is None:
            raise RuntimeError("Call fetch() before join().")

        coral_gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df["lon"], df["lat"]),
            crs="EPSG:4326",
        ).to_crs("EPSG:3395")

        joined = (
            gpd.sjoin_nearest(coral_gdf, self._samples, how="left")
            .to_crs("EPSG:4326")
            .loc[lambda d: ~d.index.duplicated(keep="first")]
        )
        return pd.DataFrame(joined.drop(columns=["geometry", "index_right"]))
