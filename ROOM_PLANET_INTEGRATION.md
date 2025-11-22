# Room-Planet Integration Summary

## Overview

The Room-Planet integration allows builders to associate rooms with planets from the planet system. This provides proper context for room locations and enables future planet-based room features.

## What Was Implemented

### 1. Updated Room Typeclass
**File**: `typeclasses/rooms.py`

Added `self.db.planet` attribute to store planet object reference:
```python
def at_object_creation(self):
    # ... existing code ...
    self.db.planet = None  # Planet object reference
```

### 2. Created Room Management Command
**File**: `commands/dune/CmdRoom.py`

Comprehensive `+room` command with the following switches:
- **View**: `+room` or `+room <dbref>` - View room information
- **/planet**: `+room/planet here=<planet>` - Associate room with planet
- **/area**: `+room/area here=<name>/<code>` - Set area information
- **/hierarchy**: `+room/hierarchy here=<planet>,<region>` - Set location hierarchy
- **/places**: `+room/places here` - Toggle places system

### 3. Added to Command Set
**File**: `commands/dune/dune_cmdset.py`

Added CmdRoom to DuneCmdSet, making it available to all builders.

### 4. Documentation Created
- `ROOM_COMMAND_README.md` - Complete room management documentation
- `ROOM_QUICK_REFERENCE.md` - Quick command reference
- Updated `commands/dune/README.md` - Added room command section
- Updated `PLANET_SYSTEM_SUMMARY.md` - Added room integration notes
- Updated `PLANET_SETUP.md` - Added room integration information

## Key Features

### Planet Association with Validation

The `/planet` switch includes comprehensive validation:

```python
# Validates planet exists
planets = search_object(planet_name, typeclass="typeclasses.planets.Planet")
if not planets:
    self.caller.msg(f"No planet found with the name '{planet_name}'.")
    return

# Validates unique match
if len(planets) > 1:
    self.caller.msg(f"Multiple planets found: {', '.join([p.key for p in planets])}")
    return

# Validates target is a room
if not inherits_from(room, "typeclasses.rooms.Room"):
    self.caller.msg(f"{room.key} is not a room.")
    return
```

### Automatic Hierarchy Update

When associating a room with a planet, the location hierarchy is automatically updated:

```python
# Update the first element of hierarchy to be the planet name
if len(current_hierarchy) >= 2:
    room.db.location_hierarchy = [planet.key, current_hierarchy[1]]
else:
    room.db.location_hierarchy = [planet.key, "Unknown Region"]
```

### Flexible Room Targeting

Commands support both "here" for current room and dbrefs for remote work:

```python
if room_target.lower() == "here":
    room = self.caller.location
else:
    room = self.caller.search(room_target, global_search=True)
```

## Usage Examples

### Basic Planet Association

```bash
# Associate current room with Vallabhi
+room/planet here=Vallabhi

# Associate room #123 with Arrakis
+room/planet #456=Arrakis

# Clear planet association
+room/planet here=
```

### Complete Room Setup

```bash
# Create planet
+planet/create Vallabhi
+planet/set Vallabhi/type=Mineral World
+planet/set Vallabhi/star=Beta Tucanae IV

# Create and configure room
@dig Mining Complex
@tel Mining Complex
+room/planet here=Vallabhi
+room/area here=Industrial District/ID02
+room

# View the result
look
```

### Batch Room Setup

```bash
# Set up multiple rooms on the same planet
+room/planet #123=Vallabhi
+room/area #123=Mining Tunnels/MT01

+room/planet #124=Vallabhi
+room/area #124=Mining Tunnels/MT02

+room/planet #125=Vallabhi
+room/area #125=Mining Tunnels/MT03
```

## Room Information Display

When viewing a room with `+room`, you'll see:

```
================================================================================
                Room Information: Mining Complex                               
================================================================================

Room Name: Mining Complex
DB Reference: #123
Planet: Vallabhi
Area Name: Industrial District
Area Code: ID02
Location Hierarchy: Vallabhi > Industrial District
Places System: Inactive

Description:
[Room description]

================================================================================
```

## Integration Benefits

### Current Benefits

1. **Proper Context**: Rooms have clear planetary context
2. **Organized World-Building**: Rooms are logically grouped by planet
3. **Automatic Updates**: Location hierarchy updates automatically
4. **Validation**: Prevents invalid planet associations
5. **Flexibility**: Can work on rooms remotely or in-place

### Future Benefits

The room-planet association enables future features:

1. **Atmospheric Effects**: Rooms inherit planet atmosphere (toxic, thin, normal, etc.)
2. **Gravity Modifiers**: Rooms can apply planet-specific gravity effects
3. **Weather Systems**: Weather based on planet type and location
4. **Local Time**: Time of day based on planet's rotation
5. **Resources**: Available resources based on planet industries
6. **Political Context**: NPC reactions based on planet affiliation
7. **Search/Filter**: Find all rooms on a specific planet
8. **Economic Systems**: Trade and commerce based on planet

## Validation and Error Handling

The command includes comprehensive error handling:

### Planet Not Found
```
> +room/planet here=InvalidPlanet
No planet found with the name 'InvalidPlanet'.
Use +planet/list to see available planets.
```

### Multiple Matches
```
> +room/planet here=A
Multiple planets found: Arrakis, Atreides Prime
Please be more specific.
```

### Not a Room
```
> +room/planet Paul=Arrakis
Paul is not a room.
```

### Not in a Room
```
> +room/planet here=Arrakis
You are not in a room.
```

## Best Practices

### 1. Create Planets First
Always create and configure planets before associating rooms:
```bash
+planet/create Vallabhi
+planet/set Vallabhi/type=Mineral World
# ... configure planet ...
# Then associate rooms
+room/planet here=Vallabhi
```

### 2. Use Consistent Naming
Keep planet names consistent between the planet system and room hierarchies.

### 3. Set Complete Information
Set all relevant room information for best results:
```bash
+room/planet here=Vallabhi
+room/area here=Industrial District/ID02
+room/hierarchy here=Vallabhi,Industrial District
```

### 4. Batch Operations
When setting up multiple rooms, work efficiently:
```bash
# Set up multiple rooms at once
+room/planet #101=Vallabhi
+room/planet #102=Vallabhi
+room/planet #103=Vallabhi
+room/planet #104=Vallabhi
```

### 5. Verify Your Work
Always check the results:
```bash
+room
look
```

## Technical Implementation

### Storage
- Planet reference stored in `room.db.planet`
- Stores the actual planet object, not just the name
- Allows direct access to all planet properties

### Access Pattern
```python
# Get planet from room
planet = room.db.planet
if planet:
    planet_name = planet.key
    planet_type = planet.db.world_type
    planet_pop = planet.db.population
```

### Hierarchy Management
```python
# Hierarchy is a 2-element list: [Planet, Region]
room.db.location_hierarchy = [planet.key, region_name]
```

## Command Permissions

- **Permission Required**: Builder or higher
- **Lock**: `cmd:perm(Builder)`
- **Who Can Use**: Staff only

## Related Systems

### Planet System
- **Command**: `+planet`
- **Purpose**: Create and manage planets
- **Integration**: Rooms reference planets created with +planet

### House System
- **Command**: `+house`
- **Purpose**: Manage noble houses
- **Integration**: Planets can be affiliated with houses

### Organization System
- **Command**: `+org`
- **Purpose**: Manage organizations
- **Integration**: Planets can host organizations

## Command Reference

### All +room Switches

| Switch | Usage | Description |
|--------|-------|-------------|
| (none) | `+room [<dbref>]` | View room information |
| /planet | `+room/planet <target>=<planet>` | Associate with planet |
| /area | `+room/area <target>=<name>/<code>` | Set area information |
| /hierarchy | `+room/hierarchy <target>=<p>,<r>` | Set location hierarchy |
| /places | `+room/places [<target>]` | Toggle places system |

### Target Options

- `here` - Current room
- `<dbref>` - Specific room by database reference
- (empty) - Current room (for viewing only)

## Troubleshooting Guide

### Planet Association Issues

**Problem**: Can't associate room with planet

**Check**:
1. Does the planet exist? (`+planet/list`)
2. Are you in a room or targeting a valid room?
3. Is the planet name spelled correctly?
4. Do you have Builder permissions?

### Hierarchy Display Issues

**Problem**: Room header shows wrong information

**Solutions**:
1. Check current hierarchy: `+room`
2. Update manually: `+room/hierarchy here=<planet>,<region>`
3. Re-associate with planet: `+room/planet here=<planet>`

### Permission Issues

**Problem**: "Permission denied" or command not found

**Solutions**:
1. Verify Builder permissions
2. Check command is loaded: `@reload`
3. Contact admin if needed

## Future Enhancements

### Planned Features

1. **Bulk Operations**
   ```bash
   +room/planet #101-#150=Vallabhi
   ```

2. **Room Templates**
   ```bash
   +room/template Vallabhi Mining Room
   ```

3. **Planet-Based Effects**
   ```bash
   +room/effects here
   # Shows planet-based environmental effects
   ```

4. **Search by Planet**
   ```bash
   +room/find planet=Vallabhi
   # Lists all rooms on Vallabhi
   ```

5. **Automatic Area Codes**
   ```bash
   +room/planet here=Vallabhi
   # Automatically assigns next available area code
   ```

## Summary

The room-planet integration provides:
- ✅ Complete planet association system
- ✅ Comprehensive validation
- ✅ Automatic hierarchy updates
- ✅ Flexible room targeting
- ✅ Clear error messages
- ✅ Full documentation
- ✅ Builder-friendly workflow
- ✅ Foundation for future features

The system is fully functional and ready to use after `@reload`.

