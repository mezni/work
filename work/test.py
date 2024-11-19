import openpyxl

def get_excel_version(file_path):
    try:
        # Load Excel file
        wb = openpyxl.load_workbook(file_path)
        
        # Get Excel file version
        excel_version = wb.excel_version
        
        return excel_version
    
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return None


# Example usage
file_path = 'example.xlsx'
excel_version = get_excel_version(file_path)

print(f"Excel Version: {excel_version}")