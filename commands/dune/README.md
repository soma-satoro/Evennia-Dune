# Dune MUSH - 2d20 System Commands

This directory contains commands specific to the Dune MUSH implementation using the Modiphus 2d20 system.

## Overview

The Dune MUSH uses the Modiphus 2d20 system, which features:
- Attribute + Skill based tests
- Rolling 2d20 (or more) against a target number
- Success counting (rolling equal or under the target)
- Critical successes (rolling 1 = 2 successes)
- Complications (rolling 20)
- Momentum (group resource)
- Determination (individual hero points)

## Commands

### Character Management

#### +sheet
Display your character sheet or another character's sheet.

**Usage:**
```
+sheet
+sheet <character name>
+sheet/full
```

**Switches:**
- `/full` - Display extended information including background

**Examples:**
```
+sheet - View your own character sheet
+sheet Paul - View Paul's character sheet
+sheet/full - View your full character sheet with background
```

#### +stats (Staff Only)
Set or view character statistics.

**Usage:**
```
+stats <character>
+stats <character>/<type>/<stat>=<value>
```

**Types:**
- `attr` - Attributes (control, dexterity, fitness, insight, presence, reason)
- `skill` - Skills (battle, communicate, discipline, move, understand)

**Examples:**
```
+stats Paul - View Paul's stats
+stats Paul/attr/fitness=9 - Set Paul's fitness to 9
+stats Paul/skill/battle=3 - Set Paul's battle skill to 3
```

#### +focus
Manage character focuses (skill specializations).

**Usage:**
```
+focus - List your focuses
+focus/add <skill>: <specialization> - Add a focus
+focus/remove <focus> - Remove a focus
```

**Examples:**
```
+focus/add Battle: Knife Fighting
+focus/remove Battle: Knife Fighting
```

#### +stress
Manage character stress (damage).

**Usage:**
```
+stress - View your current stress
+stress <character> - View another character's stress
+stress/take <amount> - Take stress damage
+stress/heal <amount> - Heal stress
+stress/set <character>=<amount> - Set stress (staff only)
```

**Examples:**
```
+stress - Check your stress
+stress/take 3 - Take 3 stress
+stress/heal 2 - Heal 2 stress
```

### Dice Rolling

#### +roll
Roll dice using the 2d20 system.

**Usage:**
```
+roll <attribute> + <skill>
+roll <attribute> + <skill> vs <difficulty>
+roll <attribute> + <skill> vs <difficulty> focus
+roll <attribute> + <skill> vs <difficulty> bonus <dice>
+roll/private <attribute> + <skill> vs <difficulty>
```

**Switches:**
- `/private` or `/p` - Only you see the result

**Attributes:**
- control, dexterity, fitness, insight, presence, reason

**Skills:**
- battle, communicate, discipline, move, understand

**The 2d20 System:**
- Roll 2d20 (or more with assists)
- Each die that rolls equal or under (Attribute + Skill) is a success
- Rolling a 1 generates 2 successes (critical!)
- Rolling a 20 is a complication
- Having a relevant focus lets you roll an extra d20
- You need to meet or exceed the difficulty to succeed
- Extra successes generate Momentum for the group

**Examples:**
```
+roll fitness + battle - Simple roll
+roll fitness + battle vs 2 - Roll against difficulty 2
+roll fitness + battle vs 2 focus - Roll with a relevant focus
+roll control + communicate vs 3 bonus 1 - Roll with 1 bonus die
+roll/private insight + understand vs 2 - Private roll only you see
```

#### +momentum
Manage the group Momentum pool.

**Usage:**
```
+momentum - View current momentum
+momentum/spend <amount> - Spend momentum
+momentum/add <amount> - Add momentum (staff/GM)
+momentum/set <amount> - Set momentum (staff/GM)
+momentum/reset - Reset momentum to 0 (staff/GM)
```

Momentum is a group resource that can be spent to:
- Add extra dice to rolls
- Activate special abilities
- Create advantages in scenes
- Obtain information

**Examples:**
```
+momentum - Check current momentum
+momentum/spend 2 - Spend 2 momentum
+momentum/add 3 - Add 3 momentum (GM)
```

#### +determination
Manage your character's Determination points.

**Usage:**
```
+determination - View your determination
+determination/spend - Spend 1 determination for a special action
+determination/add <character>=<amount> - Award determination (staff)
```

Determination can be spent to:
- Re-roll a failed test
- Perform a heroic action
- Resist a serious consequence
- Activate powerful abilities

**Examples:**
```
+determination - Check your determination
+determination/spend - Spend 1 determination
+determination/add Paul=1 - Award Paul 1 determination (staff)
```

## Character Stats Structure

### Attributes (range 6-12 for humans)
- **Control** - Mental discipline and willpower
- **Dexterity** - Physical coordination and agility
- **Fitness** - Physical health and endurance
- **Insight** - Awareness and intuition
- **Presence** - Force of personality and leadership
- **Reason** - Intelligence and logic

### Skills (range 0-5)
- **Battle** - Combat and warfare
- **Communicate** - Social interaction and persuasion
- **Discipline** - Mental fortitude and focus
- **Move** - Physical movement and athletics
- **Understand** - Knowledge and comprehension

### Focuses
Specializations within skills that provide bonus dice when relevant.
Format: "Skill: Specialization"
Example: "Battle: Knife Fighting", "Communicate: Persuasion"

### Resources
- **Stress** - Current damage (max = Fitness + Discipline)
- **Determination** - Hero points for special actions (typically 3)
- **Experience** - XP for character advancement

### Other Character Info
- **Traits** - Special abilities and characteristics
- **Assets** - Resources, items, and special possessions
- **Drives** - Character motivations (duty, faith, justice, power, truth)
- **House** - Great House affiliation
- **Faction** - Organization membership

## Integration

These commands are automatically added to all characters through the `DuneCmdSet` in `commands/dune/dune_cmdset.py`, which is included in the `CharacterCmdSet` in `commands/default_cmdsets.py`.

## Files

### Commands
- `CmdSheet.py` - Character sheet and stats management commands
- `CmdRoll.py` - Dice rolling and resource management commands
- `CmdHouse.py` - Noble House creation and management commands (staff only)
- `CmdRoster.py` - Roster viewing and management commands
- `CmdOrganization.py` - Organization (School/Guild/Order/Faction) commands (staff only)
- `dune_cmdset.py` - Command set definition
- `__init__.py` - Package initialization

### Documentation
- `README.md` - This file
- `HOUSE_SYSTEM_README.md` - Complete House system documentation
- `HOUSE_QUICK_REFERENCE.md` - Quick reference for House commands
- `ROSTER_SYSTEM_README.md` - Complete roster system documentation
- `ROSTER_QUICK_REFERENCE.md` - Quick reference for roster commands

### House Management

A comprehensive Noble House system allows staff to create and manage the Great Houses of the Imperium. Players can view House information and characters can be assigned to serve specific Houses.

**For detailed House system documentation, see:**
- `HOUSE_SYSTEM_README.md` - Complete House system documentation
- `HOUSE_QUICK_REFERENCE.md` - Quick command reference

### Roster System

A detailed roster system tracks membership in Houses and Organizations (Schools, Guilds, Orders, Factions) with titles, descriptions, and roles. Characters can belong to one House and multiple Organizations.

**For detailed roster system documentation, see:**
- `ROSTER_SYSTEM_README.md` - Complete roster system documentation
- `ROSTER_QUICK_REFERENCE.md` - Quick command reference

#### +house (All Players)
View Noble House information.

**Usage:**
```
+house <name> - View House details
+house/list - List all Houses
```

**Examples:**
```
+house Atreides
+house Molay
+house/list
```

#### House Creation Commands (Staff Only - Builder+)

All House creation and editing commands require Builder permission or higher.

**Commands:**
- `+housecreate <name>=<type>` - Create a new House
- `+houseset <house>/<switch>=<value>` - Set House properties
- `+housedomain <house>/...` - Manage domains (areas of expertise)
- `+houserole <house>/...` - Manage House roles (Ruler, Heir, etc.)
- `+houseenemy <house>/...` - Manage enemy Houses
- `+housemember <house>/...` - Manage House membership

#### Roster Commands

View and manage organizational rosters with detailed member information.

**Viewing (All Players):**
```
+roster <org> - View roster
+roster/members <org> - Members only view
+roster/full <org> - Full detailed view
```

**Management (Staff Only - Builder+):**
```
+rosterset <org>/add <character>=<title>:<description>
+rosterset <org>/remove <character>
+rosterset <org>/title <character>=<title>
+rosterset <org>/desc <character>=<description>
```

**Examples:**
```
+roster Atreides
+roster Bene Gesserit
+rosterset Molay/add Paul=Master Poet:Lead instructor
```

#### Organization Commands (Staff Only - Builder+)

Create and manage Schools, Guilds, Orders, and Factions.

**Commands:**
```
+org <name> - View organization
+org/list [type] - List all organizations
+orgcreate <name>=<type> - Create new (school, guild, order, faction)
+orgset <org>/<switch>=<value> - Configure organization
+orgrole <org>/... - Manage organization positions
```

**Examples:**
```
+orgcreate Bene Gesserit=school
+orgset Bene Gesserit/trait=Secretive
+orgset Bene Gesserit/headquarters=Wallach IX
+orgrole Bene Gesserit/set Reverend Mother=Gaius Helen Mohiam
+rosterset Bene Gesserit/add Lady Jessica=Reverend Mother:Trained in Voice
```

**Example:**
```
+housecreate Molay=House Minor
+houseset Molay/banner=White,Red
+houseset Molay/crest=Scroll
+housedomain Molay/add primary=Artistic:Produce:Poetry
+houserole Molay/set Ruler=Lady Elara Molay
+houseenemy Molay/add=House Arcuri:Loathing:Morality
+housemember Molay/add=YourCharacter
```

See the House documentation files for complete details on:
- House Types (Nascent, Minor, Major, Great)
- Domains and areas of expertise
- House traits and gameplay integration
- Roles and positions
- Enemy Houses and rivalries
- Homeworld creation

## Future Development

Potential additions:
- Combat system commands
- Asset/equipment management
- Talent/trait activation commands
- Character creation wizard
- Experience spending system
- House resource management
- Territory control mechanics
- Organization reputation tracking
- Training progression systems
- Rank advancement workflows

