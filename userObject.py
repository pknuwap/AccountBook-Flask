# 회비 납부를 위한 user class

class User:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
        self.month = [0,0,0,0,0,0,0,0,0,0,0,0]

    def add_month(self, m):
        self.month[m] = 1

