# Planet System Summary

## Overview

The Planet system allows staff to create and manage planetary bodies throughout the Imperium. Each planet has various characteristics including habitability, population, industries, and political affiliations with Houses.

## Key Features

### Planet Characteristics
- **Habitability Type**: Uninhabitable, Habitable, Asteroid, or Terran
- **World Type**: 20 different world types (Gas giant, Rocky world, Arid World, etc.)
- **Star System**: Name of the star system the planet orbits
- **Political Affiliation**: House that controls the planet
- **Population**: Number of inhabitants (displayed with comma formatting)
- **Industries**: Description of industries present or what planet is known for
- **Military Power**: Description of military capabilities
- **Lifestyle**: General lifestyle on the planet

### Political and Social Structure
- **Houses Present**: Multiple Houses can have presence on a planet
- **Political Affiliation**: One House controls the planet politically
- **Organizations**: Multiple organizations (Schools, Guilds, Orders, Factions) can be present
- **Notes**: Two types of notes (Planet Notes and Other Notes) for detailed descriptions
  - Notes support text formatting: `%r` for newlines, `%t` for tabs

### Display Format
Planet information is displayed in a green-themed format with organized sections showing all characteristics, affiliated houses and organizations, and detailed notes.

## Command Summary

### Viewing (All Players)
```
+planet <name>          View planet information
+planet/list            List all planets
```

### Creation (Staff Only - Builder+)
```
+planet/create <name>                       Create new planet
+planet/destroy <name>                      Destroy planet
```

### Configuration (Staff Only - Builder+)
```
+planet/set <planet>/habitability=<type>    Set habitability type
+planet/set <planet>/type=<world type>      Set world type
+planet/set <planet>/star=<system>          Set star system
+planet/set <planet>/affiliation=<house>    Set political affiliation
+planet/set <planet>/population=<number>    Set population
+planet/set <planet>/industries=<text>      Set industries
+planet/set <planet>/military=<text>        Set military power
+planet/set <planet>/notes=<text>           Set planet notes
+planet/set <planet>/other=<text>           Set other notes
```

### House Management (Staff Only - Builder+)
```
+planet/house <planet>/list                 List houses on planet
+planet/house <planet>/add=<house>          Add house to planet
+planet/house <planet>/remove=<house>       Remove house from planet
```

### Organization Management (Staff Only - Builder+)
```
+planet/org <planet>/list                   List organizations on planet
+planet/org <planet>/add=<org>              Add organization to planet
+planet/org <planet>/remove=<org>           Remove organization from planet
```

## World Types

### Uninhabitable
- Gas giant
- Toxic Atmosphere
- Furnace
- Volcanic
- Asteroid
- Ice Asteroid

### Marginal Habitability
- Moon planetoid
- Ice Giant
- Mineral Rich Asteroid
- Frozen World
- Mined-Out World

### Habitable
- Rocky world
- Alpine World
- Mineral World
- Ocean World
- Arid World
- Forested World
- Tropical World
- Savanna World
- Earth-Like

## Example: Creating Vallabhi

Complete setup of a mineral world:

```
+planet/create Vallabhi
+planet/set Vallabhi/habitability=Habitable
+planet/set Vallabhi/type=Mineral World
+planet/set Vallabhi/star=Beta Tucanae IV
+planet/set Vallabhi/population=3,300,000
+planet/set Vallabhi/industries=Ore-refining of local metals and gems
+planet/set Vallabhi/military=Ground forces, space fleet, basic planetary defenses
+planet/set Vallabhi/affiliation=House Nagara
+planet/house Vallabhi/add=House Molay
+planet/house Vallabhi/add=House Arcuri
+planet/org Vallabhi/add=Bene Gesserit School
+planet/org Vallabhi/add=Spacing Guild
+planet/set Vallabhi/notes=Vallabhi is a mountainous world with deep valleys. It has vast lakes rather than seas, and many islands. These islands are dangerous to live on due to unpredictable and violent tides, but fishermen and smugglers from minor Houses make a home here.
+planet/set Vallabhi/other=House Nagara's home city of Kyotashi is set upon one of the broad mountain terraces that make up the Rinumian Ridge, a chain of mountains that are extensively mined. House Nagara manages the mineral wealth of the planet, with the assistance of the minor House Arcuri. However the dramatic landscape has also inspired poets, who are drawn to the training halls of the other minor House Molay.
+planet Vallabhi
```

## Integration with Other Systems

### Houses
- Planets can be affiliated with a House (political control)
- Multiple Houses can have presence on a planet
- Setting affiliation automatically adds the House to the planet

### Organizations
- Multiple organizations can have presence on a planet
- Organizations are tracked separately from Houses
- Useful for Schools, Guilds, and other factions with planetary influence

### Rooms
Rooms can be associated with planets using the `+room` command:
- Use `+room/planet here=<planet>` to associate current room
- Use `+room/planet <room>=<planet>` to set any room's planet
- Planet association updates the room's location hierarchy
- Validation ensures planet exists before association
- Future enhancements will include:
  - Atmospheric conditions
  - Gravity effects
  - Local time and weather
  - Political context
  - Available resources

## Technical Details

### Typeclass
**Location**: `typeclasses/planets.py`

**Key Methods**:
- `format_population()` - Formats population with commas
- `get_affiliation_name()` - Returns affiliated House name or "Independent"
- `add_house(house)` - Add a House presence
- `remove_house(house)` - Remove a House presence
- `add_organization(org)` - Add an Organization presence
- `remove_organization(org)` - Remove an Organization presence
- `get_display()` - Returns formatted green-themed display

### Command
**Location**: `commands/dune/CmdPlanet.py`

**Permissions**:
- Viewing: All players
- Creation/Editing: Builder+
- Deletion: Admin (via default locks)

### Command Set
Added to `DuneCmdSet` in `commands/dune/dune_cmdset.py`

## Documentation Files

### Complete Documentation
**File**: `commands/dune/PLANET_SYSTEM_README.md`

Contains:
- Detailed command usage with examples
- All planet properties explained
- Complete setup examples
- Technical details about the typeclass
- Tips and best practices

### Quick Reference
**File**: `commands/dune/PLANET_QUICK_REFERENCE.md`

Contains:
- Command syntax quick lookup
- All habitability and world types
- Quick setup example

### Test File
**File**: `commands/dune/TEST_PLANET_CREATION.txt`

Contains:
- Step-by-step creation of Vallabhi example
- Expected output display
- Additional test cases

## Display Example

When viewing a planet with `+planet Vallabhi`, you'll see:

```
================================================================================

                                VALLABHI                                      

                            BETA TUCANAE IV

================================================================================

Habitability: Habitable     Type: Mineral World    Affiliation: House Nagara

--------------------------------------------------------------------------------

Population:       3,300,000 inhabitants

Industries:       Ore-refining of local metals and gems

Military Power:   Ground forces, space fleet, basic planetary defenses

Houses:           Nagara, Molay, Arcuri

Organizations:    Bene Gesserit School, Spacing Guild

--------------------------------------------------------------------------------

Planet Notes:

Vallabhi is a mountainous world with deep valleys. It has vast lakes rather than
seas, and many islands. These islands are dangerous to live on due to
unpredictable and violent tides, but fishermen and smugglers from minor Houses
make a home here.


Other Notes:

House Nagara's home city of Kyotashi is set upon one of the broad mountain
terraces that make up the Rinumian Ridge, a chain of mountains that are
extensively mined. House Nagara manages the mineral wealth of the planet, with
the assistance of the minor House Arcuri. However the dramatic landscape has
also inspired poets, who are drawn to the training halls of the other minor
House Molay.

================================================================================
```

## Design Philosophy

### Consistency with House System
The planet system follows the same design patterns as the House system:
- Single command with switches (following MUX conventions)
- Staff-only creation and editing
- Public viewing
- Comprehensive display format
- Detailed documentation

### Green Theme
Planets use green ANSI coloration to distinguish them from:
- Houses (yellow)
- Organizations (yellow)
- Character sheets (cyan/blue)
- Other system outputs

### Flexibility
The system is designed to be flexible:
- Multiple houses can have presence
- Multiple organizations can have presence
- Rich text descriptions with word wrapping
- Support for various world types and habitabilities
- Future extensibility for room integration

## Future Enhancements

Planned additions:
- Room-planet linkage system
- Planetary effects on rooms (gravity, atmosphere)
- Resource tracking tied to planets
- Economic system integration
- Weather systems based on planet type
- Local time zones per planet
- Trade route management between planets

