import random


class Amity(object):
    MAX_OFFICE_OCCUPANTS = 6
    MAX_LIVING_OCCUPANTS = 4
    rooms = {
        'office': {},
        'livingspace': {}
    }
    persons = {
        'fellow': [],
        'staff': []
        }

    def create_room(self, room_name, room_type):
        if not room_name or not room_type:
            return "Provide both room name and room type."

        amity_rooms = self.rooms.get(room_type, None)
        if room_type not in self.rooms.keys():
            return "Insert office or livingspace for room type"

        if amity_rooms.get(room_name):
            return "This room already exists"

        # This can be a function on it own add_living
        if room_type.lower() == "livingspace":  # {"Lagos": []}
            self.rooms["livingspace"][room_name] = []
            return self.rooms.get("livingspace")

        if room_type.lower() == "office":
            self.rooms["office"][room_name] = []
            return self.rooms.get("office")

        return "Invalid entry. Please retry."

    def add_person(self, person_name, person_type='fellow', wants_accomodation="N"):
        if not person_name:
            return "Please insert a name"

        if person_name in self.persons.get(person_type):
            return "Name already exists. Choose another name:"
        allocated_space = {}
        self.persons.get(person_type).append(person_name)
        allocated_office = self._search_room(
                                        person_name,
                                        "office",
                                        self.MAX_OFFICE_OCCUPANTS
                                        )
        if allocated_office:
            allocated_space["office"] = allocated_office
        if person_type.lower() == "fellow":
            if wants_accomodation is not "N":
                allocated_livingspace = self._search_room(
                                                            person_name,
                                                            "livingspace",
                                                            self.MAX_LIVING_OCCUPANTS
                                                            )
                if allocated_livingspace:
                    allocated_space["livingspace"] = allocated_livingspace
        return allocated_space

    def _search_room(self, person_name, room_type, max_occupants):
        office = self.rooms.get(room_type).key()
        searching = True
        while searching:
            random_office = random.choice(office)
            occupants = self.rooms.get(room_type)[random_office]
        # check # of occupants in room against MAX_OFFICE_OCCUPANTS
            if len(occupants) < max_occupants:
                occupants.append[person_name]
                return random_office
            # pop a room once it has been chosen
            office.remove(random_office)
            # check if len of office is 1 exit
            if not len(office):
                searching = False

        return None

    def reallocate_person(self, person_name, room_name, max_occupants):
        # check if person has been allocated a room
        if person_name not in self.rooms:
            return "Person has not yet been allocated a room"
        # check if the room they want has space
        # self._full_room(room_name, "office", self.MAX_OFFICE_OCCUPANTS)
        # # check the room where they have been allocated currently

    # def _full_room(self, room_name, room_type, max_occupants):
    #     preffered_room = self.rooms.get(room_name)
    #     occupants = self.rooms.get(room_type)[preffered_room]
    #     if len(occupants) == max_occupants:
    #         return "No space available in this room"

    def load_people(self, filename):
        with open('load_people.txt', 'r') as filename:
            content = filename.readlines()
            for line in content:
                data = line.split()
                firstname = data[0]
                secondname = data[1]
                fullname = firstname + " " + secondname
                position = data[2].lower()
                try:
                    accomodation = data[3]
                except IndexError:
                    pass
                self.add_person(fullname, position, accomodation)

    def print_allocations(self, room_type, filename):
        get_those_rooms = self.rooms.get(room_type)
        return get_those_rooms

        with open('rooms.txt', 'w') as myfile:
            for key in sorted(get_those_rooms):
                myfile.write(key + '\n' + '-' * 60 + '\n' + ','.join(get_those_rooms[key]) + '\n')

    def print_unallocated(self, room_type, room_name, filename):
        unallocated = []
        get_those_rooms = self.rooms.get(room_type)
        for value in self.persons[room_type]:
            if value not in get_those_rooms:
                unallocated.append(value)
        return unallocated

    def print_room(self, room_type, room_name):
        get_those_rooms = self.rooms.get(room_type)
        return get_those_rooms[room_name]

    def save_state(self):
        pass

    def load_state(self):
        pass
