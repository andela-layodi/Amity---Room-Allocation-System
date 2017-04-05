# Amity---Room-Allocation-System
*AMity* is a room allocation application written in the Python language.

### Features
* Allows the user to create room, either a living space or an office .
* Enables the user to add a person who is automatically allocated to a room.
* The user is able to reallocate a person to a room of their choice.
* The user can add people through a text file.
* The user  is able to print out information such as allocated people and can output it to a text file.
* Allows the user to save and retrieve records from a database.
* Easy to user interface to interact with.

### Dependencies | Requirements
### Dependencies | Requirements
* appdirs (1.4.3)
* appnope (0.1.0)
* autopep8 (1.3.1)
* codacy-coverage (1.3.6)
* coverage (4.3.4)
* decorator (4.0.11)
* docopt (0.6.2)
* flake8 (3.3.0)
* ipdb (0.10.2)
* ipython (5.3.0)
* ipython-genutils (0.2.0)
* mccabe (0.6.1)
* nose (1.3.7)
* packaging (16.8)
* pdb (0.1)
* pep8 (1.7.0)
* pexpect (4.2.1)
* pickleshare (0.7.4)
* pip (9.0.1)
* prompt-toolkit (1.0.13)
* ptyprocess (0.5.1)
* pycodestyle (2.3.1)
* pyfiglet (0.7.5)
* pyflakes (1.5.0)
* Pygments (2.2.0)
* pyparsing (2.2.0)
* python-gnupg (0.4.0)
* PyYAML (3.12)
* requests (2.13.0)
* setuptools (34.3.2)
* simplegeneric (0.8.1)
* six (1.10.0)
* SQLAlchemy (1.1.6)
* termcolor (1.1.0)
* titlecase (0.9.0)
* traitlets (4.3.2)
* wcwidth (0.1.7)

#### To install all requirements, download the [requirements.txt] (https://github.com/andela-layodi/bc-14--ToDo-Console-Application-/blob/master/Desktop/todo_console/requirements.txt) file then type this in your terminal application:
             pip install -r /path/to/requirements.txt



### Commands

|Command| Description|
|-----|---------------------------------------------------------|
| create_room <room_name> <room_type> | Create a room. |
| add_person <first_name> <second_name> <person_type> [--Y] | Adds a person. |
| reallocate_person <first_name> <second_name> <new_room> | Reallocates a person to a new room. |
| load_people <filename> | Loads people from a text file. |
| print_allocations <filename> | Output the rooms with the people who have been allocated. |
| print_unallocated <filename> | Output the people who are yet to be allocated a room. |
| print_room <room_name> | Output the occupants of the specified room |
| save_state <db_name> | Save records to a database for future reference. |
| load_state <db_name> | Load records from a database. |


### Contact Information
Find the author at [@andela-layodi] (https://github.com/andela-layodi) on github.
