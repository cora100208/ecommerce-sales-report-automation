
import pandas as pd


def build_daily_summary(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by day."""
    daily = (
        orders_df.groupby("order_date", as_index=False)
        .agg(
            total_orders=("order_id", "nunique"),
            total_units=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
        )
        .sort_values("order_date")
    )
    return daily


def build_sku_summary(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by SKU."""
    sku_summary = (
        orders_df.groupby(["sku", "product_name"], as_index=False)
        .agg(
            total_units_sold=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            avg_unit_price=("unit_price", "mean"),
        )
        .sort_values(["total_revenue", "total_units_sold"], ascending=False)
    )
    return sku_summary


def build_channel_summary(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by channel."""
    channel_summary = (
        orders_df.groupby("channel", as_index=False)
        .agg(
            total_units=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
    )
    return channel_summary


def build_inventory_alerts(
    sku_summary_df: pd.DataFrame, inventory_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge sales and inventory, then generate simple restock recommendations.
    Rule:
    - low_stock_flag = current_stock <= reorder_level
    - suggested_restock = max(reorder_level * 2 - current_stock, 0)
    """
    merged = inventory_df.merge(
        sku_summary_df[["sku", "product_name", "total_units_sold"]],
        on=["sku", "product_name"],
        how="left"
    )

    merged["total_units_sold"] = merged["total_units_sold"].fillna(0)
    merged["low_stock_flag"] = merged["current_stock"] <= merged["reorder_level"]
    merged["suggested_restock"] = (
        (merged["reorder_level"] * 2 - merged["current_stock"]).clip(lower=0)
    )

    merged["action"] = merged.apply(_build_action_text, axis=1)

    return merged.sort_values(
        ["low_stock_flag", "suggested_restock", "total_units_sold"],
        ascending=[False, False, False]
    )


def _build_action_text(row) -> str:
    """Generate a plain-language action note for each SKU."""
    if row["low_stock_flag"] and row["total_units_sold"] > 0:
        return f"Restock soon. Suggested qty: {int(row['suggested_restock'])}"
    if row["low_stock_flag"] and row["total_units_sold"] == 0:
        return "Low stock, but no recent sales. Check before restocking."
    return "Stock level looks acceptable."
