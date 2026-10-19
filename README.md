# Smart Student Performance Monitoring System

A system that predicts which students are at risk of failing or withdrawing
from a course, explains the reasons behind each prediction, and helps curators
decide who to contact first.

Project Management course, team of 5: Zhaniya, Madina, Makhabbat, Nuray, Merey.

## Data

Open University Learning Analytics Dataset (OULAD), licensed CC-BY.
Download: https://analyse.kmi.open.ac.uk/open_dataset

The dataset is **not** stored in this repository. Download it yourself and put
the seven CSV files into `data/raw/`:


`studentVle.csv` has millions of rows. Read it in chunks or aggregate on load.

## Folder structure


## Setup

Requires Python 3.10 or newer.

```bash
git clone https://github.com/Mik5355/SSPMS-Data-Engineer.git
cd SSPMS-Data-Engineer

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Running

Notebooks:

```bash
jupyter notebook
```

Application:

```bash
streamlit run app/main.py
```

The app opens at http://localhost:8501

## Workflow

- `main` is protected: work in a branch named after your story, e.g. `us4-pipeline`
- Open a pull request and have one teammate review it before merging
- Keep notebooks for exploration; move anything reused into `src/`

## Team

| Name | Role |
|---|---|
| Zhaniya | ML Engineer |
| Madina | Data Engineer |
| Makhabbat | Data Analyst & Visualization |
| Nuray | App Developer & QA |
| Merey | Scrum Master & Documentation |

Project tracking: Jira (project SCRUM)


