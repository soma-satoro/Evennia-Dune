# Roster System Quick Reference

## Quick Commands

### Everyone

```bash
# View rosters
+roster <org>                    # View roster
+roster/members <org>            # Members only
+roster/full <org>               # Full details

# View organizations
+org <name>                      # View organization
+org/list                        # List all
+org/list school                 # Filter by type

# Who is online
who                              # Standard who
who/house                        # Grouped by House
```

### Staff Only (Builder+)

```bash
# Roster management
+rosterset <org>/add <char>=<title>:<desc>
+rosterset <org>/remove <char>
+rosterset <org>/title <char>=<title>
+rosterset <org>/desc <char>=<description>
+rosterset <org>/sync            # Migrate legacy data

# Organization creation
+orgcreate <name>=<type>         # school, guild, order, faction

# Organization properties
+orgset <org>/trait=<trait>
+orgset <org>/headquarters=<location>
+orgset <org>/requirements=<text>
+orgset <org>/benefits=<text>

# Organization roles
+orgrole <org>/list
+orgrole <org>/set <role>=<name>[:<desc>][:<traits>]
+orgrole <org>/remove <role>
```

## Organization Types

| Type | Description | Examples |
|------|-------------|----------|
| **school** | Educational institution | Bene Gesserit, Suk School, Mentat School |
| **guild** | Trade organization | Spacing Guild, CHOAM |
| **order** | Religious group | Zensunni Wanderers |
| **faction** | Political movement | Fremen, Sardaukar |

## Member Information

Each member has:
- **Title**: Rank or position (e.g., "Master Poet", "Reverend Mother")
- **Description**: Tie to organization (e.g., "Lead instructor at the academy")
- **Date Joined**: Automatically tracked

## Quick Examples

### Add Member with Full Info
```bash
+rosterset Bene Gesserit/add Lady Jessica=Reverend Mother:Concubine to Duke Leto
```

### Update Title Only
```bash
+rosterset Molay/title Paul=Master Poet
```

### Update Description Only
```bash
+rosterset Molay/desc Paul=Lead instructor at northern academy
```

### Create Complete Organization (5 min)
```bash
# Create
+orgcreate Bene Gesserit=school

# Configure
+orgset Bene Gesserit/trait=Secretive
+orgset Bene Gesserit/headquarters=Wallach IX
+orgset Bene Gesserit/requirements=Female only, rigorous testing
+orgset Bene Gesserit/benefits=Enhanced abilities, Voice training

# Add role
+orgrole Bene Gesserit/set Reverend Mother Superior=Gaius Helen Mohiam

# Add members
+rosterset Bene Gesserit/add Lady Jessica=Reverend Mother:Trained in Voice

# View
+org Bene Gesserit
+roster Bene Gesserit
```

## Affiliation Rules

- **Houses**: One per character
- **Organizations**: Multiple per character

Example: Lady Jessica
- House: Atreides
- Organizations: Bene Gesserit

## Common Titles by Organization

### Schools
- Reverend Mother (Bene Gesserit)
- Suk Doctor (Suk School)
- Mentat (Mentat School)
- Swordmaster (Ginaz School)
- Student, Instructor, Master

### Guilds
- Guildmaster
- Navigator (Spacing Guild)
- Representative
- Agent
- Treasurer

### Orders
- High Priest/Priestess
- Elder
- Keeper
- Acolyte

### Factions
- Naib (Fremen leader)
- Fedaykin (Fremen elite)
- Commander
- Warrior

## Display Format

### Standard Roster View
```
================================= House Molay - Roster ==================================
Type: House Minor
Banner: White, Red - Scroll
Traits: Secretive, Artistic

------------------------------------ Members (3) ------------------------------------
  Paul - Master Poet
    Lead instructor at the northern poetry academy
  
  Jessica - Poet
    Senior member training in assassination techniques
  
  Marcus - Apprentice
    New student showing great promise

================================ 78 ============================================
```

### Full Roster View
Includes:
- Complete organization details
- All domains/specializations
- Key roles
- Full member information with join dates

## Tips

1. **Always include descriptions** - They add flavor and context
2. **Use meaningful titles** - They show rank and role
3. **Keep descriptions concise** - One sentence is usually enough
4. **Update regularly** - As characters advance or change roles
5. **Use +roster to verify** - Always check your work

## File Locations

- **Commands**: `commands/dune/CmdRoster.py`, `CmdOrganization.py`
- **Typeclasses**: `typeclasses/houses.py`, `typeclasses/organizations.py`
- **Documentation**: `commands/dune/ROSTER_SYSTEM_README.md`

## Troubleshooting

### Member not showing up?
- Use `+rosterset <org>/sync` to migrate legacy members
- Verify the character name is correct
- Check that they were added with `+rosterset <org>/add`

### Can't create organization?
- Ensure you have Builder+ permission
- Check the organization type is valid: school, guild, order, faction
- Verify the name doesn't already exist

### Organization not found?
- Use `+org/list` to see all organizations
- Check spelling carefully
- Organizations are case-sensitive

## Support

For help:
1. Read full documentation: `ROSTER_SYSTEM_README.md`
2. Use in-game help: `help +roster`, `help +rosterset`
3. Contact staff via +jobs

---

**Quick Start**: `+orgcreate <name>=<type>` → `+orgset` properties → `+rosterset <org>/add` members → `+roster <org>` to view

