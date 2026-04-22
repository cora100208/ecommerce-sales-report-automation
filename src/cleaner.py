
import pandas as pd


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize order data."""
    df = df.copy()

    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Remove obvious whitespace
    text_cols = ["sku", "product_name", "channel", "country", "status"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Convert data types
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0)

    # Drop rows with missing key fields
    df = df.dropna(subset=["order_date", "sku", "product_name"])

    # Keep only paid orders for revenue analysis
    df = df[df["status"].str.lower() == "paid"].copy()

    # Calculate revenue
    df["revenue"] = df["quantity"] * df["unit_price"]

    return df


def clean_inventory(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize inventory data."""
    df = df.copy()

    df.columns = [col.strip().lower() for col in df.columns]

    text_cols = ["sku", "product_name"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    numeric_cols = ["current_stock", "reorder_level", "supplier_lead_days"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df = df.dropna(subset=["sku", "product_name"])

    return df
