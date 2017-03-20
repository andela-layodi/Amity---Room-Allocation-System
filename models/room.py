class Room(object):

    def __init__(self, room_name, room_type):
        self.room_name = room_name
        self.room_type = room_type


class Office(Room):
    max_capacity = 6
    def __init__(self, room_name, person_name, occupant_no):
        super(Office, self).__init__(room_name, room_type)


class LivingSpace(Room):
    max_capacity = 4
    def __init__(self, room_name, person_name, occupant_no):
        super(LivingSpace, self).__init__(room_name, room_type)
