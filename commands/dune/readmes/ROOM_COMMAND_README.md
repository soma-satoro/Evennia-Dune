# Room Management Command (+room)

This document describes the `+room` command for managing rooms in the Dune MUSH, with special emphasis on associating rooms with planets.

## Overview

The `+room` command allows builders to manage room properties, including associating rooms with planets from the planet system. This integration allows rooms to inherit planet features and provides proper context for the room's location in the universe.

## Permission Requirements

- **Permission Required**: Builder or higher
- **Who Can Use**: Staff only
- **Command**: `+room` with all switches

## Command Syntax

### Viewing Room Information

**View current room:**
```
+room
```

**View specific room:**
```
+room <room dbref>
```

Example:
```
+room
+room #123
+room #456
```

### Associating Rooms with Planets

**Set planet for current room:**
```
+room/planet here=<planet name>
```

**Set planet for specific room:**
```
+room/planet <room>=<planet name>
```

**Clear planet association:**
```
+room/planet here=
+room/planet <room>=
```

Examples:
```
+room/planet here=Vallabhi
+room/planet #123=Arrakis
+room/planet here=
```

### Setting Area Information

**Set area for current room:**
```
+room/area here=<area name>/<area code>
```

**Set area for specific room:**
```
+room/area <room>=<area name>/<area code>
```

Examples:
```
+room/area here=Palace District/PD01
+room/area #123=Desert Outpost/DO05
```

### Setting Planetary Location

**Set location for current room:**
```
+room/location here=<location>
+room/loc here=<location>
```

**Set location for specific room:**
```
+room/location <room>=<location>
+room/loc <room>=<location>
```

Examples:
```
+room/location here=Kyotashi
+room/loc here=Palace District
+room/location #123=Arrakeen City
```

### Setting Location Hierarchy

**Set full hierarchy for current room:**
```
+room/hierarchy here=<location>,<planet>
```

**Set hierarchy for specific room:**
```
+room/hierarchy <room>=<location>,<planet>
```

Examples:
```
+room/hierarchy here=Kyotashi,Vallabhi
+room/hierarchy #123=Arrakeen City,Arrakis
```

### Toggling Places System

**Toggle places for current room:**
```
+room/places here
```

**Toggle places for specific room:**
```
+room/places <room>
```

Examples:
```
+room/places here
+room/places #123
```

## Location Hierarchy Structure

The room header displays: **Room Name - Location - Planet**

For example: `Nagara Square - Kyotashi - Vallabhi`

- **Room Name**: The name of the room itself
- **Location**: The planetary location (city, district, region, etc) - set with `+room/location`
- **Planet**: The planet name - set with `+room/planet`

## Planet Association Details

### What It Does

When you associate a room with a planet using `+room/planet here=<planet name>`, the command:

1. **Validates the planet exists** - Checks that the planet name matches an existing planet in the system
2. **Sets the planet reference** - Stores the planet object on the room's `db.planet` attribute
3. **Updates location hierarchy** - Automatically updates the planet (second element) in the room's location hierarchy

### Validation

The command includes validation to ensure:
- The planet name exists in the planet system
- If multiple planets match, it asks you to be more specific
- The target is actually a room (not another object type)

### Benefits

Associating rooms with planets:
- Provides proper context for the room's location
- Updates the room header to display the planet name
- Allows future features to inherit planet characteristics (gravity, atmosphere, etc.)
- Enables filtering and searching of rooms by planet
- Integrates with the planet system for comprehensive world-building

## Complete Example: Setting Up a Room

Here's a complete example of setting up a room on Vallabhi in the city of Kyotashi:

```
# First, create the planet (if not already done)
+planet/create Vallabhi
+planet/set Vallabhi/type=Mineral World
+planet/set Vallabhi/star=Beta Tucanae IV

# Now set up the room
@dig Nagara Square
@tel Nagara Square

# View current room info
+room

# Set the planetary location (city/district)
+room/location here=Kyotashi

# Associate with planet (automatically updates hierarchy)
+room/planet here=Vallabhi

# Set area information
+room/area here=Palace District/PD01

# View updated room info
+room

# Look at the room to see the new display
look
```

The room header will now display:
```
====> Nagara Square - Kyotashi - Vallabhi <===
```

## Room Information Display

When you use `+room` to view a room, you'll see:

```
================================================================================
                Room Information: Nagara Square                               
================================================================================

Room Name: Nagara Square
DB Reference: #123
Planet: Vallabhi
Area Name: Palace District
Area Code: PD01
Location Hierarchy: Nagara Square - Kyotashi - Vallabhi
Places System: Inactive

Description:
[Room description here]

================================================================================
```

## Room Display Integration

When players look at a room that's been properly configured, they'll see the full hierarchy in the room header:

```
====> Nagara Square - Kyotashi - Vallabhi <===

[Room description]

----> Characters <----------------------------------------------------------
Soma.............................4m

----> Directions <----------------------------------------------------------
East <E>                        West <W>

======> IC Area - PD01 <====
```

The header format is: **Room Name - Location - Planet**

## Working with Multiple Rooms

You can set up multiple rooms on the same planet efficiently:

```
# Set up Room 1
@tel #123
+room/planet here=Vallabhi
+room/area here=Palace District/PD01

# Set up Room 2
@tel #124
+room/planet here=Vallabhi
+room/area here=Palace District/PD02

# Set up Room 3 (without teleporting)
+room/planet #125=Vallabhi
+room/area #125=Industrial District/ID01
```

## Clearing Planet Association

If you need to remove a planet association:

```
+room/planet here=
```

This will:
- Clear the planet reference from the room
- Leave the location hierarchy unchanged (you can update it separately if needed)

## Tips and Best Practices

1. **Create planets first**: Always create and configure planets before associating rooms with them.

2. **Use consistent naming**: Make sure planet names in room hierarchies match the actual planet objects.

3. **Set hierarchy after planet**: The `/planet` switch automatically updates the location hierarchy's first element. You can manually adjust it afterward if needed.

4. **Batch room setup**: When building multiple rooms in the same area, set up one room completely, then use it as a template for others.

5. **Check your work**: Use `+room` to view room info and verify all settings are correct.

6. **Use dbrefs for remote work**: You don't need to be in a room to modify it. Use `+room/planet #123=Arrakis` to work on rooms remotely.

## Planet Validation

The command validates planet names by:

1. Searching for planets by name
2. Checking if exactly one planet matches
3. Returning an error if no planets or multiple planets match
4. Suggesting to use `+planet/list` to see available planets

Example validation errors:

```
> +room/planet here=Arrakiss
No planet found with the name 'Arrakiss'.
Use +planet/list to see available planets.

> +room/planet here=A
Multiple planets found: Arrakis, Atreides Prime
Please be more specific.
```

## Integration with Planet System

The room-planet association integrates seamlessly with the planet system:

- **Planet Display**: Use `+planet <name>` to see planet information
- **Room Context**: Rooms inherit contextual information from their planet
- **Future Features**: Room features like gravity, atmosphere, and time will be based on the planet

## Common Tasks

### Task: Set up a new building area

```
# Create the planet if needed
+planet/create MyPlanet

# Dig your rooms
@dig Main Hall
@dig East Wing
@dig West Wing

# Set up Main Hall
@tel Main Hall
+room/planet here=MyPlanet
+room/area here=Royal Palace/RP01

# Set up East Wing
@tel East Wing
+room/planet here=MyPlanet
+room/area here=Royal Palace/RP02

# Set up West Wing
@tel West Wing
+room/planet here=MyPlanet
+room/area here=Royal Palace/RP03
```

### Task: Change a room's planet

```
# View current settings
+room

# Change to new planet
+room/planet here=NewPlanet

# Verify change
+room
look
```

### Task: Update multiple rooms at once

```
# Use dbrefs to update remotely
+room/planet #123=Arrakis
+room/planet #124=Arrakis
+room/planet #125=Arrakis
+room/planet #126=Arrakis

# Or use a loop with softcode (if available)
# This is just an example - actual implementation depends on your system
```

## Troubleshooting

### Problem: "You are not in a room"

**Solution**: Make sure you're in an actual room location, not in limbo or another non-room location.

### Problem: "No planet found with the name 'X'"

**Solution**: 
1. Check the planet exists: `+planet/list`
2. Check spelling of planet name
3. Create the planet if it doesn't exist: `+planet/create <name>`

### Problem: "X is not a room"

**Solution**: Make sure you're targeting a room object, not a character, exit, or other object type.

### Problem: Room header not updating

**Solution**: The room header displays the location hierarchy. Make sure you've set it using either:
- `+room/planet here=<planet>` (automatically updates hierarchy)
- `+room/hierarchy here=<planet>,<region>` (manually set)

## Future Enhancements

Planned additions to room-planet integration:

- Automatic inheritance of planet features (gravity, atmosphere)
- Weather systems based on planet type
- Local time display based on planet
- Resource availability based on planet industries
- Automatic area code assignment
- Bulk room operations
- Room templates per planet

## Related Commands

- `+planet` - View and manage planets
- `+planet/list` - List all available planets
- `@dig` - Create new rooms
- `@desc` - Set room descriptions
- `@name` - Rename rooms
- `look` - View room display

## Documentation Files

For more information, see:
- `PLANET_SYSTEM_README.md` - Complete planet system documentation
- `PLANET_QUICK_REFERENCE.md` - Quick planet command reference
- `commands/dune/README.md` - Main commands documentation

