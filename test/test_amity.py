import unittest
from amity.amity import Amity
import os


class AmityTest(unittest.TestCase):
    def setUp(self):
        self.Amity = Amity()


    def _create_rooms(self):
        room_types = {"office": ['MOMBASA', 'HOGWARTS', 'LAGOS'],
        "livingspace": ['KENYA', 'PLATFORM', 'VALHALLA']
        }
        keys = room_types.keys()
        for room in keys:
            for names in room_types.get(room):
                self.Amity.assign_room_name(room, names)

    def test_create_room_without_room(self):
        room_created = self.Amity.create_room("", 'LivingSpace')
        self.assertIn("Error", room_created)

    def test_create_room_without_type(self):
        room_created = self.Amity.create_room("Platform", "")
        self.assertIn("Error", room_created)

    def test_room_created_exists(self):
        self.Amity.create_room('Lagos', 'office')
        room_created = self.Amity.create_room('Lagos', 'office')
        print (self.Amity.rooms)
        self.assertEqual(room_created, "This room already exists")

    def test_amity_room_object(self):
        rooms = self.Amity.rooms.keys()
        self.assertEqual(len(rooms), 2)
        self.assertIn("office", rooms)
        self.assertIn("livingspace", rooms)

    def test_amity_has_no_rooms(self):
        rooms = self.Amity.rooms
        self.assertEqual(len(rooms.get('office')), 0)
        self.assertEqual(len(rooms.get('livingspace')), 0)

    def test_create_office(self):
        office = self.Amity.create_room("Platform", "office")
        self.assertIn("Platform", office)

    def test_create_livingspace(self):
        livingspace = self.Amity.create_room("Rongai", "livingspace")
        self.assertIn("Rongai", livingspace)

    def test_create_invalid(self):
        livingspace = self.Amity.create_room("Rongai", "school")
        self.assertEqual(livingspace, "Insert office or livingspace for room type")

    def test_add_person_without_name(self):
        person_added = self.Amity.add_person('', 'fellow', 'N')
        self.assertEqual(person_added, "Please insert a name.")

    def test_add_person_exists(self):
        self._create_rooms()
        self.Amity.add_person('LESLEY AYODI', 'staff', 'Y')
        person_added = self.Amity.add_person('LESLEY AYODI', 'staff', 'Y')
        self.assertEqual(person_added, "Name already exists. Choose another name.")

    def test_add_person_to_room(self):
        self._create_rooms()
        room_allocated = self.Amity.add_person('EMILY MBELENGA', 'staff', 'N')
        room_name = room_allocated["office"]
        list_of_occupants = self.Amity.rooms.get("office")[room_name]
        self.assertIn("EMILY MBELENGA", list_of_occupants)

    def test_check_occupants(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        self.Amity.add_person('LAVENDER AYODI', 'fellow', 'N')
        self.Amity.add_person('PATIENCE AYODI', 'staff', 'N')
        room_occupants =  self.Amity._find_room_occupant('office', 'MOMBASA')
        self.assertEqual(len(room_occupants), 3)

    def test_invalid_room_type(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        room_occupants =  self.Amity._find_room_occupant('offic', 'MOMBASA')
        self.assertIn("Error", room_occupants)

    def test_invalid_room_name(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        room_occupants =  self.Amity._find_room_occupant('office', 'MOMBA')
        self.assertIn("Error", room_occupants)

    def test_reallocate_person(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        self.Amity.add_person('LAVENDER AYODI', 'staff', 'N')
        self.Amity.create_room('LAGOS', 'office')
        reallocate_person = self.Amity.reallocate_person("office", 'MOMBASA', 'LAGOS', 'LAVENDER AYODI')
        self.assertEqual(True,reallocate_person)

    def test_reallocate_invalid_person(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.create_room('LAGOS', 'office')
        reallocate_person = self.Amity.reallocate_person("office", 'MOMBASA', 'LAGOS', 'ISABEL AYODI')
        self.assertIn('Error', reallocate_person)

    def test_reallocate_invalid_room(self):
        invalid_room = self.Amity.reallocate_person("office", 'MOMBASA', 'LAGOS', 'ISABEL AYODI')
        self.assertIn('Error', invalid_room)

    def test_full_room(self):
        self.Amity.create_room('LAGOS', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        self.Amity.create_room('MOMBASA', 'office')
        occupants = ['A', 'B', 'C', 'D', 'E', 'F']
        office = self.Amity.rooms.get('office')
        office['MOMBASA'] = occupants
        reallocate_person = self.Amity.reallocate_person("office", 'LAGOS', 'MOMBASA', 'LESLEY AYODI')
        self.assertEqual(False, reallocate_person)

    def test_print_allocations(self):
        self.Amity.create_room('LAGOS', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        allocated_room = self.Amity.print_allocations('office', 'rooms.txt')
        self.assertEqual(allocated_room, {'LAGOS': ['LESLEY AYODI']})


    def test_print_allocations_terminal(self):
        self.Amity.create_room('LAGOS', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        allocated_room = self.Amity.print_allocations('office', 'rooms.txt')
        self.assertEqual(allocated_room, {'LAGOS': ['LESLEY AYODI']})

    def test_print_room_occupants(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        self.Amity.add_person('LAVENDER AYODI', 'fellow', 'N')
        self.Amity.add_person('PATIENCE AYODI', 'staff', 'N')
        available_occupants = self.Amity.print_room('office', 'MOMBASA')
        self.assertIn('Success', available_occupants)


    def test_load_people_from_file(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.create_room('KENYA', 'livingspace')
        persons_list = self.Amity.persons.get('fellow')
        self.assertEqual(len(persons_list), 0)
        self.Amity.load_people("test_people.txt")
        self.assertEqual(len(persons_list), 4)

    def test_allocated_people(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        self.Amity.add_person('LAVENDER AYODI', 'fellow', 'N')
        self.Amity.add_person('PATIENCE AYODI', 'staff', 'N')
        self.Amity.add_person('SIMON AYODI', 'staff', 'N')
        self.Amity.add_person('GRACE AYODI', 'staff', 'N')
        self.Amity.add_person('GRACE NJERI', 'staff', 'N')
        self.Amity.create_room('PLATFORM', 'livingspace')
        self.Amity.add_person('LESLEY MBINGU', 'fellow', 'Y')
        self.Amity.add_person('MARY NJERI', 'fellow', 'Y')
        allocate_persons = self.Amity.print_unallocated('fellow', "test_people.txt")
        self.assertEqual(len(allocate_persons), 3)

if __name__ == '__main__':
    unittest.main()
