import unittest
from models.amity import Amity


class AmityTest(unittest.TestCase):
    def setUp(self):
        self.Amity = Amity()

    def _create_rooms(self):
        room_types = {
            "office": ['MOMBASA', 'HOGWARTS', 'LAGOS'],
            "livingspace": ['KENYA', 'PLATFORM', 'VALHALLA']
        }
        keys = room_types.keys()
        for room in keys:
            for names in room_types.get(room):
                self.Amity._assign_room_name(room, names)

    def test_create_room_without_name(self):
        room_created = self.Amity.create_room("", 'LivingSpace')
        self.assertIn("Error", room_created)

    def test_create_room_without_type(self):
        room_created = self.Amity.create_room("Platform", "")
        self.assertIn("Error", room_created)

    def test_room_created_exists(self):
        self.Amity.create_room('Lagos', 'office')
        room_created = self.Amity.create_room('Lagos', 'office')
        print (self.Amity.rooms)
        self.assertIn("Error", room_created)

    def test_amity_room_object(self):
        rooms = self.Amity.rooms.keys()
        self.assertEqual(len(rooms), 2)
        self.assertIn("office", rooms)
        self.assertIn("livingspace", rooms)

    def test_create_office(self):
        office = self.Amity.create_room("Platform", "office")
        self.assertIn("Success", office)

    def test_create_livingspace(self):
        livingspace = self.Amity.create_room("Rongai", "livingspace")
        print (livingspace)
        self.assertIn("Success", livingspace)

    def test_create_invalid(self):
        livingspace = self.Amity.create_room("Rongai", "school")
        self.assertIn("Error", livingspace)

    def test_assign_room_name(self):
        assigned_name = self.Amity._assign_room_name('office', 'MOMBASA')
        self.assertEqual(assigned_name, {'MOMBASA': []})

    def test_add_person_without_name(self):
        person_added = self.Amity.add_person('', 'fellow', 'N')
        self.assertIn('Error', person_added)

    def test_add_person_exists(self):
        self._create_rooms()
        self.Amity.add_person('LESLEY AYODI', 'staff', 'Y')
        person_added = self.Amity.add_person('LESLEY AYODI', 'staff', 'Y')
        self.assertIn('Error', person_added)

    def test_add_person_to_room(self):
        # self._create_rooms()
        room_allocated = self.Amity.add_person('EMILY MBELENGA', 'fellow', 'N')
        print (room_allocated)
        self.assertIn("Done", room_allocated)

    # def test_add_invalid_person_type(self):
    #     self._create_rooms()
    #     type_added = self.Amity.add_person('LESLEY AYODI', 'cook', 'N')
    #     self.assertIn('Error', type_added)

    def test_check_occupants(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        self.Amity.add_person('LAVENDER AYODI', 'fellow', 'N')
        self.Amity.add_person('PATIENCE AYODI', 'staff', 'N')
        room_occupants = self.Amity._find_room_occupant('office', 'MOMBASA')
        print (room_occupants)
        self.assertEqual(len(room_occupants), 3)

    def test_invalid_room_type(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        room_occupants = self.Amity._find_room_occupant('offic', 'MOMBASA')
        self.assertIn("Error", room_occupants)

    def test_invalid_room_name(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        room_occupants = self.Amity._find_room_occupant('office', 'MOMBA')
        self.assertIn("Error", room_occupants)

    def test_reallocate_person(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        self.Amity.add_person('LAVENDER AYODI', 'staff', 'N')
        self.Amity.create_room('LAGOS', 'office')
        reallocate_person = self.Amity.reallocate_person(
            "office", 'MOMBASA', 'LAGOS', 'LAVENDER AYODI')
        self.assertEqual(True, reallocate_person)

    def test_reallocate_invalid_person(self):
        self.Amity.create_room('MOMBASA', 'office')
        self.Amity.create_room('LAGOS', 'office')
        reallocate_person = self.Amity.reallocate_person(
            "office", 'MOMBASA', 'LAGOS', 'ISABEL AYODI')
        self.assertIn('Error', reallocate_person)

    def test_reallocate_invalid_room(self):
        invalid_room = self.Amity.reallocate_person(
            "office", 'MOMBASA', 'LAGOS', 'ISABEL AYODI')
        self.assertIn('Error', invalid_room)

    def test_full_room(self):
        self.Amity.create_room('LAGOS', 'office')
        self.Amity.add_person('LESLEY AYODI', 'staff', 'N')
        self.Amity.create_room('MOMBASA', 'office')
        occupants = ['A', 'B', 'C', 'D', 'E', 'F']
        office = self.Amity.rooms.get('office')
        office['MOMBASA'] = occupants
        reallocate_person = self.Amity.reallocate_person(
            "office", 'LAGOS', 'MOMBASA', 'LESLEY AYODI')
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
        self.Amity.load_people("people.txt")
        self.assertEqual(len(persons_list), 4)

    def test_save_state_works(self):
        saved_state = self.Amity.save_state('test_amity.db')
        self.assertEqual(True, saved_state)

    def test_load_state_works(self):
        loaded_state = self.Amity.load_state('test_amity.db')
        self.assertEqual(True, loaded_state)

    # def tearDown(self):
    #     self.Amity.dispose()


if __name__ == '__main__':
    unittest.main()
