from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.evtable import EvTable


class CmdPlace(MuxCommand):
    """
    Manage places within a room.

    Usage:
      +place/create <name>[=<description>]  - Create a new place
      +place/join <name>                     - Join a place
      +place/leave                           - Leave your current place
      +place/list                            - List all places in the room
      +place/who [<name>]                    - See who's at a place (or your current place)
      +place/desc <name>=<description>       - Set or change a place's description
      +place/delete <name>                   - Delete a place (staff only, or if you created it)
      +place                                 - Show your current place

    Places allow you to create sub-locations within a room where you can have
    private conversations using the 'tt' (table talk) command. Only people at
    the same place can hear table talk.

    Examples:
      +place/create Corner Table=A cozy corner table with comfortable chairs
      +place/join Corner Table
      +place/list
      +place/who
      +place/leave
    """

    key = "+place"
    aliases = ["place"]
    locks = "cmd:all()"
    help_category = "RP Commands"

    def func(self):
        """Execute the command."""
        caller = self.caller
        location = caller.location

        if not location:
            caller.msg("You need to be in a room to use place commands.")
            return

        # Initialize places dict on room if it doesn't exist
        if not hasattr(location.db, 'places') or location.db.places is None:
            location.db.places = {}

        # Parse the switch and arguments
        if not self.switches:
            # No switch - show current place
            self._show_current_place()
        elif "create" in self.switches:
            self._create_place()
        elif "join" in self.switches:
            self._join_place()
        elif "leave" in self.switches:
            self._leave_place()
        elif "list" in self.switches:
            self._list_places()
        elif "who" in self.switches:
            self._show_who()
        elif "desc" in self.switches or "describe" in self.switches:
            self._set_description()
        elif "delete" in self.switches or "remove" in self.switches:
            self._delete_place()
        else:
            caller.msg("Unknown switch. See 'help +place' for usage.")

    def _show_current_place(self):
        """Show the caller's current place."""
        caller = self.caller
        
        if not caller.db.place:
            caller.msg("You are not currently at any place.")
            caller.msg("Use '+place/list' to see available places or '+place/create <name>' to create one.")
            return

        place_name = caller.db.place
        location = caller.location
        place_info = location.db.places.get(place_name, {})
        
        msg = f"\n|wCurrent Place:|n {place_name}\n"
        
        if place_info.get('description'):
            msg += f"|wDescription:|n {place_info['description']}\n"
        
        # Show who else is at this place
        others = []
        for obj in location.contents:
            if hasattr(obj, 'has_account') and obj.has_account and obj.db.place == place_name and obj != caller:
                others.append(obj.name)
        
        if others:
            msg += f"|wOthers here:|n {', '.join(others)}"
        else:
            msg += "|wOthers here:|n (none)"
        
        caller.msg(msg)

    def _create_place(self):
        """Create a new place."""
        caller = self.caller
        location = caller.location

        if not self.args:
            caller.msg("You must specify a name for the place.")
            return

        # Parse name and optional description
        if '=' in self.args:
            place_name, description = self.args.split('=', 1)
            place_name = place_name.strip()
            description = description.strip()
        else:
            place_name = self.args.strip()
            description = ""

        if not place_name:
            caller.msg("You must specify a name for the place.")
            return

        # Check if place already exists
        if place_name in location.db.places:
            caller.msg(f"A place called '{place_name}' already exists here.")
            return

        # Create the place
        location.db.places[place_name] = {
            'description': description,
            'creator': caller.id,
            'created_at': caller.location.db.places.get('_timestamp', 0)
        }

        caller.msg(f"|gCreated place:|n {place_name}")
        if description:
            caller.msg(f"|gDescription:|n {description}")
        
        # Announce to room
        caller.location.msg_contents(
            f"{caller.name} has created a new place: {place_name}",
            exclude=[caller]
        )

    def _join_place(self):
        """Join a place."""
        caller = self.caller
        location = caller.location

        if not self.args:
            caller.msg("Which place do you want to join? Use '+place/list' to see available places.")
            return

        place_name = self.args.strip()

        # Check if place exists
        if place_name not in location.db.places:
            caller.msg(f"There is no place called '{place_name}' here.")
            caller.msg("Use '+place/list' to see available places.")
            return

        # Check if already at a place
        old_place = caller.db.place
        if old_place:
            if old_place == place_name:
                caller.msg(f"You're already at {place_name}.")
                return
            else:
                # Notify people at the old place
                for obj in location.contents:
                    if hasattr(obj, 'has_account') and obj.has_account and obj.db.place == old_place and obj != caller:
                        obj.msg(f"{caller.name} leaves {old_place}.")

        # Join the place
        caller.db.place = place_name
        caller.msg(f"|gYou join {place_name}.|n")

        # Notify people at the new place
        for obj in location.contents:
            if hasattr(obj, 'has_account') and obj.has_account and obj.db.place == place_name and obj != caller:
                obj.msg(f"{caller.name} joins {place_name}.")

    def _leave_place(self):
        """Leave the current place."""
        caller = self.caller
        location = caller.location

        if not caller.db.place:
            caller.msg("You're not at any place.")
            return

        place_name = caller.db.place

        # Notify others at the place
        for obj in location.contents:
            if hasattr(obj, 'has_account') and obj.has_account and obj.db.place == place_name and obj != caller:
                obj.msg(f"{caller.name} leaves {place_name}.")

        caller.db.place = None
        caller.msg(f"|gYou leave {place_name}.|n")

    def _list_places(self):
        """List all places in the room."""
        caller = self.caller
        location = caller.location

        if not location.db.places:
            caller.msg("There are no places in this room yet.")
            caller.msg("Use '+place/create <name>' to create one.")
            return

        # Create a formatted table
        table = EvTable(
            "|wPlace Name|n",
            "|wPeople|n",
            "|wDescription|n",
            border="cells",
            width=78
        )

        for place_name, place_info in sorted(location.db.places.items()):
            # Count people at this place
            people = []
            for obj in location.contents:
                if hasattr(obj, 'has_account') and obj.has_account and obj.db.place == place_name:
                    # Highlight the caller's name
                    if obj == caller:
                        people.append(f"|c{obj.name}|n")
                    else:
                        people.append(obj.name)

            people_str = ", ".join(people) if people else "|x(empty)|n"
            desc = place_info.get('description', '')
            
            # Truncate description if too long
            if len(desc) > 40:
                desc = desc[:37] + "..."

            table.add_row(place_name, people_str, desc or "|x(none)|n")

        caller.msg(f"\n|wPlaces in {location.name}:|n")
        caller.msg(str(table))
        caller.msg("\nUse '+place/join <name>' to join a place or '+place/who <name>' for details.")

    def _show_who(self):
        """Show who is at a place."""
        caller = self.caller
        location = caller.location

        # If no argument, show current place
        if not self.args:
            if not caller.db.place:
                caller.msg("You're not at any place. Specify a place name to see who's there.")
                return
            place_name = caller.db.place
        else:
            place_name = self.args.strip()

        # Check if place exists
        if place_name not in location.db.places:
            caller.msg(f"There is no place called '{place_name}' here.")
            return

        place_info = location.db.places[place_name]

        # Get people at this place
        people = []
        for obj in location.contents:
            if hasattr(obj, 'has_account') and obj.has_account and obj.db.place == place_name:
                people.append(obj)

        msg = f"\n|w{place_name}|n\n"
        msg += "-" * len(place_name) + "\n"
        
        if place_info.get('description'):
            msg += f"{place_info['description']}\n\n"

        if people:
            msg += f"|wPeople here ({len(people)}):|n\n"
            for person in people:
                if person == caller:
                    msg += f"  |c{person.name}|n (you)\n"
                else:
                    msg += f"  {person.name}\n"
        else:
            msg += "|wPeople here:|n (none)\n"

        caller.msg(msg)

    def _set_description(self):
        """Set or change a place's description."""
        caller = self.caller
        location = caller.location

        if '=' not in self.args:
            caller.msg("Usage: +place/desc <name>=<description>")
            return

        place_name, description = self.args.split('=', 1)
        place_name = place_name.strip()
        description = description.strip()

        if not place_name:
            caller.msg("You must specify a place name.")
            return

        if place_name not in location.db.places:
            caller.msg(f"There is no place called '{place_name}' here.")
            return

        # Check if they have permission (creator or staff)
        place_info = location.db.places[place_name]
        is_creator = place_info.get('creator') == caller.id
        is_staff = caller.check_permstring("builders")

        if not (is_creator or is_staff):
            caller.msg("You don't have permission to change this place's description.")
            return

        # Update description
        location.db.places[place_name]['description'] = description
        caller.msg(f"|gUpdated description for {place_name}.|n")

        # Notify people at the place
        for obj in location.contents:
            if hasattr(obj, 'has_account') and obj.has_account and obj.db.place == place_name and obj != caller:
                obj.msg(f"The description of {place_name} has been updated.")

    def _delete_place(self):
        """Delete a place."""
        caller = self.caller
        location = caller.location

        if not self.args:
            caller.msg("Which place do you want to delete?")
            return

        place_name = self.args.strip()

        if place_name not in location.db.places:
            caller.msg(f"There is no place called '{place_name}' here.")
            return

        # Check if they have permission (creator or staff)
        place_info = location.db.places[place_name]
        is_creator = place_info.get('creator') == caller.id
        is_staff = caller.check_permstring("builders")

        if not (is_creator or is_staff):
            caller.msg("You don't have permission to delete this place.")
            return

        # Check if anyone is at the place
        people_at_place = []
        for obj in location.contents:
            if hasattr(obj, 'has_account') and obj.has_account and obj.db.place == place_name:
                people_at_place.append(obj)

        # Remove people from the place
        for person in people_at_place:
            person.db.place = None
            person.msg(f"{place_name} has been removed. You are no longer at any place.")

        # Delete the place
        del location.db.places[place_name]
        caller.msg(f"|gDeleted place:|n {place_name}")

        # Announce to room
        location.msg_contents(
            f"{caller.name} has removed the place: {place_name}",
            exclude=[caller]
        )

