# Room Hierarchy System Update

## Overview

The room hierarchy system has been updated to provide a clearer, more intuitive structure for displaying room locations throughout the game world.

## Changes Made

### 1. Hierarchy Structure Change

**Previous Structure:**
```
Room Name - Planet - Region
```

**New Structure:**
```
Room Name - Location - Planet
```

This change makes the hierarchy more logical by moving from the specific (room) to the general (planet), with the immediate location (city, district, etc.) in between.

### 2. New Command: +room/location

Added a new switch to set the planetary location:

```bash
+room/location here=<location>
+room/loc here=<location>         # Short form
```

The location represents the immediate area on the planet, such as:
- City name (Kyotashi, Arrakeen City, etc.)
- District (Palace District, Industrial Zone, etc.)
- Region (Northern Mountains, Deep Desert, etc.)

### 3. Text Processing for Planet Notes

Planet notes now support special character substitutions:
- `%r` = newline/carriage return
- `%t` = tab character

This allows for better formatting of planet descriptions:

```bash
+planet/set Vallabhi/notes=First paragraph.%r%rSecond paragraph with%tindented text.
```

### 4. Automatic Hierarchy Updates

When you set the planet for a room, the system now:
- Updates the **second element** of the hierarchy (planet)
- Preserves the **first element** (location)
- Provides clear feedback about the updated hierarchy

## Implementation Details

### Modified Files

1. **typeclasses/planets.py**
   - Added import for `process_special_characters` from utils.text
   - Updated `get_display()` to process special characters in notes

2. **typeclasses/rooms.py**
   - Updated `at_object_creation()` to use new hierarchy structure
   - Changed default from `["Unknown Planet", "Unknown Region"]` to `["Unknown Location", "Unknown Planet"]`

3. **commands/dune/CmdRoom.py**
   - Updated help text to reflect new hierarchy
   - Added `set_location()` method for new `/location` and `/loc` switches
   - Modified `set_planet()` to update second element of hierarchy
   - Updated `set_hierarchy()` with new format and examples
   - Updated `func()` to route to new location handler

4. **Documentation Files Updated**
   - `commands/dune/ROOM_COMMAND_README.md`
   - `commands/dune/ROOM_QUICK_REFERENCE.md`
   - `commands/dune/README.md`
   - `commands/dune/PLANET_SYSTEM_README.md`
   - `PLANET_SYSTEM_SUMMARY.md`

## Usage Examples

### Setting Up a Room with New System

```bash
# Create planet first
+planet/create Vallabhi
+planet/set Vallabhi/type=Mineral World
+planet/set Vallabhi/star=Beta Tucanae IV

# Create and configure room
@dig Nagara Square
@tel Nagara Square

# Set location (city/district)
+room/location here=Kyotashi

# Set planet (automatically updates hierarchy)
+room/planet here=Vallabhi

# Set area code
+room/area here=Palace District/PD01

# View the result
+room
look
```

### Result

The room header will display:
```
====> Nagara Square - Kyotashi - Vallabhi <===
```

The `+room` info will show:
```
Location Hierarchy: Nagara Square - Kyotashi - Vallabhi
```

### Setting Planet Notes with Formatting

```bash
+planet/set Vallabhi/notes=Vallabhi is a mountainous world with deep valleys.%r%rIt has vast lakes rather than seas, and many islands. These islands are dangerous to live on due to unpredictable and violent tides.
```

This creates proper paragraph breaks in the planet display.

## Command Reference

### New/Updated Commands

| Command | Description |
|---------|-------------|
| `+room/location here=<location>` | Set planetary location (first element) |
| `+room/loc here=<location>` | Short form of /location |
| `+room/planet here=<planet>` | Set planet (second element, auto-updates) |
| `+room/hierarchy here=<loc>,<planet>` | Set full hierarchy manually |

### Hierarchy Elements

1. **First Element (Location)**: Set with `+room/location` or `+room/loc`
   - City name
   - District
   - Region
   - Any immediate location identifier

2. **Second Element (Planet)**: Set with `+room/planet`
   - Planet name from the planet system
   - Automatically validated against existing planets

## Workflow Recommendations

### Best Practice Workflow

1. **Create the planet** (if not already created)
2. **Dig the room**
3. **Set the location** first (`+room/location here=<city>`)
4. **Set the planet** second (`+room/planet here=<planet>`)
5. **Set area information** (`+room/area here=<name>/<code>`)

This order ensures the hierarchy is built logically from immediate to general.

### Example Workflow

```bash
# Step 1: Create planet
+planet/create Vallabhi
+planet/set Vallabhi/type=Mineral World

# Step 2: Build room
@dig Nagara Square
@tel Nagara Square

# Step 3: Set location
+room/loc here=Kyotashi

# Step 4: Set planet
+room/planet here=Vallabhi

# Step 5: Set area
+room/area here=PD01/Palace District

# Result: Nagara Square - Kyotashi - Vallabhi
```

## Backward Compatibility

### Existing Rooms

Rooms created before this update may have the old hierarchy structure. To update them:

```bash
@tel <old room>
+room/location here=<appropriate location>
+room/planet here=<planet name>
```

This will convert the hierarchy to the new format.

### Migration Strategy

For multiple rooms, use dbrefs to update remotely:

```bash
+room/location #123=Kyotashi
+room/planet #123=Vallabhi

+room/location #124=Kyotashi
+room/planet #124=Vallabhi

+room/location #125=Mining District
+room/planet #125=Vallabhi
```

## Benefits of New System

### 1. Logical Progression
The hierarchy now flows naturally: Room → Location → Planet

### 2. Clearer Context
Players immediately see what city/district they're in, then the planet

### 3. Better Organization
Easier to group rooms by location within a planet

### 4. Intuitive Commands
Separate commands for location and planet make the system clearer

### 5. Formatted Notes
Planet descriptions can now have proper paragraph breaks and formatting

## Visual Comparison

### Old System
```
====> Mining Complex - Vallabhi - Northern Mountains <===
```
Issue: Unclear if "Northern Mountains" is on Vallabhi or elsewhere

### New System
```
====> Nagara Square - Kyotashi - Vallabhi <===
```
Clear: Nagara Square is in Kyotashi, which is on Vallabhi

## Text Formatting in Planet Notes

### Before
```
+planet/set Arrakis/notes=Arrakis is a desert world.

The spice melange is found only here.
```
Result: Single line with awkward spacing

### After
```
+planet/set Arrakis/notes=Arrakis is a desert world.%r%rThe spice melange is found only here.
```
Result: Proper paragraph breaks in the display

## Technical Notes

### Hierarchy Storage

Hierarchy is stored as a 2-element list in `room.db.location_hierarchy`:
```python
[location, planet]
```

### Text Processing

Planet notes are processed through `utils.text.process_special_characters()` which:
- Converts `%r` to `\n`
- Converts `%t` to `\t`
- Handles other special characters consistently

### Validation

- Planet validation ensures planet exists before association
- Location can be any string (no validation required)
- Hierarchy is always maintained as exactly 2 elements

## Summary

The updated room hierarchy system provides:
- ✅ Clearer room location context
- ✅ Intuitive command structure
- ✅ Better text formatting for planet notes
- ✅ Logical progression from specific to general
- ✅ Easier room organization
- ✅ Backward compatible with migration path

All changes are live after `@reload`.

