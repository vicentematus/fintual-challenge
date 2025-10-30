class StockInvalidError(Exception):
    """
    Stock is a negative number
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
