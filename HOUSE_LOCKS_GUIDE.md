# House-Based Lock Functions Guide

## Overview

This guide covers the lock functions available for restricting movement and access based on House affiliation. These locks can be applied to exits, objects, and commands to create House-specific areas and restrictions.

## Available Lock Functions

### Basic House Checks

#### `house(House Name)`
Checks if a character serves a specific House.

**Usage:**
```
@lock/traverse north = house(House Atreides)
@lock/traverse palace_door = house(Atreides)
```

**Examples:**
- Palace entrance restricted to House Atreides members
- Private quarters accessible only to house members
- House-specific training facilities

#### `hashouse()`
Checks if a character serves ANY House.

**Usage:**
```
@lock/traverse diplomatic_hall = hashouse()
```

**Examples:**
- Landsraad chambers (any House member)
- Noble-only areas
- Political gathering spaces

#### `nohouse()`
Checks if a character serves NO House (independent/unaffiliated).

**Usage:**
```
@lock/traverse smuggler_den = nohouse()
```

**Examples:**
- Criminal underworld areas
- Independent trader zones
- Areas hostile to nobility

### House Type Checks

#### `housetype(Type)`
Checks if a character's House is of a specific type.

**Valid Types:**
- `Nascent House` or `Nascent`
- `House Minor` or `Minor`
- `House Major` or `Major`
- `Great House` or `Great`

**Usage:**
```
@lock/traverse imperial_court = housetype(Great)
@lock/traverse landsraad_chamber = housetype(Major)
```

**Examples:**
- Imperial Court (Great Houses only)
- Major House council chambers
- Tier-restricted facilities

#### `housemintype(Type)`
Checks if a character's House meets a MINIMUM type requirement.

**Hierarchy:** Nascent < Minor < Major < Great

**Usage:**
```
@lock/traverse restricted_wing = housemintype(Minor)
```

**Result:**
- `housemintype(Minor)` - Allows Minor, Major, Great (NOT Nascent)
- `housemintype(Major)` - Allows Major, Great (NOT Minor or Nascent)
- `housemintype(Great)` - Allows Great only

**Examples:**
- VIP areas requiring established Houses
- Strategic meeting rooms for Major Houses and above
- Great House exclusive spaces

### Multiple House Access

#### `houseor(House1, House2, ...)`
Checks if a character serves ONE of multiple specified Houses (allied access).

**Usage:**
```
@lock/traverse alliance_hall = houseor(Atreides, Molay, Vernius)
@lock/traverse trade_office = houseor(House Atreides, House Richese)
```

**Examples:**
- Allied House meeting rooms
- Shared facilities between friendly Houses
- Multi-House diplomatic spaces
- Coalition headquarters

### Exclusion Locks

#### `not_house(House Name)`
Checks if a character does NOT serve a specific House (enemy exclusion).

**Usage:**
```
@lock/traverse atreides_compound = not_house(Harkonnen)
@lock/traverse secure_area = not_house(House Ordos)
```

**Examples:**
- Blocking enemy Houses from facilities
- War-time restrictions
- Hostile territory markers
- Kanly-related exclusions

### Role-Based Locks

#### `houserole(Role Name)`
Checks if a character holds a specific role in their House.

**Valid Roles:**
- Ruler, Consort, Advisor, Chief Physician
- Councilor, Envoy, Heir, Marshal
- Scholar, Spymaster, Swordmaster, Treasurer, Warmaster

**Usage:**
```
@lock/traverse war_room = houserole(Warmaster)
@lock/traverse treasury = houserole(Treasurer)
@lock/traverse throne_room = houserole(Ruler)
```

**Examples:**
- War room (Warmaster only)
- Treasury (Treasurer only)
- Throne room (Ruler and Consort only)
- Intelligence center (Spymaster only)

### Future/Placeholder

#### `housealliance(House Name)`
Checks if character's House is allied with specified House.

**Status:** Placeholder for future alliance system

## Combining Locks

You can combine multiple lock functions for complex access control:

### AND Logic (all must pass)
```
@lock/traverse secure_vault = house(Atreides) AND houserole(Treasurer)
```
Only House Atreides Treasurer can enter.

### OR Logic (any can pass)
```
@lock/traverse command_center = houserole(Ruler) OR houserole(Warmaster)
```
Either Ruler or Warmaster can enter.

### NOT Logic (inverse)
```
@lock/traverse public_plaza = NOT house(Harkonnen)
```
Anyone except Harkonnen House members.

### Complex Combinations
```
@lock/traverse diplomatic_suite = (houseor(Atreides, Molay) OR housemintype(Major)) AND not_house(Harkonnen)
```
Accessible to:
- House Atreides members
- House Molay members
- Any Major or Great House member
- BUT NOT House Harkonnen members

## Practical Examples

### House Atreides Palace Complex

**Main Entrance**
```
@lock/traverse palace_entrance = house(Atreides) OR perm(Builder)
@desc palace_entrance = A grand entrance to the Atreides palace. Only house members may enter.
```

**Throne Room**
```
@lock/traverse throne_room = houserole(Ruler) OR houserole(Consort) OR houserole(Heir)
@desc throne_room = The seat of House Atreides power. Only the ruling family may enter.
```

**War Room**
```
@lock/traverse war_room = house(Atreides) AND (houserole(Warmaster) OR houserole(Ruler) OR perm(Builder))
@desc war_room = Strategic planning center. Restricted to military leadership.
```

**Treasury Vault**
```
@lock/traverse vault = house(Atreides) AND houserole(Treasurer)
@desc vault = The House treasury. Only the Treasurer has access.
```

**Guest Quarters**
```
@lock/traverse guest_wing = hashouse()
@desc guest_wing = Guest quarters for visiting nobles.
```

### Multi-House Scenarios

**Allied Coalition Headquarters**
```
@lock/traverse coalition_hq = houseor(Atreides, Molay, Vernius)
@desc coalition_hq = Headquarters for the allied Houses.
```

**Landsraad Assembly Hall**
```
@lock/traverse assembly = housemintype(Minor)
@desc assembly = The Landsraad assembly. All recognized Houses may enter.
```

**Imperial Court**
```
@lock/traverse imperial_court = housetype(Great) OR perm(Admin)
@desc imperial_court = The Imperial Court. Only Great Houses may attend.
```

### Hostile Territory

**Enemy Exclusion**
```
@lock/traverse atreides_territory = not_house(Harkonnen)
@desc atreides_territory = Atreides-controlled space. Harkonnen agents are not welcome.
```

**Kanly War Zone**
```
@lock/traverse battlefield = houseor(Atreides, Harkonnen)
@desc battlefield = Active Kanly zone. Only the feuding Houses may enter.
```

### Public vs. Noble Areas

**Public Square (anyone)**
```
@lock/traverse public_square = all()
@desc public_square = A bustling public square open to all.
```

**Noble Quarter (any House)**
```
@lock/traverse noble_quarter = hashouse()
@desc noble_quarter = Residential area for noble Houses.
```

**Commoner District (no House)**
```
@lock/traverse commoner_district = nohouse() OR perm(Builder)
@desc commoner_district = Working class neighborhood. Nobles may face hostility here.
```

## Setting Locks on Exits

### Using @lock Command

**Basic Syntax:**
```
@lock/traverse <exit name> = <lock function>
```

**Examples:**
```
@lock/traverse north = house(Atreides)
@lock/traverse palace_door = houserole(Ruler)
@lock/traverse secure_passage = housemintype(Major)
```

### Using @dig with Locks

When creating exits, you can set locks immediately:

```
@dig Palace;palace,p = palace_entrance,out;palace_exit,o = 
@lock/traverse palace_entrance = house(Atreides)
```

### Lock Bypass for Staff

Always include staff bypass for testing and admin access:

```
@lock/traverse restricted_area = house(Atreides) OR perm(Builder)
```

This ensures Builders and above can always access for maintenance.

## Testing Locks

### Check if Lock Works
```
@examine <exit>
```
Look for the "Lock" section showing the lock string.

### Test with Different Characters
1. Create test characters with different House affiliations
2. Try to traverse the locked exit
3. Verify correct access granted/denied

### Debug Lock Issues
```
@examine/locks <exit>
```
Shows detailed lock information.

## Lock Error Messages

### Customizing Failure Messages

When a character fails a lock check, you can customize the message:

```
@lock/traverse palace_entrance = house(Atreides)
@fail palace_entrance = The guards cross their spears. "Only House Atreides may enter."
```

**Examples:**
```
@fail war_room = "This area is restricted to military leadership."
@fail treasury = "The vault door remains sealed. Only the Treasurer has the key."
@fail imperial_court = "Only Great Houses may attend the Imperial Court."
@fail enemy_territory = "You sense hostile attention. This is dangerous ground for you."
```

## Best Practices

### 1. Clear Lock Purpose
Always document why a lock exists in the room description.

### 2. Graceful Degradation
Include staff bypasses:
```
@lock/traverse area = <condition> OR perm(Builder)
```

### 3. Consistent Lock Patterns
Use similar locks for similar security levels across your game.

### 4. Player Communication
Use @fail messages to explain WHY access was denied:
```
@fail entrance = "This facility is restricted to House Atreides members."
```

### 5. Test Thoroughly
Test locks with characters from:
- The allowed House
- Different Houses
- No House affiliation
- Different roles

### 6. Layer Security
Combine multiple checkpoints:
```
Palace Entrance → house(Atreides)
Inner Palace → house(Atreides) AND hashouse()
Throne Room → house(Atreides) AND houserole(Ruler)
```

### 7. Emergency Access
Always have a way for admins to access locked areas:
```
@lock/traverse critical_area = <lock> OR perm(Admin)
```

## Common Patterns

### Pattern: House Headquarters
```
Main Gate: house(YourHouse) OR perm(Builder)
Public Areas: house(YourHouse) OR hashouse() [guests]
Private Wing: house(YourHouse)
War Room: house(YourHouse) AND houserole(Warmaster)
Treasury: house(YourHouse) AND houserole(Treasurer)
Throne: houserole(Ruler) OR houserole(Heir)
```

### Pattern: Diplomatic Facility
```
Entrance: housemintype(Minor) [all recognized Houses]
Meeting Rooms: houseor(House1, House2) [specific Houses]
Great Hall: hashouse() [any noble]
Secure Room: housemintype(Major) AND not_house(Enemy)
```

### Pattern: Hostile Territory
```
Border: not_house(EnemyHouse)
Checkpoints: house(YourHouse) OR perm(Builder)
Inner Sanctum: house(YourHouse) AND houserole(Spymaster)
```

## Troubleshooting

### Lock Not Working

**Check:**
1. Lock string syntax correct?
2. House name spelled correctly? (case-insensitive but must match)
3. Character actually has house attribute set?
4. Staff bypass included for testing?

**Debug:**
```
@examine/locks <exit>
@py accessing_obj.db.house
@py accessing_obj.db.house.key if accessing_obj.db.house else "No house"
```

### Character Can't Move

**Check:**
1. Is there a lock on the exit?
2. Does character have required house affiliation?
3. Is role requirement met if using houserole()?
4. Check @fail message for clue

### All Characters Blocked

**Likely Issue:** Lock syntax error or missing condition

**Fix:**
```
@lock/del/traverse <exit>  # Remove broken lock
@lock/traverse <exit> = <corrected lock>
```

## Security Considerations

### Don't Rely Solely on Locks

Locks prevent movement but don't prevent:
- Teleportation by staff
- Looking into rooms
- Remote commands
- Admin access

### Additional Security

For truly sensitive areas, combine:
1. Movement locks (traverse)
2. Description locks (view)
3. Command locks (cmd)
4. Object locks on items within

**Example Full Security:**
```
@lock room = house(Atreides) OR perm(Builder)
@lock/view room = house(Atreides) OR perm(Builder)
@lock/traverse entrance = house(Atreides) OR perm(Builder)
```

## Future Enhancements

### Planned Lock Functions

1. **`housestatus(min, max)`** - Check House status level
2. **`housealliance(House)`** - Check if allied (when alliance system added)
3. **`houseenemy(House)`** - Check if at war (inverse of alliance)
4. **`housereputation(level)`** - Check House reputation
5. **`houseskill(skill, min)`** - Check if House skill meets minimum

---

*"Control access, control power. A lock is not just security—it's a statement of authority."*

