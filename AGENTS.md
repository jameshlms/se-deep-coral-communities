# Southeast Deep Coral Communities

## Research Context

This project is based on [this research paper](https://repository.library.noaa.gov/view/noaa/54687) that demonstrates that deep-sea coral and sponge assemblages are mostly predictable from local environmental conditions. The southeast coast deep-sea coral communities project aims to apply methods used in the Alaska deep-sea coral and sponge location research to predict communities along the southeast coast. The project will use cluster corals into communities and predict the location of communities. Use their techniques but with aim to improve their methods or implement fixes in their gaps in research.

## Data Context

Data comes from the [Deep Coral Reef National Database](https://www.ncei.noaa.gov/erddap/tabledap/deep_sea_corals.html). All columns and what they measure are in the page. Data will be loaded in first into `/data/raw` and the validated records will be in `/data/interim`. When cleaning data or other wrangling steps don't concern initial raw data loading and validating, use `data/interim`.

## Model Training

When training a model, ensure these metrics are captured:
- Accuracy (Training, Validation, and Testing splits)
- Precision (Training, Validation, and Testing splits)
- Recall (Training, Validation, and Testing splits)
- ROC Curves (Training, Validation, and Testing splits)
- Training Duration
- Number of Features

## Data Loading

When adding addition data to the primary coral reef observations dataset, implement the `ContextSource` interface from `src/se_deep_coral_communities/data_loading/context_source.py`. This ensures consistency of contextual data loading across sources and provides reusability.