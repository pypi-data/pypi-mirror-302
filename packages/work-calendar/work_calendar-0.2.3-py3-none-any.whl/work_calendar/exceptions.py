class NoDataForYearError(Exception):
    def __init__(self, year: int):
        self.year = year
        self.message = f"No data found for year {self.year}"
        super().__init__(self.message)
