"""
Room Management Commands

Commands for building and managing rooms in the Dune MUSH.
All commands require builder+ permission.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia import search_object
from evennia.utils.utils import inherits_from


class CmdRoom(MuxCommand):
    """
    Manage room properties and associations.

    Usage:
        +room | +room <room dbref>
        +room/planet here=<planet> | +room/planet <room>=<planet> | +room/planet here=
        +room/location here=<location> | +room/loc here=<location> | +room/location <room>=<location>
        +room/area here=<name>/<code> | +room/area <room>=<name>/<code>
        +room/hierarchy here=<loc>,<planet> | +room/hierarchy <room>=<loc>,<planet>
        +room/places here | +room/places <room>

    Examples:
        +room | +room #123 | +room/planet here=Vallabhi | +room/location here=Kyotashi
        +room/area here=Palace District/PD01 | +room/hierarchy here=Kyotashi,Vallabhi | +room/places here

    Notes: /planet associates room with planet (updates location hierarchy). /location sets planetary location (city, district, region) shown in room header. Room header format: Room Name - Location - Planet (e.g., "Nagara Square - Kyotashi - Vallabhi"). /area sets IC area name and code in footer. /hierarchy sets full location hierarchy manually (format: location,planet). /places toggles places system display.

    Staff Only: All commands require Builder permission or higher.
    """
    
    key = "+room"
    aliases = ["room"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Main command dispatcher"""
        
        # Route to appropriate handler
        if "planet" in self.switches:
            self.set_planet()
        elif "location" in self.switches or "loc" in self.switches:
            self.set_location()
        elif "area" in self.switches:
            self.set_area()
        elif "hierarchy" in self.switches:
            self.set_hierarchy()
        elif "places" in self.switches:
            self.toggle_places()
        elif not self.switches:
            # No switches - view room info
            self.view_room()
        else:
            self.caller.msg("Invalid switch. See 'help +room' for available options.")
    
    def view_room(self):
        """View room information."""
        # Determine which room to view
        if self.args:
            # Try to find the room by dbref or name
            room = self.caller.search(self.args.strip(), global_search=True)
            if not room:
                return
        else:
            # Use current location
            room = self.caller.location
            if not room:
                self.caller.msg("You are not in a room.")
                return
        
        # Check if it's actually a room
        if not inherits_from(room, "typeclasses.rooms.Room"):
            self.caller.msg(f"{room.key} is not a room.")
            return
        
        # Build room info display
        output = []
        output.append("|c" + "=" * 78 + "|n")
        output.append("|c" + f" Room Information: {room.key} ".center(78, "=") + "|n")
        output.append("|c" + "=" * 78 + "|n")
        
        output.append(f"\n|wRoom Name:|n {room.key}")
        output.append(f"|wDB Reference:|n #{room.id}")
        
        # Planet association
        planet = room.db.planet
        if planet:
            output.append(f"|wPlanet:|n {planet.key}")
        else:
            output.append(f"|wPlanet:|n Not set")
        
        # Area information
        area_name = room.db.area_name or "Not set"
        area_code = room.db.area_code or "Not set"
        output.append(f"|wArea Name:|n {area_name}")
        output.append(f"|wArea Code:|n {area_code}")
        
        # Location hierarchy
        hierarchy = room.db.location_hierarchy
        if hierarchy:
            hierarchy_str = " > ".join(hierarchy)
            output.append(f"|wLocation Hierarchy:|n {hierarchy_str}")
        else:
            output.append(f"|wLocation Hierarchy:|n Not set")
        
        # Places system
        places_active = room.db.places_active
        output.append(f"|wPlaces System:|n {'Active' if places_active else 'Inactive'}")
        
        # Description
        if room.db.desc:
            output.append(f"\n|wDescription:|n")
            output.append(room.db.desc)
        
        output.append("\n|c" + "=" * 78 + "|n")
        
        self.caller.msg("\n".join(output))
    
    def set_planet(self):
        """Associate a room with a planet."""
        if "=" not in self.args:
            self.caller.msg("Usage: +room/planet <here|room>=<planet name>")
            self.caller.msg("Leave planet name empty to clear: +room/planet here=")
            return
        
        # Parse room target and planet name
        room_target, planet_name = self.args.split("=", 1)
        room_target = room_target.strip()
        planet_name = planet_name.strip()
        
        # Determine which room to modify
        if room_target.lower() == "here":
            room = self.caller.location
            if not room:
                self.caller.msg("You are not in a room.")
                return
        else:
            # Search for the room
            room = self.caller.search(room_target, global_search=True)
            if not room:
                return
        
        # Check if it's actually a room
        if not inherits_from(room, "typeclasses.rooms.Room"):
            self.caller.msg(f"{room.key} is not a room.")
            return
        
        # If planet_name is empty, clear the planet association
        if not planet_name:
            room.db.planet = None
            self.caller.msg(f"Cleared planet association for {room.key}.")
            return
        
        # Search for the planet
        planets = search_object(planet_name, typeclass="typeclasses.planets.Planet")
        if not planets:
            self.caller.msg(f"No planet found with the name '{planet_name}'.")
            self.caller.msg("Use +planet/list to see available planets.")
            return
        
        if len(planets) > 1:
            self.caller.msg(f"Multiple planets found: {', '.join([p.key for p in planets])}")
            self.caller.msg("Please be more specific.")
            return
        
        planet = planets[0]
        
        # Associate the room with the planet
        room.db.planet = planet
        
        # Update the location hierarchy - planet is the SECOND element
        # Hierarchy is [Location, Planet]
        current_hierarchy = room.db.location_hierarchy or ["Unknown Location", "Unknown Planet"]
        if len(current_hierarchy) >= 2:
            # Keep the location (first element), update planet (second element)
            room.db.location_hierarchy = [current_hierarchy[0], planet.key]
        else:
            # If hierarchy is malformed, set it properly
            location = current_hierarchy[0] if current_hierarchy else "Unknown Location"
            room.db.location_hierarchy = [location, planet.key]
        
        self.caller.msg(f"Associated {room.key} with planet {planet.key}.")
        self.caller.msg(f"Updated location hierarchy to: {room.key} - {' - '.join(room.db.location_hierarchy)}")
    
    def set_location(self):
        """Set planetary location (city, region, etc) for a room."""
        if "=" not in self.args:
            self.caller.msg("Usage: +room/location <here|room>=<location name>")
            self.caller.msg("Example: +room/location here=Kyotashi")
            return
        
        # Parse room target and location name
        room_target, location_name = self.args.split("=", 1)
        room_target = room_target.strip()
        location_name = location_name.strip()
        
        # Determine which room to modify
        if room_target.lower() == "here":
            room = self.caller.location
            if not room:
                self.caller.msg("You are not in a room.")
                return
        else:
            # Search for the room
            room = self.caller.search(room_target, global_search=True)
            if not room:
                return
        
        # Check if it's actually a room
        if not inherits_from(room, "typeclasses.rooms.Room"):
            self.caller.msg(f"{room.key} is not a room.")
            return
        
        # Update the location hierarchy - location is the FIRST element
        # Hierarchy is [Location, Planet]
        current_hierarchy = room.db.location_hierarchy or ["Unknown Location", "Unknown Planet"]
        if len(current_hierarchy) >= 2:
            # Update location (first element), keep planet (second element)
            room.db.location_hierarchy = [location_name, current_hierarchy[1]]
        else:
            # If hierarchy is malformed, set it properly
            planet = current_hierarchy[1] if len(current_hierarchy) > 1 else "Unknown Planet"
            room.db.location_hierarchy = [location_name, planet]
        
        self.caller.msg(f"Set location for {room.key} to: {location_name}")
        self.caller.msg(f"Location hierarchy: {room.key} - {' - '.join(room.db.location_hierarchy)}")
    
    def set_area(self):
        """Set area name and code for a room."""
        if "=" not in self.args or "/" not in self.args:
            self.caller.msg("Usage: +room/area <here|room>=<area name>/<area code>")
            self.caller.msg("Example: +room/area here=Palace District/PD01")
            return
        
        # Parse room target and area info
        room_target, area_info = self.args.split("=", 1)
        room_target = room_target.strip()
        
        if "/" not in area_info:
            self.caller.msg("Area info must be in format: <area name>/<area code>")
            return
        
        area_name, area_code = area_info.split("/", 1)
        area_name = area_name.strip()
        area_code = area_code.strip()
        
        # Determine which room to modify
        if room_target.lower() == "here":
            room = self.caller.location
            if not room:
                self.caller.msg("You are not in a room.")
                return
        else:
            # Search for the room
            room = self.caller.search(room_target, global_search=True)
            if not room:
                return
        
        # Check if it's actually a room
        if not inherits_from(room, "typeclasses.rooms.Room"):
            self.caller.msg(f"{room.key} is not a room.")
            return
        
        # Set the area information
        room.db.area_name = area_name
        room.db.area_code = area_code
        
        self.caller.msg(f"Set area for {room.key}:")
        self.caller.msg(f"  Area Name: {area_name}")
        self.caller.msg(f"  Area Code: {area_code}")
    
    def set_hierarchy(self):
        """Set location hierarchy for a room."""
        if "=" not in self.args:
            self.caller.msg("Usage: +room/hierarchy <here|room>=<location>,<planet>")
            self.caller.msg("Example: +room/hierarchy here=Kyotashi,Vallabhi")
            return
        
        # Parse room target and hierarchy
        room_target, hierarchy_str = self.args.split("=", 1)
        room_target = room_target.strip()
        hierarchy_str = hierarchy_str.strip()
        
        # Parse hierarchy (comma-separated)
        hierarchy = [h.strip() for h in hierarchy_str.split(",")]
        
        if len(hierarchy) < 2:
            self.caller.msg("Hierarchy should have 2 levels (location, planet).")
            self.caller.msg("Example: Kyotashi,Vallabhi")
            return
        
        # Use only the first 2 levels
        if len(hierarchy) > 2:
            self.caller.msg(f"Note: Only using first 2 levels: {hierarchy[0]}, {hierarchy[1]}")
            hierarchy = hierarchy[:2]
        
        # Determine which room to modify
        if room_target.lower() == "here":
            room = self.caller.location
            if not room:
                self.caller.msg("You are not in a room.")
                return
        else:
            # Search for the room
            room = self.caller.search(room_target, global_search=True)
            if not room:
                return
        
        # Check if it's actually a room
        if not inherits_from(room, "typeclasses.rooms.Room"):
            self.caller.msg(f"{room.key} is not a room.")
            return
        
        # Set the location hierarchy [Location, Planet]
        room.db.location_hierarchy = hierarchy
        
        self.caller.msg(f"Set location hierarchy for {room.key}:")
        self.caller.msg(f"  {room.key} - {' - '.join(hierarchy)}")
    
    def toggle_places(self):
        """Toggle places system for a room."""
        # Determine which room to modify
        if self.args:
            room_target = self.args.strip()
            if room_target.lower() == "here":
                room = self.caller.location
                if not room:
                    self.caller.msg("You are not in a room.")
                    return
            else:
                # Search for the room
                room = self.caller.search(room_target, global_search=True)
                if not room:
                    return
        else:
            # Use current location
            room = self.caller.location
            if not room:
                self.caller.msg("You are not in a room.")
                return
        
        # Check if it's actually a room
        if not inherits_from(room, "typeclasses.rooms.Room"):
            self.caller.msg(f"{room.key} is not a room.")
            return
        
        # Toggle places
        current_state = room.db.places_active or False
        new_state = not current_state
        room.db.places_active = new_state
        
        self.caller.msg(f"Places system for {room.key}: {'Active' if new_state else 'Inactive'}")

