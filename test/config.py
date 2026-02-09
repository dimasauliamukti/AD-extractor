from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent

DATASETS_DIR=BASE_DIR/"datasets"
AD_DIR=DATASETS_DIR/"docs"
JSON=DATASETS_DIR/"json"/"data.json"

ASSETS=BASE_DIR/"assets"/"result.png"