# Dune MUSH - Setup Guide

This guide explains the setup and structure of the Dune MUSH using Evennia and the Modiphus 2d20 system.

## Overview

This is a Dune-themed MUSH (Multi-User Shared Hallucination) built on the Evennia framework, implementing the Modiphus 2d20 game system. The system is designed for collaborative storytelling in the Dune universe.

## What's Been Implemented

### 1. Typeclasses

#### Characters (`typeclasses/characters.py`)
Full 2d20 character system including:
- **Attributes** (Control, Dexterity, Fitness, Insight, Presence, Reason)
- **Skills** (Battle, Communicate, Discipline, Move, Understand)
- **Focuses** (skill specializations)
- **Traits** (special abilities)
- **Assets** (resources and items)
- **Drives** (character motivations)
- **Stress tracking** (health/damage)
- **Determination points** (hero points)
- **Experience points**

Helper methods:
- `get_attribute()`, `set_attribute()`
- `get_skill()`, `set_skill()`
- `add_focus()`, `remove_focus()`
- `add_trait()`, `remove_trait()`
- `add_asset()`, `remove_asset()`
- `take_stress()`, `heal_stress()`
- `spend_determination()`, `gain_determination()`
- `get_sheet_display()`

#### NPCs (`typeclasses/npcs.py`)
Non-player character system with:
- Same stat structure as player characters
- NPC tiers: minor, notable, major
- Pre-configured NPC types (guard, soldier, officer, advisor)
- AI/behavior flags for future automation
- Simplified stats for minor NPCs
- Full character abilities for major NPCs

Helper methods:
- `set_as_minor_npc()`, `set_as_notable_npc()`, `set_as_major_npc()`
- All the same stat management methods as Characters

#### Rooms (`typeclasses/rooms.py`)
Formatted room display system featuring:
- Styled headers with location hierarchy
- Character listing with idle times
- Separated cardinal directions from other exits
- Places system integration
- IC area codes and region mapping
- Theme color support

Features:
- `get_display_header()` - Formatted room name with hierarchy
- `get_display_characters()` - Shows PCs/NPCs with idle times
- `get_display_directions()` - Cardinal direction exits
- `get_display_exits()` - Other exits
- `get_display_footer()` - Area code display
- `set_area_info()` - Configure room area
- `add_place()` - Add places to room
- `set_places_active()` - Enable/disable places

### 2. Commands

#### Character Commands (`commands/dune/CmdSheet.py`)

**+sheet** - Display character sheets
```
+sheet
+sheet <character>
+sheet/full
```

**+stats** - Set character stats (staff only)
```
+stats <character>
+stats <character>/attr/<attribute>=<value>
+stats <character>/skill/<skill>=<value>
```

**+focus** - Manage skill focuses
```
+focus
+focus/add <skill>: <specialization>
+focus/remove <focus>
```

**+stress** - Manage stress (damage)
```
+stress
+stress/take <amount>
+stress/heal <amount>
+stress/set <character>=<amount> (staff)
```

#### Dice Commands (`commands/dune/CmdRoll.py`)

**+roll** - 2d20 dice rolling
```
+roll <attribute> + <skill>
+roll <attribute> + <skill> vs <difficulty>
+roll <attribute> + <skill> vs <difficulty> focus
+roll <attribute> + <skill> vs <difficulty> bonus <dice>
+roll/private <attribute> + <skill> vs <difficulty>
```

**+momentum** - Manage group momentum pool
```
+momentum
+momentum/spend <amount>
+momentum/add <amount> (staff)
+momentum/set <amount> (staff)
```

**+determination** - Manage determination points
```
+determination
+determination/spend
+determination/add <character>=<amount> (staff)
```

### 3. Command Sets

**DuneCmdSet** (`commands/dune/dune_cmdset.py`)
- Contains all Dune-specific 2d20 system commands
- Automatically added to all characters

**CommonMuxCmdSet** (`commands/commonmux/commonmux_cmdset.py`)
- Contains MUX-style roleplay commands
- Communication and social commands
- Already integrated

### 4. Integration

The command sets are integrated in `commands/default_cmdsets.py`:
```python
from commands.commonmux.commonmux_cmdset import CommonMuxCmdSet
from commands.dune.dune_cmdset import DuneCmdSet

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CommonMuxCmdSet)
        self.add(DuneCmdSet)
```

## The 2d20 System

### Basic Mechanics

1. **Task Resolution**
   - Roll 2d20 (base) + additional dice from assists/momentum/focus
   - Compare each die to Target Number (Attribute + Skill)
   - Each die ≤ target number = 1 success
   - Rolling a 1 = 2 successes (critical!)
   - Rolling a 20 = complication

2. **Difficulty**
   - Most tasks require 1-3 successes
   - Extra successes beyond difficulty generate Momentum

3. **Resources**
   - **Momentum** - Group resource, spent for bonuses
   - **Determination** - Individual hero points for special actions
   - **Stress** - Damage tracker (max = Fitness + Discipline)

### Example Play

```
> +roll fitness + battle vs 2
Rolls: 7 (success), 15 (success)
Successes: 2
SUCCESS!

> +roll control + communicate vs 3 focus
Using relevant Focus
Rolls: 1 (CRITICAL!), 8 (success), 19 (fail)
Successes: 3
SUCCESS!
Generate 0 Momentum

> +stress/take 4
You take 4 stress. Current: 4/12
```

## Getting Started

### For Players

1. Create your character normally with Evennia's commands
2. Staff will initialize your character sheet with starting stats
3. Use `+sheet` to view your character
4. Use `+roll <attribute> + <skill> vs <difficulty>` to make tests
5. Track your stress with `+stress/take` and `+stress/heal`

### For Staff

1. Initialize new characters using `+stats`:
   ```
   +stats Paul/attr/fitness=9
   +stats Paul/skill/battle=3
   ```

2. Award determination for good roleplay:
   ```
   +determination/add Paul=1
   ```

3. Manage momentum for scenes:
   ```
   +momentum/set 5
   ```

4. Configure rooms:
   ```python
   room.set_area_info("Arrakeen Palace", "AR01", ["Arrakis", "Arrakeen"])
   ```

## Character Creation Guidelines

### Starting Stats (Typical)

**Attributes:** 
- Start with 7 in each attribute
- Distribute +6 points among attributes (max 12)

**Skills:**
- All skills start at 0
- Distribute 10 points among skills (max 5 in any skill)

**Focuses:**
- Choose 3-5 focuses based on background

**Resources:**
- Stress: Fitness + Discipline
- Determination: 3 points
- Experience: 0 (awarded through play)

### Example Character: House Atreides Guard

```
Attributes:
  Control: 7, Dexterity: 8, Fitness: 9
  Insight: 7, Presence: 7, Reason: 7

Skills:
  Battle: 3, Communicate: 1, Discipline: 2
  Move: 2, Understand: 1

Focuses:
  - Battle: Lasgun
  - Battle: Close Combat
  - Discipline: Guard Duty

Stress: 11/11 (Fitness 9 + Discipline 2)
Determination: 3
```

## Next Steps

### Recommended Additions

1. **Character Creation Wizard**
   - Guided character creation command
   - Point-buy system for attributes/skills
   - Focus selection interface

2. **Combat System**
   - Initiative tracking
   - Combat commands (+attack, +defend)
   - Weapon/armor integration

3. **House System**
   - House membership and reputation
   - House resources and assets
   - Political intrigue mechanics

4. **Faction System**
   - Bene Gesserit, Spacing Guild, CHOAM, etc.
   - Faction standing tracking
   - Faction-specific abilities

5. **Equipment System**
   - Personal shields
   - Weapons (crysknife, maula pistol, lasgun)
   - Stillsuits and desert gear
   - Asset management

6. **Experience System**
   - XP spending commands
   - Advancement rules
   - Milestone tracking

7. **Spice Mechanics**
   - Melange effects
   - Prescience and heightened abilities
   - Addiction tracking

8. **Mentat/Bene Gesserit Systems**
   - Special abilities for trained characters
   - Computation and analysis mechanics
   - Voice and truthsaying

## File Structure

```
C:\Evennia-Dune\
├── typeclasses\
│   ├── characters.py     # Player character typeclass (2d20 system)
│   ├── npcs.py          # NPC typeclass
│   ├── rooms.py         # Formatted room display
│   ├── objects.py       # Base object parent class
│   └── ...
├── commands\
│   ├── dune\
│   │   ├── __init__.py
│   │   ├── dune_cmdset.py    # Dune command set
│   │   ├── CmdSheet.py       # Character sheet commands
│   │   ├── CmdRoll.py        # Dice rolling commands
│   │   └── README.md         # Command documentation
│   ├── commonmux\
│   │   └── ...              # MUX-style RP commands
│   └── default_cmdsets.py   # Command set integration
├── world\
│   └── ...
└── server\
    └── conf\
        └── settings.py      # Server configuration
```

## Resources

- **Evennia Documentation**: https://www.evennia.com/docs/latest/
- **Modiphus 2d20 SRD**: See `modiphus srd/` directory
- **Dune Wiki**: https://dune.fandom.com/

## Support

For questions or issues:
1. Check the command help: `help +roll`, `help +sheet`, etc.
2. Review this documentation
3. Consult the Evennia documentation
4. Check the Modiphus 2d20 SRD PDFs

## Credits

Built using:
- Evennia MUD/MUSH framework
- Modiphus 2d20 system
- Based on Frank Herbert's Dune universe

