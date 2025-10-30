class AllocationError(Exception):
    """
    Allocation sum is not 100% or is negative
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
