import random


class Amity(object):
    def __init__(self):
        self.MAX_OFFICE_OCCUPANTS = 6
        self.MAX_LIVING_OCCUPANTS = 4
        self.rooms = {
            'office': {},
            'livingspace': {}
        }
        self.persons = {
            'fellow': [],
            'staff': []
            }

    def create_room(self, room_name, room_type):
        if not room_name or not room_type:
            return {"Error": "Provide both room name and room type."}

        amity_rooms = self.rooms.get(room_type, None)
        if room_type not in self.rooms.keys():
            return "Insert office or livingspace for room type"
        if amity_rooms.get(room_name) is not None:
            return "This room already exists"
        # check if room is either office or livingspace
        print (self.rooms.get(room_type))
        if self.rooms.get(room_type, None) is not None:
            return self.assign_room_name(room_type, room_name)  # {"Lagos": []}
        # room type does not exist
        return "Invalid entry. Please retry."

    def assign_room_name(self, room_type, room_name):
        if room_type.lower() == room_type:  # {"Lagos": []}
            self.rooms[room_type][room_name] = []
            return self.rooms.get(room_type)

    def add_person(self, person_name, person_type='fellow', wants_accomodation="N"):
        if not person_name:
            return "Please insert a name."

        if person_name in self.persons.get(person_type):
            return "Name already exists. Choose another name."
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
        office = self.rooms.get(room_type).keys()
        search_office = list(office)
        searching = True
        while searching:
            random_office = random.choice(search_office)
            occupants = self.rooms.get(room_type)[random_office]
        # check # of occupants in room against MAX_OFFICE_OCCUPANTS
            if len(occupants) < max_occupants:
                occupants.append(person_name)
                return random_office
            # pop a room once it has been chosen
            search_office.remove(random_office)
            # check if len of office is 1 exit
            if not len(search_office):
                searching = False

        return None

    def reallocate_person(self, room_type, current_room, room_name, person_name):
        """
            Returns : {`Error`: <Message>}  on error
                      True on successful reallocation
                      False on fail
         """
        maximum = self.MAX_LIVING_OCCUPANTS
        current_roommates = self._find_room_occupant(room_type, current_room)
        if "Error" in current_roommates:
            return current_roommates

        if person_name not in current_roommates:
            return {"Error": "{} not found in {}".format(person_name, current_room)}

        new_roommates = self._find_room_occupant(room_type, room_name)
        if "Error" in new_roommates:
            return new_roommates
        if room_type == "office":
            maximum = self.MAX_OFFICE_OCCUPANTS
        if len(new_roommates) < maximum:
            new_roommates.append(person_name)
            current_roommates.remove(person_name)
            return True

        return False


    def _find_room_occupant(self, room_type, room_name):
        check_room_type = self.rooms.get(room_type)
        if check_room_type is None:
            return {"Error": "Insert either office or livingspace"}
        # get room name
        occupants_list = check_room_type.get(room_name)
        # if occupants list is none it means room does not exist
        # expect either [...*]/ [] not None
        if occupants_list is None:
            return {"Error": "{} does not exist".format(room_name)}

        return occupants_list

    def load_people(self, filename):
        with open(filename, 'r') as file_name:
            content = file_name.readlines()
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
        return {'Done': "File has been loaded successfully"}

    def print_allocations(self, room_type, filename):
        allocated_rooms = self.rooms.get(room_type)
        # return get_those_rooms

        with open('rooms.txt', 'w') as myfile:
            for key in sorted(allocated_rooms):
                myfile.write(key + '\n' + '-' * 60 + '\n' + ','.join(allocated_rooms[key]) + '\n')
        return allocated_rooms

    def print_unallocated(self, room_type, room_name, filename):
        unallocated = []
        allocated_rooms = self.rooms.get(room_type)
        for value in self.persons[room_type]:
            if value not in allocated_rooms:
                unallocated.append(value)
        return unallocated

    def print_room(self, room_type, room_name):
        allocated_rooms = self.rooms.get(room_type)
        available_occupants = allocated_rooms[room_name]
        return {"Success": "The occupants of {} are {}".format(room_name, available_occupants)}

    def save_state(self):
        pass

    def load_state(self):
        pass
