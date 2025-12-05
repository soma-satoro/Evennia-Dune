# Character Advancement System - README

## 🎯 Quick Start

### For Players
1. **Check your points**: `+advance`
2. **Spend points**: `+advance/spend <type>/<name>`
3. **View history**: `+advance/history`

### For GMs
1. **Award points**: `+xp/<type> <character>`
2. **Track session**: `+xp/session`
3. **Clear session**: `+xp/session/clear`

## 📚 Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| **ADVANCEMENT_SYSTEM.md** | Complete rules and mechanics | Players & GMs |
| **ADVANCEMENT_QUICK_REFERENCE.md** | Command cheat sheet | Players & GMs |
| **ADVANCEMENT_IMPLEMENTATION_SUMMARY.md** | Technical details | Staff & Developers |

## 🚀 Installation

### Step 1: Server Already Updated
The advancement system is already integrated into the command set.

### Step 2: Initialize Existing Characters
Run this command in-game:
```python
@py from scripts.init_advancement import init_all_characters; init_all_characters()
```

### Step 3: Reload Server
```
@reload
```

### Step 4: Test
```
+advance
```

## 🎮 Basic Usage

### Earning Points

Points are awarded for:
- **Pain** (defeated): 1 point
- **Failure** (D3+ test): 1 point
- **Peril** (4+ Threat): 1 point
- **Ambition minor**: 1 point
- **Ambition major**: 3 points
- **Impress group**: 1 point (max 1/session)

### Spending Points

Players can purchase:
- **Skills** (10+ points): Increase by +1, max 8, once per skill
- **Focuses** (varies): New focus, requires skill 6+
- **Talents** (varies): New talent
- **Assets** (3 points): Make permanent

### Retraining

Half cost (rounded up), but must remove an existing ability.

## 📖 Commands Reference

### Player Commands

```
+advance                              # View status
+advance/spend skill/battle           # Increase skill
+advance/spend focus/Tactics          # Buy focus
+advance/spend talent/Mentat          # Buy talent
+advance/retrain skill=move/battle    # Retrain skill
+advance/history                      # View history
```

### GM Commands

```
+xp/pain Paul                         # Award 1 point (defeat)
+xp/failure Alia                      # Award 1 point (failed test)
+xp/peril Jessica                     # Award 1 point (Threat)
+xp/ambition Leto                     # Award 1 point (minor)
+xp/ambition/major Ghanima            # Award 3 points (major)
+xp/impress Duncan                    # Award 1 point (group)
+xp/custom Stilgar=5                  # Award custom amount
+xp/session                           # View session
+xp/session/list                      # List awards
+xp/session/clear                     # New session
```

## 💡 Examples

### Example 1: Award and Spend

**GM awards a point:**
```
> +xp/failure Jessica
[XP] Failure: Awarded 1 advancement point to Jessica
```

**Player spends it:**
```
> +advance
Available Advancement Points: 12
Focus: 7 points

> +advance/spend focus/Poison
Purchased focus: Poison!
Cost: 7 points, Remaining: 5 points
```

### Example 2: Retraining

**Player retrains a skill:**
```
> +advance/retrain skill=move/battle
Retrained skills!
  Move: 6 → 5
  Battle: 7 → 8
Cost: 6 points (half of 12), Remaining: 2 points
```

### Example 3: Session Tracking

**GM tracks session awards:**
```
> +xp/session/list
================================================================================
                        SESSION ADVANCEMENT AWARDS
================================================================================
Session Start: 2025-12-05 18:00:00

Paul: 4 points
  • Ambition (Major): 3 points (Major contribution to ambition)
  • Pain: 1 point (Defeated in conflict)

Jessica: 2 points
  • Failure: 1 point (Failed Difficulty 3+ test)
  • Peril: 1 point (GM spent 4+ Threat at once)
================================================================================

> +xp/session/clear
[XP] Session tracking cleared.
New session started.
```

## 🧪 Testing

Run the test suite:
```python
@py from scripts.test_advancement import run_all_tests; run_all_tests()
```

Tests include:
- ✅ Initialization
- ✅ Cost calculations
- ✅ Skill advancement
- ✅ Focus advancement
- ✅ Talent advancement
- ✅ Retraining mechanics

## 📋 Cost Summary

| What | Cost | Notes |
|------|------|-------|
| First Skill | 10 | Increases by 1 each time |
| Second Skill | 11 | ... |
| Third Skill | 12 | ... |
| Focus | Current Count | Must have skill 6+ |
| Talent | 3 × Current Count | ... |
| Asset | 3 | Make permanent |
| Retrain | Half (rounded up) | Must sacrifice ability |

## ⚙️ Technical Details

### Data Stored on Characters

```python
character.db.advancement_points        # Current points
character.db.advancement_history       # Complete log
character.db.skill_advances           # Per-skill tracking
character.db.total_skill_advances     # Total count
```

### Files Structure

```
commands/dune/
├── CmdAdvancement.py          # Main advancement command
├── CmdAdvanceAward.py         # Quick award commands
└── dune_cmdset.py            # Command set integration

scripts/
├── init_advancement.py        # Initialize existing characters
└── test_advancement.py        # Test suite

Documentation/
├── ADVANCEMENT_SYSTEM.md              # Complete rules
├── ADVANCEMENT_QUICK_REFERENCE.md     # Cheat sheet
├── ADVANCEMENT_IMPLEMENTATION_SUMMARY.md  # Technical details
└── ADVANCEMENT_README.md              # This file
```

## 🔧 Maintenance

### Initialize New Characters
Characters created through chargen will automatically have advancement tracking.

### Initialize Existing Characters
```python
@py from scripts.init_advancement import init_specific_character; init_specific_character("CharName")
```

### Reset Character Tracking (Staff Only)
```
+advance/reset <character>
```

### Backup Data
```python
@py char = caller.search("CharName")
@py backup = {
    "points": char.db.advancement_points,
    "history": char.db.advancement_history,
    "advances": char.db.skill_advances,
    "total": char.db.total_skill_advances
}
```

## ⚠️ Important Rules

1. **One Advance Per Adventure**: Characters can only purchase ONE advance after each adventure
2. **Skills Cap at 8**: Maximum skill value is 8
3. **Each Skill Advances Once**: Can only advance each skill once
4. **Focus Requires Skill 6+**: Must have at least one skill at 6 or higher
5. **Retraining Costs Half**: All retraining costs half (rounded up)
6. **Retraining Requires Sacrifice**: Must remove/reduce an existing ability

## 🎯 Design Goals

This implementation follows Modiphius 2d20 rules exactly:
- ✅ All costs match official rules
- ✅ All restrictions enforced
- ✅ Complete history tracking
- ✅ Player-friendly interface
- ✅ GM-friendly tools
- ✅ Comprehensive validation
- ✅ Clear error messages

## 🆘 Common Issues

### "I can't buy a focus"
→ You need at least one skill at 6 or higher

### "I can't advance a skill"
→ Each skill can only be advanced once, or it's at max (8)

### "Retrain is half cost?"
→ Yes, but you must sacrifice an existing ability

### "How many advances per adventure?"
→ Only ONE advance per adventure

### "Can I save points?"
→ Yes! Points accumulate and never expire

## 📞 Support

1. **Rules Questions**: Check `ADVANCEMENT_SYSTEM.md`
2. **Command Help**: Use `help +advance` or `help +xp`
3. **Quick Reference**: Check `ADVANCEMENT_QUICK_REFERENCE.md`
4. **Technical Issues**: Check `ADVANCEMENT_IMPLEMENTATION_SUMMARY.md`
5. **Staff Support**: Contact game staff

## 🎓 Learning Path

1. **Start Here**: `ADVANCEMENT_QUICK_REFERENCE.md` (5 min)
2. **Player Guide**: `ADVANCEMENT_SYSTEM.md` - "Gaining Points" & "Spending Points" sections (15 min)
3. **GM Guide**: `ADVANCEMENT_SYSTEM.md` - "GM Guidelines" section (10 min)
4. **Advanced**: `ADVANCEMENT_IMPLEMENTATION_SUMMARY.md` (for developers)

## 🏆 Best Practices

### For Players
1. Save points for meaningful advances
2. Consider your character's story
3. Plan ahead (costs increase!)
4. Don't rush - think strategically
5. Retraining is expensive - be sure!

### For GMs
1. Award points consistently
2. Track session awards with `+xp/session`
3. Be fair with ambition judgements
4. Use clear session boundaries
5. Announce awards publicly

## 📈 Typical Progression

### Early Game (0-10 points)
- Buy 1-2 focuses
- Or save for first skill

### Mid Game (10-30 points)
- 1-2 skill advances
- Several focuses
- 1-2 talents

### Late Game (50+ points)
- Multiple skills advanced
- Many focuses (7-10)
- Several talents (3-5)
- Specialized build

## 🌟 Tips & Tricks

💡 **Get to skill 6 first** to unlock focuses

💡 **Focuses are cheap** early on (0, 1, 2 points)

💡 **Skills get expensive** fast (10, 11, 12...)

💡 **Talents are moderate** cost (0, 3, 6, 9...)

💡 **Retraining** lets you fix mistakes

💡 **Save points** for important milestones

💡 **Match your character** concept

## 🔗 Related Systems

- **Character Generation** (`help chargen`) - Initial creation
- **Character Sheet** (`+sheet`) - View stats
- **Skills & Focuses** (`+stats`) - Manage stats
- **Talents** (`+stats/talent`) - Manage talents
- **Combat** (`help conflict`) - Use your advances!

---

**Version**: 1.0  
**Date**: December 5, 2025  
**Status**: Production Ready  
**Modiphius Compliant**: ✅ Yes

## Quick Links

- [Complete Rules](ADVANCEMENT_SYSTEM.md)
- [Quick Reference](ADVANCEMENT_QUICK_REFERENCE.md)
- [Implementation Details](ADVANCEMENT_IMPLEMENTATION_SUMMARY.md)
- [Test Suite](scripts/test_advancement.py)
- [Initialization Script](scripts/init_advancement.py)

---

*Happy Advancing! May your characters grow and prosper in the Imperium!* 🌌

