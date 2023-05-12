#!/usr/bin/python3
"""Defines a command line interpreter."""

import cmd
import re
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """HBNBCommand is a command line interpreter"""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Exits the program."""
        print()
        return True

    def emptyline(self):
        """Does nothing."""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it, and prints the id."""
        if arg:
            try:
                base = eval(arg.split()[0])()
                base.save()
                print(base.id)
            except NameError:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, arg):
        """Prints the string representation of an instance based
        on the class name and id."""
        self.check_args(arg, self.printing)

    def do_destroy(self, arg):
        """Delete a BaseModel instance"""
        self.check_args(arg, self.delete_arg)

    def do_all(self, arg):
        """Prints all the BaseModel instance created"""
        all_d = storage.all()
        if arg:
            try:
                base = eval(arg.split()[0])()
                if isinstance(base, BaseModel):
                    for k, v in all_d.items():
                        if k.split(".")[0] == arg.split()[0]:
                            print(v)
                else:
                    print("** class doesn't exist **")
            except NameError:
                print("** class doesn't exist **")
        else:
            [print(v) for k, v in all_d.items()]

    def do_update(self, arg):
        """Updates a BaseModel instance object, adds new or update attribute
        e.g update <class_name> <class_id> <key> <value>"""
        obj = self.check_args(arg, self.get_object)
        if obj:
            # update the value of object
            self.run_update(obj, arg)

    @staticmethod
    def run_update(obj, arg):
        """Updates the value of a given object using the regex to get
        the values and keys"""
        # parse simple words, "complex", "more complex", number, float
        u = \
            '([0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})'
        args = re.findall(
            rf'((\d+(\.\d*))|{u}|\w.*?\b|\".*\s*?.*\")',
            arg)
        try:
            # parsed args contains extra space on the end
            key = args[2][0].split()[0]
        except IndexError:
            print("** attribute name missing **")
            return
        try:
            value = args[3][0]
            # test if it's a double string
            if len(value.split('"')) > 1:
                # "double strings" fails on eval
                value = value.split('"')[1]
            else:
                value = HBNBCommand.valtype(value)(value)
            setattr(obj, key, value)
            obj.save()
        except IndexError:
            print("** value missing **")

    @staticmethod
    def valtype(arg):
        """Get and return the type of a value to update"""
        try:
            return type(eval(arg))
        except (NameError, TypeError):
            return str

    @staticmethod
    def get_object(arg):
        """retrieves the object to update"""
        return (storage.all()[f"{arg[0]}.{arg[1]}"])

    @staticmethod
    def printing(arg):
        """prints a given object"""
        print(storage.all()[f"{arg[0]}.{arg[1]}"])

    @staticmethod
    def delete_arg(arg):
        """deletes an object and update storage"""
        del storage.all()[f"{arg[0]}.{arg[1]}"]
        storage.save()

    @staticmethod
    def check_args(arg, func):
        """parses and checks the needed argument to a function"""
        arg = arg.split()
        arg_len = len(arg)
        if arg_len < 1:
            print("** class name missing **")
            return
        try:
            base = eval(arg[0])()
            if isinstance(base, BaseModel):
                if arg_len < 2:
                    print("** instance id missing **")
                    return
                try:
                    return (func(arg))
                except KeyError:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")
        except (TypeError, NameError):
            print("** class doesn't exist **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
