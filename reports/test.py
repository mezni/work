class Mesure:
    def __init__(self, **kwargs):
        """
        Initialize a Mesure object with optional parameters.
        """
        self.name = kwargs.get('name', None)
        self.mesure_type = kwargs.get('mesure_type', None)
        self.table_name = kwargs.get('table_name', None)
        self.column_name = kwargs.get('column_name', None)
        self.mesure_format = kwargs.get('mesure_format', None)
        self.period = kwargs.get('period', None)
        self.period_start = kwargs.get('period_start', None)
        self.period_end = kwargs.get('period_end', None)
        self.mesure = ""
        self.generate()

    def generate(self):
        if self.mesure_type == "SUM":
            expression = f"{self.mesure_type}({self.table_name}[{self.column_name}])"
            if self.mesure_format:
                expression = f"FORMAT({expression}, \"{self.mesure_format}\")"
        
        if self.period is not None:
            if self.period_start is not None and self.period_end is not None:
                expression = f"""
    VAR _start_date =  IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) {self.period_start}, 4, 1), DATE(YEAR(TODAY()) {self.period_start} - 1, 4, 1)) 
    VAR _end_date = IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) {self.period_end} + 1, 3, 31), DATE(YEAR(TODAY()) {self.period_end}, 3, 31))              
    VAR _result1 = CALCULATE(
        {self.mesure_type}({self.table_name}[{self.column_name}]),
        {date_table_name}[{date_column_name}] >= _start_date &&
        {date_table_name}[{date_column_name}] <= _end_date
        )"""
                if self.mesure_format:
                        expression += f"\n  VAR result = FORMAT(_result1, \"{self.mesure_format}\")"
                expression += f"\n  RETURN _result"

        self.mesure = expression

    def display(self):
        """
        Print the generated measure.
        """
        print(f"{self.name} = {self.mesure}\n")

    def write(self, output_file="output.txt"):
        """
        Write the measure to the specified output file.
        """
        try:
            with open(output_file, 'a') as file:
                file.write(f"{self.name} = {self.mesure}\n\n")
        except Exception as e:
            print(f"Error writing to file '{output_file}': {e}")

date_table_name="dimCalendrier"
date_column_name="Date"
# Example usage
#mesure = Mesure(
#    name="TotalReelF",
#    mesure_type="SUM",
#    table_name="reel",
#    column_name="reel",
#    mesure_format="### ### ### $"
#)

mesure = Mesure(
    name="TotalReelY-1_0",
    mesure_type="SUM",
    table_name="reel",
    column_name="reel",
    period="Year",
    period_start=-1,
    period_end=0,
    mesure_format="### ### ### $"
)
mesure.display()
#output_file = "output.txt"
#mesure.write(output_file)
