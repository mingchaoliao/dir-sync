class ApplicationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

    def get_message(self) -> str:
        return self.args[0]