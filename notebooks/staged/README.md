# Staged notebooks

Work in progress for issues #9, #10 and #11, kept separate from `final_deliverable.ipynb` until it is ready to merge in. The clustering labels used by the exploration and results notebooks come from `notebooks/taxon_clustering.ipynb` (#9).

Run in order, after `notebooks/ingest.ipynb` and `notebooks/clean.ipynb`:

1. `../taxon_clustering.ipynb` (#9): groups survey events into communities by k-means on coral family presence, with DBSCAN as a check. Saves the labels to `data/processed/taxon_cluster_*`.
2. `01_explore.ipynb` (#10): where the dives were, which animals were recorded, specimen counts, missing data, and environmental measurements against depth. It only needs the cleaned records, so it can run before or after the clustering.
3. `02_cluster.ipynb` (#9, comparison): an alternative clustering of dive depth bands on order-level coral and sponge shares, comparing k-means, Gaussian mixtures, DBSCAN and mean-shift, and ending with a comparison against `taxon_clustering.ipynb`. Nothing downstream uses its labels.
4. `03_cluster_results.ipynb` (#11): what each community from `taxon_clustering.ipynb` is made of, how well defined the communities are (silhouette, plus a classifier evaluated on held-out areas), which families distinguish them, where they occur, and whether they track the data provider.

Every figure is also saved as SVG to `figures/` at the repo root for the poster.

These notebooks need `scikit-learn` and `matplotlib` (in `requirements.txt`). The maps download the Natural Earth coastline to `data/external/` on first run.
