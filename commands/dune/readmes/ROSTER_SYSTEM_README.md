# Roster System Documentation

## Overview

The Roster System provides comprehensive member tracking for Houses, Schools, Guilds, Orders, and Factions in the Dune MUSH. This system allows staff to manage organizational membership with detailed information about each member's role, title, and ties to the organization.

## Key Features

- **Detailed Member Tracking**: Track member names, titles, descriptions, and join dates
- **Multiple Affiliations**: Characters can belong to a House AND other organizations
- **Rich Display**: Beautiful roster displays showing all member information
- **Staff Control**: Builder+ permission required for roster management
- **Backward Compatible**: Works with existing House system

## Organizations

### Houses
Noble Houses that rule planets and control resources. Characters can belong to ONE House.

**Examples**: House Atreides, House Harkonnen, House Corrino

### Schools
Educational or training institutions that teach specific skills.

**Examples**: Bene Gesserit, Suk School, Mentat School, Swordmaster Schools

### Guilds
Professional trade organizations that control industries.

**Examples**: Spacing Guild, CHOAM, Water Sellers Guild

### Orders
Religious or ideological organizations.

**Examples**: Orange Catholic Bible Scholars, Zensunni Wanderers

### Factions
Political or social movements.

**Examples**: Fremen, Sardaukar, Fedaykin

## Commands Reference

### Viewing Rosters (All Users)

#### +roster <organization>
View the roster of any House or Organization.

```
+roster Atreides
+roster Bene Gesserit
+roster Spacing Guild
```

#### +roster/members <organization>
View only the members list (compact view).

```
+roster/members Molay
```

#### +roster/full <organization>
View full detailed roster with all information.

```
+roster/full Bene Gesserit
```

### Roster Management (Builder+)

#### +rosterset <org>/add <character>=<title>:<description>
Add a member with title and description.

```
+rosterset Molay/add Paul=Poet:Aspiring member of the poetry school
+rosterset Bene Gesserit/add Lady Jessica=Reverend Mother:Concubine to Duke Leto
+rosterset Spacing Guild/add Navigator Edric=Guild Navigator:Steersman of the heighliner
```

**Format**: `<title>:<description>`
- **Title**: The character's rank or position
- **Description**: Their tie or relationship to the organization

#### +rosterset <org>/remove <character>
Remove a member from the organization.

```
+rosterset Molay/remove Paul
```

#### +rosterset <org>/title <character>=<title>
Set or change a member's title.

```
+rosterset Molay/title Paul=Master Poet
+rosterset Bene Gesserit/title Lady Jessica=Reverend Mother
```

#### +rosterset <org>/desc <character>=<description>
Set or change a member's description.

```
+rosterset Molay/desc Paul=Lead instructor at the northern academy
+rosterset Bene Gesserit/desc Lady Jessica=Trained in the Voice and Weirding Way
```

#### +rosterset <org>/sync
Migrate legacy members to the new roster system.

```
+rosterset Molay/sync
```

### Viewing Organizations (All Users)

#### +org <name>
View detailed information about a School, Guild, Order, or Faction.

```
+org Bene Gesserit
+org Spacing Guild
+org Fremen
```

#### +org/list [type]
List all Organizations, optionally filtered by type.

```
+org/list
+org/list school
+org/list guild
```

**Types**: school, guild, order, faction

### Organization Management (Builder+)

#### +orgcreate <name>=<type>
Create a new Organization.

```
+orgcreate Bene Gesserit=school
+orgcreate Spacing Guild=guild
+orgcreate Zensunni Wanderers=order
+orgcreate Fremen=faction
```

#### +orgset <org>/<switch>=<value>
Set Organization properties.

**Common Switches**:
- `/trait` - Add an organization trait
- `/headquarters` - Set main location
- `/requirements` - Set membership requirements
- `/benefits` - Set membership benefits

**Examples**:
```
+orgset Bene Gesserit/trait=Secretive
+orgset Bene Gesserit/headquarters=Wallach IX
+orgset Bene Gesserit/requirements=Female only, rigorous testing
+orgset Bene Gesserit/benefits=Enhanced abilities, Voice training
```

**Type-Specific Switches**:
- `/curriculum` - Add to curriculum (schools only)
- `/industry` - Set industry (guilds only)
- `/philosophy` - Set philosophy (orders only)
- `/goals` - Set goals (factions only)

```
+orgset Bene Gesserit/curriculum=Voice
+orgset Spacing Guild/industry=Interstellar travel and navigation
+orgset Zensunni Wanderers/philosophy=Wandering and meditation
+orgset Fremen/goals=Preserve Arrakis and its secrets
```

#### +orgrole <org>/<switch>
Manage Organization positions.

```
+orgrole Bene Gesserit/list
+orgrole Bene Gesserit/set Reverend Mother=Gaius Helen Mohiam
+orgrole Bene Gesserit/set Proctor=Lady Margot:Proctor of Arrakis
+orgrole Bene Gesserit/remove Proctor
```

### Enhanced Who Command

#### who
Show all connected players with their House affiliations.

```
who
```

#### who/house
Show connected players grouped by House.

```
who/house
```

## Example: Creating the Bene Gesserit

Here's a complete example of creating and populating the Bene Gesserit school:

```bash
# 1. Create the organization
+orgcreate Bene Gesserit=school

# 2. Set basic properties
+orgset Bene Gesserit/trait=Secretive
+orgset Bene Gesserit/trait=Manipulative
+orgset Bene Gesserit/headquarters=Wallach IX

# 3. Set organization details
+orgset Bene Gesserit/requirements=Female only. Candidates must pass rigorous testing and training
+orgset Bene Gesserit/benefits=Enhanced physical and mental abilities, Voice training, political influence
+orgset Bene Gesserit/leadership=Led by the Reverend Mother Superior and Council of Reverend Mothers

# 4. Add curriculum (school-specific)
+orgset Bene Gesserit/curriculum=The Voice
+orgset Bene Gesserit/curriculum=Weirding Way combat
+orgset Bene Gesserit/curriculum=Prana-bindu training
+orgset Bene Gesserit/curriculum=Political manipulation
+orgset Bene Gesserit/curriculum=Truthsaying

# 5. Set key roles
+orgrole Bene Gesserit/set Reverend Mother Superior=Gaius Helen Mohiam:Leader of the order
+orgrole Bene Gesserit/set Proctor=Lady Margot Fenring:Proctor to House Corrino

# 6. Add members
+rosterset Bene Gesserit/add Lady Jessica=Reverend Mother:Concubine to Duke Leto Atreides
+rosterset Bene Gesserit/add Alia Atreides=Abomination:Born a Reverend Mother

# View the roster
+roster Bene Gesserit
+org Bene Gesserit
```

## Example: Creating the Spacing Guild

```bash
# 1. Create the organization
+orgcreate Spacing Guild=guild

# 2. Set basic properties
+orgset Spacing Guild/trait=Mysterious
+orgset Spacing Guild/headquarters=Junction

# 3. Set guild-specific details
+orgset Spacing Guild/industry=Interstellar travel and navigation
+orgset Spacing Guild/requirements=Navigators must be exposed to spice gas
+orgset Spacing Guild/benefits=Monopoly on space travel, prescient abilities

# 4. Set key roles
+orgrole Spacing Guild/set Guildmaster=Edric:Navigator and spokesman

# 5. Add members
+rosterset Spacing Guild/add Navigator Edric=Guild Navigator:Steersman of the heighliner
+rosterset Spacing Guild/add Guild Agent=Representative:Ambassador to the Landsraad

# View the roster
+roster/full Spacing Guild
```

## Example: Creating the Fremen Faction

```bash
# 1. Create the organization
+orgcreate Fremen=faction

# 2. Set basic properties
+orgset Fremen/trait=Resilient
+orgset Fremen/trait=Secretive
+orgset Fremen/headquarters=Sietch Tabr (hidden)

# 3. Set faction-specific details
+orgset Fremen/goals=Terraform Arrakis into a paradise, preserve way of life
+orgset Fremen/requirements=Survival skills, water discipline, loyalty to the tribe

# 4. Set key roles
+orgrole Fremen/set Naib=Stilgar:Leader of Sietch Tabr
+orgrole Fremen/set Sayyadina=Reverend Mother Ramallo:Spiritual leader

# 5. Add members
+rosterset Fremen/add Stilgar=Naib:Leader of Sietch Tabr
+rosterset Fremen/add Chani=Warrior:Daughter of Liet-Kynes
+rosterset Fremen/add Paul Atreides=Muad'Dib:Lisan al-Gaib, prophesied messiah

# View the roster
+roster Fremen
```

## Member Information Fields

Each roster entry contains:

### Title
The character's rank, position, or role in the organization.

**Examples**:
- "Master Poet" (House Molay)
- "Reverend Mother" (Bene Gesserit)
- "Guild Navigator" (Spacing Guild)
- "Naib" (Fremen)
- "Swordmaster" (Ginaz School)

### Description
A brief description of their tie, relationship, or specific role.

**Examples**:
- "Lead instructor at the northern poetry academy"
- "Concubine to Duke Leto Atreides, mother of Paul"
- "Steersman of the heighliner, prescient navigator"
- "Leader of Sietch Tabr, mentor to Paul Atreides"
- "Teaches advanced combat techniques to nobles"

### Date Joined
Automatically tracked when a member is added (not displayed by default).

## Multiple Affiliations

Characters in Dune can belong to multiple organizations:

- **One House**: Characters can only serve one Noble House
- **Multiple Organizations**: Characters can belong to multiple Schools, Guilds, Orders, or Factions

### Example: Lady Jessica
```
House: Atreides
Organizations: Bene Gesserit
```

### Example: Paul Atreides
```
House: Atreides  
Organizations: Bene Gesserit (partial training), Fremen, Fedaykin (elite fighters)
```

### Example: Thufir Hawat
```
House: Atreides
Organizations: Mentat School (graduate)
```

## Staff Workflows

### Adding a New Member
1. Use `+rosterset <org>/add <character>=<title>:<description>`
2. View the roster with `+roster <org>` to verify
3. Character can now see their affiliation with `+roster <org>`

### Updating Member Info
1. Use `+rosterset <org>/title <character>=<new title>` to update title
2. Use `+rosterset <org>/desc <character>=<new description>` to update description
3. Changes take effect immediately

### Removing a Member
1. Use `+rosterset <org>/remove <character>`
2. Character loses affiliation immediately
3. For Houses: character.db.house is set to None
4. For Organizations: removed from character.db.organizations list

### Creating a New Organization
1. Decide on type: school, guild, order, or faction
2. Use `+orgcreate <name>=<type>`
3. Use `+orgset` to configure properties
4. Use `+orgrole` to set key positions
5. Use `+rosterset` to add members
6. Test with `+roster` and `+org` commands

## Technical Details

### Data Storage

#### House Member Roster
```python
house.db.member_roster = {
    character_id: {
        'title': 'Master Poet',
        'description': 'Lead instructor at the academy',
        'date_joined': datetime_object
    }
}
```

#### Organization Member Roster
```python
organization.db.member_roster = {
    character_id: {
        'title': 'Reverend Mother',
        'description': 'Trained in Voice and Weirding Way',
        'date_joined': datetime_object
    }
}
```

#### Character Affiliations
```python
character.db.house = house_object  # Single House
character.db.organizations = [org1, org2, org3]  # Multiple Organizations
```

### Typeclass Hierarchy

```
DefaultObject
    └── House
            └── Organization
                    ├── School
                    ├── Guild
                    ├── Order
                    └── Faction
```

### Methods

#### House/Organization
- `add_member(character, title, description)` - Add a member
- `remove_member(character)` - Remove a member
- `set_member_title(character, title)` - Set member title
- `set_member_description(character, description)` - Set member description
- `get_member_info(character)` - Get member information
- `get_all_members()` - Get all members with info

## Permissions

### Viewing
- **+roster**: All users
- **+org**: All users
- **+org/list**: All users
- **who**: All users

### Management
- **+rosterset**: Builder+ only
- **+orgcreate**: Builder+ only
- **+orgset**: Builder+ only
- **+orgrole**: Builder+ only

## Future Enhancements

Possible additions:
- Rank progression tracking
- Membership fees/requirements automation
- Training skill bonuses
- Organization reputation system
- Alliance/enemy organizations
- Automatic roster reports
- Web interface for roster viewing
- Member activity tracking
- Promotion/demotion workflows

## Credits

Based on the Groups system from PyReach/World of Darkness MUSH.
Adapted for Dune: Adventures in the Imperium by Modiphius Entertainment.
Implemented for Evennia MUD/MUSH.

---

*"The mystery of life isn't a problem to solve, but a reality to experience." - Frank Herbert, Dune*

