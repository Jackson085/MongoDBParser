class SimpleClass:
    def __init__(self):
        self.var1 = 1
        self.var2 = 2
        self.private_var = "private"

    def __dict__(self):
        return {
            'var1': self.var1,
            'var2': self.var2,
        }


class ClassWithSubclass:
    def __init__(self):
        self.normal_var = 1
        self.sub_class = SimpleClass()
        self.private_var = "private"

    def __dict__(self):
        return {
            'normal_var': self.normal_var,
            'sub_class': self.sub_class,
        }


class ClassWithTwoSubclasses:
    def __init__(self):
        self.parent_var = 1
        self.child_class = ClassWithSubclass()
        self.private_var = "private"

    def __dict__(self):
        return {
            'parent_var': self.parent_var,
            'child_class': self.child_class,
        }


class ClassWithList:
    def __init__(self):
        self.parent_var = 1
        self.my_list = [15, 15, 15]
        self.private_var = "private"

    def __dict__(self):
        return {
            'parent_var': self.parent_var,
            'my_list': self.my_list,
        }


class ClassWith2DList:
    def __init__(self):
        self.parent_var = 1
        self.my_list = [15, [42, 42, 42], 15]
        self.private_var = "private"

    def __dict__(self):
        return {
            'parent_var': self.parent_var,
            'my_list': self.my_list,
        }


class ClassWithObjectsInList:
    def __init__(self):
        self.parent_var = 1
        self.my_list = [SimpleClass(), SimpleClass()]
        self.private_var = "private"

    def __dict__(self):
        return {
            'parent_var': self.parent_var,
            'my_list': self.my_list,
        }


class ClassWithObjectsIn2DList:
    def __init__(self):
        self.parent_var = 1
        self.my_list = [SimpleClass(), [SimpleClass()]]
        self.private_var = "private"

    def __dict__(self):
        return {
            'parent_var': self.parent_var,
            'my_list': self.my_list,
        }