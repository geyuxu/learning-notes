# Labs

- Notebooks: `LABS/notebooks/`
- Reusable code: `LABS/src/`

## Setup (venv)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import numpy, pandas, matplotlib; print('ok')"
python -m ipykernel install --user --name learning-notes --display-name "learning-notes"
jupyter lab
``` 

## Notebook naming
- E_YYYY-MM-DD_<topic>.ipynb exploratory
- R_###_<topic>.ipynb reproducible

## Notebook header (paste at top)

Purpose:
Data:
Steps:
Outputs:
Conclusion:

