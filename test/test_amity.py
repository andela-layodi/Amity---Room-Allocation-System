import unittest
from amity.amity import Amity


class AmityTest(unittest.TestCase):
    def setUp(self):
        self.Amity = Amity()

    def test_create_room_without_room(self):
        room_created = self.Amity.create_room("", 'LivingSpace')
        self.assertEqual(room_created, "Provide both room name and room type.")

    def test_create_room_without_type(self):
        room_created = self.Amity.create_room("Platform", "")
        self.assertEqual(room_created, "Provide both room name and room type.")

    def test_room_created_exists(self):
        room_created = self.Amity.create_room('Lagos', 'office')
        self.assertEqual(room_created, "This room already exists.")

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
        person_added = self.Amity.add_person('LESLEY AYODI', 'staff', 'Y')
        self.assertEqual(person_added, "Name already exists. Choose another name.")

    def test_add_person_to_room(self):
        person_added = self.Amity.add_person('EMILY MBELENGA', 'staff', 'Y')
        self.assertEqual(person_added, "Lagos")

    def test_person_already_allocated(self):
        person_allocated = self.Amity.reallocate_person('EMILY MBELENGA', 'Lagos', 6)
        self.assertEqual(person_allocated, "Person has not yet been allocated a room.")

    # def test_if_room_has_space(self):
    #     room_space = self.Amity.reallocate_person('ISABELA WAKESHO', 'Lagos', 6)
    #     self.assertEqual(room_space, "No space available in this room")

    # def test_check_occupants_name(self):
    #     pace = self.Amity.reallocate_person('LESLEY AYODI', 'Lagos', 6)
    #     self.assertEqual(pace, "LESLEY AYODI")







if __name__ == '__main__':
    unittest.main()
