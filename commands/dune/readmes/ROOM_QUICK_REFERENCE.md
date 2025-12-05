# Room Command Quick Reference

## Viewing
```
+room                                       View current room info
+room <dbref>                               View specific room info
```

## Planet Association (Builder+)
```
+room/planet here=<planet>                  Associate current room with planet
+room/planet <room>=<planet>                Associate room with planet
+room/planet here=                          Clear planet association
```

## Planetary Location (Builder+)
```
+room/location here=<location>              Set planetary location (city, etc)
+room/loc here=<location>                   Short form of /location
+room/location <room>=<location>            Set location for specific room
```

## Area Management (Builder+)
```
+room/area here=<name>/<code>               Set area name and code
+room/area <room>=<name>/<code>             Set area for specific room
```

## Location Hierarchy (Builder+)
```
+room/hierarchy here=<location>,<planet>    Set full location hierarchy
+room/hierarchy <room>=<location>,<planet>  Set hierarchy for room
```

## Places System (Builder+)
```
+room/places here                           Toggle places for current room
+room/places <room>                         Toggle places for specific room
```

## Quick Setup Example
```
# Create and configure room
@dig Nagara Square
@tel Nagara Square
+room/location here=Kyotashi
+room/planet here=Vallabhi
+room/area here=Palace District/PD01
+room

# Result: Room Name - Kyotashi - Vallabhi

# Set up another room remotely
+room/location #456=Arrakeen City
+room/planet #456=Arrakis
+room/area #456=Desert Outpost/DO05
```

## Common Tasks

### Set up complete room hierarchy
```
+room/location here=Kyotashi
+room/planet here=Vallabhi
```

### Associate current room with planet
```
+room/planet here=Vallabhi
```

### Set planetary location
```
+room/location here=Kyotashi
```

### Associate specific room with planet
```
+room/planet #123=Arrakis
```

### Clear planet association
```
+room/planet here=
```

### Set area information
```
+room/area here=Palace District/PD01
```

### View room details
```
+room
```

## Hierarchy Structure

Room headers display: **Room Name - Location - Planet**

Example: `Nagara Square - Kyotashi - Vallabhi`

- **Location**: Set with `+room/location` (city, district, region, etc)
- **Planet**: Set with `+room/planet` (automatically updates hierarchy)

## Validation

The `/planet` switch validates:
- Planet exists in the system
- Target is actually a room
- Planet name is unique (or prompts for clarification)

## Tips

- Create planets before associating rooms
- Set location first, then planet for best workflow
- Use `+planet/list` to see available planets
- Use dbrefs to work on rooms remotely
- `/planet` automatically updates the planet element of hierarchy
- `/location` (or `/loc`) sets the location element of hierarchy

