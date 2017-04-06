from abc import ABCMeta


class Person(object):
    __metaclass__ = ABCMeta

    def __init__(self, person_name, person_type):
        self.person_name = person_name
        self.person_type = person_type


class Fellow(Person):
    def __init__(self, person_name):
        super(Fellow, self).__init__(person_name, 'fellow')


class Staff(Person):
    def __init__(self, person_name):
        super(Staff, self).__init__(person_name, 'staff')
