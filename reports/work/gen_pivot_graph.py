import pandas as pd
import matplotlib.pyplot as plt

def generate_and_write_pivot_to_excel(excel_file_path, source_sheet_name, index_columns, values_column, aggfunc='sum', output_excel_path=None, dest_sheet_name=None):
    """
    Reads an Excel file, generates a pivot table, and writes it to a new sheet in an Excel file.
    
    Args:
    - excel_file_path (str): Path to the input Excel file.
    - source_sheet_name (str): The sheet name in the Excel file to read data from.
    - index_columns (list): The columns to use as the index for the pivot table.
    - values_column (str): The column to use for the values in the pivot table.
    - aggfunc (str or function, default 'sum'): The aggregation function to apply on the values column.
    - output_excel_path (str, optional): Path for saving the output Excel file with the pivot table.
    - dest_sheet_name (str): The sheet name where the pivot table will be written.
    
    Returns:
    - None
    """
    try:
        # Read the Excel sheet into a DataFrame
        df = pd.read_excel(excel_file_path, sheet_name=source_sheet_name)
        
        # Create the pivot table with multiple index columns
        pivot_table = pd.pivot_table(df, 
                                     index=index_columns, 
                                     values=values_column, 
                                     aggfunc=aggfunc)
        
        # Define output path if not provided
        if output_excel_path is None:
            output_excel_path = excel_file_path  # Save over the original file or specify a new path
        
        # Write the pivot table to a new sheet in the Excel file
        with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a') as writer:
            pivot_table.to_excel(writer, sheet_name=dest_sheet_name)
        
        print(f"Pivot table has been successfully written to: {output_excel_path}")
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage
generate_and_write_pivot_to_excel('sales.xlsx', 'sales', ['Region', 'Sales Rep'], 'Total Sales', 'sum', 'sales.xlsx', 'Sales by Region and Rep')


import pandas as pd
import openpyxl
from openpyxl.chart import BarChart, Reference

def generate_and_write_pivot_with_excel_graph(excel_file_path, source_sheet_name, index_columns, values_column, aggfunc='sum', output_excel_path=None, dest_sheet_name=None):
    """
    Reads an Excel file, generates a pivot table, writes it to a new sheet, and generates an Excel chart (BarChart).
    
    Args:
    - excel_file_path (str): Path to the input Excel file.
    - source_sheet_name (str): The sheet name in the Excel file to read data from.
    - index_columns (list): The columns to use as the index for the pivot table.
    - values_column (str): The column to use for the values in the pivot table.
    - aggfunc (str or function, default 'sum'): The aggregation function to apply on the values column.
    - output_excel_path (str, optional): Path for saving the output Excel file with the pivot table.
    - dest_sheet_name (str): The sheet name where the pivot table will be written.
    
    Returns:
    - None
    """
    try:
        # Read the Excel sheet into a DataFrame
        df = pd.read_excel(excel_file_path, sheet_name=source_sheet_name)
        
        # Create the pivot table with multiple index columns
        pivot_table = pd.pivot_table(df, 
                                     index=index_columns, 
                                     values=values_column, 
                                     aggfunc=aggfunc)
        
        # Define output path if not provided
        if output_excel_path is None:
            output_excel_path = excel_file_path  # Save over the original file or specify a new path
        
        # Write the pivot table to a new sheet in the Excel file
        with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a') as writer:
            pivot_table.to_excel(writer, sheet_name=dest_sheet_name)
        
        # Open the workbook using openpyxl
        wb = openpyxl.load_workbook(output_excel_path)
        ws = wb[dest_sheet_name]
        
        # Create a bar chart
        chart = BarChart()
        chart.type = "col"
        chart.style = 10
        chart.title = "Sales by Region and Rep"
        chart.x_axis.title = "Region and Sales Rep"
        chart.y_axis.title = "Total Sales"
        
        # Define the data range for the chart (from the pivot table)
        data = Reference(ws, min_col=3, min_row=1, max_col=3, max_row=len(pivot_table) + 1)  # Adjust min_col/max_col to your data
        categories = Reference(ws, min_col=1, min_row=2, max_row=len(pivot_table) + 1)  # Adjust to the categories (Region and Sales Rep)
        
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)
        
        # Position the chart on the sheet
        ws.add_chart(chart, "E5")  # Change this to where you'd like the chart to appear
        
        # Save the workbook with the chart
        wb.save(output_excel_path)
        
        print(f"Pivot table and chart have been successfully written to: {output_excel_path}")
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
generate_and_write_pivot_with_excel_graph('sales.xlsx', 'sales', ['Region', 'Sales Rep'], 'Total Sales', 'sum', 'sales.xlsx', 'Sales by Region and Rep graph')
