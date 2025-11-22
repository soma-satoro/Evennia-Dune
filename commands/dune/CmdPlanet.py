"""
Planet Management Commands

Consolidated command for creating and managing Planets in the Dune MUSH.
All commands require builder+ permission except viewing.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia import create_object, search_object
from typeclasses.planets import Planet, HABITABILITY_TYPES, WORLD_TYPES


class CmdPlanet(MuxCommand):
    """
    View and manage Planets.

    Usage:
        +planet <planet name>                - View Planet information
        +planet/list                         - List all Planets
        +planet/create <name>                - Create a new Planet (staff only)
        +planet/destroy <name>               - Destroy a Planet (staff only)
        +planet/set <planet>/habitability=<type>    - Set habitability (staff only)
        +planet/set <planet>/type=<world type>      - Set world type (staff only)
        +planet/set <planet>/star=<star system>     - Set star system (staff only)
        +planet/set <planet>/affiliation=<house>    - Set political affiliation (staff only)
        +planet/set <planet>/population=<number>    - Set population (staff only)
        +planet/set <planet>/lifestyle=<text>       - Set lifestyle (staff only)
        +planet/set <planet>/industries=<text>      - Set industries (staff only)
        +planet/set <planet>/military=<text>        - Set military power (staff only)
        +planet/set <planet>/notes=<text>           - Set planet notes (staff only)
        +planet/set <planet>/other=<text>           - Set other notes (staff only)
        +planet/house <planet>/list          - List Houses on planet (staff only)
        +planet/house <planet>/add=<house>   - Add House to planet (staff only)
        +planet/house <planet>/remove=<house> - Remove House from planet (staff only)
        +planet/org <planet>/list            - List Organizations on planet (staff only)
        +planet/org <planet>/add=<organization> - Add Organization (staff only)
        +planet/org <planet>/remove=<organization> - Remove Organization (staff only)
        +planet/spaces <planet>              - View space allocations (staff only)
        +planet/spaces <planet>/total=<#>    - Set total spaces (staff only)
        +planet/spaces <planet>/allocate=<house>:<#> - Allocate spaces to House (staff only)
        +planet/spaces <planet>/deallocate=<house> - Remove House allocation (staff only)

    Habitability Types: Uninhabitable, Habitable, Asteroid, Terran
    World Types: Gas giant, Rocky world, Moon planetoid, Ice Giant, Toxic Atmosphere, Furnace, Volcanic, Asteroid, Ice Asteroid, Mineral Rich Asteroid, Alpine World, Mineral World, Frozen World, Ocean World, Arid World, Forested World, Tropical World, Savanna World, Mined-Out World, Earth-Like

    Examples:
        +planet Vallabhi | +planet/list | +planet/create Arrakis
        +planet/set Arrakis/habitability=Habitable | +planet/set Arrakis/type=Arid World
        +planet/set Arrakis/star=Beta Tucanae IV | +planet/set Arrakis/affiliation=House Atreides
        +planet/spaces Arrakis/total=80 | +planet/spaces Arrakis/allocate=House Atreides:60
        +planet/house Arrakis/add=House Atreides | +planet/org Arrakis/add=Spacing Guild

    Staff Only: All management commands require Builder permission or higher.
    """
    
    key = "+planet"
    aliases = ["planet"]
    locks = "cmd:all()"
    help_category = "Dune"
    
    def func(self):
        """Main command dispatcher"""
        
        # Check for staff-only switches first
        staff_switches = ['create', 'destroy', 'set', 'house', 'org', 'spaces']
        
        # Check if any staff switch is used
        needs_staff = any(sw in self.switches for sw in staff_switches)
        
        if needs_staff:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("You need Builder permission or higher to manage Planets.")
                return
        
        # Route to appropriate handler
        if "list" in self.switches:
            self.list_planets()
        elif "create" in self.switches:
            self.create_planet()
        elif "destroy" in self.switches:
            self.destroy_planet()
        elif "set" in self.switches:
            self.set_property()
        elif "spaces" in self.switches:
            self.manage_spaces()
        elif "house" in self.switches:
            self.manage_houses()
        elif "org" in self.switches:
            self.manage_organizations()
        elif not self.switches:
            # No switches - view a Planet
            self.view_planet()
        else:
            self.caller.msg("Invalid switch. See 'help +planet' for available options.")
    
    def list_planets(self):
        """List all Planets."""
        from typeclasses.planets import Planet
        planets = Planet.objects.all()
        if not planets:
            self.caller.msg("No Planets have been created yet.")
            return
        
        self.caller.msg("|g" + "=" * 80 + "|n")
        self.caller.msg("|g" + " Planets of the Imperium ".center(80, "=") + "|n")
        self.caller.msg("|g" + "=" * 80 + "|n")
        
        for planet in sorted(planets, key=lambda x: x.key):
            world_type = planet.db.world_type
            affiliation = planet.get_affiliation_name()
            pop = planet.format_population()
            self.caller.msg(f"  |c{planet.key}|n - {world_type} ({affiliation}) - {pop}")
        
        self.caller.msg("|g" + "=" * 80 + "|n")
    
    def view_planet(self):
        """View specific Planet information."""
        if not self.args:
            self.caller.msg("Usage: +planet <planet name> or +planet/list")
            return
        
        planets = search_object(self.args.strip(), typeclass="typeclasses.planets.Planet")
        if not planets:
            self.caller.msg(f"No Planet found with the name '{self.args.strip()}'.")
            return
        
        if len(planets) > 1:
            self.caller.msg(f"Multiple Planets found: {', '.join([p.key for p in planets])}")
            return
        
        planet = planets[0]
        self.caller.msg(planet.get_display())
    
    def create_planet(self):
        """Create a new Planet."""
        if not self.args:
            self.caller.msg("Usage: +planet/create <planet name>")
            return
        
        planet_name = self.args.strip()
        
        # Check if Planet already exists
        existing = search_object(planet_name, typeclass="typeclasses.planets.Planet")
        if existing:
            self.caller.msg(f"A Planet named '{planet_name}' already exists.")
            return
        
        # Create the Planet
        planet = create_object(
            typeclass="typeclasses.planets.Planet",
            key=planet_name,
            location=None
        )
        
        self.caller.msg(f"|gCreated planet {planet_name}.|n")
        self.caller.msg(f"Use +planet/set to configure habitability, type, star system, and other details.")
    
    def destroy_planet(self):
        """Destroy a Planet."""
        if not self.args:
            self.caller.msg("Usage: +planet/destroy <planet name>")
            return
        
        planets = search_object(self.args.strip(), typeclass="typeclasses.planets.Planet")
        if not planets:
            self.caller.msg(f"No Planet found with the name '{self.args.strip()}'.")
            return
        
        if len(planets) > 1:
            self.caller.msg(f"Multiple Planets found: {', '.join([p.key for p in planets])}")
            return
        
        planet = planets[0]
        planet_name = planet.key
        
        planet.delete()
        self.caller.msg(f"|rDestroyed Planet {planet_name}.|n")
    
    def set_property(self):
        """Set Planet properties."""
        if not self.lhs or "=" not in self.args:
            self.caller.msg("Usage: +planet/set <planet>/<property>=<value>")
            self.caller.msg("See 'help +planet' for available properties.")
            return
        
        # Parse planet name from lhs (before the /)
        parts = self.lhs.split("/")
        if len(parts) < 2:
            self.caller.msg("Usage: +planet/set <planet>/<property>=<value>")
            return
        
        planet_name = parts[0].strip()
        property_name = parts[1].strip().lower()
        value = self.rhs.strip()
        
        # Find the Planet
        planets = search_object(planet_name, typeclass="typeclasses.planets.Planet")
        if not planets:
            self.caller.msg(f"No Planet found with the name '{planet_name}'.")
            return
        
        if len(planets) > 1:
            self.caller.msg(f"Multiple Planets found: {', '.join([p.key for p in planets])}")
            return
        
        planet = planets[0]
        
        # Handle different properties
        if property_name == "habitability":
            if value not in HABITABILITY_TYPES:
                self.caller.msg(f"Invalid habitability type. Valid: {', '.join(HABITABILITY_TYPES)}")
                return
            planet.db.habitability_type = value
            self.caller.msg(f"Set {planet.key} habitability to {value}.")
            
        elif property_name == "type":
            if value not in WORLD_TYPES:
                self.caller.msg(f"Invalid world type. Valid types:")
                for wtype in WORLD_TYPES:
                    self.caller.msg(f"  {wtype}")
                return
            planet.db.world_type = value
            self.caller.msg(f"Set {planet.key} world type to {value}.")
            
        elif property_name == "star":
            planet.db.star = value
            self.caller.msg(f"Set {planet.key} star system to: {value}")
            
        elif property_name == "affiliation":
            # Search for the House
            houses = search_object(value, typeclass="typeclasses.houses.House")
            if not houses:
                self.caller.msg(f"No House found with the name '{value}'.")
                return
            if len(houses) > 1:
                self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
                return
            
            house = houses[0]
            planet.db.political_affiliation = house
            
            # Automatically add the house to the planet if not already present
            if house not in planet.db.houses:
                planet.db.houses.append(house)
            
            self.caller.msg(f"Set {planet.key} political affiliation to: {house.key}")
            
        elif property_name == "population":
            try:
                # Allow numbers with commas
                pop_value = int(value.replace(",", ""))
                planet.db.population = pop_value
                self.caller.msg(f"Set {planet.key} population to: {pop_value:,}")
            except ValueError:
                self.caller.msg("Population must be a number.")
                
        elif property_name == "lifestyle":
            planet.db.lifestyle = value
            self.caller.msg(f"Set {planet.key} lifestyle.")
            
        elif property_name == "industries":
            planet.db.industries = value
            self.caller.msg(f"Set {planet.key} industries.")
            
        elif property_name == "military":
            planet.db.military_power = value
            self.caller.msg(f"Set {planet.key} military power.")
            
        elif property_name == "notes":
            planet.db.planet_notes = value
            self.caller.msg(f"Set {planet.key} planet notes.")
            
        elif property_name == "other":
            planet.db.other_notes = value
            self.caller.msg(f"Set {planet.key} other notes.")
            
        else:
            self.caller.msg(f"Unknown property '{property_name}'. See 'help +planet' for available properties.")
    
    def manage_houses(self):
        """Manage Houses present on the planet."""
        if not self.lhs:
            self.caller.msg("Usage: +planet/house <planet>/<action>[=<value>]")
            return
        
        # Parse planet name
        planet_name = self.lhs.split("/")[0].strip()
        
        # Find the Planet
        planets = search_object(planet_name, typeclass="typeclasses.planets.Planet")
        if not planets:
            self.caller.msg(f"No Planet found with the name '{planet_name}'.")
            return
        
        if len(planets) > 1:
            self.caller.msg(f"Multiple Planets found: {', '.join([p.key for p in planets])}")
            return
        
        planet = planets[0]
        
        # Determine action
        if "/list" in self.lhs.lower():
            if not planet.db.houses:
                self.caller.msg(f"No Houses are present on {planet.key}.")
                return
            
            output = [f"\n|g{'Houses on ' + planet.key:=^80}|g"]
            for house in sorted(planet.db.houses, key=lambda x: x.key):
                is_affiliation = " |y(Political Affiliation)|n" if house == planet.db.political_affiliation else ""
                output.append(f"  |c{house.key}|n{is_affiliation}")
            
            self.caller.msg("\n".join(output))
            
        elif "/add" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +planet/house <planet>/add=<house name>")
                return
            
            house_name = self.rhs.strip()
            houses = search_object(house_name, typeclass="typeclasses.houses.House")
            if not houses:
                self.caller.msg(f"No House found with the name '{house_name}'.")
                return
            if len(houses) > 1:
                self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
                return
            
            house = houses[0]
            success, message = planet.add_house(house)
            self.caller.msg(message)
            
        elif "/remove" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +planet/house <planet>/remove=<house name>")
                return
            
            house_name = self.rhs.strip()
            houses = search_object(house_name, typeclass="typeclasses.houses.House")
            if not houses:
                self.caller.msg(f"No House found with the name '{house_name}'.")
                return
            if len(houses) > 1:
                self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
                return
            
            house = houses[0]
            success, message = planet.remove_house(house)
            self.caller.msg(message)
        else:
            self.caller.msg("Usage: +planet/house <planet>/list|add|remove")
    
    def manage_organizations(self):
        """Manage Organizations present on the planet."""
        if not self.lhs:
            self.caller.msg("Usage: +planet/org <planet>/<action>[=<value>]")
            return
        
        # Parse planet name
        planet_name = self.lhs.split("/")[0].strip()
        
        # Find the Planet
        planets = search_object(planet_name, typeclass="typeclasses.planets.Planet")
        if not planets:
            self.caller.msg(f"No Planet found with the name '{planet_name}'.")
            return
        
        if len(planets) > 1:
            self.caller.msg(f"Multiple Planets found: {', '.join([p.key for p in planets])}")
            return
        
        planet = planets[0]
        
        # Determine action
        if "/list" in self.lhs.lower():
            if not planet.db.organizations:
                self.caller.msg(f"No Organizations are present on {planet.key}.")
                return
            
            output = [f"\n|g{'Organizations on ' + planet.key:=^80}|g"]
            for org in sorted(planet.db.organizations, key=lambda x: x.key):
                output.append(f"  |c{org.key}|n")
            
            self.caller.msg("\n".join(output))
            
        elif "/add" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +planet/org <planet>/add=<organization name>")
                return
            
            org_name = self.rhs.strip()
            orgs = search_object(org_name, typeclass="typeclasses.organizations.Organization")
            if not orgs:
                self.caller.msg(f"No Organization found with the name '{org_name}'.")
                return
            if len(orgs) > 1:
                self.caller.msg(f"Multiple Organizations found: {', '.join([o.key for o in orgs])}")
                return
            
            org = orgs[0]
            success, message = planet.add_organization(org)
            self.caller.msg(message)
            
        elif "/remove" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +planet/org <planet>/remove=<organization name>")
                return
            
            org_name = self.rhs.strip()
            orgs = search_object(org_name, typeclass="typeclasses.organizations.Organization")
            if not orgs:
                self.caller.msg(f"No Organization found with the name '{org_name}'.")
                return
            if len(orgs) > 1:
                self.caller.msg(f"Multiple Organizations found: {', '.join([o.key for o in orgs])}")
                return
            
            org = orgs[0]
            success, message = planet.remove_organization(org)
            self.caller.msg(message)
        else:
            self.caller.msg("Usage: +planet/org <planet>/list|add|remove")
    
    def manage_spaces(self):
        """Manage space allocations on the planet."""
        if not self.lhs:
            self.caller.msg("Usage: +planet/spaces <planet>[/<action>][=<value>]")
            return
        
        # Parse planet name
        planet_name = self.lhs.split("/")[0].strip()
        
        # Find the Planet
        planets = search_object(planet_name, typeclass="typeclasses.planets.Planet")
        if not planets:
            self.caller.msg(f"No Planet found with the name '{planet_name}'.")
            return
        
        if len(planets) > 1:
            self.caller.msg(f"Multiple Planets found: {', '.join([p.key for p in planets])}")
            return
        
        planet = planets[0]
        
        # Determine action
        if "/total" in self.lhs.lower():
            # Set total spaces
            if "=" not in self.args:
                self.caller.msg("Usage: +planet/spaces <planet>/total=<number>")
                self.caller.msg("Default: 80 for planets, 30 for moons")
                return
            
            try:
                total = int(self.rhs.strip())
                if total < 0:
                    self.caller.msg("Total spaces must be positive.")
                    return
                
                # Check if reducing would cause allocation issues
                allocated = planet.get_allocated_spaces()
                if total < allocated:
                    self.caller.msg(f"|rWarning:|n Reducing total spaces to {total} when {allocated} are already allocated!")
                    self.caller.msg(f"You must deallocate {allocated - total} spaces first.")
                    return
                
                planet.db.total_spaces = total
                available = planet.get_available_spaces()
                self.caller.msg(f"Set total spaces on {planet.key} to {total}. ({available} available)")
                
            except ValueError:
                self.caller.msg("Total spaces must be a number.")
            
        elif "/allocate" in self.lhs.lower():
            # Allocate spaces to a House
            if "=" not in self.args:
                self.caller.msg("Usage: +planet/spaces <planet>/allocate=<house name>:<spaces>")
                self.caller.msg("Example: +planet/spaces Arrakis/allocate=House Atreides:60")
                return
            
            # Parse house:spaces format
            parts = self.rhs.strip().split(":")
            if len(parts) != 2:
                self.caller.msg("Format: <house name>:<spaces>")
                self.caller.msg("Example: House Atreides:60")
                return
            
            house_name, spaces_str = parts
            house_name = house_name.strip()
            
            # Find the House
            houses = search_object(house_name, typeclass="typeclasses.houses.House")
            if not houses:
                self.caller.msg(f"No House found with the name '{house_name}'.")
                return
            if len(houses) > 1:
                self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
                return
            
            house = houses[0]
            
            # Allocate spaces
            success, message = house.allocate_spaces_on_planet(planet, spaces_str.strip())
            self.caller.msg(message)
            
            if success:
                # Show updated information
                available = planet.get_available_spaces()
                total_house = house.get_total_spaces()
                required = house.get_domain_space_requirements()
                self.caller.msg(f"{planet.key}: {available} spaces available")
                self.caller.msg(f"{house.key}: {total_house} total spaces, {required} required for domains")
            
        elif "/deallocate" in self.lhs.lower():
            # Remove all allocations for a House
            if "=" not in self.args:
                self.caller.msg("Usage: +planet/spaces <planet>/deallocate=<house name>")
                return
            
            house_name = self.rhs.strip()
            
            # Find the House
            houses = search_object(house_name, typeclass="typeclasses.houses.House")
            if not houses:
                self.caller.msg(f"No House found with the name '{house_name}'.")
                return
            if len(houses) > 1:
                self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
                return
            
            house = houses[0]
            
            # Deallocate spaces
            success, message = house.deallocate_spaces_on_planet(planet)
            self.caller.msg(message)
            
        else:
            # Show space information
            output = [f"\n|g{'Space Allocations for ' + planet.key:=^80}|n"]
            
            total = planet.db.total_spaces if hasattr(planet.db, 'total_spaces') else 80
            allocated = planet.get_allocated_spaces()
            available = planet.get_available_spaces()
            
            output.append(f"\n|wTotal Spaces:|n {total}")
            output.append(f"|wAllocated:|n {allocated}")
            output.append(f"|wAvailable:|n {available}")
            
            if hasattr(planet.db, 'space_allocations') and planet.db.space_allocations:
                output.append(f"\n|wAllocations by House:|n")
                from evennia import ObjectDB
                for house_id, spaces in sorted(planet.db.space_allocations.items(), key=lambda x: x[1], reverse=True):
                    try:
                        house = ObjectDB.objects.get(id=house_id)
                        percentage = (spaces / total * 100) if total > 0 else 0
                        output.append(f"  |c{house.key}|n: {spaces} spaces ({percentage:.1f}%)")
                    except ObjectDB.DoesNotExist:
                        pass
            else:
                output.append(f"\n|yNo space allocations yet.|n")
            
            output.append(f"\n|wCommands:|n")
            output.append(f"  +planet/spaces {planet.key}/total=<number>")
            output.append(f"  +planet/spaces {planet.key}/allocate=<house>:<spaces>")
            output.append(f"  +planet/spaces {planet.key}/deallocate=<house>")
            
            self.caller.msg("\n".join(output))

