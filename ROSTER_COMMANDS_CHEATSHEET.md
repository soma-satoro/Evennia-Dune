# Roster Characters - Command Cheatsheet

## 🚀 Quick Setup (Copy and Paste)

### Complete Setup - Three Commands
```python
@py from world.dune.setup_atreides_house import setup_all; setup_all()
@py from world.dune.roster_characters import create_all_roster; create_all_roster()
@py from world.dune.setup_roster_access import quick_setup_no_accounts; quick_setup_no_accounts()
```

### Verify It Worked
```python
+house Atreides
+roster Atreides
@ic Alia Atreides
+sheet
@ooc
```

### Alternative: Move Characters to Throne Room
```python
@py from world.dune.setup_atreides_house import setup_all; setup_all()
@py from world.dune.roster_characters import create_all_roster; create_all_roster()
@py from world.dune.setup_roster_access import quick_move_to_throne_room; quick_move_to_throne_room()
```

Then:
```python
@tel me = Arrakeen Palace - Throne Room
+sheet Alia Atreides
```

---

## 📝 Alternative Methods

### Just House Atreides (No Characters)
```python
@py from world.dune.setup_atreides_house import setup_house_atreides; setup_house_atreides()
```

### Just Roster Characters (No House Setup)
```python
@py from world.dune.roster_characters import create_all_roster; create_all_roster()
```

### Individual Characters
```python
@py from world.dune.roster_characters import create_character
@py create_character("alia")
@py create_character("leto")
@py create_character("ghanima")
@py create_character("duncan")
@py create_character("jessica")
@py create_character("irulan")
@py create_character("stilgar")
@py create_character("gurney")
```

### Using Batch Command
```python
@batchcommand world.batch_roster_characters
```

---

## 🎭 The 8 Roster Characters

| Short Name | Full Name | Role |
|------------|-----------|------|
| `alia` | Alia Atreides | Regent of the Imperium |
| `leto` | Leto II Atreides | Pre-Born Heir |
| `ghanima` | Ghanima Atreides | Pre-Born Twin |
| `duncan` | Duncan Idaho | Ghola Swordmaster |
| `irulan` | Irulan Corrino | Empress & Historian |
| `jessica` | Lady Jessica | Reverend Mother |
| `stilgar` | Stilgar | Fremen Naib |
| `gurney` | Gurney Halleck | Warmaster |

---

## 🔍 Viewing Commands

```python
# View character sheet
+sheet Alia Atreides
+sheet "Leto II Atreides"

# View House info
+house Atreides

# View roster
+roster Atreides
+roster/full Atreides

# Find characters
@find Alia Atreides
@find Duncan Idaho
```

---

## 🎮 Playing Characters

```python
# Possess a character (as staff/admin)
@ic Alia Atreides

# Return to your normal character
@ooc

# Teleport character to location
@tel "Alia Atreides" = Arrakeen Palace - Throne Room

# Find throne room ID first
@find Arrakeen Palace
@tel "Alia Atreides" = #<room_id>
```

---

## ⚙️ Common Issues

### Error: "NameError: name 'world' is not defined"
**Wrong:**
```python
@py world.dune.roster_characters.create_all_roster()
```

**Right:**
```python
@py from world.dune.roster_characters import create_all_roster; create_all_roster()
```

### Error: "Could not find 'Alia Atreides'" or "is not a character"
This happens because `+sheet` only searches in your current location. **Solutions:**

**Option 1: Move roster characters to throne room (Recommended)**
```python
@py from world.dune.setup_roster_access import quick_move_to_throne_room; quick_move_to_throne_room()
```
Then go to throne room and use `+sheet <character>`

**Option 2: Set up roster access (for puppeting)**
```python
@py from world.dune.setup_roster_access import quick_setup_no_accounts; quick_setup_no_accounts()
```
Then use `@ic <character>` and `+sheet` while puppeting

**Option 3: View sheet directly with Python**
```python
@py from evennia import search_object
@py char = search_object('Alia Atreides')[0]
@py me.msg(char.get_sheet_display())
```

**Option 4: Puppet the character to view**
```python
@ic Alia Atreides
+sheet
@ooc
```

### Error: "House Atreides not found"
Create the house first:
```python
@py from world.dune.setup_atreides_house import setup_house_atreides; setup_house_atreides()
```

### Error: "Permission denied"
Make sure you're logged in as superuser/admin:
```python
@perm me = Admin
```

### Character Already Exists
This is fine! The script will update the existing character instead of creating a duplicate.

---

## 🛠️ Advanced Usage

### Create Accounts for Roster Characters (Player Login)
If you want players to log in as roster characters:
```python
@py from world.dune.setup_roster_access import quick_setup_with_accounts; quick_setup_with_accounts()
```

This creates accounts with:
- Username: Character name (e.g., "Alia Atreides")
- Password: Character name (CHANGE THIS!)

To change passwords:
```python
@password Alia Atreides = <new_secure_password>
```

Then players can log in with:
```
connect Alia Atreides <password>
```

### Import and Use Multiple Times
```python
# Import once
@py from world.dune.roster_characters import create_character

# Then use multiple times
@py create_character("alia")
@py create_character("duncan")
@py create_character("leto")
```

### Check What Was Created
```python
@py from evennia import search_object
@py chars = search_object("*Atreides")
@py for char in chars: print(f"{char.name} - {char.db.role}")
```

### Modify a Character
```python
@py from evennia import search_object
@py char = search_object("Alia Atreides")[0]
@py char.set_skill("battle", 5)
@py char.add_focus("Battle: Assassination")
@py print(f"Updated {char.name}")
```

---

## 📚 Full Documentation

- **Quick Setup:** ROSTER_SETUP_QUICKSTART.md
- **System Overview:** ROSTER_CHARACTERS_README.md
- **Complete Guide:** ROSTER_CHARACTERS_GUIDE.md (60+ pages)
- **Master Index:** ROSTER_INDEX.md

---

## ✅ Success Checklist

After running setup, you should have:
- ✅ House Atreides created
- ✅ 8 roster characters created
- ✅ Characters have full stats and backgrounds
- ✅ Throne room location created
- ✅ Can view with `+sheet <character>`
- ✅ Can view with `+house Atreides`
- ✅ Can possess with `@ic <character>`

---

**Quick Test:**
```python
@py from world.dune.setup_atreides_house import setup_all; setup_all()
@py from world.dune.roster_characters import create_all_roster; create_all_roster()
+sheet Alia Atreides
```

If you see Alia's complete character sheet, it worked! 🎉

---

*"I must not fear. Fear is the mind-killer."*

