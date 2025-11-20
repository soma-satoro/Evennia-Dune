# Dune MUSH House System

## Overview

The House System implements the Noble House creation and management rules from Modiphius' Dune: Adventures in the Imperium 2d20 RPG system. This system allows staff (builder+) to create and manage Noble Houses that player characters can serve.

## Key Features

- **Four House Types**: Nascent House, House Minor, House Major, Great House
- **Domain System**: Primary and secondary areas of expertise (Artistic, Military, Political, etc.)
- **House Traits**: Gameplay traits that characters can access
- **Roles**: Key positions like Ruler, Heir, Spymaster, etc.
- **Enemy Houses**: Rivalries with different hatred levels
- **Homeworld Details**: Rich world-building information
- **Heraldry**: Banner colors and crest symbols

## Staff-Only Access

**All creation and editing commands require Builder permission or higher.** Only the viewing command (+house) is available to all players.

## House Types and Threat Levels

### Nascent House
- Just acquired Minor House status
- Starting Threat: 0 per player
- Domains: 0 primary, 1 secondary
- Small retinue, little land

### House Minor
- Established vassal House
- Starting Threat: 1 per player
- Domains: 1 primary, 1 secondary
- Controls ~1/3 of a planet

### House Major
- Ruling power of entire planet
- Starting Threat: 2 per player
- Domains: 1 primary, 2 secondary
- Several Minor Houses serve them

### Great House
- Controls multiple planets
- Starting Threat: 3 per player
- Domains: 2 primary, 3 secondary
- Legion of resources

## Domain Areas of Expertise

Each domain has a **type** and **subtype**:

### Domain Types
- **Artistic**: Plays, poetry, music, theater
- **Espionage**: Spies, intelligence, surveillance
- **Farming**: Agriculture, crops, animal products
- **Industrial**: Manufacturing, spacecraft, technology
- **Kanly**: Assassination, poisons, vendetta warfare
- **Military**: Soldiers, weapons, tactics
- **Political**: Diplomacy, court intrigue, favors
- **Religion**: Faith, clergy, religious artifacts
- **Science**: Research, drugs, genetic engineering

### Domain Subtypes
- **Machinery**: Large-scale equipment and devices
- **Produce**: Actual products or outputs
- **Expertise**: Leaders and specialists
- **Workers**: Staff and laborers
- **Understanding**: Theoretical knowledge and techniques

### Examples
- Primary: Artistic (Produce) - Poetry
- Secondary: Kanly (Workers) - Assassins
- Primary: Military (Expertise) - Tacticians
- Secondary: Political (Produce) - Information and secrets

## Commands Reference

### Viewing Houses (All Users)

#### +house <house name>
View detailed information about a Noble House.

```
+house Atreides
```

#### +house/list
List all Noble Houses in the game.

```
+house/list
```

### Creating Houses (Builder+)

#### +housecreate <name>=<type>
Create a new Noble House.

```
+housecreate Molay=House Minor
+housecreate Arcuri=House Minor
+housecreate Richese=House Major
```

### Setting House Properties (Builder+)

#### +houseset <house>/<switch>=<value>

**Switches:**
- `/type` - Set House type
- `/banner` - Set banner colors (comma-separated)
- `/crest` - Set House crest/symbol
- `/trait` - Add a House trait
- `/homeworld` - Set homeworld name
- `/desc` - Set homeworld description
- `/weather` - Set weather description
- `/habitation` - Set habitation type
- `/crime` - Set crime rate description
- `/populace` - Set populace mood
- `/wealth` - Set wealth distribution

**Examples:**
```
+houseset Molay/type=House Minor
+houseset Molay/banner=White,Red
+houseset Molay/crest=Scroll
+houseset Molay/trait=Secretive
+houseset Molay/trait=Artistic
+houseset Molay/homeworld=Molay Prime
+houseset Molay/desc=A string of large islands with varied terrain that inspire poets
+houseset Molay/weather=Temperate with seasonal storms
+houseset Molay/habitation=Sparse villages with one main town
+houseset Molay/crime=Low, strictly enforced
+houseset Molay/populace=Generally happy and artistic
+houseset Molay/wealth=Moderate, focused on arts and culture
```

### Managing Domains (Builder+)

#### +housedomain <house>/list
List current domains for a House.

```
+housedomain Molay/list
```

#### +housedomain <house>/areas
List all available domain areas and subtypes.

```
+housedomain Molay/areas
```

#### +housedomain <house>/add primary=<area>:<subtype>:<description>
Add a primary domain.

```
+housedomain Molay/add primary=Artistic:Produce:Renowned poetry and verse
+housedomain Richese/add primary=Industrial:Machinery:Advanced spacecraft
```

#### +housedomain <house>/add secondary=<area>:<subtype>:<description>
Add a secondary domain.

```
+housedomain Molay/add secondary=Kanly:Workers:Trained assassins
+housedomain Atreides/add secondary=Military:Expertise:Military tacticians
```

#### +housedomain <house>/remove primary|secondary=<number>
Remove a domain by number (from /list).

```
+housedomain Molay/remove secondary=1
```

### Managing Roles (Builder+)

#### +houserole <house>/list
List all roles and current holders.

```
+houserole Molay/list
```

#### +houserole <house>/set <role>=<character>[:<description>][:<traits>]
Assign a character to a role.

**Available Roles:**
- Ruler, Consort, Advisor, Chief Physician, Councilor, Envoy
- Heir, Marshal, Scholar, Spymaster, Swordmaster, Treasurer, Warmaster

**Examples:**
```
+houserole Molay/set Ruler=Lady Elara Molay:Wise and just:Honorable,Political
+houserole Molay/set Heir=Lord Marcus Molay:Young and ambitious
+houserole Molay/set Spymaster=Shadow Master Kael:Mysterious:Secretive
+houserole Atreides/set Ruler=Duke Leto Atreides:Noble and honorable:Honorable
+houserole Atreides/set Consort=Lady Jessica:Bene Gesserit concubine
```

#### +houserole <house>/remove <role>
Clear a role.

```
+houserole Molay/remove Advisor
```

### Managing Enemies (Builder+)

#### +houseenemy <house>/list
List all enemy Houses.

```
+houseenemy Molay/list
```

#### +houseenemy <house>/add=<enemy>:<hatred>:<reason>
Add an enemy House.

**Hatred Levels:**
- **Dislike**: +1 Difficulty to interactions
- **Rival**: Active political opposition
- **Loathing**: Plans destruction, but cautious
- **Kanly**: All-out blood feud

**Reasons:**
- Competition, Slight, Debt, Ancient Feud, Morality, Servitude
- Family Ties, Theft, Jealousy, No Reason

**Examples:**
```
+houseenemy Molay/add=House Arcuri:Loathing:Morality
+houseenemy Atreides/add=House Harkonnen:Kanly:Ancient Feud
+houseenemy Richese/add=House Vernius:Rival:Competition
```

#### +houseenemy <house>/remove=<number>
Remove an enemy by number.

```
+houseenemy Molay/remove=1
```

### Managing Members (Builder+)

#### +housemember <character>
Check which House a character serves.

```
+housemember Paul
```

#### +housemember <house>/list
List all members of a House.

```
+housemember Molay/list
```

#### +housemember <house>/add=<character>
Add a character to a House.

```
+housemember Molay/add=Paul
+housemember Atreides/add=Duncan
```

#### +housemember <house>/remove=<character>
Remove a character from a House.

```
+housemember Molay/remove=Paul
```

## Example: Creating House Molay

Here's a complete example of creating House Molay from the rulebook:

```
# 1. Create the House
+housecreate Molay=House Minor

# 2. Set banner and crest
+houseset Molay/banner=White,Red
+houseset Molay/crest=Scroll

# 3. Set homeworld details
+houseset Molay/homeworld=Molay Prime
+houseset Molay/desc=A string of large islands with varied terrain that inspire the greatest poets in the Imperium
+houseset Molay/weather=Temperate maritime climate with dramatic seasonal storms
+houseset Molay/habitation=Sparsely populated fishing villages and one main coastal town
+houseset Molay/crime=Low crime rate, strictly but fairly enforced
+houseset Molay/populace=Generally content, proud of their artistic heritage
+houseset Molay/wealth=Moderate, with public works supporting the arts

# 4. Add domains
+housedomain Molay/add primary=Artistic:Produce:Poetry - the most incredible verses in the universe
+housedomain Molay/add secondary=Kanly:Workers:Assassins trained in poetry schools

# 5. Add traits
+houseset Molay/trait=Secretive
# Note: Artistic trait is automatically added from primary domain

# 6. Set key roles
+houserole Molay/set Ruler=Lady Elara Molay:Wise patroness of the arts:Artistic,Honorable
+houserole Molay/set Heir=Lord Marcus Molay:Young poet and warrior
+houserole Molay/set Spymaster=The Verse Master:Runs the hidden assassin schools:Secretive

# 7. Add enemy House
+houseenemy Molay/add=House Arcuri:Loathing:Morality

# 8. Add members (characters)
+housemember Molay/add=YourCharacterName
```

## Example: Creating House Arcuri (Enemy)

```
# 1. Create the enemy House
+housecreate Arcuri=House Minor

# 2. Set banner
+houseset Arcuri/banner=Gold,Purple
+houseset Arcuri/crest=Holy Flame

# 3. Set domains
+housedomain Arcuri/add primary=Religion:Expertise:Puritanical clergy
+housedomain Arcuri/add secondary=Political:Expertise:Religious diplomats

# 4. Add traits
+houseset Arcuri/trait=Puritanical
+houseset Arcuri/trait=Religious

# 5. Set roles
+houserole Arcuri/set Ruler=Patriarch Severus Arcuri:Stern religious leader:Religious,Judgmental

# 6. Add the reciprocal enemy
+houseenemy Arcuri/add=House Molay:Loathing:Morality
```

## House Traits and Gameplay

Characters serving a House can use House traits during gameplay:

- **Spending 1 Momentum**: A player can apply one House trait to their character for the remainder of the scene
- **Multiple Uses**: Can spend Momentum multiple times to apply different House traits
- **Recognition Required**: Only works when the character is recognized as a member of that House

### Example Trait Usage
If House Molay has traits "Artistic" and "Secretive":
- During a poetry recital, spend 1 Momentum to use the "Artistic" trait
- During an infiltration, spend 1 Momentum to use the "Secretive" trait

## Technical Details

### Typeclass
- **File**: `typeclasses/houses.py`
- **Class**: `House(DefaultObject)`
- **Location**: None (Houses are abstract organizations)

### Commands
- **File**: `commands/dune/CmdHouse.py`
- **Added to**: `commands/dune/dune_cmdset.py` (DuneCmdSet)

### Permissions
- **Viewing**: All players can use `+house` and `+house/list`
- **Creation/Editing**: All other commands require Builder+ permission

### Data Storage
Houses store data using Evennia's attribute system (`.db`):
- `house_type` - House Type
- `primary_domains` - List of primary domain dicts
- `secondary_domains` - List of secondary domain dicts
- `banner_colors` - List of color names
- `crest` - Crest description
- `traits` - List of trait names
- `homeworld_name`, `homeworld_desc`, etc. - Homeworld details
- `roles` - Dict of role assignments
- `enemies` - List of enemy house dicts
- `members` - List of character DBRefs

### Character Integration
Characters link to their House via:
```python
character.db.house = house_object
```

House membership is stored in:
```python
house.db.members = [character_dbref1, character_dbref2, ...]
```

## Future Enhancements

Possible additions for future development:
- Resource management system
- House wealth and CHOAM shares tracking
- Territory control mechanics
- Political influence mechanics
- Alliance system between Houses
- House projects and construction
- Automated events based on enemy hatred levels
- Integration with character generation (auto-assign Houses)

## Credits

Based on the House creation system from:
**Dune: Adventures in the Imperium**
by Modiphius Entertainment
2d20 System

Implemented for Evennia MUD/MUSH by the staff of [Your MUSH Name].

## Support

For issues or questions about the House system:
1. Check this documentation
2. Use `help +house` (and other commands) in-game
3. Contact staff via +jobs or +staff channel

---

*"A House is not just a name or a banner. It is the people who serve it, the ideals it upholds, and the legacy it leaves."*

