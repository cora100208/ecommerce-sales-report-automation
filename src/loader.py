
import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    df = pd.read_csv(file_path)
    return df
