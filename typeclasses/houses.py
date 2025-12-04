"""
House Typeclass

Noble Houses for the Dune MUSH, implementing the Modiphius 2d20 system.
Houses are organizations that player characters serve.

This module requires builder+ permission to create and manage Houses.
"""

from evennia.objects.objects import DefaultObject
from evennia.utils.ansi import ANSIString


# Domain areas of expertise and their subtypes
DOMAIN_AREAS = {
    "Artistic": {
        "Machinery": ["Stage effects", "Scenery pieces", "Scenic art", "Lighting and sound systems"],
        "Produce": ["Plays", "Poems", "Novels", "Comedy sketches", "Musical pieces"],
        "Expertise": ["Playwrights", "Poets", "Composers", "Directors"],
        "Workers": ["Actors", "Stage crew", "Musicians", "Speakers", "Traveling companies"],
        "Understanding": ["Philosophy", "Literary criticism", "Theatrical performance styles"]
    },
    "Espionage": {
        "Machinery": ["Surveillance devices", "Sensors", "Jamming technology"],
        "Produce": ["Information and secrets from other Houses"],
        "Expertise": ["Spymasters", "Agent handlers"],
        "Workers": ["Agents", "Spies", "Infiltrators"],
        "Understanding": ["Espionage techniques", "Counterintelligence techniques"]
    },
    "Farming": {
        "Machinery": ["Tractors", "Harvesters", "Large-scale farming equipment"],
        "Produce": ["Crops", "Animal products", "Specialty foods"],
        "Expertise": ["Stewards", "Land managers"],
        "Workers": ["Farm laborers", "Shepherds", "Herders"],
        "Understanding": ["New farming techniques", "Rotation methods"]
    },
    "Industrial": {
        "Machinery": ["Factory machines", "Spacecraft", "Large vehicles"],
        "Produce": ["Mass-produced goods", "Refined alloys", "Consumer products"],
        "Expertise": ["Supervisors", "Business managers"],
        "Workers": ["Factory workers", "Craftsmen", "Mechanics"],
        "Understanding": ["Business management", "Factory operation techniques"]
    },
    "Kanly": {
        "Machinery": ["Hunter-seekers", "Mines", "Bombs", "Assassination weapons"],
        "Produce": ["Poisons", "Toxins", "Incapacitants"],
        "Expertise": ["Assassin masters", "Operation planners", "Trainers"],
        "Workers": ["Assassins", "Thugs", "Infiltration specialists"],
        "Understanding": ["Assassination methods", "Infiltration techniques", "Deadly combat strikes"]
    },
    "Military": {
        "Machinery": ["Battlefield weapons", "Artillery", "Large-scale shields", "Tanks"],
        "Produce": ["Ammunition", "Personal weapons", "Small arms"],
        "Expertise": ["Tacticians", "Officers", "Strategists"],
        "Workers": ["Soldiers", "Engineers", "Pilots", "Logistics personnel"],
        "Understanding": ["Military strategies", "New tactics"]
    },
    "Political": {
        "Machinery": ["Couture fashion", "Expensive trinkets", "Message services"],
        "Produce": ["Information", "Secrets", "Favors", "Political influence"],
        "Expertise": ["Political analysts", "Mediators", "Diplomats", "Fashionistas"],
        "Workers": ["Courtiers", "Spies", "Administrators", "Servants"],
        "Understanding": ["Diplomacy techniques", "Forms of etiquette"]
    },
    "Religion": {
        "Machinery": ["Churches", "Statues", "Prayer beads", "Religious symbols", "Religious books"],
        "Produce": ["Prayers", "Hymns", "Religious writings", "Inspirational texts"],
        "Expertise": ["Philosophers", "Clergy"],
        "Workers": ["Choristers", "Altar servants", "Community managers"],
        "Understanding": ["New religious philosophies", "New forms of faith"]
    },
    "Science": {
        "Machinery": ["Laboratory equipment", "Quarantine areas", "Scientific facilities"],
        "Produce": ["Chemical compounds", "Drugs", "Genetically-adapted organisms"],
        "Expertise": ["Scientists", "Researchers"],
        "Workers": ["Lab assistants", "Lab managers"],
        "Understanding": ["New scientific research", "Technological advances"]
    }
}

# House roles
HOUSE_ROLES = [
    "Ruler", "Consort", "Advisor", "Chief Physician", "Councilor", "Envoy",
    "Heir", "Marshal", "Scholar", "Spymaster", "Swordmaster", "Treasurer", "Warmaster"
]

# Enemy hatred levels
HATRED_LEVELS = {
    "Dislike": "Any interaction with this House is at +1 Difficulty, due to distrust",
    "Rival": "Actively seeks to bring the House down through gossip and politics",
    "Loathing": "Always has plans to destroy the House, but won't risk resources lightly",
    "Kanly": "Dedicated all resources to wiping out the House to the last person"
}

# Enemy reasons
ENEMY_REASONS = [
    "Competition", "Slight", "Debt", "Ancient Feud", "Morality", "Servitude",
    "Family Ties", "Theft", "Jealousy", "No Reason"
]


class House(DefaultObject):
    """
    A Noble House in the Dune universe.
    
    Houses are organizations that characters serve. They have various attributes:
    - House Type (Nascent, Minor, Major, Great)
    - Domains (primary and secondary areas of expertise)
    - Homeworld description
    - Banner (colors and crest)
    - House Traits
    - Key Roles (Ruler, Heir, etc.)
    - Enemy Houses
    
    Only staff (builder+) can create and modify Houses.
    """
    
    def at_object_creation(self):
        """Called when the House is first created."""
        super().at_object_creation()
        
        # House Type
        self.db.house_type = "Nascent House"  # Nascent, House Minor, House Major, Great House
        
        # House Skills - representing House capabilities
        self.db.skills = {
            "Battle": 0,        # Military power and tactical skill
            "Communicate": 0,   # Diplomatic reputation and influence
            "Discipline": 0,    # Loyalty of people and forces
            "Move": 0,          # Response time and crisis management
            "Understand": 0     # Academic excellence and research
        }
        
        # Status and Reputation (0-100 scale)
        self.db.status = 0  # Set based on House type
        
        # Space Management (domains and territory)
        # Format: {planet_id: spaces_allocated}
        self.db.planet_spaces = {}
        
        # Economics - Wealth and Resources
        self.db.wealth = 0  # Financial power and spare funds
        self.db.resources = 0  # Raw materials and trade goods
        
        # Domains
        self.db.primary_domains = []  # List of {area, subtype, description}
        self.db.secondary_domains = []
        
        # Homeworld
        self.db.homeworld_name = ""
        self.db.homeworld_desc = ""
        self.db.weather = ""
        self.db.habitation = ""
        self.db.crime_rate = ""
        self.db.populace_mood = ""
        self.db.wealth_distribution = ""
        
        # Banner and Arms
        self.db.banner_colors = []  # e.g., ["White", "Red"]
        self.db.crest = ""  # e.g., "Scroll"
        
        # House Quote
        self.db.quote = ""  # A memorable quote or motto for the House
        
        # House Traits
        self.db.traits = []  # List of trait names
        
        # Roles - dict of role_name: {name, description, traits}
        self.db.roles = {}
        
        # Enemies - list of {house_name, hatred_level, reason}
        self.db.enemies = []
        
        # Members - now stores detailed member information
        # Format: {character_id: {'title': '', 'description': '', 'date_joined': datetime}}
        self.db.member_roster = {}
        self.db.members = []  # Legacy list for backward compatibility
        
        # Set default locks
        self.locks.add("view:all();edit:perm(Builder);delete:perm(Admin)")
    
    def get_threat_level(self):
        """
        Get the starting Threat per player based on House type.
        
        Returns:
            int: Threat level (0-3)
        """
        threat_map = {
            "Nascent House": 0,
            "House Minor": 1,
            "House Major": 2,
            "Great House": 3
        }
        return threat_map.get(self.db.house_type, 0)
    
    def get_default_skill_values(self):
        """
        Get the default skill values for the House type.
        These should be assigned by the player/staff during setup.
        
        Returns:
            list: List of default skill values to assign
        """
        skill_map = {
            "Great House": [9, 8, 7, 6, 5],
            "House Major": [8, 7, 6, 5, 4],
            "House Minor": [7, 6, 6, 5, 4],
            "Nascent House": [6, 5, 5, 4, 4]
        }
        return skill_map.get(self.db.house_type, [6, 5, 5, 4, 4])
    
    def set_skill(self, skill_name, value):
        """
        Set a House skill value.
        
        Args:
            skill_name (str): Name of the skill (Battle, Communicate, etc.)
            value (int): Skill value (typically 4-9)
            
        Returns:
            tuple: (success, message)
        """
        if skill_name not in self.db.skills:
            return False, f"Invalid skill. Valid skills: {', '.join(self.db.skills.keys())}"
        
        try:
            value = int(value)
        except ValueError:
            return False, "Skill value must be a number."
        
        if value < 0 or value > 12:
            return False, "Skill value must be between 0 and 12."
        
        self.db.skills[skill_name] = value
        return True, f"Set {skill_name} to {value}."
    
    def get_skill(self, skill_name):
        """
        Get a House skill value.
        
        Args:
            skill_name (str): Name of the skill
            
        Returns:
            int: Skill value or 0 if not found
        """
        return self.db.skills.get(skill_name, 0)
    
    def initialize_skills(self, battle=0, communicate=0, discipline=0, move=0, understand=0):
        """
        Initialize all skills at once.
        
        Args:
            battle (int): Battle skill value
            communicate (int): Communicate skill value
            discipline (int): Discipline skill value
            move (int): Move skill value
            understand (int): Understand skill value
            
        Returns:
            tuple: (success, message)
        """
        self.db.skills = {
            "Battle": int(battle),
            "Communicate": int(communicate),
            "Discipline": int(discipline),
            "Move": int(move),
            "Understand": int(understand)
        }
        return True, "Skills initialized successfully."
    
    def get_default_status(self):
        """
        Get the default starting status for the House type.
        
        Returns:
            int: Default status value
        """
        status_map = {
            "Nascent House": 15,
            "House Minor": 25,
            "House Major": 45,
            "Great House": 65
        }
        return status_map.get(self.db.house_type, 15)
    
    def get_reputation(self):
        """
        Get the House's reputation based on status and House type.
        
        Returns:
            str: Reputation level (Feeble, Weak, Respected, Strong, Problematic, Dangerous)
        """
        status = self.db.status
        house_type = self.db.house_type
        
        # Nascent House uses Minor House reputation table
        if house_type == "Nascent House":
            house_type = "House Minor"
        
        # Reputation thresholds by House type
        if house_type == "House Minor":
            if status <= 10:
                return "Feeble"
            elif status <= 20:
                return "Weak"
            elif status <= 40:
                return "Respected"
            elif status <= 50:
                return "Strong"
            elif status <= 70:
                return "Problematic"
            else:  # 71+
                return "Dangerous"
                
        elif house_type == "House Major":
            if status <= 20:
                return "Feeble"
            elif status <= 40:
                return "Weak"
            elif status <= 60:
                return "Respected"
            elif status <= 70:
                return "Strong"
            elif status <= 80:
                return "Problematic"
            else:  # 81+
                return "Dangerous"
                
        elif house_type == "Great House":
            if status <= 40:
                return "Feeble"
            elif status <= 60:
                return "Weak"
            elif status <= 70:
                return "Respected"
            elif status <= 80:
                return "Strong"
            elif status <= 90:
                return "Problematic"
            else:  # 91+
                return "Dangerous"
        
        # Default (shouldn't happen)
        return "Unknown"
    
    def get_reputation_description(self):
        """
        Get a description of what the current reputation means.
        
        Returns:
            str: Description of the reputation level
        """
        reputation = self.get_reputation()
        
        descriptions = {
            "Feeble": "The House is considered alone and without allies. Any attempt to secure new allies or aggressive actions suffers significant penalties. Attacks by other Houses are inevitable.",
            "Weak": "The House has recently taken a few knocks but still has friends. Its word doesn't carry the same weight it did before. All aggressive actions and attempts to gain allies suffer penalties.",
            "Respected": "Everything is as it should be. The House occupies exactly the space in the Imperium its peers expect. No penalties or modifiers apply.",
            "Strong": "The House is doing well for itself, not beyond the boundaries of its power, but still very well. Difficulties for House actions are reduced. The people of the House are more confident and enthusiastic.",
            "Problematic": "The House is getting a little too ambitious. It may be planning a move for greater power, making others nervous. If trying aggressive actions, the Difficulty is reduced, but diplomatic actions and gaining favor or alliances suffer penalties. Other Houses may be discussing what to do about the problematic House.",
            "Dangerous": "The House is doing far too well for itself and clearly has designs on resources above it. Several of its peers (and possibly even the Emperor) are plotting its downfall. The House can reduce action difficulties, but suffers increased penalties to all diplomatic actions. Any House action or venture generates Threat for the gamemaster."
        }
        
        return descriptions.get(reputation, "Status unknown.")
    
    def get_reputation_effects(self):
        """
        Get the mechanical effects of the current reputation.
        
        Returns:
            str: Game effects description
        """
        reputation = self.get_reputation()
        
        effects = {
            "Feeble": "Aggressive actions: +2 Difficulty penalty | Gaining allies: +2 Difficulty penalty",
            "Weak": "All aggressive actions: +1 Difficulty penalty | Gaining allies/favor: +1 Difficulty penalty",
            "Respected": "No modifiers",
            "Strong": "All House actions: -1 Difficulty reduction | People more confident and enthusiastic",
            "Problematic": "Aggressive actions: -2 Difficulty reduction | Diplomatic actions: +1 Difficulty penalty | Gaining favor/alliance: +1 Difficulty penalty | +1 Threat when discussed",
            "Dangerous": "House actions: -2 Difficulty reduction | Diplomatic actions: +2 Difficulty penalty | Any House action/venture: +1 Threat"
        }
        
        return effects.get(reputation, "No effects.")
    
    def set_status(self, value):
        """
        Set the House's status value.
        
        Args:
            value (int): New status value (0-100)
            
        Returns:
            tuple: (success, message)
        """
        try:
            value = int(value)
        except ValueError:
            return False, "Status must be a number."
        
        if value < 0 or value > 100:
            return False, "Status must be between 0 and 100."
        
        old_reputation = self.get_reputation()
        self.db.status = value
        new_reputation = self.get_reputation()
        
        if old_reputation != new_reputation:
            return True, f"Status set to {value}. Reputation changed from {old_reputation} to {new_reputation}."
        else:
            return True, f"Status set to {value}. Reputation remains {new_reputation}."
    
    def adjust_status(self, amount):
        """
        Adjust the House's status by a relative amount.
        
        Args:
            amount (int): Amount to add (positive) or subtract (negative)
            
        Returns:
            tuple: (success, message)
        """
        try:
            amount = int(amount)
        except ValueError:
            return False, "Amount must be a number."
        
        old_status = self.db.status
        old_reputation = self.get_reputation()
        new_status = max(0, min(100, old_status + amount))
        self.db.status = new_status
        new_reputation = self.get_reputation()
        
        change = new_status - old_status
        
        if old_reputation != new_reputation:
            return True, f"Status changed by {change:+d} ({old_status} → {new_status}). Reputation changed from {old_reputation} to {new_reputation}!"
        else:
            return True, f"Status changed by {change:+d} ({old_status} → {new_status}). Reputation remains {new_reputation}."
    
    def get_domain_limits(self):
        """
        Get the number of primary and secondary domains allowed.
        
        Returns:
            tuple: (primary_count, secondary_count)
        """
        limits = {
            "Nascent House": (0, 1),
            "House Minor": (1, 1),
            "House Major": (1, 2),
            "Great House": (2, 3)
        }
        return limits.get(self.db.house_type, (0, 1))
    
    def get_typical_spaces(self):
        """
        Get the typical number of spaces for this House type.
        
        Returns:
            int: Typical spaces
        """
        spaces_map = {
            "Nascent House": 10,
            "House Minor": 35,
            "House Major": 60,
            "Great House": 100
        }
        return spaces_map.get(self.db.house_type, 10)
    
    def get_total_spaces(self):
        """
        Get the total number of spaces controlled by this House across all planets.
        
        Returns:
            int: Total spaces
        """
        if not hasattr(self.db, 'planet_spaces') or not self.db.planet_spaces:
            return 0
        # Convert values to int in case any are stored as strings
        return sum(int(v) if isinstance(v, (str, int)) else 0 for v in self.db.planet_spaces.values())
    
    def get_domain_space_requirements(self):
        """
        Calculate the total space requirements for all domains.
        
        Returns:
            int: Total spaces required
        """
        total = 0
        # Primary domains: 25 spaces each
        if self.db.primary_domains:
            total += len(self.db.primary_domains) * 25
        # Secondary domains: 10 spaces each
        if self.db.secondary_domains:
            total += len(self.db.secondary_domains) * 10
        return total
    
    def get_space_surplus_deficit(self):
        """
        Calculate the surplus or deficit of spaces versus domain requirements.
        
        Returns:
            int: Positive for surplus, negative for deficit
        """
        controlled = self.get_total_spaces()
        required = self.get_domain_space_requirements()
        return controlled - required
    
    def allocate_spaces_on_planet(self, planet, spaces):
        """
        Allocate spaces to this House on a specific planet.
        Updates both House and Planet records.
        
        Args:
            planet: Planet object
            spaces (int or str): Number of spaces to allocate
            
        Returns:
            tuple: (success, message)
        """
        if not hasattr(self.db, 'planet_spaces'):
            self.db.planet_spaces = {}
        
        # Convert spaces to int if it's a string
        try:
            spaces = int(spaces)
        except (ValueError, TypeError):
            return False, f"Invalid spaces value: {spaces}"
        
        # Try to allocate on the planet
        success, message = planet.allocate_spaces(self, spaces)
        
        if success:
            # Update House records
            if spaces == 0:
                # Remove allocation
                if planet.id in self.db.planet_spaces:
                    del self.db.planet_spaces[planet.id]
            else:
                self.db.planet_spaces[planet.id] = spaces
        
        return success, message
    
    def deallocate_spaces_on_planet(self, planet):
        """
        Remove all space allocations on a specific planet.
        
        Args:
            planet: Planet object
            
        Returns:
            tuple: (success, message)
        """
        if not hasattr(self.db, 'planet_spaces'):
            self.db.planet_spaces = {}
        
        success, message = planet.deallocate_spaces(self)
        
        if success:
            if planet.id in self.db.planet_spaces:
                del self.db.planet_spaces[planet.id]
        
        return success, message
    
    def get_planet_allocations(self):
        """
        Get a list of (planet, spaces) tuples for all planet allocations.
        
        Returns:
            list: List of (planet_obj, spaces) tuples
        """
        from evennia import ObjectDB
        
        if not hasattr(self.db, 'planet_spaces') or not self.db.planet_spaces:
            return []
        
        allocations = []
        for planet_id, spaces in self.db.planet_spaces.items():
            try:
                planet = ObjectDB.objects.get(id=planet_id)
                allocations.append((planet, spaces))
            except ObjectDB.DoesNotExist:
                # Planet no longer exists, clean up
                del self.db.planet_spaces[planet_id]
        
        return sorted(allocations, key=lambda x: x[1], reverse=True)
    
    def calculate_domain_income(self):
        """
        Calculate total Wealth and Resources generated by all domains.
        
        Returns:
            tuple: (total_resources, total_wealth)
        """
        total_resources = 0
        total_wealth = 0
        
        # Base generation by subtype
        primary_base = {
            "Machinery": (12, 32),
            "Produce": (10, 30),
            "Expertise": (6, 44),
            "Workers": (8, 40),
            "Understanding": (6, 42)
        }
        
        secondary_base = {
            "Machinery": (6, 16),
            "Produce": (5, 18),
            "Expertise": (3, 22),
            "Workers": (4, 20),
            "Understanding": (3, 22)
        }
        
        # Domain type modifiers
        # Fewer Resources, More Wealth
        wealth_focused = ["Artistic", "Espionage", "Political", "Religion"]
        # More Resources, Less Wealth
        resource_focused = ["Farming", "Industrial", "Kanly", "Military", "Science"]
        
        # Process primary domains
        for domain in self.db.primary_domains:
            area = domain["area"]
            subtype = domain["subtype"]
            
            # Get base generation
            resources, wealth = primary_base.get(subtype, (6, 40))
            
            # Apply domain type modifiers
            if area in wealth_focused:
                resources -= 3
                wealth += 8
            elif area in resource_focused:
                resources += 3
                wealth -= 6
            
            # Enforce minimums
            resources = max(2, resources)
            wealth = max(10, wealth)
            
            total_resources += resources
            total_wealth += wealth
        
        # Process secondary domains
        for domain in self.db.secondary_domains:
            area = domain["area"]
            subtype = domain["subtype"]
            
            # Get base generation
            resources, wealth = secondary_base.get(subtype, (3, 20))
            
            # Apply domain type modifiers
            if area in wealth_focused:
                resources -= 1
                wealth += 4
            elif area in resource_focused:
                resources += 1
                wealth -= 4
            
            # Enforce minimums
            resources = max(2, resources)
            wealth = max(10, wealth)
            
            total_resources += resources
            total_wealth += wealth
        
        return (total_resources, total_wealth)
    
    def calculate_role_bonuses(self):
        """
        Calculate bonuses from filled roles.
        
        Returns:
            tuple: (bonus_resources, bonus_wealth)
        """
        bonus_resources = 0
        bonus_wealth = 0
        
        # Treasurer adds +10 Wealth from shrewd investments
        if "Treasurer" in self.db.roles:
            bonus_wealth += 10
        
        # Future: other roles may provide bonuses
        
        return (bonus_resources, bonus_wealth)
    
    def get_total_income(self):
        """
        Calculate total income from domains and roles.
        
        Returns:
            tuple: (total_resources, total_wealth)
        """
        domain_resources, domain_wealth = self.calculate_domain_income()
        role_resources, role_wealth = self.calculate_role_bonuses()
        
        return (domain_resources + role_resources, domain_wealth + role_wealth)
    
    def add_wealth(self, amount):
        """
        Add wealth to the House treasury.
        
        Args:
            amount (int): Amount to add
            
        Returns:
            tuple: (success, message)
        """
        try:
            amount = int(amount)
        except ValueError:
            return False, "Amount must be a number."
        
        if amount < 0:
            return False, "Use remove_wealth for negative amounts."
        
        self.db.wealth += amount
        return True, f"Added {amount} Wealth. New total: {self.db.wealth}"
    
    def remove_wealth(self, amount):
        """
        Remove wealth from the House treasury.
        
        Args:
            amount (int): Amount to remove
            
        Returns:
            tuple: (success, message)
        """
        try:
            amount = int(amount)
        except ValueError:
            return False, "Amount must be a number."
        
        if amount < 0:
            return False, "Use add_wealth for negative amounts."
        
        if self.db.wealth < amount:
            return False, f"Insufficient Wealth. Current: {self.db.wealth}, Requested: {amount}"
        
        self.db.wealth -= amount
        return True, f"Removed {amount} Wealth. New total: {self.db.wealth}"
    
    def add_resources(self, amount):
        """
        Add resources to the House.
        
        Args:
            amount (int): Amount to add
            
        Returns:
            tuple: (success, message)
        """
        try:
            amount = int(amount)
        except ValueError:
            return False, "Amount must be a number."
        
        if amount < 0:
            return False, "Use remove_resources for negative amounts."
        
        self.db.resources += amount
        return True, f"Added {amount} Resources. New total: {self.db.resources}"
    
    def remove_resources(self, amount):
        """
        Remove resources from the House.
        
        Args:
            amount (int): Amount to remove
            
        Returns:
            tuple: (success, message)
        """
        try:
            amount = int(amount)
        except ValueError:
            return False, "Amount must be a number."
        
        if amount < 0:
            return False, "Use add_resources for negative amounts."
        
        if self.db.resources < amount:
            return False, f"Insufficient Resources. Current: {self.db.resources}, Requested: {amount}"
        
        self.db.resources -= amount
        return True, f"Removed {amount} Resources. New total: {self.db.resources}"
    
    def trade_wealth_for_resources(self, wealth_amount):
        """
        Trade Wealth for Resources (3 Wealth = 1 Resource).
        Maximum 1/3 of current Wealth can be traded.
        
        Args:
            wealth_amount (int): Amount of Wealth to spend
            
        Returns:
            tuple: (success, message)
        """
        try:
            wealth_amount = int(wealth_amount)
        except ValueError:
            return False, "Amount must be a number."
        
        if wealth_amount <= 0:
            return False, "Amount must be positive."
        
        if wealth_amount > self.db.wealth:
            return False, f"Insufficient Wealth. Current: {self.db.wealth}"
        
        # Check 1/3 limit
        max_tradeable = self.db.wealth // 3
        if wealth_amount > max_tradeable:
            return False, f"Can only trade up to {max_tradeable} Wealth (1/3 of total)."
        
        # Exchange rate: 3 Wealth = 1 Resource
        resources_gained = wealth_amount // 3
        wealth_spent = resources_gained * 3
        
        if resources_gained == 0:
            return False, "Need at least 3 Wealth to gain 1 Resource."
        
        self.db.wealth -= wealth_spent
        self.db.resources += resources_gained
        
        return True, f"Traded {wealth_spent} Wealth for {resources_gained} Resources. New totals: {self.db.resources} Resources, {self.db.wealth} Wealth"
    
    def trade_resources_for_wealth(self, resource_amount):
        """
        Trade Resources for Wealth (1 Resource = 3 Wealth).
        Maximum 1/3 of current Resources can be traded.
        
        Args:
            resource_amount (int): Amount of Resources to sell
            
        Returns:
            tuple: (success, message)
        """
        try:
            resource_amount = int(resource_amount)
        except ValueError:
            return False, "Amount must be a number."
        
        if resource_amount <= 0:
            return False, "Amount must be positive."
        
        if resource_amount > self.db.resources:
            return False, f"Insufficient Resources. Current: {self.db.resources}"
        
        # Check 1/3 limit
        max_tradeable = self.db.resources // 3
        if resource_amount > max_tradeable:
            return False, f"Can only trade up to {max_tradeable} Resources (1/3 of total)."
        
        # Exchange rate: 1 Resource = 3 Wealth
        wealth_gained = resource_amount * 3
        
        self.db.resources -= resource_amount
        self.db.wealth += wealth_gained
        
        return True, f"Traded {resource_amount} Resources for {wealth_gained} Wealth. New totals: {self.db.resources} Resources, {self.db.wealth} Wealth"
    
    def add_domain(self, is_primary, area, subtype, description):
        """
        Add a domain to the House.
        
        Args:
            is_primary (bool): Whether this is a primary domain
            area (str): Domain area (e.g., "Artistic", "Military")
            subtype (str): Domain subtype (e.g., "Produce", "Workers")
            description (str): Specific description of this domain
            
        Returns:
            tuple: (success, message)
        """
        primary_limit, secondary_limit = self.get_domain_limits()
        
        if is_primary:
            if len(self.db.primary_domains) >= primary_limit:
                return False, f"House can only have {primary_limit} primary domain(s)."
            self.db.primary_domains.append({
                "area": area,
                "subtype": subtype,
                "description": description
            })
            # Add area as a trait if it's a primary domain
            if area not in self.db.traits:
                self.db.traits.append(area)
        else:
            if len(self.db.secondary_domains) >= secondary_limit:
                return False, f"House can only have {secondary_limit} secondary domain(s)."
            self.db.secondary_domains.append({
                "area": area,
                "subtype": subtype,
                "description": description
            })
        
        return True, "Domain added successfully."
    
    def remove_domain(self, is_primary, index):
        """
        Remove a domain by index.
        
        Args:
            is_primary (bool): Whether to remove from primary domains
            index (int): Index of the domain to remove
            
        Returns:
            tuple: (success, message)
        """
        domains = self.db.primary_domains if is_primary else self.db.secondary_domains
        
        if index < 0 or index >= len(domains):
            return False, "Invalid domain index."
        
        removed = domains.pop(index)
        
        # Remove trait if it was a primary domain
        if is_primary and removed["area"] in self.db.traits:
            self.db.traits.remove(removed["area"])
        
        return True, f"Removed domain: {removed['area']} - {removed['description']}"
    
    def set_role(self, role_name, character_name, description="", traits=None, caller=None, is_npc=False):
        """
        Assign a character to a House role.
        
        Args:
            role_name (str): Name of the role (e.g., "Ruler", "Heir")
            character_name (str): Name of the character filling this role
            description (str): Description of the character
            traits (list): List of trait strings for this character
            caller: The object doing the search (for character validation)
            is_npc (bool): If True, skip character validation (for NPCs)
            
        Returns:
            tuple: (success, message)
        """
        if role_name not in HOUSE_ROLES:
            return False, f"Invalid role. Valid roles: {', '.join(HOUSE_ROLES)}"
        
        character_obj = None
        
        # Try to find the character if caller is provided and not an NPC
        if caller and not is_npc:
            from evennia.utils.search import search_object
            # Search for character by name
            results = search_object(character_name, typeclass="typeclasses.characters.Character")
            if results:
                if len(results) > 1:
                    return False, f"Multiple characters found matching '{character_name}'. Please be more specific."
                character_obj = results[0]
            else:
                # Try searching all objects in case it's a different typeclass
                results = search_object(character_name)
                if results:
                    for result in results:
                        if hasattr(result, 'db') and hasattr(result.db, 'stats'):
                            character_obj = result
                            break
                    if not character_obj:
                        return False, f"'{character_name}' was found but is not a character. Use /npc flag for NPCs."
                else:
                    return False, f"Character '{character_name}' not found. Use /npc flag if this is an NPC."
        
        # Clear the role from any previous character
        if role_name in self.db.roles:
            old_char_name = self.db.roles[role_name].get("character", "")
            if old_char_name:
                # Try to find and clear the old character's role
                old_results = search_object(old_char_name, typeclass="typeclasses.characters.Character")
                if old_results:
                    old_char = old_results[0]
                    if hasattr(old_char, 'db') and old_char.db.role == role_name:
                        old_char.db.role = ""
        
        # Set the role
        self.db.roles[role_name] = {
            "character": character_name,
            "description": description,
            "traits": traits or [],
            "is_npc": is_npc
        }
        
        # Set the character's role attribute if we found the character
        if character_obj:
            character_obj.db.role = role_name
            # Also make sure the character is a member of this house
            if hasattr(character_obj, 'db') and character_obj.db.house != self:
                character_obj.db.house = self
        
        npc_note = " (NPC)" if is_npc else ""
        return True, f"Set {role_name} to {character_name}{npc_note}."
    
    def remove_role(self, role_name):
        """
        Remove a character from a House role.
        
        Args:
            role_name (str): Name of the role to clear
            
        Returns:
            tuple: (success, message)
        """
        if role_name not in self.db.roles:
            return False, f"{role_name} is not currently filled."
        
        # Get the character name before removing
        char_name = self.db.roles[role_name].get("character", "")
        
        # Try to find and clear the character's role attribute
        if char_name:
            from evennia.utils.search import search_object
            results = search_object(char_name, typeclass="typeclasses.characters.Character")
            if results:
                char_obj = results[0]
                if hasattr(char_obj, 'db') and char_obj.db.role == role_name:
                    char_obj.db.role = ""
        
        del self.db.roles[role_name]
        return True, f"Cleared {role_name} role."
    
    def add_enemy(self, house_name, hatred_level, reason):
        """
        Add an enemy House.
        
        Args:
            house_name (str): Name of the enemy House
            hatred_level (str): Level of hatred (Dislike, Rival, Loathing, Kanly)
            reason (str): Reason for the enmity
            
        Returns:
            tuple: (success, message)
        """
        if hatred_level not in HATRED_LEVELS:
            return False, f"Invalid hatred level. Valid: {', '.join(HATRED_LEVELS.keys())}"
        
        # Case-insensitive reason matching
        reason_lower = reason.lower()
        valid_reason = None
        for r in ENEMY_REASONS:
            if r.lower() == reason_lower:
                valid_reason = r  # Use the correctly capitalized version
                break
        
        if not valid_reason:
            return False, f"Invalid reason. Valid: {', '.join(ENEMY_REASONS)}"
        
        self.db.enemies.append({
            "house": house_name,
            "hatred": hatred_level,
            "reason": valid_reason  # Use the correctly capitalized version
        })
        
        return True, f"Added enemy: {house_name} ({hatred_level})"
    
    def remove_enemy(self, index):
        """
        Remove an enemy House by index.
        
        Args:
            index (int): Index of the enemy to remove
            
        Returns:
            tuple: (success, message)
        """
        if index < 0 or index >= len(self.db.enemies):
            return False, "Invalid enemy index."
        
        removed = self.db.enemies.pop(index)
        return True, f"Removed enemy: {removed['house']}"
    
    def add_member(self, character, title="", description=""):
        """
        Add a character as a member of this House.
        
        Args:
            character: Character object to add
            title (str): Optional title/rank in the House
            description (str): Optional description of their tie to the House
            
        Returns:
            tuple: (success, message)
        """
        from django.utils import timezone
        
        if character.id in self.db.member_roster:
            return False, f"{character.name} is already a member of {self.key}."
        
        # Add to detailed roster
        self.db.member_roster[character.id] = {
            'title': title,
            'description': description,
            'date_joined': timezone.now()
        }
        
        # Legacy support
        if character.id not in self.db.members:
            self.db.members.append(character.id)
        
        character.db.house = self
        
        return True, f"{character.name} is now a member of {self.key}."
    
    def remove_member(self, character):
        """
        Remove a character from this House.
        
        Args:
            character: Character object to remove
            
        Returns:
            tuple: (success, message)
        """
        if character.id not in self.db.member_roster and character.id not in self.db.members:
            return False, f"{character.name} is not a member of {self.key}."
        
        # Remove from roster
        if character.id in self.db.member_roster:
            del self.db.member_roster[character.id]
        
        # Legacy support
        if character.id in self.db.members:
            self.db.members.remove(character.id)
        
        character.db.house = None
        
        return True, f"{character.name} has been removed from {self.key}."
    
    def set_member_title(self, character, title):
        """
        Set a member's title in the House.
        
        Args:
            character: Character object
            title (str): Title/rank in the House
            
        Returns:
            tuple: (success, message)
        """
        if character.id not in self.db.member_roster:
            return False, f"{character.name} is not a member of {self.key}."
        
        self.db.member_roster[character.id]['title'] = title
        return True, f"Set {character.name}'s title to: {title}"
    
    def set_member_description(self, character, description):
        """
        Set a member's description of their tie to the House.
        
        Args:
            character: Character object
            description (str): Description of tie to House
            
        Returns:
            tuple: (success, message)
        """
        if character.id not in self.db.member_roster:
            return False, f"{character.name} is not a member of {self.key}."
        
        self.db.member_roster[character.id]['description'] = description
        return True, f"Set {character.name}'s description."
    
    def get_member_info(self, character):
        """
        Get a member's roster information.
        
        Args:
            character: Character object
            
        Returns:
            dict: Member information or None
        """
        return self.db.member_roster.get(character.id)
    
    def get_all_members(self):
        """
        Get all members with their full information.
        
        Returns:
            list: List of (character, info_dict) tuples
        """
        from evennia import ObjectDB
        
        members = []
        for char_id, info in self.db.member_roster.items():
            try:
                character = ObjectDB.objects.get(id=char_id)
                members.append((character, info))
            except ObjectDB.DoesNotExist:
                continue
        
        return members
    
    def get_display(self):
        """
        Get a formatted display of the House information.
        
        Returns:
            str: Formatted House information
        """
        output = []
        
        # Header
        output.append("|y" + "=" * 78 + "|n")
        output.append("|y" + f" {self.key} ".center(78, "=") + "|n")
        output.append("|y" + "=" * 78 + "|n")
        
        # House Type and Threat
        output.append(f"\n|wHouse Type:|n {self.db.house_type}")
        output.append(f"|wThreat Level:|n {self.get_threat_level()} per player")
        
        # Status and Reputation
        if hasattr(self.db, 'status') and self.db.status is not None:
            reputation = self.get_reputation()
            reputation_color = {
                "Feeble": "|r",
                "Weak": "|y",
                "Respected": "|g",
                "Strong": "|c",
                "Problematic": "|m",
                "Dangerous": "|R"
            }.get(reputation, "|w")
            
            output.append(f"\n|wStatus:|n {self.db.status}/100")
            output.append(f"|wReputation:|n {reputation_color}{reputation}|n")
            output.append(f"  {self.get_reputation_effects()}")
        else:
            default_status = self.get_default_status()
            output.append(f"\n|yStatus not yet set. Default for {self.db.house_type}: {default_status}|n")
        
        # House Skills
        if self.db.skills and any(self.db.skills.values()):
            output.append("\n|w" + "House Skills".center(78, "-") + "|n")
            output.append(f"  |cBattle:|n {self.db.skills.get('Battle', 0)} (Military power and tactical skill)")
            output.append(f"  |cCommunicate:|n {self.db.skills.get('Communicate', 0)} (Diplomatic reputation and influence)")
            output.append(f"  |cDiscipline:|n {self.db.skills.get('Discipline', 0)} (Loyalty of people and forces)")
            output.append(f"  |cMove:|n {self.db.skills.get('Move', 0)} (Response time and crisis management)")
            output.append(f"  |cUnderstand:|n {self.db.skills.get('Understand', 0)} (Academic excellence and research)")
        else:
            default_values = self.get_default_skill_values()
            output.append(f"\n|ySkills not yet assigned. Recommended values: {', '.join(map(str, default_values))}|n")
        
        # Space Management
        total_spaces = self.get_total_spaces()
        required_spaces = self.get_domain_space_requirements()
        typical_spaces = self.get_typical_spaces()
        surplus_deficit = self.get_space_surplus_deficit()
        
        output.append("\n|w" + "Territory and Domains".center(78, "-") + "|n")
        output.append(f"|wTotal Spaces Controlled:|n {total_spaces} (Typical for {self.db.house_type}: {typical_spaces})")
        output.append(f"|wDomain Requirements:|n {required_spaces} spaces")
        
        if surplus_deficit >= 0:
            output.append(f"|wSurplus:|n |g{surplus_deficit} spaces available|n")
        else:
            output.append(f"|wDeficit:|n |r{abs(surplus_deficit)} spaces needed!|n")
        
        # Show planet allocations if any
        allocations = self.get_planet_allocations()
        if allocations:
            output.append(f"\n|wPlanet Allocations:|n")
            for planet, spaces in allocations:
                output.append(f"  |c{planet.key}|n: {spaces} spaces")
        elif total_spaces == 0:
            output.append(f"\n|yNo space allocations yet.|n")
        
        # Economics - Wealth and Resources
        output.append("\n|w" + "Economics".center(78, "-") + "|n")
        
        # Current treasury
        current_wealth = self.db.wealth if hasattr(self.db, 'wealth') else 0
        current_resources = self.db.resources if hasattr(self.db, 'resources') else 0
        output.append(f"|wWealth:|n {current_wealth}")
        output.append(f"|wResources:|n {current_resources}")
        
        # Domain income calculation
        domain_resources, domain_wealth = self.calculate_domain_income()
        role_resources, role_wealth = self.calculate_role_bonuses()
        total_income_resources, total_income_wealth = self.get_total_income()
        
        if self.db.primary_domains or self.db.secondary_domains:
            output.append(f"\n|wIncome from Domains:|n")
            output.append(f"  Resources: {domain_resources}")
            output.append(f"  Wealth: {domain_wealth}")
            
            if role_resources > 0 or role_wealth > 0:
                output.append(f"|wBonuses from Roles:|n")
                if role_resources > 0:
                    output.append(f"  Resources: +{role_resources}")
                if role_wealth > 0:
                    output.append(f"  Wealth: +{role_wealth}")
                
                output.append(f"|wTotal Income:|n")
                output.append(f"  Resources: {total_income_resources}")
                output.append(f"  Wealth: {total_income_wealth}")
        else:
            output.append(f"\n|yNo domains yet. Add domains to generate income.|n")
        
        # Trading information
        if current_wealth >= 3 or current_resources >= 1:
            max_wealth_trade = current_wealth // 3
            max_resource_trade = current_resources // 3
            output.append(f"\n|wTrading Capacity (1/3 limit):|n")
            if current_wealth >= 3:
                output.append(f"  Can trade up to {max_wealth_trade} Wealth for {max_wealth_trade // 3} Resources")
            if current_resources >= 1:
                output.append(f"  Can trade up to {max_resource_trade} Resources for {max_resource_trade * 3} Wealth")
        
        # Banner
        if self.db.banner_colors or self.db.crest:
            colors = ", ".join(self.db.banner_colors) if self.db.banner_colors else "Not set"
            crest = self.db.crest if self.db.crest else "Not set"
            output.append(f"\n|wBanner Colors:|n {colors}")
            output.append(f"|wCrest:|n {crest}")
        
        # Quote
        if self.db.quote:
            output.append(f"\n|wQuote:|n \"{self.db.quote}\"")
        
        # Traits
        if self.db.traits:
            output.append(f"\n|wHouse Traits:|n {', '.join(self.db.traits)}")
        
        # Primary Domains
        if self.db.primary_domains:
            output.append("\n|w" + "Primary Domains".center(78, "-") + "|n")
            for i, domain in enumerate(self.db.primary_domains):
                output.append(f"  {i+1}. |c{domain['area']}|n ({domain['subtype']}): {domain['description']}")
        
        # Secondary Domains
        if self.db.secondary_domains:
            output.append("\n|w" + "Secondary Domains".center(78, "-") + "|n")
            for i, domain in enumerate(self.db.secondary_domains):
                output.append(f"  {i+1}. |c{domain['area']}|n ({domain['subtype']}): {domain['description']}")
        
        # Homeworld
        if self.db.homeworld_name:
            output.append("\n|w" + "Homeworld".center(78, "-") + "|n")
            output.append(f"|wName:|n {self.db.homeworld_name}")
            if self.db.homeworld_desc:
                output.append(f"|wDescription:|n {self.db.homeworld_desc}")
            if self.db.weather:
                output.append(f"|wWeather:|n {self.db.weather}")
            if self.db.habitation:
                output.append(f"|wHabitation:|n {self.db.habitation}")
            if self.db.crime_rate:
                output.append(f"|wCrime Rate:|n {self.db.crime_rate}")
            if self.db.populace_mood:
                output.append(f"|wPopulace:|n {self.db.populace_mood}")
            if self.db.wealth_distribution:
                output.append(f"|wWealth Distribution:|n {self.db.wealth_distribution}")
        
        # Roles
        if self.db.roles:
            output.append("\n|w" + "Key Roles".center(78, "-") + "|n")
            for role, info in sorted(self.db.roles.items()):
                traits_str = f" ({', '.join(info['traits'])})" if info.get('traits') else ""
                desc_str = f" - {info['description']}" if info.get('description') else ""
                npc_str = " |r(NPC)|n" if info.get('is_npc', False) else ""
                output.append(f"  |c{role}:|n {info['character']}{npc_str}{traits_str}{desc_str}")
        
        # Enemies
        if self.db.enemies:
            output.append("\n|w" + "Enemy Houses".center(78, "-") + "|n")
            for i, enemy in enumerate(self.db.enemies):
                output.append(f"  {i+1}. |r{enemy['house']}|n - {enemy['hatred']} ({enemy['reason']})")
                output.append(f"      {HATRED_LEVELS[enemy['hatred']]}")
        
        # Members Roster
        if self.db.member_roster:
            output.append("\n|w" + f"Members ({len(self.db.member_roster)})".center(78, "-") + "|n")
            members = self.get_all_members()
            
            if members:
                # Sort by name
                members.sort(key=lambda x: x[0].name)
                
                for character, info in members:
                    char_line = f"  |c{character.name}|n"
                    
                    # Add title if present
                    if info.get('title'):
                        char_line += f" - {info['title']}"
                    
                    output.append(char_line)
                    
                    # Add description if present
                    if info.get('description'):
                        output.append(f"    {info['description']}")
            else:
                output.append(f"  {len(self.db.member_roster)} character(s) serve this House")
        elif self.db.members:  # Legacy support
            output.append("\n|w" + f"Members ({len(self.db.members)})".center(78, "-") + "|n")
            output.append(f"  {len(self.db.members)} character(s) serve this House")
        
        output.append("\n|y" + "=" * 78 + "|n")
        
        return "\n".join(output)

