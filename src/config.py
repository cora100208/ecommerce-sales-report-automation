
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

ORDERS_FILE = DATA_DIR / "orders_sample.csv"
INVENTORY_FILE = DATA_DIR / "inventory_sample.csv"
REPORT_FILE = OUTPUT_DIR / "sales_report.xlsx"
