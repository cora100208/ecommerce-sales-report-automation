from pathlib import Path
import pandas as pd


def export_report(
    report_file: Path,
    daily_summary: pd.DataFrame,
    sku_summary: pd.DataFrame,
    channel_summary: pd.DataFrame,
    inventory_alerts: pd.DataFrame,
) -> None:
    """Export all outputs to one Excel workbook with auto-adjusted column widths."""
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(report_file, engine="openpyxl") as writer:
        # 把四个 DataFrame 写入不同 sheet
        daily_summary.to_excel(writer, sheet_name="daily_summary", index=False)
        sku_summary.to_excel(writer, sheet_name="sku_summary", index=False)
        channel_summary.to_excel(writer, sheet_name="channel_summary", index=False)
        inventory_alerts.to_excel(writer, sheet_name="inventory_alerts", index=False)

        # 自动调整列宽（让 Excel 更美观）
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

    print(f"Excel report saved to: {report_file}")