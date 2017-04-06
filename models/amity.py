import random
import sqlite3

from titlecase import titlecase

from models.room import Office, LivingSpace
from models.person import Fellow, Staff


class Amity(object):
    """
        This class contains all the rooms and all the people added
        the Amity Room Allocation System.
    """

    def __init__(self):
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

        if room_type not in self.rooms.keys():
            return {"Error": "Insert office or livingspace for room type"}
        if room_name in self._get_all_room_names():
            return {"Error": "This room already exists"}
        if self.rooms.get(room_type, None) is not None:
            new_room = self._assign_room_name(room_type, room_name)
            return {
                "Success": "{} has been added successfully"
                .format(new_room.room_name)
            }

    def _assign_room_name(self, room_type, room_name):
        """
            Used by the create_room function.
            This is where the respective room type is specified before the
            room name is added and saved.
        """
        if room_type.lower() == 'office':
            office = Office(room_name)
            self.rooms[room_type][office] = []
            return office

        if room_type.lower() == 'livingspace':
            livingspace = LivingSpace(room_name)
            self.rooms[room_type][livingspace] = []
            return livingspace

    def add_person(
            self, person_name, person_type='fellow', wants_accomodation="N"):
        """
            Adds new people into the system by specifying their role and
            automatically allocates them to a random room.
        """
        person_name = titlecase(person_name)
        if not person_name:
            return {"Error": "Please insert a name."}

        if person_type not in self.persons.keys():
            return {"Error": "Insert fellow or staff for person type"}

        if person_name in [person.person_name for person in
                           self._get_all_people()]:
            return {"Error": "Name already exists. Choose another name."}
        allocated_space = {}
        if person_type.lower() == 'fellow':
            self.persons.get(person_type).append(Fellow(person_name))
        elif person_type.lower() == 'staff':
            self.persons.get(person_type).append(Staff(person_name))
        else:
            return ("Invalid person type {}".format(person_type))
        if person_type.lower() == 'fellow' or 'staff':
            allocated_office = self._search_room(
                person_name,
                "office"
            )
            if allocated_office:
                allocated_space["office"] = allocated_office

        if person_type.lower() == "fellow" and wants_accomodation is not "N":
            allocated_livingspace = self._search_room(
                person_name,
                "livingspace"
            )
            if allocated_livingspace:
                allocated_space["livingspace"] = allocated_livingspace

        for keys, values in self.rooms.items():
            for name, occupants in values.items():
                if person_name in occupants:
                    return {
                        "Done": "{} has been successfully added to room"
                        .format(person_name)}
                else:
                    return {
                        "Fail": "{} has been added but is not allocated yet"
                        .format(person_name)}

    def _search_room(self, person_name, room_type):
        """
            Used by the add_person function.
            Assists in the selection and allocation of a random room from
            the available rooms.
        """
        rooms = self.rooms.get(room_type).keys()
        search_rooms = list(rooms)
        if not search_rooms:
            return "the system. No rooms available at the moment."
        searching = True
        while searching:
            random_room = random.choice(search_rooms)
            occupants = self.rooms.get(room_type)[random_room]
            if len(occupants) < random_room.max_occupants:
                person_title = titlecase(person_name)
                occupants.append(person_title)
                return random_room
            search_rooms.remove(random_room)
            if not len(search_rooms):
                searching = False

        return None

    def _get_all_people(self):
        all_people = []
        for people_list in self.persons.values():
            all_people += people_list
        return all_people

    def _get_all_people_names(self):
        return [person.person_name for person in self._get_all_people()]

    def _get_all_rooms(self):
        all_rooms = []
        for room in self._merge_rooms().keys():
            all_rooms.append(room)
        return all_rooms

    def _get_all_room_names(self):
        return [room.room_name.lower() for room in self._get_all_rooms()]

    def _get_room_object(self, room_name):
        room_index = self._get_all_room_names().index(room_name.lower())
        if room_index:
            return self._get_all_rooms()[room_index]
        return False

    def _merge_rooms(self):
        return {**self.rooms.get('office'), **self.rooms.get('livingspace')}

    def reallocate_person(
            self, person_name, new_room_name):
        """
            Reallocates a person from the current room to a new room of
            their choice, only if space is available.
            Returns : {`Error`: <Message>}  on error
                      True on successful reallocation
                      False on fail
        """
        try:
            for person in self.persons['fellow'] + self.persons['staff']:
                if person_name == person.person_name and person.person_type == 'staff':
                    self._reallocate_staff(person_name, new_room_name)
                    break
                elif person_name == person.person_name and person.person_type == 'fellow':
                    self._reallocate_fellow(person_name, new_room_name)
                    break
        except:
            return {'Person does not exist'}

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
        occupants = check_room_type.get(room_name)
        if occupants is None:
            return {"Error": "{} does not exist".format(room_name)}

        return occupants

    def _delete_from_previous_allocated_office(self, person_name):
        for room, occupants in self.rooms['office'].items():
            for person in occupants:
                if person == person_name:
                    self.rooms['office'][room].remove(person_name)

    def _delete_from_previous_allocated_livingspace(self, person_name):
        for room, occupants in self.rooms['livingspace'].items():
            for person in occupants:
                if person == person_name:
                    self.rooms['livingspace'][room].remove(person_name)

    def _reallocate_fellow(self, person_name, new_room_name):
        try:
            for room in self.rooms['office']:
                if room.room_name == new_room_name:
                    for person in self.rooms[room.room_type][room]:
                        if person_name == person:
                            return{
                                '{} is already in this room'.format(
                                    person_name)}
                            break
                    if len(self.rooms[room.room_type]
                            [room]) > room.max_occupants:
                        return{'Room is already full.'}
                        break
                    else:
                        self._delete_from_previous_allocated_office(
                            person_name)
                        self.rooms[room.room_type][room].append(person_name)
            for room in self.rooms['livingspace']:
                if room.room_name == new_room_name:
                    for person in self.rooms[room.room_type][room]:
                        if person_name == person:
                            return{
                                '{} is already in this room'.format(
                                    person_name)}
                            break
                    if len(self.rooms[room.room_type]
                           [room]) > room.max_occupants:
                        return {'Room is already full.'}
                        break
                    else:
                        self._delete_from_previous_allocated_livingspace(
                            person_name)
                        self.rooms[room.room_type][room].append(person_name)
        except Exception as e:
            return e

    def _reallocate_staff(self, person_name, new_room_name):
        for room in self.rooms['office']:
            if room.room_name == new_room_name:
                for person in self.rooms[room.room_type][room]:
                    if person_name == person:
                        return {
                            '{} is already in this room'.format(person_name)}
                if len(self.rooms[room.room_type][room]) > room.max_occupants:
                    return {'Room is already full.'}
                else:
                    self._delete_from_previous_allocated_office(person_name)
                    self.rooms[room.room_type][room].append(person_name)
        for room in self.rooms['livingspace']:
            if room.room_name == new_room_name:
                return {'Staff cannot be allocated to a livingspace'}

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
                name = titlecase(fullname)
                position = data[2].lower()
                try:
                    accomodation = data[3]
                except IndexError:
                    pass
                self.add_person(name, position, accomodation)

        return {'Done': "File has been loaded successfully"}

    def print_allocations(self, filename):
        """
            Prints out and outputs to a text file the members of each room in
            the Amity system.
        """
        for room, occupants in self.rooms['office'].items():
            if occupants:
                print(room.room_name)
                print(occupants)
            else:
                print(room.room_name)
                print('Room is empty')

        for room, occupants in self.rooms['livingspace'].items():
            if occupants:
                print(room.room_name)
                print(occupants)
            else:
                print(room.room_name)
                print('Room is empty')

        with open(filename, 'w') as myfile:
            for room, occupants in self.rooms['office'].items():
                myfile.write(
                    "%s \n  %s\n" % (room.room_name, occupants))
            for room, occupants in self.rooms['livingspace'].items():
                myfile.write(
                    "%s \n  %s\n" % (room.room_name, occupants))
            return True

    def print_unallocated(self, filename):
        """
            Prints out and outputs to a text file a list of people who are yet
            to be allocated a room.
        """
        occupants = []
        for keys, values in self.rooms['office'].items():
            occupants += values
        all_people = self._get_all_people_names()
        unallocated_people = set(all_people) - set(occupants)

        with open(filename, 'w') as file_handler:
            for person in unallocated_people:
                file_handler.write("{}\n".format(person))
        return unallocated_people

    def print_room(self, room_name):
        """
            Prints out the members of a specified room in the Amity system.
        """
        for room, occupants in self.rooms['office'].items():
            if room.room_name == room_name:
                print(room_name)
                print(occupants)
                break

        for room, occupants in self.rooms['livingspace'].items():
            if room.room_name == room_name:
                print(room_name)
                print(occupants)
                break

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
                (fellow.person_name, 'fellow',))

        all_staff = self.persons.get('staff')
        for staff in all_staff:
            cur.execute(
                'INSERT INTO Person(Name, Role) VALUES(?, ?)',
                (staff.person_name, "staff")
            )

        all_offices = self.rooms.get('office')
        for office in all_offices:
            cur.execute(
                'INSERT INTO Room(Name, Type) VALUES(?, ?)',
                (office.room_name, "office")
            )

        all_livingspaces = self.rooms.get('livingspace')
        for livingspace in all_livingspaces:
            cur.execute(
                'INSERT INTO Room(Name, Type) VALUES(?, ?)',
                (livingspace.room_name, "livingspace"))

        allocated_offices = self.rooms.get('office')
        for office, people in allocated_offices.items():
            for values in people:
                cur.execute(
                    'INSERT INTO Allocated(Person_Name, Room_Name) \
                    VALUES(?, ?)', (values, office.room_name))

        allocated_livingspaces = self.rooms.get('livingspace')
        for livingspace, people in allocated_livingspaces.items():
            for values in people:
                cur.execute(
                    'INSERT INTO Allocated(Person_Name, Room_Name) \
                     VALUES(?, ?)', (values, livingspace.room_name))
        conn.commit()
        conn.close()
        return True

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
                self.persons['fellow'].append(Fellow(fellow_element))

        cur.execute('SELECT Name FROM Person WHERE Role = "staff"')
        all_staff = cur.fetchall()
        for staff_tuple in all_staff:
            staff_list = list(staff_tuple)
            for staff_element in staff_list:
                self.persons['staff'].append(Staff(staff_element))

        cur.execute('SELECT Name FROM Room WHERE Type = "office"')
        load_office = cur.fetchall()
        for office_tuple in load_office:
            office_list = list(office_tuple)
            for office_element in office_list:
                office = Office(office_element)
                self.rooms['office'][office] = []

        cur.execute('SELECT Name FROM Room WHERE Type = "livingspace"')
        load_livingspace = cur.fetchall()
        for livingspace_tuple in load_livingspace:
            livingspace_list = list(livingspace_tuple)
            for livingspace_element in livingspace_list:
                livingspace = LivingSpace(livingspace_element)
                self.rooms['livingspace'][livingspace] = []

        cur.execute('SELECT * FROM Allocated')
        load_allocated_all = cur.fetchall()
        for all_tuple in load_allocated_all:
            all_list = list(all_tuple)
            person_name = all_list[0]
            room_name = all_list[1]
            offices = self.rooms.get('office')
            livingspaces = self.rooms.get('livingspace')
            for room in offices.keys():
                if room.room_name == room_name:
                    self.rooms['office'][room].append(person_name)
            for room in livingspaces.keys():
                if room.room_name == room_name:
                    self.rooms['livingspace'][room].append(person_name)

        conn.close()
        return True
