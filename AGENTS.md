# Southeast Deep Coral Communities

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

