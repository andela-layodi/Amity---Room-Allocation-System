class Person(object):
    def __init__(self, person_name, person_type, wants_accomodation):
        self.person_name = person_name
        self.person_type = person_type
        self.wants_accomodation = wants_accomodation


class Staff(Person):
    def __init__(self, person_name, wants_accomodation, room_name):
        super(Staff, self).__init__(person_name, person_type, wants_accomodation)


class Fellow(Person):
    def __init__(self, person_name, wants_accomodation, room_name):
        super(Fellow, self).__init__(person_name, person_type, wants_accomodation)
