# Dune MUSH House System

## Overview

The House System implements the Noble House creation and management rules from Modiphius' Dune: Adventures in the Imperium 2d20 RPG system. This system allows staff (builder+) to create and manage Noble Houses that player characters can serve.

## Key Features

- **Four House Types**: Nascent House, House Minor, House Major, Great House
- **Status and Reputation**: 0-100 status scale with six reputation levels affecting gameplay
- **House Skills**: Five key capabilities (Battle, Communicate, Discipline, Move, Understand)
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

## House Skills

Each House has five skills representing its collective capabilities and resources:

### The Five Skills

1. **Battle** - Military power and tactical skill
   - Quality of soldiers, spacecraft, and weapons
   - Leadership of generals and tacticians
   - Strategic positioning of forces
   
2. **Communicate** - Diplomatic reputation and influence
   - Court standing and political favors
   - Spy networks and intelligence gathering
   - Diplomatic corps and envoys
   
3. **Discipline** - Loyalty and internal stability
   - Loyalty of subjects and forces
   - Resistance to infiltration
   - Internal security and morale
   
4. **Move** - Response time and crisis management
   - Well-placed agents across the Imperium
   - Rapid deployment capability
   - Crisis response (both military and diplomatic)
   
5. **Understand** - Academic excellence and innovation
   - Scientific research capabilities
   - Technological advancement
   - Artistic and craft mastery

### Starting Skill Values

Assign these values to your five skills in any order:

- **Great House:** 9, 8, 7, 6, 5
- **House Major:** 8, 7, 6, 5, 4
- **House Minor:** 7, 6, 6, 5, 4
- **Nascent House:** 6, 5, 5, 4, 4

**See:** `HOUSE_SKILLS_README.md` for detailed skill descriptions and usage guidelines.
**See:** `HOUSE_SKILLS_QUICK_REFERENCE.md` for quick reference and examples.

## Status and Reputation

Each House has a **Status** rating (0-100) that determines its **Reputation** in the Landsraad and broader Imperium. Reputation has significant mechanical effects on House actions.

### Status Scale
- **0-100 range:** Represents political power and influence
- **Dynamic:** Changes based on House actions and events
- **Type-dependent:** Same status means different things for different House types

### Six Reputation Levels

| Reputation | Effect Summary |
|------------|----------------|
| **Feeble** | Aggressive actions +2 Diff / Gaining allies +2 Diff |
| **Weak** | Aggressive actions +1 Diff / Gaining allies +1 Diff |
| **Respected** | No modifiers (baseline) |
| **Strong** | All House actions -1 Diff |
| **Problematic** | Aggressive -2 Diff / Diplomatic +1 Diff / +1 Threat |
| **Dangerous** | Actions -2 Diff / Diplomatic +2 Diff / +1 Threat per action |

### Status Thresholds by House Type

**House Minor (and Nascent):**
- Feeble: 0-10 | Weak: 11-20 | Respected: 21-40
- Strong: 41-50 | Problematic: 51-70 | Dangerous: 71+
- Starting: Nascent 15, Minor 25

**House Major:**
- Feeble: 0-20 | Weak: 21-40 | Respected: 41-60
- Strong: 61-70 | Problematic: 71-80 | Dangerous: 81+
- Starting: 45

**Great House:**
- Feeble: 0-40 | Weak: 41-60 | Respected: 61-70
- Strong: 71-80 | Problematic: 81-90 | Dangerous: 91+
- Starting: 65

### Key Concepts

- **Most Houses are "Respected"** - This is the baseline, expected position
- **"Feeble" and "Weak"** - Make actions harder, House is vulnerable
- **"Strong"** - Sweet spot of success without drawing too much attention
- **"Problematic" and "Dangerous"** - Powerful but isolated, generating opposition

**See:** `HOUSE_STATUS_REPUTATION_README.md` for complete documentation.
**See:** `HOUSE_STATUS_QUICK_REFERENCE.md` for quick reference and thresholds.

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

#### +house/create <name>=<type>
Create a new Noble House.

```
+house/create Molay=House Minor
+house/create Arcuri=House Minor
+house/create Richese=House Major
```

### Managing House Skills (Builder+)

#### +house/skill <house>/values
View recommended skill values and current settings.

```
+house/skill Molay/values
```

#### +house/skill <house>/init=<b>,<c>,<d>,<m>,<u>
Initialize all five skills at once (Battle, Communicate, Discipline, Move, Understand).

```
+house/skill Molay/init=7,6,6,5,4
+house/skill Atreides/init=8,9,8,7,6
```

#### +house/skill <house>/set <skill>=<value>
Set an individual skill value.

```
+house/skill Molay/set Battle=8
+house/skill Atreides/set Communicate=9
```

### Managing House Status (Builder+)

#### +house/status <house>
View current status and reputation summary.

```
+house/status Molay
```

#### +house/status <house>/set=<value>
Set status to a specific value (0-100).

```
+house/status Molay/set=30
+house/status Atreides/set=75
```

#### +house/status <house>/adjust=<+/-amount>
Adjust status by a relative amount.

```
+house/status Molay/adjust=+5
+house/status Harkonnen/adjust=-10
```

#### +house/status <house>/reputation
View detailed reputation information including thresholds and effects.

```
+house/status Molay/reputation
```

### Setting House Properties (Builder+)

#### +house/set <house>/<switch>=<value>

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
+house/set Molay/type=House Minor
+house/set Molay/banner=White,Red
+house/set Molay/crest=Scroll
+house/set Molay/trait=Secretive
+house/set Molay/trait=Artistic
+house/set Molay/homeworld=Molay Prime
+house/set Molay/desc=A string of large islands with varied terrain that inspire poets
+house/set Molay/weather=Temperate with seasonal storms
+house/set Molay/habitation=Sparse villages with one main town
+house/set Molay/crime=Low, strictly enforced
+house/set Molay/populace=Generally happy and artistic
+house/set Molay/wealth=Moderate, focused on arts and culture
```

### Managing Domains (Builder+)

#### +house/domain <house>/list
List current domains for a House.

```
+house/domain Molay/list
```

#### +house/domain <house>/areas
List all available domain areas and subtypes.

```
+house/domain Molay/areas
```

#### +house/domain <house>/add primary=<area>:<subtype>:<description>
Add a primary domain.

```
+house/domain Molay/add primary=Artistic:Produce:Renowned poetry and verse
+house/domain Richese/add primary=Industrial:Machinery:Advanced spacecraft
```

#### +house/domain <house>/add secondary=<area>:<subtype>:<description>
Add a secondary domain.

```
+house/domain Molay/add secondary=Kanly:Workers:Trained assassins
+house/domain Atreides/add secondary=Military:Expertise:Military tacticians
```

#### +house/domain <house>/remove primary|secondary=<number>
Remove a domain by number (from /list).

```
+house/domain Molay/remove secondary=1
```

### Managing Roles (Builder+)

#### +house/role <house>/list
List all roles and current holders.

```
+house/role Molay/list
```

#### +house/role <house>/set <role>=<character>[:<description>][:<traits>]
Assign a character to a role.

**Available Roles:**
- Ruler, Consort, Advisor, Chief Physician, Councilor, Envoy
- Heir, Marshal, Scholar, Spymaster, Swordmaster, Treasurer, Warmaster

**Examples:**
```
+house/role Molay/set Ruler=Lady Elara Molay:Wise and just:Honorable,Political
+house/role Molay/set Heir=Lord Marcus Molay:Young and ambitious
+house/role Molay/set Spymaster=Shadow Master Kael:Mysterious:Secretive
+house/role Atreides/set Ruler=Duke Leto Atreides:Noble and honorable:Honorable
+house/role Atreides/set Consort=Lady Jessica:Bene Gesserit concubine
```

#### +house/role <house>/remove <role>
Clear a role.

```
+house/role Molay/remove Advisor
```

### Managing Enemies (Builder+)

#### +house/enemy <house>/list
List all enemy Houses.

```
+house/enemy Molay/list
```

#### +house/enemy <house>/add=<enemy>:<hatred>:<reason>
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
+house/enemy Molay/add=House Arcuri:Loathing:Morality
+house/enemy Atreides/add=House Harkonnen:Kanly:Ancient Feud
+house/enemy Richese/add=House Vernius:Rival:Competition
```

#### +house/enemy <house>/remove=<number>
Remove an enemy by number.

```
+house/enemy Molay/remove=1
```

### Managing Members (Builder+)

#### +house/member <character>
Check which House a character serves.

```
+house/member Paul
```

#### +house/member <house>/list
List all members of a House.

```
+house/member Molay/list
```

#### +house/member <house>/add=<character>
Add a character to a House.

```
+house/member Molay/add=Paul
+house/member Atreides/add=Duncan
```

#### +house/member <house>/remove=<character>
Remove a character from a House.

```
+house/member Molay/remove=Paul
```

## Example: Creating House Molay

Here's a complete example of creating House Molay from the rulebook:

```
# 1. Create the House (automatically sets status to 25)
+house/create Molay=House Minor
# Default status: 25 (Respected)

# 2. Set banner and crest
+house/set Molay/banner=White,Red
+house/set Molay/crest=Scroll

# 3. Assign House Skills (Minor House: 7,6,6,5,4)
+house/skill Molay/values
# Review the recommendations, then assign:
+house/skill Molay/init=6,7,5,4,6
# Battle: 6 (adequate military)
# Communicate: 7 (strong political/artistic connections)
# Discipline: 5 (moderate loyalty)
# Move: 4 (slower response)
# Understand: 6 (artistic excellence)

# 4. Adjust status if needed (optional)
+house/status Molay
# Check current status and reputation
# Can adjust: +house/status Molay/adjust=+/-amount

# 5. Set homeworld details
+house/set Molay/homeworld=Molay Prime
+house/set Molay/desc=A string of large islands with varied terrain that inspire the greatest poets in the Imperium
+house/set Molay/weather=Temperate maritime climate with dramatic seasonal storms
+house/set Molay/habitation=Sparsely populated fishing villages and one main coastal town
+house/set Molay/crime=Low crime rate, strictly but fairly enforced
+house/set Molay/populace=Generally content, proud of their artistic heritage
+house/set Molay/wealth=Moderate, with public works supporting the arts

# 6. Add domains
+house/domain Molay/add primary=Artistic:Produce:Poetry - the most incredible verses in the universe
+house/domain Molay/add secondary=Kanly:Workers:Assassins trained in poetry schools

# 7. Add traits
+house/set Molay/trait=Secretive
# Note: Artistic trait is automatically added from primary domain

# 8. Set key roles
+house/role Molay/set Ruler=Lady Elara Molay:Wise patroness of the arts:Artistic,Honorable
+house/role Molay/set Heir=Lord Marcus Molay:Young poet and warrior
+house/role Molay/set Spymaster=The Verse Master:Runs the hidden assassin schools:Secretive

# 9. Add enemy House
+house/enemy Molay/add=House Arcuri:Loathing:Morality

# 10. Add members (characters)
+house/member Molay/add=YourCharacterName
```

## Example: Creating House Arcuri (Enemy)

```
# 1. Create the enemy House
+house/create Arcuri=House Minor

# 2. Set banner
+house/set Arcuri/banner=Gold,Purple
+house/set Arcuri/crest=Holy Flame

# 3. Assign House Skills (Minor House: 7,6,6,5,4)
+house/skill Arcuri/init=5,7,7,4,6
# Battle: 5 (modest military)
# Communicate: 7 (strong religious diplomacy)
# Discipline: 7 (zealous loyalty through faith)
# Move: 4 (bureaucratic, slower)
# Understand: 6 (theological scholarship)

# 4. Set domains
+house/domain Arcuri/add primary=Religion:Expertise:Puritanical clergy
+house/domain Arcuri/add secondary=Political:Expertise:Religious diplomats

# 5. Add traits
+house/set Arcuri/trait=Puritanical
+house/set Arcuri/trait=Religious

# 6. Set roles
+house/role Arcuri/set Ruler=Patriarch Severus Arcuri:Stern religious leader:Religious,Judgmental

# 7. Add the reciprocal enemy
+house/enemy Arcuri/add=House Molay:Loathing:Morality
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
- **Status and Reputation system** (planned next)
- **Domain roles and benefits** (planned next)
- **Planet resources and wealth generation** (planned next)
- **Ventures system** - Projects to improve House skills
- **Skill maintenance costs** - Wealth required to maintain skills
- **Skill degradation** - Skills decrease without investment
- Resource management system
- House wealth and CHOAM shares tracking
- Territory control mechanics
- Political influence mechanics
- Alliance system between Houses
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

