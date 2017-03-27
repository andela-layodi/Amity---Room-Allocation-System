class Room(object):
    def __init__(self):
        pass


class Office(Room):
    def __init__(self):
        super(Office, self).__init__()
        self.MAX_OFFICE_OCCUPANTS = 6


class LivingSpace(Room):
    def __init__(self):
        super(LivingSpace, self).__init__()
        self.MAX_LIVING_OCCUPANTS = 4
