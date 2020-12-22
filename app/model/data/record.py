
class Record:

    def __init__(self, id : int = 0, name : str = None, number : int = 0):
        self.id = id
        self.name = name
        self.number = number

    def __str__(self):
        return str(self.__dict__)
        # return f"({self.id}, {self.name}, {self.number})"