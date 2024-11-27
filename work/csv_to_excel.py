import pandas as pd

def csv_to_excel(csv_file_path, excel_file_path, sheet_name):
    """
    Converts a CSV file to an Excel file with a sheet named 'sales'.
    
    Args:
    - csv_file_path (str): The path to the input CSV file.
    - excel_file_path (str): The path to the output Excel file.
    - sheet_name (str): sheet name
    """
    try:
        df = pd.read_csv(csv_file_path)
        
        df.to_excel(excel_file_path, index=False, sheet_name=sheet_name)
        
        print(f"CSV file has been successfully converted to Excel: {excel_file_path}")
    except Exception as e:
        print(f"Error: {e}")


csv_to_excel('sales.csv', 'sales.xlsx','sales')
