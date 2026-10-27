# Southeast Deep Sea Coral Community Clustering

## Environment Setup

Create a virtual environment.

```bash
python -m venv .venv
```
You can rename `.venv` to whatever environment name you prefer.

Activate the environment if it is not already.

(Windows)

```powershell
.venv/Scripts/Activate
```

(MacOS & Linux)

```bash
source .venv/bin/activate
```

If you named your virtual environment something other than `.venv` you'll need to change the command appropriately

Once your environment is activated, install the required packages specified in `requirements.txt`

```bash
pip install -r requirements.txt
```

That is the environment configured, now create a `data` directory with `raw` and `processed` subdirectories.

(Windows)
```powershell
md data/raw data/interim data/processed
```

(MacOS & Linux)
```bash
mkdir -p data/{raw,interim,processed}
```
