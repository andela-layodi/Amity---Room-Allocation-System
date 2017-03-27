class Person(object):
    def __init__(self):
        pass


class Fellow(Person):
    def __init__(self):
        super(Fellow, self).__init__()


class Staff(Person):
    def __init__(self):
        super(Staff, self).__init__()
