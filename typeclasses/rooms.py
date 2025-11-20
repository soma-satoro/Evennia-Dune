"""
Room

Rooms are simple containers that has no location of their own.
Room typeclass with formatted displays for the Dune MUSH game.
"""

from evennia.objects.objects import DefaultRoom
from evennia.utils import utils, evtable
from evennia.utils.ansi import ANSIString
from evennia.server.models import ServerConfig
import time

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms with custom formatting for Dune MUSH.
    
    Features:
    - Formatted room headers with location hierarchy
    - Character display with idle times and shortdesc
    - Separated directions (cardinal) from other exits
    - Places system integration
    - IC Area mapping integration
    
    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        """
        Called once when the room is first created.
        Set up default attributes for the room display.
        """
        super().at_object_creation()
        
        # Default attributes for room display
        self.db.area_name = "Unknown Area"
        self.db.area_code = "XX00"
        self.db.location_hierarchy = ["Unknown Planet", "Unknown Region"]
        self.db.places_active = False
        
    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.
        
        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
            
        # Build the formatted room display
        appearance_parts = []
        
        # Header
        header = self.get_display_header(looker)
        if header:
            appearance_parts.append(header)
            
        # Description
        desc = self.get_display_desc(looker)
        if desc:
            appearance_parts.append(desc)
            
        # Places section
        places = self.get_display_places(looker)
        if places:
            appearance_parts.append(places)
            
        # Characters section
        characters = self.get_display_characters(looker)
        if characters:
            appearance_parts.append(characters)
            
        # Directions section
        directions = self.get_display_directions(looker)
        if directions:
            appearance_parts.append(directions)
            
        # Exits section
        exits = self.get_display_exits(looker)
        if exits:
            appearance_parts.append(exits)
            
        # Footer
        footer = self.get_display_footer(looker)
        if footer:
            appearance_parts.append(footer)
            
        return "\n".join(appearance_parts)

    def get_theme_colors(self):
        """Get theme colors from server config or defaults."""
        theme_colors = ServerConfig.objects.conf("ROOM_THEME_COLORS")
        if theme_colors:
            colors = theme_colors.split(",")
            if len(colors) >= 3:
                return colors[0], colors[1], colors[2]
        # Default colors (amber/orange for Dune desert theme)
        return 'y', 'y', 'y'
    
    def get_display_header(self, looker, **kwargs):
        """
        Get the formatted header for the room display.
        
        Format: ===> Room Name - Area1 - Area2 <===
        """
        # Get theme colors
        header_color, text_color, divider_color = self.get_theme_colors()
        
        room_name = self.get_display_name(looker)
        hierarchy = self.db.location_hierarchy or ["Unknown Planet", "Unknown Region"]
        
        # Convert _SaverList to regular list if needed
        if hasattr(hierarchy, '__iter__') and not isinstance(hierarchy, (str, bytes)):
            hierarchy = list(hierarchy)
        
        # Ensure we have exactly 2 hierarchy items
        if len(hierarchy) < 2:
            hierarchy = hierarchy + ["Unknown"] * (2 - len(hierarchy))
        elif len(hierarchy) > 2:
            hierarchy = hierarchy[:2]
        
        # Build the location string
        location_string = " - ".join([room_name] + hierarchy)
        
        # Create the header with proper centering and theme colors
        header_content = f" {location_string} "
        total_width = 80
        equals_per_side = (total_width - len(header_content) - 4) // 2  # -4 for the arrows
        
        header = f"|{header_color}" + "=" * equals_per_side + ">" + f"|{text_color}" + header_content + f"|{header_color}" + "<" + "=" * equals_per_side + "|n"
        
        return header

    def get_display_desc(self, looker, **kwargs):
        """
        Get the room description with proper formatting.
        """
        desc = self.db.desc
        if not desc:
            return ""
            
        # Process special characters
        desc = desc.replace('%r%r', '\n\n').replace('%r', '\n').replace('%t', '     ')
            
        # Format description with proper indentation and spacing
        formatted_desc = "\n\n"
        
        # Split into paragraphs and add proper spacing
        paragraphs = desc.split('\n\n')
        for i, paragraph in enumerate(paragraphs):
            # Clean up the paragraph and add tab indentation
            clean_paragraph = ' '.join(paragraph.split())
            formatted_desc += f"\t{clean_paragraph}\n"
            if i < len(paragraphs) - 1:  # Add spacing between paragraphs
                formatted_desc += "\n"
                
        return formatted_desc

    def get_display_places(self, looker, **kwargs):
        """
        Get the places section display.
        """
        if not self.db.places_active:
            return ""
            
        # Check if there are any places defined
        places = getattr(self.db, 'places', {})
        if not places:
            return ""
            
        places_text = "\n"
        places_text += " " * 12 + "Places are active here. Use plook and plook # to see descriptions." + " " * 12
        places_text += "\n"
        
        return places_text

    def get_display_characters(self, looker, **kwargs):
        """
        Get the characters section with idle times and shortdesc.
        
        Format: Name                     IdleTime Description
        """
        # Get all characters in the room (including the looker)
        characters = [obj for obj in self.contents if obj.has_account]
        
        if not characters:
            return ""
            
        # Get theme colors
        header_color, text_color, divider_color = self.get_theme_colors()
        
        char_lines = []
        char_lines.append(f"|{divider_color}----> Characters <" + "-" * 62 + "|n")
        
        # Display characters in two columns with dot leaders
        for i in range(0, len(characters), 2):
            left_char = characters[i]
            right_char = characters[i + 1] if i + 1 < len(characters) else None
            
            # Left column
            left_name = left_char.get_display_name(looker)
            left_idle = self.get_character_idle_time(left_char)
            # Create dot leader between name and idle time (total width 28 chars)
            left_dots = "." * (35 - len(left_name) - len(left_idle))
            left_text = f"{left_name}{left_dots}{left_idle}"
            
            # Right column (if exists)
            if right_char:
                right_name = right_char.get_display_name(looker)
                right_idle = self.get_character_idle_time(right_char)
                # Create dot leader between name and idle time (total width 28 chars)
                right_dots = "." * (35 - len(right_name) - len(right_idle))
                right_text = f"{right_name}{right_dots}{right_idle}"
            else:
                right_text = ""
            
            # Combine columns with proper spacing (left column is 39 chars total)
            line = f"{left_text:<39} {right_text}"
            char_lines.append(line.rstrip())
            
        return "\n" + "\n".join(char_lines)

    def get_character_idle_time(self, character):
        """
        Calculate and format the idle time for a character.
        
        Returns:
            str: Formatted idle time (e.g., "5m", "2h", "0s")
        """
        # Get the character's session
        sessions = character.sessions.all()
        if not sessions:
            return "?"
            
        # Get the most recent activity time
        last_activity = None
        for session in sessions:
            if hasattr(session, 'cmd_last') and session.cmd_last:
                if not last_activity or session.cmd_last > last_activity:
                    last_activity = session.cmd_last
                    
        if not last_activity:
            return "0s"
            
        # Calculate idle time
        idle_seconds = int(time.time() - last_activity)
        
        if idle_seconds < 60:
            return f"{idle_seconds}s"
        elif idle_seconds < 3600:
            return f"{idle_seconds // 60}m"
        else:
            return f"{idle_seconds // 3600}h"

    def get_display_directions(self, looker, **kwargs):
        """
        Get exits that are cardinal directions.
        
        Cardinal directions: north, south, east, west, northeast, northwest, southeast, southwest, up, down
        """
        cardinal_directions = {
            'north': 'N', 'south': 'S', 'east': 'E', 'west': 'W',
            'northeast': 'NE', 'northwest': 'NW', 'southeast': 'SE', 'southwest': 'SW',
            'up': 'U', 'down': 'D', 'n': 'N', 's': 'S', 'e': 'E', 'w': 'W',
            'ne': 'NE', 'nw': 'NW', 'se': 'SE', 'sw': 'SW', 'u': 'U', 'd': 'D'
        }
        
        directions = []
        
        # Get all exits and filter for cardinal directions
        for exit_obj in self.exits:
            exit_name = exit_obj.key.lower()
            exit_aliases = [alias.lower() for alias in exit_obj.aliases.all()]
            
            # Check if this exit is a cardinal direction
            is_cardinal = False
            matched_abbrev = None
            
            # First check if any of the exit's aliases match a cardinal direction
            for alias in exit_aliases:
                if alias in cardinal_directions:
                    is_cardinal = True
                    matched_abbrev = cardinal_directions[alias]
                    break
            
            # If no alias matched, check if the exit name exactly matches a cardinal direction
            if not is_cardinal and exit_name in cardinal_directions:
                is_cardinal = True
                matched_abbrev = cardinal_directions[exit_name]
            
            if is_cardinal:
                # Get the destination name
                dest_name = "Unknown"
                if exit_obj.destination:
                    dest_name = exit_obj.destination.get_display_name(looker)
                
                directions.append(f"{dest_name} <{matched_abbrev}>")
                    
        if not directions:
            return ""
            
        # Get theme colors
        header_color, text_color, divider_color = self.get_theme_colors()
        
        # Format directions section
        dir_lines = []
        dir_lines.append(f"|{divider_color}----> Directions <" + "-" * 62 + "|n")
        
        # Display directions in groups of 3 per line
        for i in range(0, len(directions), 3):
            line_dirs = directions[i:i+3]
            formatted_dirs = []
            for direction in line_dirs:
                formatted_dirs.append(f"{direction:<30}")
            dir_lines.append("".join(formatted_dirs).rstrip())
            
        return "\n" + "\n".join(dir_lines)

    def get_display_exits(self, looker, **kwargs):
        """
        Get exits that are NOT cardinal directions.
        """
        cardinal_directions = {
            'north', 'south', 'east', 'west', 'northeast', 'northwest', 
            'southeast', 'southwest', 'up', 'down', 'n', 's', 'e', 'w',
            'ne', 'nw', 'se', 'sw', 'u', 'd'
        }
        
        other_exits = []
        
        # Get all exits and filter for non-cardinal directions
        for exit_obj in self.exits:
            exit_name = exit_obj.key.lower()
            exit_aliases = [alias.lower() for alias in exit_obj.aliases.all()]
            
            # Check if this exit is NOT a cardinal direction
            is_cardinal = False
            
            # First check if any of the exit's aliases match a cardinal direction
            for alias in exit_aliases:
                if alias in cardinal_directions:
                    is_cardinal = True
                    break
            
            # If no alias matched, check if the exit name exactly matches a cardinal direction
            if not is_cardinal and exit_name in cardinal_directions:
                is_cardinal = True
                    
            if not is_cardinal:
                # Get the exit display (usually just the key, but could include aliases)
                exit_display = exit_obj.key
                if exit_obj.aliases.all():
                    # Show primary alias in brackets
                    exit_display += f" <{exit_obj.aliases.all()[0]}>"
                other_exits.append(exit_display)
                
        if not other_exits:
            return ""
            
        # Get theme colors
        header_color, text_color, divider_color = self.get_theme_colors()
        
        # Format exits section
        exit_lines = []
        exit_lines.append(f"|{divider_color}----> Exits <" + "-" * 67 + "|n")
        
        # Display exits in groups of 3 per line
        for i in range(0, len(other_exits), 3):
            line_exits = other_exits[i:i+3]
            formatted_exits = []
            for exit in line_exits:
                formatted_exits.append(f"{exit:<30}")
            exit_lines.append("".join(formatted_exits).rstrip())
            
        return "\n" + "\n".join(exit_lines)

    def get_display_footer(self, looker, **kwargs):
        """
        Get the footer with IC Area information.
        
        Format: ======> IC Area - AREACODE <====
        """
        # Get theme colors
        header_color, text_color, divider_color = self.get_theme_colors()
        
        area_name = self.db.area_name or "Unknown Area"
        area_code = self.db.area_code or "XX00"
        
        footer_content = f" IC Area - {area_code} "
        total_width = 80
        equals_per_side = (total_width - len(footer_content) - 4) // 2  # -4 for the arrows
        
        footer = f"|{header_color}" + "=" * equals_per_side + ">" + f"|{text_color}" + footer_content + f"|{header_color}" + "<" + "=" * equals_per_side + "|n"
        
        return "\n" + footer

    def set_area_info(self, area_name, area_code, location_hierarchy=None):
        """
        Convenience method to set area information for the room.
        
        Args:
            area_name (str): The name of the IC area
            area_code (str): The area code (e.g., "AR01")
            location_hierarchy (list): List of location names for the header
        """
        self.db.area_name = area_name
        self.db.area_code = area_code
        if location_hierarchy:
            self.db.location_hierarchy = list(location_hierarchy)

    def set_places_active(self, active=True):
        """
        Enable or disable the places system display for this room.
        
        Args:
            active (bool): Whether places should be shown
        """
        self.db.places_active = active

    def add_place(self, place_name, place_desc, place_number=None):
        """
        Add a place to this room's places system.
        
        Args:
            place_name (str): Name of the place
            place_desc (str): Description of the place
            place_number (int): Optional specific number for the place
        """
        if not hasattr(self.db, 'places') or not self.db.places:
            self.db.places = {}
            
        if place_number is None:
            # Find the next available number
            existing_numbers = [int(k) for k in self.db.places.keys() if k.isdigit()]
            place_number = max(existing_numbers, default=0) + 1
        
        # Process special characters in the place description
        processed_desc = place_desc.replace('%r%r', '\n\n').replace('%r', '\n').replace('%t', '     ')
            
        self.db.places[str(place_number)] = {
            'name': place_name,
            'desc': processed_desc
        }
        
        return place_number
