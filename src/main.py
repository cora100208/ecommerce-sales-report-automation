from config import ORDERS_FILE, INVENTORY_FILE, REPORT_FILE
from loader import load_csv
from cleaner import clean_orders, clean_inventory
from analyzer import (
    build_daily_summary,
    build_sku_summary,
    build_channel_summary,
    build_inventory_alerts,
)
from reporter import export_report


def main() -> None:
    orders_raw = load_csv(ORDERS_FILE)
    inventory_raw = load_csv(INVENTORY_FILE)

    orders_df = clean_orders(orders_raw)
    inventory_df = clean_inventory(inventory_raw)

    daily_summary = build_daily_summary(orders_df)
    sku_summary = build_sku_summary(orders_df)
    channel_summary = build_channel_summary(orders_df)
    inventory_alerts = build_inventory_alerts(sku_summary, inventory_df)

    export_report(
        REPORT_FILE,
        daily_summary,
        sku_summary,
        channel_summary,
        inventory_alerts,
    )

    print("Report created successfully:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()