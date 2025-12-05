# Roster Characters - Quick Setup Guide

This guide will walk you through setting up the Children of Dune era roster characters for your game.

## Prerequisites

- Admin/Superuser access to the game
- Evennia server running
- Access to the in-game Python interpreter (`@py` command)

## Step-by-Step Setup

### Step 1: Setup House Atreides (Optional but Recommended)

If House Atreides doesn't exist yet or needs updating for this era:

```python
@py from world.dune.setup_atreides_house import setup_all; setup_all()
```

This will:
- Create/update House Atreides with appropriate stats for this era
- Set Alia as Regent
- Create the Arrakeen Palace Throne Room
- Set up house roles, domains, and relationships

**Alternative** (just the house, no locations):
```python
@py from world.dune.setup_atreides_house import setup_house_atreides; setup_house_atreides()
```

### Step 2: Create Roster Characters

Create all 8 major roster characters at once:

```python
@py from world.dune.roster_characters import create_all_roster; create_all_roster()
```

This creates:
1. **Alia Atreides** - Regent of the Imperium
2. **Leto II Atreides** - Pre-born Heir
3. **Ghanima Atreides** - Pre-born Twin
4. **Duncan Idaho (Hayt)** - Ghola Swordmaster
5. **Irulan Corrino** - Empress and Historian
6. **Lady Jessica** - Bene Gesserit Reverend Mother
7. **Stilgar** - Fremen Naib
8. **Gurney Halleck** - Warmaster

Each character is created with:
- Full skill ratings (Battle, Communicate, Discipline, Move, Understand)
- Appropriate focuses and talents
- Drive ratings and statements
- Background, personality, and relationships
- Languages and other attributes

### Step 3: Verify Creation

Check that characters were created successfully:

```python
@find Alia Atreides
@find Duncan Idaho
@find Leto II Atreides
```

View a character's full sheet:

```python
+sheet Alia Atreides
```

### Step 4: Place Characters (Optional)

Move characters to appropriate starting locations:

```python
@tel Alia Atreides = Arrakeen Palace - Throne Room
@tel Duncan Idaho = Arrakeen Palace - Throne Room
@tel Leto II Atreides = <Sietch Tabr location>
@tel Ghanima Atreides = <Sietch Tabr location>
```

Or find the throne room first:

```python
@find Arrakeen Palace
@tel Alia Atreides = #<throne_room_id>
```

### Step 5: Add to House Roster (Optional)

If using the roster system, add characters to House Atreides:

```python
+rosterset Atreides/add "Alia Atreides"=Regent:Pre-born Regent of the Imperium, sister of Paul Muad'Dib
+rosterset Atreides/add "Duncan Idaho"=Swordmaster:Resurrected ghola, husband of Alia, legendary warrior
+rosterset Atreides/add "Leto II Atreides"=Heir:Pre-born son of Paul and Chani
+rosterset Atreides/add "Ghanima Atreides"=Heir:Pre-born daughter of Paul and Chani
+rosterset Atreides/add "Lady Jessica"=Advisor:Reverend Mother, mother of Paul and Alia
+rosterset Atreides/add "Stilgar"=Marshal:Fremen Naib, guardian to the twins
+rosterset Atreides/add "Gurney Halleck"=Warmaster:Veteran warrior and strategist
+rosterset Atreides/add "Irulan Corrino"=Consort:Empress, historian, and tutor
```

## Alternative Methods

### Method A: Using Batch Commands

```python
@batchcommand world.batch_roster_characters
```

### Method B: Create Individual Characters

Create one character at a time:

```python
@py from world.dune.roster_characters import create_character
@py create_character("alia")
@py create_character("duncan")
@py create_character("leto")
```

Available shortcuts:
- `alia`, `leto`, `leto2`, `ghanima`, `duncan`, `idaho`, `irulan`, `jessica`, `stilgar`, `gurney`

### Method C: Direct Function Calls

```python
@py from world.dune import roster_characters
@py roster_characters.create_alia()
@py roster_characters.create_leto_ii()
@py roster_characters.create_ghanima()
@py roster_characters.create_duncan_idaho()
@py roster_characters.create_irulan()
@py roster_characters.create_jessica()
@py roster_characters.create_stilgar()
@py roster_characters.create_gurney_halleck()
```

## Making Characters Playable

### Option 1: Direct Possession (For Testing)

```python
@ic Alia Atreides
```

This lets you puppet the character directly. Use `@ooc` to return to your regular character.

### Option 2: Assign to Player Account

1. Have the player create an account
2. Assign the character:

```python
@charcreate <playername>=<password>
@force <playername> = @ic Alia Atreides
```

### Option 3: Roster System

If you have a roster/chargen app:

```python
@set Alia Atreides/ROSTER = 1
@set Alia Atreides/ROSTER_AVAILABLE = 1
```

## Customizing Characters

### Modify Descriptions

```python
@ic Alia Atreides
@desc me = <new description>
+bio/personality <text>
+bio/background <text>
```

### Add Assets

```python
@ic Duncan Idaho
+asset/create Personal Shield
+asset/create Atreides Blade
```

### Adjust Skills (if needed)

```python
@py from evennia import search_object
@py char = search_object("Alia Atreides")[0]
@py char.set_skill("battle", 5)
@py char.add_focus("Battle: Assassination")
```

## Viewing and Managing

### View Character Sheet

```python
+sheet Alia Atreides
```

### View House Info

```python
+house Atreides
```

### View Roster

```python
+roster Atreides
+roster/full Atreides
```

### List All Roster Characters

```python
@find *Atreides
@find Duncan Idaho
@find Stilgar
```

## Troubleshooting

### Character Already Exists

If a character already exists, the script will update their stats instead of creating a duplicate.

### Missing House

If you get errors about House Atreides not existing:

```python
@py world.dune.setup_atreides_house.setup_house_atreides()
```

### Character Not Found

Make sure you use the exact name:
- "Alia Atreides" (not "Alia")
- "Duncan Idaho" (not "Duncan")
- "Leto II Atreides" (not "Leto")

### Permission Errors

Make sure you're logged in as a superuser or admin:

```python
@perm me = Admin
```

## Next Steps

After creating the roster characters:

1. **Create Additional Locations**
   - Sietch Tabr
   - Various palace rooms
   - Desert locations
   - Off-world sites

2. **Create Supporting Characters**
   - House guards
   - Fremen warriors
   - Palace staff
   - Political figures

3. **Set Up Organizations**
   - Bene Gesserit (School)
   - Spacing Guild (Guild)
   - Fremen tribes (Faction)

4. **Create Plot Hooks**
   - Alia's possession storyline
   - Leto's transformation
   - Corrino restoration plots
   - Desert conflicts

5. **Configure Permissions**
   - Set up who can play roster characters
   - Configure staff vs player access
   - Set up approval processes

## Full Setup Command (All-In-One)

For a complete automated setup:

```python
@py world.dune.setup_atreides_house.setup_all()
@py world.dune.roster_characters.create_all_roster()
```

Then verify:

```python
+house Atreides
+roster Atreides
+sheet Alia Atreides
```

## Reference Files

- **Detailed Guide:** `ROSTER_CHARACTERS_GUIDE.md`
- **Python Module:** `world/dune/roster_characters.py`
- **House Setup:** `world/dune/setup_atreides_house.py`
- **Batch Commands:** `world/batch_roster_characters.ev`

## Support

For issues or questions:
1. Check the detailed guide: `ROSTER_CHARACTERS_GUIDE.md`
2. Review the Python source: `world/dune/roster_characters.py`
3. Contact your game admin

---

**Happy Gaming in the Dune Universe!**

*"The mystery of life isn't a problem to solve, but a reality to experience."*

