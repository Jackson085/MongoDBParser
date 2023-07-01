from MongoClientParser import MongoClientParser


class Person:
    def __init__(self):
        self.age = 5
        self.height = 15
        self.asd = 1599

    def __dict__(self):
        return {'age': self.age, 'height': self.height}


class MyClass:
    def __init__(self):
        self.my_attribute = 42
        self.sub_instance = SubClass()
        self.private = 0

    def __dict__(self):
        return {'my_attribute': self.my_attribute, 'sub_instance': self.sub_instance}


class MyClass2:
    def __init__(self):
        self.my_attribute = 424
        self.private = 1

    def __dict__(self):
        return {'my_attribute': self.my_attribute}


class SubClass:
    def __init__(self):
        self.another_attribute = "Hello"
        self.test = [0, MyClass2()]
        self.private = 2

    def __dict__(self):
        return {'another_attribute': self.another_attribute, 'test': self.test}


if __name__ == '__main__':
    m = MyClass()
    p = Person()
    d = MongoClientParser('TestDatabase', 'TestTable')
    # d.parse_insert_one(m)
    r = d.parse_find_one(MyClass(), {'my_attribute': 42})
    # result = d.parse_find_one(Person())
    print(r.sub_instance.test[1].my_attribute)
