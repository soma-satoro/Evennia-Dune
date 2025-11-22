# Planet System Setup Guide

## What Has Been Installed

The Planet system for the Dune MUSH has been fully implemented with the following components:

### 1. Planet Typeclass
**File**: `typeclasses/planets.py`

A complete typeclass for managing planet objects with:
- Habitability types (Uninhabitable, Habitable, Asteroid, Terran)
- 20 different world types
- Star system tracking
- Political affiliation with Houses
- Population tracking with comma formatting
- Industries and military power descriptions
- House and organization presence tracking
- Rich text notes with word wrapping
- Green-themed display format

### 2. Planet Command
**File**: `commands/dune/CmdPlanet.py`

A comprehensive staff command (+planet) with switches for:
- Viewing planet information (all players)
- Creating and destroying planets (Builder+)
- Setting all planet properties (Builder+)
- Managing houses on planets (Builder+)
- Managing organizations on planets (Builder+)

### 3. Command Set Integration
**File**: `commands/dune/dune_cmdset.py`

The CmdPlanet command has been added to the DuneCmdSet, making it available to all characters automatically.

### 4. Documentation
Created comprehensive documentation:

**In commands/dune/:**
- `PLANET_SYSTEM_README.md` - Complete system documentation
- `PLANET_QUICK_REFERENCE.md` - Quick command reference
- `TEST_PLANET_CREATION.txt` - Example walkthrough
- Updated `README.md` - Added planet system section

**In root directory:**
- `PLANET_SYSTEM_SUMMARY.md` - High-level system overview
- `PLANET_SETUP.md` - This file

## Installation Steps

### Step 1: Reload the Server

After these files have been created, you need to reload the Evennia server to activate the new commands:

```
@reload
```

Or restart the server:

```
evennia reload
```

### Step 2: Verify Installation

Check that the command is available:

```
help +planet
```

You should see the help text for the planet command.

### Step 3: Test Basic Functionality

Try listing planets (should be empty initially):

```
+planet/list
```

### Step 4: Create Your First Planet (Builder+ Only)

If you have Builder permissions, try creating a test planet:

```
+planet/create TestWorld
+planet/set TestWorld/habitability=Habitable
+planet/set TestWorld/type=Earth-Like
+planet TestWorld
```

You should see a green-themed display of the planet.

### Step 5: Create Example Planet (Optional)

Follow the complete example in `TEST_PLANET_CREATION.txt` to create the Vallabhi planet:

```
+planet/create Vallabhi
+planet/set Vallabhi/habitability=Habitable
+planet/set Vallabhi/type=Mineral World
+planet/set Vallabhi/star=Beta Tucanae IV
+planet/set Vallabhi/population=3,300,000
+planet/set Vallabhi/industries=Ore-refining of local metals and gems
+planet/set Vallabhi/military=Ground forces, space fleet, basic planetary defenses
```

(Continue with the rest of the commands in TEST_PLANET_CREATION.txt)

## Quick Start Guide

### For Players

**View a planet:**
```
+planet <planet name>
```

**List all planets:**
```
+planet/list
```

### For Staff (Builder+)

**Create a planet:**
```
+planet/create <name>
```

**Set basic properties:**
```
+planet/set <planet>/habitability=<type>
+planet/set <planet>/type=<world type>
+planet/set <planet>/star=<star system>
+planet/set <planet>/population=<number>
```

**Add houses and organizations:**
```
+planet/house <planet>/add=<house name>
+planet/org <planet>/add=<organization name>
```

**Set political control:**
```
+planet/set <planet>/affiliation=<house name>
```

## Integration with Existing Systems

### Houses
The planet system integrates seamlessly with the existing House system:
- Planets can be affiliated with Houses
- Multiple Houses can have presence on a planet
- Setting a planet's affiliation automatically adds that House to the planet

**Prerequisites**: Houses must be created with `+house/create` before they can be assigned to planets.

### Organizations
The planet system integrates with the Organization system:
- Multiple organizations can have presence on a planet
- Organizations are tracked separately from Houses

**Prerequisites**: Organizations must be created with `+org/create` before they can be assigned to planets.

### Rooms
The planet system integrates with rooms through the `+room` command:
- Rooms can be associated with planets
- Use `+room/planet here=<planet>` to associate current room
- Use `+room/planet <room>=<planet>` to set any room's planet
- Planet association automatically updates room's location hierarchy
- Validation ensures planet exists before association

**See**: `ROOM_COMMAND_README.md` for complete room management documentation

## Permissions

### Viewing
- **Permission Required**: None
- **Who Can Use**: All players
- **Commands**: `+planet <name>`, `+planet/list`

### Creating/Editing
- **Permission Required**: Builder or higher
- **Who Can Use**: Staff only
- **Commands**: All `/create`, `/set`, `/house`, `/org` commands

### Deleting
- **Permission Required**: Admin (via default Planet typeclass locks)
- **Who Can Use**: Admin staff only
- **Commands**: `+planet/destroy <name>`

## Common Tasks

### Creating a Complete Planet

1. Create the planet
2. Set habitability and world type
3. Set star system
4. Set population
5. Set industries and military
6. Set political affiliation
7. Add additional houses
8. Add organizations
9. Add descriptive notes
10. View the completed planet

See `TEST_PLANET_CREATION.txt` for a complete example.

### Viewing House Presence

To see which planets a House has presence on, you can:
1. View the House with `+house <house name>` (if homeworld is set)
2. List all planets with `+planet/list` and check affiliations
3. View each planet individually to see house presence

### Managing Political Control

To change which House controls a planet:
```
+planet/set <planet>/affiliation=<new house>
```

This will:
- Set the political affiliation
- Automatically add the House to the planet if not already present
- Keep other Houses on the planet intact

## Troubleshooting

### Command Not Found

**Problem**: "+planet: Command not found"

**Solution**:
1. Make sure you've reloaded the server: `@reload`
2. Check that CmdPlanet is in dune_cmdset.py
3. Verify that you have the DuneCmdSet added to your character

### Permission Denied

**Problem**: "You need Builder permission or higher"

**Solution**:
- These commands are staff-only
- You need Builder permission or higher
- Contact an admin to grant permissions if needed

### House/Organization Not Found

**Problem**: "No House found with the name '<name>'"

**Solution**:
- Make sure the House or Organization exists
- Use `+house/list` or `+org/list` to see available options
- Create the House/Organization first if it doesn't exist

### Planet Already Exists

**Problem**: "A Planet named '<name>' already exists"

**Solution**:
- Choose a different name
- Or view/edit the existing planet
- Or destroy the old planet first (if you have permission)

## Documentation Reference

For more detailed information, see:

- **Complete System Documentation**: `commands/dune/PLANET_SYSTEM_README.md`
- **Quick Command Reference**: `commands/dune/PLANET_QUICK_REFERENCE.md`
- **Example Creation**: `commands/dune/TEST_PLANET_CREATION.txt`
- **System Overview**: `PLANET_SYSTEM_SUMMARY.md`
- **Main Command Documentation**: `commands/dune/README.md`

## Support and Questions

If you encounter any issues or have questions:

1. Check the documentation files listed above
2. Use `help +planet` to see command syntax
3. Contact your game administrators
4. Review the test creation file for examples

## Next Steps

After setting up the planet system:

1. Create your main planets (homeworlds for Great Houses)
2. Set up political affiliations
3. Add relevant organizations to each planet
4. Write descriptive notes for each world
5. Share planet list with players using `+planet/list`

## Future Enhancements

The planet system is designed to be extensible. Future additions may include:

- Room-planet linkage (rooms inherit planet features)
- Planetary atmospheric effects
- Resource tracking per planet
- Economic system integration
- Weather systems
- Local time zones
- Trade routes between planets

These features can be added without changing the existing planet structure.

