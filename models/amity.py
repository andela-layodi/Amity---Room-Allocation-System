import random
import sqlite3


class Amity(object):
    """
        This class contains all the rooms and all the people added
        the Amity Room Allocation System.
    """

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
        """
            Creates new rooms into the room allocation system.
        """
        if not room_name or not room_type:
            return {"Error": "Provide both room name and room type."}

        amity_rooms = self.rooms.get(room_type, None)
        if room_type not in self.rooms.keys():
            return {"Error": "Insert office or livingspace for room type"}
        if amity_rooms.get(room_name) is not None:
            return {"Error": "This room already exists"}
        if self.rooms.get(room_type, None) is not None:
            self._assign_room_name(room_type, room_name)
            return {"Success": "Room has been added successfully"}

    def _assign_room_name(self, room_type, room_name):
        """
            Used by the create_room function.
            This is where the respective room type is specified before the
            room name is added and saved.
        """
        if room_type.lower() == room_type:
            self.rooms[room_type][room_name] = []
            return self.rooms.get(room_type)

    def add_person(
            self, person_name, person_type='fellow', wants_accomodation="N"):
        """
            Adds new people into the system by specifying their role and
            automatically allocates them to a random room.
        """
        if not person_name:
            return "Please insert a name."

        if person_name in self.persons.get(person_type):
            return "Name already exists. Choose another name."
        if person_type not in self.persons.keys():
            return {"Error": "Insert fellow or staff for person type"}
        allocated_space = {}
        self.persons.get(person_type).append(person_name)
        allocated_office = self._search_room(
            person_name,
            "office",
            self.MAX_OFFICE_OCCUPANTS
        )
        if allocated_office:
            allocated_space["office"] = allocated_office
        if person_type.lower() == "fellow" and wants_accomodation is not "N":
            allocated_livingspace = self._search_room(
                person_name,
                "livingspace",
                self.MAX_LIVING_OCCUPANTS
            )
            if allocated_livingspace:
                allocated_space["livingspace"] = allocated_livingspace
        user_room = allocated_space.values()
        for room in user_room:
            return {
                "Done": "{} has been added to {}".format(person_name, room)
            }

    def _search_room(self, person_name, room_type, max_occupants):
        """
            Used by the add_person function.
            Assists in the selection and allocation of a random room from
            the available rooms.
        """
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

    def reallocate_person(
            self, room_type, current_room, room_name, person_name):
        """
            Reallocates a person from the current room to a new room of
            their choice, only if space is available.
            Returns : {`Error`: <Message>}  on error
                      True on successful reallocation
                      False on fail
        """
        maximum = self.MAX_LIVING_OCCUPANTS
        current_roommates = self._find_room_occupant(room_type, current_room)
        if "Error" in current_roommates:
            return current_roommates

        if person_name not in current_roommates:
            return {
                "Error": "{} not found in {}".format(person_name, current_room)
            }

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
        """
            Used by the reallocate person function.
            It checks the current occupants of the new room as well as checking
            if the person requesting for reallocation has a room in the first
            place.
        """
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
        """
            Loads new people form a text file to the system in order for them
            to be allocated spaces.
        """
        with open(filename, 'r') as filename:
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
        return {'Done': "File has been loaded successfully"}

    def print_allocations(self, room_type, filename):
        """
            Prints out and outputs to a text file the members of each room in
            the Amity system.
        """
        allocated_rooms = self.rooms.get(room_type)
        # return get_those_rooms

        with open('rooms.txt', 'w') as myfile:
            for key in sorted(allocated_rooms):
                myfile.write(
                    key +
                    '\n' +
                    '-' *
                    60 +
                    '\n' +
                    ','.join(
                        allocated_rooms[key]) +
                    '\n')
        return allocated_rooms

    def print_unallocated(self, room_type, room_name, filename):
        """
            Prints out and outputs to a text file a list of people who are yet
            to be allocated a room.
        """
        unallocated = []
        allocated_rooms = self.rooms.get(room_type)
        for value in self.persons[room_type]:
            if value not in allocated_rooms:
                unallocated.append(value)
        return unallocated

    def print_room(self, room_type, room_name):
        """
            Prints out the members of a specified room in the Amity system.
        """
        allocated_rooms = self.rooms.get(room_type)
        people = allocated_rooms.get(room_name)
        return {
            "Success": "The occupants of {} are {}".format(room_name, people)
        }

    def save_state(self, db_name):
        """
            Saves the data inputted into the Amity system to a SQLite database.
        """
        db_name = str(db_name)
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Person")
        cur.execute(
            'CREATE TABLE {table_name}({first_col} TEXT, {second_col} TEXT)'
            .format(
                table_name="Person",
                first_col="Name",
                second_col="Role"))
        cur.execute("DROP TABLE IF EXISTS Room")
        cur.execute(
            'CREATE TABLE {table_name}({first_col} TEXT, {second_col} TEXT)'
            .format(
                table_name="Room",
                first_col="Name",
                second_col="Type"))
        cur.execute("DROP TABLE IF EXISTS Allocated")
        cur.execute(
            'CREATE TABLE {table_name}({first_col} TEXT, {second_col} TEXT)'
            .format(
                table_name="Allocated",
                first_col="Person_Name",
                second_col="Room_Name"))
        all_fellows = self.persons.get('fellow')
        for fellow in all_fellows:
            cur.execute(
                'INSERT INTO Person(Name, Role) VALUES(?, ?)',
                (fellow, "fellow"))

        all_staff = self.persons.get('staff')
        for staff in all_staff:
            cur.execute(
                'INSERT INTO Person(Name, Role) VALUES(?, ?)', (staff, "staff")
            )

        all_offices = self.rooms.get('office')
        for office in all_offices:
            cur.execute(
                'INSERT INTO Room(Name, Type) VALUES(?, ?)', (office, "office")
            )

        all_livingspaces = self.rooms.get('livingspace')
        for livingspace in all_livingspaces:
            cur.execute(
                'INSERT INTO Room(Name, Type) VALUES(?, ?)',
                (livingspace, "livingspace"))

        allocated_offices = self.rooms.get('office')
        for office, people in allocated_offices.items():
            for values in people:
                for v in values:
                    cur.execute(
                        'INSERT INTO Allocated(Person_Name, Room_Name) \
                        VALUES(?, ?)', (v, office))

        allocated_livingspaces = self.rooms.get('livingspace')
        for livingspace, people in allocated_livingspaces.items():
            for values in people:
                for v in values:
                    cur.execute(
                        'INSERT INTO Allocated(Person_Name, Room_Name) \
                         VALUES(?, ?)', (v, livingspace))
        return True
        conn.commit()
        conn.close()

    def load_state(self, db_name):
        """
            Loads the data inputted into the Amity system from a
            SQLite database.
        """

        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        cur.execute('SELECT Name FROM Person WHERE Role = "fellow"')
        all_fellows = cur.fetchall()
        for fellow_tuple in all_fellows:
            fellow_list = list(fellow_tuple)
            for fellow_element in fellow_list:
                self.persons['fellow'].append(fellow_element)

        cur.execute('SELECT Name FROM Person WHERE Role = "staff"')
        all_staff = cur.fetchall()
        for staff_tuple in all_staff:
            staff_list = list(staff_tuple)
            for staff_element in staff_list:
                self.persons['staff'].append(staff_element)

        cur.execute('SELECT Name FROM Room WHERE Type = "office"')
        load_office = cur.fetchall()
        for office_tuple in load_office:
            office_list = list(office_tuple)
            for office_element in office_list:
                self.rooms['office'][office_element] = []

        cur.execute('SELECT Name FROM Room WHERE Type = "livingspace"')
        load_livingspace = cur.fetchall()
        for livingspace_tuple in load_livingspace:
            livingspace_list = list(livingspace_tuple)
            for livingspace_element in livingspace_list:
                self.rooms['livingspace'][livingspace_element] = []

        cur.execute('SELECT * FROM Allocated')
        load_allocated_all = cur.fetchall()
        for all_tuple in load_allocated_all:
            all_list = list(all_tuple)
            offices = self.rooms.get('office')
            livingspaces = self.rooms.get('livingspace')
            if all_list[1] in offices.keys():
                offices[all_list[1]].append(all_list[0])
            else:
                livingspaces[all_list[1]].append(all_list[0])
        return True

        conn.close()
