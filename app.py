"""
Amity
Room Allocation System
This system facilitates easier room allocation for people at Amity.
Usage:
        create_room <room_name> <room_type>
    	add_person <person_name> <person_type> <wants_accommodation>
    	reallocate_person <room_type> <current_room> <new_room> <person_name>
    	load_people <filename>
    	print_allocations <room_type>[--o=filename]
    	print_unallocated <room_type> <room_name>[--o=filename]
        print_room <room_type> <room_name>
    	load_state [--dbname]
    	save_state [--o=db_name]
    	quit
        (-i | --interactive)
        (-h | --help | --version)
Options:
    -h --help Show this screen.
    -i, --interactive  Interactive Mode.
    -v, --version.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from pyfiglet import figlet_format
from termcolor import cprint

from models.amity import Amity

# docopt(__doc__, argv=None, help=True, version=0.1, options_first=False)

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # Print a message to the user and the usage block.

            print('Invalid command has been entered!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # No need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class AmityApp(cmd.Cmd):
    intro = cprint(figlet_format("Amity Room App System", font="cosmic"), "white")
    prompt = 'Amity>>> '
    file=None

    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """
        Creates a new room in the system.
        Usage: create_room <room_name> <room_type>
        """
        room_name = arg["<room_name>"]
        room_type = arg["<room_type>"]
        print (self.amity.create_room(room_name, room_type))


    @docopt_cmd
    def do_add_person(self, args):
        """
        Creates a new person and assigns them to a random room in Amity.
        Usage: add_person <person_name> <person_type> <wants_accommodation>
        """
        person_name = arg["<person_name>"]
        person_type = arg["<person_type>"]
        wants_accommodation = arg["<wants_accommodation>"]
        add_person_status = self.amity.add_person(person_name, person_type, wants_accomodation)

        if add_person_status == "Please insert a name.":
            print ("Please insert a name.")

        if add_person_status == "Name already exists. Choose another name.":
            print ("Name already exists. Choose another name.")

        amity_rooms = self.amity.rooms.get(room_type)
        print (amity_rooms.get(room_name))

    @docopt_cmd
    def do_reallocate_person(self, args):
        """
        Reallocates a person to a new room of their choice.
        Usage: reallocate_person <room_type> <current_room> <new_room> <person_name>
        """
        pass

    @docopt_cmd
    def do_load_people(self, args):
        """
        Loads people into the Amity system from a text file.
        Usage: load_people <filename>
        """
        pass

    @docopt_cmd
    def do_print_allocations(self, args):
        """
        Prints and outputs the people who have been successfully allocated a space per room.
        Usage: print_allocations <room_type>[--o=filename]
        """
        pass

    @docopt_cmd
    def do_print_unallocated(self, args):
        """
        Prints and outputs the people who have been not yet been allocated a room.
        Usage: print_unallocated <room_type> <room_name>[--o=filename]
        """
        pass

    @docopt_cmd
    def do_print_room(self, args):
        """
        Prints the people who have been allocated the specified room.
        Usage: print_room <room_type> <room_name>
        """
        pass

    @docopt_cmd
    def do_save_state(self, args):
        """
        Saves the data to a SQLite database
        Usage: print_room <room_type> <room_name>
        """
        pass

    @docopt_cmd
    def do_load_state(self, args):
        """
        Loads the data to a SQLite database
        Usage: print_room <room_type> <room_name>
        """
        pass

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Till next time, Good Bye!')
        exit()


# opt = docopt(__doc__, sys.argv[1:])

if __name__ == '__main__':
    try:
        AmityApp().cmdloop()
    except KeyboardInterrupt:
        print ('Exiting Application')

# print(opt)
