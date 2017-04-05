from abc import ABCMeta


class Room(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, room_type, max_occupants):
        self.room_name = name
        self.room_type = room_type
        self.max_occupants = max_occupants


class Office(Room):
    def __init__(self, room_name):
        super(Office, self).__init__(
            room_name, 'office', 6)


class LivingSpace(Room):
    def __init__(self, room_name):
        super(LivingSpace, self).__init__(
            room_name, 'livingspace', 4)
