# Roster Characters - Complete Index

## 📚 Documentation Files

### Command Cheatsheet (Use This!)
**`ROSTER_COMMANDS_CHEATSHEET.md`**
- Copy-paste ready commands
- Common issues and solutions
- Quick reference for all commands
- **Start here for immediate setup**

### Quick Start (Read This First!)
**`ROSTER_SETUP_QUICKSTART.md`**
- Step-by-step setup instructions
- Quick commands
- Troubleshooting
- **Best for guided setup**

### Overview & Reference
**`ROSTER_CHARACTERS_README.md`**
- System overview
- What's included
- Character summaries
- Usage scenarios
- Quick reference card
- **Best for understanding the system**

### Complete Guide (60+ Pages)
**`ROSTER_CHARACTERS_GUIDE.md`**
- Detailed character backgrounds
- Complete stat breakdowns
- Roleplaying guidelines
- Plot hooks and storylines
- Advanced usage
- Additional character ideas
- **The comprehensive reference**

## 🐍 Python Modules

### Character Creation
**`world/dune/roster_characters.py`**
```python
# Create all characters
@py world.dune.roster_characters.create_all_roster()

# Create individual character
@py world.dune.roster_characters.create_character("alia")

# Direct function call
@py world.dune.roster_characters.create_alia()
```

**Functions:**
- `create_all_roster()` - Create all 8 characters
- `create_character(name)` - Create by short name
- `create_alia()` - Create Alia Atreides
- `create_leto_ii()` - Create Leto II
- `create_ghanima()` - Create Ghanima
- `create_duncan_idaho()` - Create Duncan Idaho
- `create_irulan()` - Create Irulan Corrino
- `create_jessica()` - Create Lady Jessica
- `create_stilgar()` - Create Stilgar
- `create_gurney_halleck()` - Create Gurney Halleck

### House Setup
**`world/dune/setup_atreides_house.py`**
```python
# Complete setup (house + locations)
@py from world.dune.setup_atreides_house import setup_all; setup_all()

# Just house
@py from world.dune.setup_atreides_house import setup_house_atreides; setup_house_atreides()

# Just throne room
@py from world.dune.setup_atreides_house import setup_arrakis_palace; setup_arrakis_palace()
```

**Functions:**
- `setup_all()` - Complete setup
- `setup_house_atreides()` - Create/update house
- `setup_arrakis_palace()` - Create throne room

### Roster Access Setup
**`world/dune/setup_roster_access.py`** ⭐ NEW
```python
# Setup without creating accounts (just fix access)
@py from world.dune.setup_roster_access import quick_setup_no_accounts; quick_setup_no_accounts()

# Setup WITH accounts for player login
@py from world.dune.setup_roster_access import quick_setup_with_accounts; quick_setup_with_accounts()

# Move all roster characters to throne room
@py from world.dune.setup_roster_access import quick_move_to_throne_room; quick_move_to_throne_room()
```

**Functions:**
- `quick_setup_no_accounts()` - Fix locks/puppeting (recommended)
- `quick_setup_with_accounts()` - Create Account objects for player login
- `quick_move_to_throne_room()` - Move characters for easy +sheet access
- `setup_character_access()` - Setup individual character
- `move_rosters_to_location()` - Move to custom location

## 📜 Batch Commands

### Batch File
**`world/batch_roster_characters.ev`**
```python
@batchcommand world.batch_roster_characters
```

Alternative method for creating characters using Evennia's batch command system.

## 🎭 The Eight Roster Characters

| Character | Role | Power Level | Key Ability |
|-----------|------|-------------|-------------|
| **Alia Atreides** | Regent | Exceptional | Bene Gesserit + Pre-Born |
| **Leto II Atreides** | Heir | High | Prescience + Pre-Born |
| **Ghanima Atreides** | Twin | High | Pre-Born + Empathy |
| **Duncan Idaho** | Swordmaster | Master | Legendary Combat |
| **Irulan Corrino** | Empress | Diplomatic | Scholar + Voice |
| **Lady Jessica** | Reverend Mother | Master | Complete Bene Gesserit |
| **Stilgar** | Naib | Warrior | Fremen Combat |
| **Gurney Halleck** | Warmaster | Veteran | Military Genius |

## 🚀 Quick Start Commands

### Complete Setup (One Command)
```python
# Setup everything
@py from world.dune.setup_atreides_house import setup_all; setup_all()
@py from world.dune.roster_characters import create_all_roster; create_all_roster()
```

### Verify
```python
+house Atreides
+roster Atreides
+sheet Alia Atreides
```

### Individual Characters
```python
@py from world.dune.roster_characters import create_character
@py create_character("alia")
@py create_character("duncan")
@py create_character("leto")
@py create_character("ghanima")
@py create_character("jessica")
@py create_character("irulan")
@py create_character("stilgar")
@py create_character("gurney")
```

## 📖 Reading Order

### If You're New
1. **ROSTER_SETUP_QUICKSTART.md** - Get started immediately
2. **ROSTER_CHARACTERS_README.md** - Understand the system
3. **ROSTER_CHARACTERS_GUIDE.md** - Deep dive when needed

### If You're Experienced
1. **ROSTER_CHARACTERS_README.md** - Quick overview
2. Run the setup commands
3. **ROSTER_CHARACTERS_GUIDE.md** - Reference as needed

### If You Want Complete Details
1. **ROSTER_CHARACTERS_GUIDE.md** - Read cover to cover
2. Review source code in `roster_characters.py`
3. Customize to your needs

## 🎯 Use Cases

### Scenario 1: Staff-Run NPCs
- Create all characters
- Staff puppets them for scenes
- Players interact but don't control

**Commands:**
```python
@py world.dune.roster_characters.create_all_roster()
@ic Alia Atreides  # Staff member possesses for scene
```

### Scenario 2: Player Roster Characters
- Create characters
- Make available for application
- Players apply and get approved

**Commands:**
```python
@py world.dune.roster_characters.create_all_roster()
@set Alia Atreides/ROSTER = 1
@set Duncan Idaho/ROSTER = 1
```

### Scenario 3: One-Shot Event
- Create for specific event
- Players pick characters
- Clean up after

**Commands:**
```python
@py world.dune.roster_characters.create_all_roster()
# Players use @ic to possess
# After event: @destroy <character> if desired
```

## 🔧 Customization

### Modify Existing Character
```python
@py from evennia import search_object
@py char = search_object("Alia Atreides")[0]
@py char.set_skill("battle", 5)
@py char.add_focus("Battle: Assassination")
@py char.db.background = "New background..."
```

### Create New Character (Template)
```python
def create_my_character():
    char = get_or_create_character("My Character")
    char.db.house = "Atreides"
    char.db.role = "Advisor"
    char.set_skill("communicate", 4)
    char.set_skill("understand", 5)
    # Add more stats...
    return char
```

## 📊 Character Stats Summary

### Skill Levels (0-5)
- **0-1:** Untrained/Basic
- **2-3:** Competent/Skilled
- **4:** Expert/Master
- **5:** Legendary/Exceptional

### Skills Defined
- **Battle:** Combat, warfare, tactics
- **Communicate:** Social, persuasion, Voice
- **Discipline:** Mental fortitude, Bene Gesserit powers
- **Move:** Physical, athletics, desert skills
- **Understand:** Knowledge, wisdom, strategy

### Drive Ratings (4-8)
Each character has five drives (Duty, Faith, Justice, Power, Truth) rated 4-8, one of each rating. Drives 6+ require statements.

## 🎬 Timeline Context

### Setting: Children of Dune Era

**What Happened:**
- Paul walked into the desert (presumed dead)
- Alia became Regent
- Twins born pre-born from Chani (who died)
- Duncan resurrected as ghola
- Holy Jihad spread across galaxy

**Current Situation:**
- Alia rules from Arrakeen
- Twins are 9-12 years old
- Alia fighting possession by Baron
- Various factions plotting
- Fremen culture transforming

**What's Coming:**
- Leto II's transformation
- Corrino restoration attempts
- The Preacher appears
- Critical choices ahead

## 🛠️ Technical Info

### Requirements
- Evennia MUD engine
- Dune 2d20 system implementation
- House system (`typeclasses.houses`)
- Character system (`typeclasses.characters`)

### Database Impact
- Creates 8 character objects
- Updates House Atreides (if exists)
- Creates throne room location (optional)
- No performance issues

### Safe to Run Multiple Times
- Checks for existing characters
- Updates instead of duplicating
- No data loss risk

## 🆘 Troubleshooting

### Character Already Exists
✅ This is fine! Script updates existing character.

### House Atreides Not Found
```python
@py world.dune.setup_atreides_house.setup_house_atreides()
```

### Permission Denied
```python
@perm me = Admin
# or login as superuser
```

### Character Not Found After Creation
```python
@find Alia Atreides
# Use exact name with quotes if needed
@find "Leto II Atreides"
```

### Can't Possess Character
```python
@ic Alia Atreides
# If that fails, check permissions
@perm Alia Atreides
```

## 📞 Getting Help

1. **Check Documentation**
   - ROSTER_SETUP_QUICKSTART.md
   - ROSTER_CHARACTERS_README.md
   - ROSTER_CHARACTERS_GUIDE.md

2. **Review Source Code**
   - world/dune/roster_characters.py
   - world/dune/setup_atreides_house.py

3. **Test Commands**
   ```python
   @py world.dune.roster_characters.CREATE_FUNCTIONS
   # Shows available creation functions
   ```

4. **Contact Admin**
   - Your game administrator
   - Evennia community forums
   - Dune MUD development team

## 🎉 Success Checklist

After setup, you should have:

- ✅ House Atreides created/updated
- ✅ 8 roster characters created
- ✅ Each character has full stats
- ✅ Characters have backgrounds and personalities
- ✅ Characters assigned to appropriate roles
- ✅ Throne room created (if using setup_all)
- ✅ Can view with `+sheet <character>`
- ✅ Can view with `+house Atreides`
- ✅ Can view with `+roster Atreides`

## 🌟 Next Steps

After creating roster characters:

1. **Create Locations**
   - Sietch Tabr
   - Palace rooms
   - Desert locations

2. **Create Supporting NPCs**
   - Guards and servants
   - Minor nobles
   - Fremen warriors

3. **Setup Organizations**
   - Bene Gesserit School
   - Spacing Guild
   - Fremen factions

4. **Plan Storylines**
   - Alia's possession arc
   - Leto's transformation
   - Political intrigue
   - Desert conflicts

5. **Configure Access**
   - Player applications
   - Staff permissions
   - Roster availability

## 📝 File Structure

```
Your-Evennia-Dune-Game/
├── ROSTER_INDEX.md                      ← You are here
├── ROSTER_SETUP_QUICKSTART.md           ← Quick start guide
├── ROSTER_CHARACTERS_README.md          ← System overview
├── ROSTER_CHARACTERS_GUIDE.md           ← Complete guide (60+ pages)
├── world/
│   ├── batch_roster_characters.ev       ← Batch command file
│   └── dune/
│       ├── roster_characters.py         ← Main character creation (900+ lines)
│       └── setup_atreides_house.py      ← House setup module
└── typeclasses/
    ├── characters.py                    ← Character typeclass
    ├── houses.py                        ← House typeclass
    └── ...
```

## 🎭 Character Quick Reference

```
Alia Atreides        → Regent, Pre-Born, Bene Gesserit Master
Leto II Atreides     → Heir, Pre-Born, Prescient, Future God Emperor
Ghanima Atreides     → Twin, Pre-Born, Wise, Supportive
Duncan Idaho         → Swordmaster, Ghola, Legendary Warrior
Irulan Corrino       → Empress, Historian, Bene Gesserit Scholar
Lady Jessica         → Reverend Mother, Paul's Mother, Matriarch
Stilgar              → Fremen Naib, Guardian, Traditional Warrior
Gurney Halleck       → Warmaster, Veteran, Troubadour
```

## 💡 Pro Tips

1. **Create house first** for proper relationships
2. **Read character backgrounds** before possessing
3. **Use +sheet** to see full character details
4. **Characters are pre-configured** - ready to play
5. **Safe to re-run** if you need to update
6. **Customize freely** - they're your characters now

---

## The Complete Command

```python
# The full setup in two commands:
@py from world.dune.setup_atreides_house import setup_all; setup_all()
@py from world.dune.roster_characters import create_all_roster; create_all_roster()

# Verify it worked:
+house Atreides
+roster Atreides
+sheet Alia Atreides

# Start playing:
@ic Alia Atreides
```

---

**That's it! You're ready to play in the Dune universe!**

*May thy knife chip and shatter.*
— Traditional Fremen blessing

---

**Version:** 1.0  
**System:** Modiphius 2d20 Dune  
**Era:** Children of Dune  
**Characters:** 8 Major Roster Characters  
**Documentation:** Complete (4 files, 100+ pages total)  
**Code:** 1200+ lines Python  
**Status:** ✅ Production Ready

