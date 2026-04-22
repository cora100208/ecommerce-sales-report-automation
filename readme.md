
# eCommerce Sales Report Automation

A Python automation project that cleans order data, analyzes sales performance, merges inventory data, and exports an Excel report with restock suggestions.

## Features
- Clean raw CSV order data
- Filter valid paid orders
- Calculate revenue automatically
- Build daily sales summary
- Build SKU-level performance summary
- Build channel summary
- Generate inventory alerts and restock suggestions
- Export everything into one Excel file

## Tech Stack
- Python
- pandas
- openpyxl

## Input Files
- `data/orders_sample.csv`
- `data/inventory_sample.csv`

## Output
- `output/sales_report.xlsx`

## Run
```bash
pip install -r requirements.txt
python src/main.py
````

## Use Cases

* Shopify sales reporting
* Amazon store reporting
* Inventory warning dashboards
* Small eCommerce operations automation

