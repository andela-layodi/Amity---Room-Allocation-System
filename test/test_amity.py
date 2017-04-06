import unittest
from models.amity import Amity
from models.room import Office, LivingSpace
from models.person import Fellow, Staff


class AmityTest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.amity.room_types = {
            "office": {Office('MOMBASA'): ['Lavender Ayodi'],
                       Office('HOGWARTS'): [],
                       Office('LAGOS'): ['A', 'B', 'C', 'D', 'E', 'F']},
            "livingspace": {LivingSpace('KENYA'): [],
                            LivingSpace('PLATFORM'): [],
                            LivingSpace('VALHALLA'): []}
        }

        self.amity.persons = {
            'fellow': [Fellow('Lavender Ayodi')],
            'staff': [Staff('John Doe')]
        }

    def _create_rooms(self):
        room_types = {
            "office": {Office('MOMBASA'), Office('HOGWARTS'), Office('LAGOS')},
            "livingspace": {LivingSpace('KENYA'), LivingSpace('PLATFORM'),
                            LivingSpace('VALHALLA')}
        }
        keys = room_types.keys()
        for room in keys:
            for names in room_types.get(room):
                self.amity._assign_room_name(room, names)

    def test_create_room_without_name(self):
        room_created = self.amity.create_room("", 'livingspace')
        self.assertIn("Error", room_created)

    def test_create_room_without_type(self):
        room_created = self.amity.create_room("Platform", "")
        self.assertIn("Error", room_created)

    def test_room_created_exists(self):
        self.amity.create_room('Lagos', 'office')
        room_created = self.amity.create_room('Lagos', 'office')
        print (self.amity.rooms)
        self.assertIn("Error", room_created)

    def test_amity_room_object(self):
        rooms = self.amity.rooms.keys()
        self.assertEqual(len(rooms), 2)
        self.assertIn("office", rooms)
        self.assertIn("livingspace", rooms)

    def test_create_office(self):
        office = self.amity.create_room("Platform", "office")
        self.assertIn("Success", office)

    def test_create_livingspace(self):
        livingspace = self.amity.create_room("Rongai", "livingspace")
        print (livingspace)
        self.assertIn("Success", livingspace)

    def test_create_invalid(self):
        livingspace = self.amity.create_room("Rongai", "school")
        self.assertIn("Error", livingspace)

    def test_add_person_without_name(self):
        person_added = self.amity.add_person('', 'fellow', 'N')
        self.assertIn('Error', person_added)

    def test_add_person_exists(self):
        self._create_rooms()
        self.amity.add_person('LESLEY AYODI', 'staff', 'Y')
        person_added = self.amity.add_person('LESLEY AYODI', 'staff', 'Y')
        self.assertIn('Error', person_added)

    def test_add_person_to_room(self):
        self.amity.create_room('MOMBASA', 'office')
        room_allocated = self.amity.add_person('EMILY MBELENGA', 'fellow', 'N')
        self.assertIn("Done", room_allocated)

    def test_add_invalid_person_type(self):
        self.amity.create_room('MOMBASA', 'office')
        type_added = self.amity.add_person('LESLEY AYODI', 'cook', 'N')
        self.assertIn('Error', type_added)

    def test_invalid_room_type(self):
        self.amity.create_room('MOMBASA', 'office')
        self.amity.add_person('LESLEY AYODI', 'staff', 'N')
        room_occupants = self.amity._find_room_occupant('offic', 'MOMBASA')
        self.assertIn("Error", room_occupants)

    def test_invalid_room_name(self):
        self.amity.create_room('MOMBASA', 'office')
        self.amity.add_person('LESLEY AYODI', 'staff', 'N')
        room_occupants = self.amity._find_room_occupant('office', 'MOMBA')
        self.assertIn("Error", room_occupants)

    def test_reallocate_person(self):
        reallocate_person = self.amity.reallocate_person(
            'Lavender Ayodi', 'HOGWARTS')
        self.assertIn("Success", reallocate_person)

    def test_reallocate_invalid_person(self):
        reallocate_person = self.amity.reallocate_person(
            'ISABEL AYODI', 'HOGWARTS')
        self.assertIn('Error', reallocate_person)

    def test_reallocate_invalid_room(self):
        invalid_room = self.amity.reallocate_person(
            'Lavender Ayodi', 'HOGWART')
        self.assertIn('Error', invalid_room)

    def test_full_room(self):
        reallocate_person = self.amity.reallocate_person(
            'Lavender Ayodi', 'LAGOS')
        self.assertEqual('Room is already full.', reallocate_person)

    def test_print_allocations(self):
        self.amity.add_person('Lesley Ayodi', 'staff', 'N')
        allocated_room = self.amity.print_allocations('room.txt')
        self.assertEqual(True, allocated_room)

    def test_print_allocations_terminal(self):
        self.amity.add_person('Lesley Ayodi', 'staff', 'N')
        allocated_room = self.amity.print_allocations('room.txt')
        self.assertEqual(True, allocated_room)

    def test_print_unallocated_persons(self):
        self.amity.add_person('LESLEY AYODI', 'fellow', 'Y')
        self.amity.add_person('LAVENDER AYODI', 'fellow', 'Y')
        self.amity.add_person('BRIAN MUTHUI', 'fellow', 'Y')
        self.amity.add_person('DENNIS MWANGI', 'fellow', 'Y')
        self.amity.add_person('MBARAK MBIGO', 'fellow', 'Y')
        self.amity.add_person('DENNIS YESWA', 'fellow', 'Y')
        self.amity.add_person('CYNTHIA ABURA', 'fellow', 'Y')
        unallocated = self.amity.print_unallocated('unallocated.txt')
        self.assertEqual(len(unallocated), 1)

    def test_print_room_occupants(self):
        available_occupants = self.amity.print_room('MOMBASA')
        self.assertIn('Lavender Ayodi', available_occupants)

    def test_load_people_from_file(self):
        persons_list = self.amity.persons.get('fellow')
        self.assertEqual(len(persons_list), 1)
        self.amity.load_people("people.txt")
        self.assertEqual(len(persons_list), 5)

    def test_save_state_works(self):
        saved_state = self.amity.save_state('test_amity.db')
        self.assertEqual(True, saved_state)

    def test_load_state_works(self):
        loaded_state = self.amity.load_state('test_amity.db')
        self.assertEqual(True, loaded_state)


if __name__ == '__main__':
    unittest.main()
