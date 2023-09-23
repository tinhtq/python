class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def greetings(self):
        return f"{self.first_name} is a student"


class CollegeStudent(Student):
    def __init__(self, first_name, last_name, major):
        super().__init__(first_name, last_name)
        self.major = major

    def greetings(self):
        return f"{self.first_name} is a college student"


student1 = Student("test", "account")
