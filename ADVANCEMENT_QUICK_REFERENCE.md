# Advancement Quick Reference

## Player Commands

### View Your Advancement Status
```
+advance                    # See points and purchase options
+advance/history            # View detailed history
```

### Spend Points
```
+advance/spend skill/<name>         # Increase skill by 1
+advance/spend focus/<name>         # Purchase new focus
+advance/spend talent/<name>        # Purchase new talent
+advance/spend asset/<name>         # Make asset permanent
```

### Retrain (Half Cost)
```
+advance/retrain skill=<old>/<new>      # Swap skills
+advance/retrain focus=<old>/<new>      # Swap focuses
+advance/retrain talent=<old>/<new>     # Swap talents
```

## GM Commands

### Award Points (Quick)
```
+xp/pain <char>                 # 1 point (defeated)
+xp/failure <char>              # 1 point (failed D3+ test)
+xp/peril <char>                # 1 point (4+ Threat spent)
+xp/ambition <char>             # 1 point (minor ambition)
+xp/ambition/major <char>       # 3 points (major ambition)
+xp/impress <char>              # 1 point (max 1/session)
+xp/custom <char>=<amount>      # Custom amount
```

### Session Tracking
```
+xp/session                     # View session summary
+xp/session/list                # Detailed session awards
+xp/session/clear               # Start new session
```

### Direct Award (Alternative)
```
+advance/award <char>=<points>  # Award points directly
```

## Costs at a Glance

| What | Cost | Notes |
|------|------|-------|
| **First Skill** | 10 | Max 8, once per skill |
| **Second Skill** | 11 | Cost = 10 + previous advances |
| **Third Skill** | 12 | ... |
| **First Focus** | 0 | Cost = current focus count |
| **Third Focus** | 2 | Requires skill 6+ |
| **Seventh Focus** | 6 | ... |
| **First Talent** | 0 | Cost = 3 × current talents |
| **Third Talent** | 6 | ... |
| **Fifth Talent** | 12 | ... |
| **Asset (Permanent)** | 3 | Make temporary asset permanent |
| **Retrain Skill** | 5+ | Half normal cost (rounded up) |
| **Retrain Focus** | 0+ | Half normal cost (rounded up) |
| **Retrain Talent** | 0+ | Half normal cost (rounded up) |

## Earning Points

| Trigger | Points | When |
|---------|--------|------|
| **Pain** | 1 | Defeated in conflict |
| **Failure** | 1 | Failed Difficulty 3+ test |
| **Peril** | 1 | GM spends 4+ Threat at once |
| **Ambition (Minor)** | 1 | Small progress toward ambition |
| **Ambition (Major)** | 3 | Major progress toward ambition |
| **Impress Group** | 1 | Great roleplay/plan (max 1/session) |

## Important Rules

1. ✅ **One advance per adventure** - Choose wisely!
2. ✅ **Skills cap at 8** - Cannot exceed maximum
3. ✅ **Each skill advances once** - Can't spam the same skill
4. ✅ **Focus needs skill 6+** - Must have high skill first
5. ✅ **Retraining requires sacrifice** - Must remove existing ability
6. ✅ **Retraining costs half** - But you lose something

## Example Progression

### New Character (0 points)
- Just starting, saving points

### After First Adventure (earned 3-5 points)
- Could buy 2-3 focuses
- Or save for a skill

### Mid-Campaign (earned 15 points total)
- Could have increased 1 skill
- Could have 3-4 talents
- Or mix of focuses and talents

### Veteran (earned 50+ points)
- Multiple skill increases
- Many focuses and talents
- Specialized and powerful

## Common Questions

**Q: Can I save points between adventures?**
A: Yes! Points accumulate and never expire.

**Q: Can I buy multiple things in one adventure?**
A: No, only ONE advance per adventure.

**Q: What counts as an "adventure"?**
A: GM determines this, typically a complete story arc.

**Q: Can I increase the same skill twice?**
A: No, each skill can only be advanced once.

**Q: Do I lose my talent when retraining?**
A: Yes, you must remove an existing talent to retrain into a new one.

**Q: Can skills go above 8?**
A: No, 8 is the absolute maximum.

**Q: Do I need to spend points immediately?**
A: No, save them as long as you want!

## Tips

💡 **Early Game**: Focus on getting a skill to 6+ so you can buy focuses

💡 **Mid Game**: Diversify with talents and multiple focuses

💡 **Late Game**: Consider retraining to optimize your build

💡 **Specialists**: Max out one skill early, then buy related focuses

💡 **Generalists**: Spread points across multiple skills and talents

💡 **Role-Players**: Choose advances that fit your character's story

## See Full Documentation

For complete rules and examples: `ADVANCEMENT_SYSTEM.md`

