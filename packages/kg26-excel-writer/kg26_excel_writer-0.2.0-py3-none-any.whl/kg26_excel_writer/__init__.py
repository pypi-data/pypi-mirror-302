import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill

def write_to_excel(df, filename, color, data_filter):
    """
    Write a DataFrame to an Excel file with formatting.

    Parameters:
    df (pd.DataFrame): The DataFrame to write to Excel.
    filename (str): The name of the output Excel file (without extension).
    color (str): The hex color code for the header fill (e.g., 'FF0000' for red).
    data_filter (bool): Whether to apply a filter to the data.
    """
    with pd.ExcelWriter(f'{filename}.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Access the workbook and the sheet
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Autofit the column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter  # Get the column letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except Exception as e:
                    print(e)
            adjusted_width = (max_length + 2)  # Adding a little padding
            worksheet.column_dimensions[column_letter].width = adjusted_width
        
        # Color the first row (header)
        fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
        for cell in worksheet[1]:  # worksheet[1] accesses the first row
            cell.fill = fill
            
        # Add filters to the columns
        if data_filter:
            worksheet.auto_filter.ref = worksheet.dimensions  # Apply filter to the entire data range
