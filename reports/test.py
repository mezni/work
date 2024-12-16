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
        self.mesure_end = kwargs.get('mesure_end', None)
        self.mesure = ""
        self.generate()

    def generate(self):
        if self.mesure_type == "SUM":
            expression = f"{self.mesure_type}({self.table_name}[{self.column_name}])"

        if self.mesure_format:
            expression = f"FORMAT({expression}, \"{self.mesure_format}\")"

        if self.period:
            print (self.period)

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


# Example usage
mesure = Mesure(
    name="TotalReelF",
    mesure_type="SUM",
    table_name="reel",
    column_name="reel",
    mesure_format="### ### ### $"
)

mesure = Mesure(
    name="TotalReelF",
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
