"""
Planet Typeclass

Planets for the Dune MUSH, representing worlds in the Imperium.
Planets have various attributes like habitability, population, industries, and political affiliations.

This module requires builder+ permission to create and manage Planets.
"""

from evennia.objects.objects import DefaultObject
from evennia.utils.ansi import ANSIString
from utils.text import process_special_characters


# Habitability types
HABITABILITY_TYPES = [
    "Uninhabitable",
    "Habitable",
    "Asteroid",
    "Terran"
]

# World types
WORLD_TYPES = [
    "Gas giant",
    "Rocky world",
    "Moon planetoid",
    "Ice Giant",
    "Toxic Atmosphere",
    "Furnace",
    "Volcanic",
    "Asteroid",
    "Ice Asteroid",
    "Mineral Rich Asteroid",
    "Alpine World",
    "Mineral World",
    "Frozen World",
    "Ocean World",
    "Arid World",
    "Forested World",
    "Tropical World",
    "Savanna World",
    "Mined-Out World",
    "Earth-Like"
]


class Planet(DefaultObject):
    """
    A planet in the Dune universe.
    
    Planets are worlds that can be affiliated with Houses, contain populations,
    and have various characteristics. Rooms can be set to be on specific planets
    to inherit planet-specific features.
    
    Attributes:
        habitability_type (str): Uninhabitable, Habitable, Asteroid, or Terran
        world_type (str): Type of planet (Gas giant, Rocky world, etc.)
        political_affiliation (obj): House that controls the planet
        military_power (str): Description of military capabilities
        population (int): Number of inhabitants
        lifestyle (str): General lifestyle on the planet
        industries (str): Industries present or what planet is known for
        planet_notes (str): General notes about the planet
        other_notes (str): Additional tangential notes
        star (str): Name of the star system
        houses (list): List of House objects present on the planet
        organizations (list): List of Organization objects present on the planet
    
    Only staff (builder+) can create and modify Planets.
    """
    
    def at_object_creation(self):
        """Called when the Planet is first created."""
        super().at_object_creation()
        
        # Basic planet characteristics
        self.db.habitability_type = "Habitable"
        self.db.world_type = "Earth-Like"
        self.db.star = ""  # Star system name
        
        # Political information
        self.db.political_affiliation = None  # House object
        
        # Population and society
        self.db.population = 0
        self.db.lifestyle = ""
        self.db.industries = ""
        
        # Military
        self.db.military_power = ""
        
        # Houses and organizations present
        self.db.houses = []  # List of House objects
        self.db.organizations = []  # List of Organization objects
        
        # Space management (domains and territory)
        self.db.total_spaces = 80  # Default for planets (30 for moons)
        self.db.space_allocations = {}  # {house_id: spaces_allocated}
        
        # Notes
        self.db.planet_notes = ""
        self.db.other_notes = ""
        
        # Set default locks
        self.locks.add("view:all();edit:perm(Builder);delete:perm(Admin)")
    
    def format_population(self):
        """
        Format population with commas for readability.
        
        Returns:
            str: Formatted population string
        """
        if self.db.population == 0:
            return "Unpopulated"
        return f"{self.db.population:,} inhabitants"
    
    def get_affiliation_name(self):
        """
        Get the name of the politically affiliated House.
        
        Returns:
            str: House name or "Independent"
        """
        if self.db.political_affiliation:
            return self.db.political_affiliation.key
        return "Independent"
    
    def add_house(self, house):
        """
        Add a House presence to the planet.
        
        Args:
            house: House object to add
            
        Returns:
            tuple: (success, message)
        """
        if house in self.db.houses:
            return False, f"{house.key} is already present on {self.key}."
        
        self.db.houses.append(house)
        return True, f"Added {house.key} to {self.key}."
    
    def remove_house(self, house):
        """
        Remove a House presence from the planet.
        
        Args:
            house: House object to remove
            
        Returns:
            tuple: (success, message)
        """
        if house not in self.db.houses:
            return False, f"{house.key} is not present on {self.key}."
        
        self.db.houses.remove(house)
        
        # If this was the politically affiliated house, clear that too
        if self.db.political_affiliation == house:
            self.db.political_affiliation = None
        
        return True, f"Removed {house.key} from {self.key}."
    
    def add_organization(self, organization):
        """
        Add an Organization presence to the planet.
        
        Args:
            organization: Organization object to add
            
        Returns:
            tuple: (success, message)
        """
        if organization in self.db.organizations:
            return False, f"{organization.key} is already present on {self.key}."
        
        self.db.organizations.append(organization)
        return True, f"Added {organization.key} to {self.key}."
    
    def remove_organization(self, organization):
        """
        Remove an Organization presence from the planet.
        
        Args:
            organization: Organization object to remove
            
        Returns:
            tuple: (success, message)
        """
        if organization not in self.db.organizations:
            return False, f"{organization.key} is not present on {self.key}."
        
        self.db.organizations.remove(organization)
        return True, f"Removed {organization.key} from {self.key}."
    
    def get_allocated_spaces(self):
        """
        Get the total number of allocated spaces on this planet.
        
        Returns:
            int: Total allocated spaces
        """
        if not hasattr(self.db, 'space_allocations') or not self.db.space_allocations:
            return 0
        return sum(self.db.space_allocations.values())
    
    def get_available_spaces(self):
        """
        Get the number of unallocated spaces remaining on this planet.
        
        Returns:
            int: Available spaces
        """
        total = self.db.total_spaces if hasattr(self.db, 'total_spaces') else 80
        allocated = self.get_allocated_spaces()
        return total - allocated
    
    def allocate_spaces(self, house, spaces):
        """
        Allocate spaces on this planet to a House.
        
        Args:
            house: House object
            spaces (int): Number of spaces to allocate
            
        Returns:
            tuple: (success, message)
        """
        if not hasattr(self.db, 'space_allocations'):
            self.db.space_allocations = {}
        
        try:
            spaces = int(spaces)
        except ValueError:
            return False, "Spaces must be a number."
        
        if spaces < 0:
            return False, "Spaces must be positive."
        
        available = self.get_available_spaces()
        current = self.db.space_allocations.get(house.id, 0)
        
        # If increasing allocation, check if enough spaces available
        if spaces > current:
            needed = spaces - current
            if needed > available:
                return False, f"Only {available} spaces available on {self.key}. House {house.key} currently has {current}."
        
        # Set allocation
        if spaces == 0:
            # Remove allocation if setting to 0
            if house.id in self.db.space_allocations:
                del self.db.space_allocations[house.id]
            # Remove from houses list if present
            if house in self.db.houses:
                self.db.houses.remove(house)
            return True, f"Removed {house.key}'s space allocation on {self.key}."
        else:
            self.db.space_allocations[house.id] = spaces
            # Add to houses list if not present
            if house not in self.db.houses:
                self.db.houses.append(house)
            return True, f"Allocated {spaces} spaces on {self.key} to {house.key}."
    
    def deallocate_spaces(self, house):
        """
        Remove all space allocations for a House on this planet.
        
        Args:
            house: House object
            
        Returns:
            tuple: (success, message)
        """
        if not hasattr(self.db, 'space_allocations'):
            self.db.space_allocations = {}
        
        if house.id not in self.db.space_allocations:
            return False, f"{house.key} has no space allocations on {self.key}."
        
        spaces = self.db.space_allocations[house.id]
        del self.db.space_allocations[house.id]
        
        # Remove from houses list if present
        if house in self.db.houses:
            self.db.houses.remove(house)
        
        return True, f"Removed {house.key}'s {spaces} space allocation from {self.key}."
    
    def get_house_spaces(self, house):
        """
        Get the number of spaces allocated to a specific House.
        
        Args:
            house: House object
            
        Returns:
            int: Spaces allocated to this House
        """
        if not hasattr(self.db, 'space_allocations'):
            return 0
        return self.db.space_allocations.get(house.id, 0)
    
    def get_display(self):
        """
        Get a formatted display of the Planet information.
        
        Returns:
            str: Formatted Planet information (green-themed)
        """
        output = []
        
        # Header with planet name
        output.append("|g" + "=" * 80 + "|n")
        output.append("")
        output.append("|g" + f"{self.key.upper()}".center(80) + "|n")
        
        # Star system name
        if self.db.star:
            output.append("|g" + f"{self.db.star.upper()}".center(80) + "|n")
        
        output.append("")
        output.append("|g" + "=" * 80 + "|n")
        
        # Basic characteristics line
        affiliation = self.get_affiliation_name()
        output.append(f"|wHabitability:|n {self.db.habitability_type}     "
                     f"|wType:|n {self.db.world_type}    "
                     f"|wAffiliation:|n {affiliation}")
        
        output.append("|g" + "-" * 80 + "|n")
        
        # Population
        output.append(f"\n|wPopulation:|n       {self.format_population()}")
        
        # Industries
        if self.db.industries:
            output.append(f"|wIndustries:|n       {self.db.industries}")
        
        # Military Power
        if self.db.military_power:
            output.append(f"|wMilitary Power:|n   {self.db.military_power}")
        
        # Space allocation
        if hasattr(self.db, 'total_spaces'):
            allocated = self.get_allocated_spaces()
            available = self.get_available_spaces()
            output.append(f"\n|wSpaces:|n           {allocated}/{self.db.total_spaces} allocated ({available} available)")
        
        # Houses present with space allocations
        if self.db.houses or (hasattr(self.db, 'space_allocations') and self.db.space_allocations):
            output.append(f"\n|wHouses Present:|n")
            
            # If we have space allocations, show detailed breakdown
            if hasattr(self.db, 'space_allocations') and self.db.space_allocations:
                from evennia import ObjectDB
                for house_id, spaces in sorted(self.db.space_allocations.items(), key=lambda x: x[1], reverse=True):
                    try:
                        house = ObjectDB.objects.get(id=house_id)
                        output.append(f"  |c{house.key}|n - {spaces} spaces")
                    except ObjectDB.DoesNotExist:
                        # House no longer exists, clean up
                        del self.db.space_allocations[house_id]
            elif self.db.houses:
                # Fallback: just list houses without space info
                house_names = ", ".join([h.key for h in self.db.houses])
                output.append(f"  {house_names}")
        
        # Organizations present
        if self.db.organizations:
            org_names = ", ".join([o.key for o in self.db.organizations])
            output.append(f"\n|wOrganizations:|n    {org_names}")
        
        output.append("\n|g" + "-" * 80 + "|n")
        
        # Planet Notes
        output.append("\n|wPlanet Notes:|n")
        if self.db.planet_notes:
            # Process special characters and word wrap the notes to 80 characters
            notes = process_special_characters(self.db.planet_notes)
            output.append(self._wrap_text(notes, 80))
        else:
            output.append("None")
        
        # Other Notes
        output.append("\n\n|wOther Notes:|n")
        if self.db.other_notes:
            # Process special characters and word wrap the notes
            notes = process_special_characters(self.db.other_notes)
            output.append(self._wrap_text(notes, 80))
        else:
            output.append("None")
        
        output.append("\n|g" + "=" * 80 + "|n")
        
        return "\n".join(output)
    
    def _wrap_text(self, text, width):
        """
        Wrap text to specified width while preserving paragraphs.
        
        Args:
            text (str): Text to wrap
            width (int): Maximum line width
            
        Returns:
            str: Wrapped text
        """
        import textwrap
        
        # Split by paragraphs (double newline)
        paragraphs = text.split('\n\n')
        wrapped_paragraphs = []
        
        for para in paragraphs:
            # Replace single newlines with spaces within a paragraph
            para = para.replace('\n', ' ')
            # Wrap the paragraph
            wrapped = textwrap.fill(para, width=width)
            wrapped_paragraphs.append(wrapped)
        
        return '\n\n'.join(wrapped_paragraphs)

