# House Status & Reputation Quick Reference

## Six Reputation Levels

| Reputation | Status Meaning | Mechanical Effect |
|------------|----------------|-------------------|
| **Feeble** | Alone & vulnerable | Aggressive: +2 Diff / Allies: +2 Diff |
| **Weak** | Recovering from losses | Aggressive: +1 Diff / Allies: +1 Diff |
| **Respected** | Normal standing | No modifiers |
| **Strong** | Thriving | All actions: -1 Diff |
| **Problematic** | Too ambitious | Aggressive: -2 Diff / Diplomatic: +1 Diff / +1 Threat |
| **Dangerous** | Threatening order | Actions: -2 Diff / Diplomatic: +2 Diff / +1 Threat |

## Status Thresholds by House Type

### House Minor (including Nascent)
```
Feeble:  0-10  │ Weak: 11-20  │ Respected: 21-40
Strong: 41-50  │ Problematic: 51-70  │ Dangerous: 71+
```
**Starting Status:** Nascent: 15 | Minor: 25

### House Major
```
Feeble:  0-20  │ Weak: 21-40  │ Respected: 41-60
Strong: 61-70  │ Problematic: 71-80  │ Dangerous: 81+
```
**Starting Status:** 45

### Great House
```
Feeble:  0-40  │ Weak: 41-60  │ Respected: 61-70
Strong: 71-80  │ Problematic: 81-90  │ Dangerous: 91+
```
**Starting Status:** 65

## Commands

```
+house <name>                           View House (includes status)
+house/status <house>                   View status summary
+house/status <house>/set=<0-100>      Set status (staff)
+house/status <house>/adjust=<+/-#>    Adjust status (staff)
+house/status <house>/reputation       View reputation details (staff)
```

## Quick Examples

### Set Status on Creation
```
+house/create Molay=House Minor
# Auto-sets status to 25 (Respected)

+house/status Molay/set=30
# Manually adjust if needed
```

### Adjust After Major Event
```
+house/status Molay/adjust=+8
# After military victory

+house/status Arcuri/adjust=-12
# After major scandal
```

### Check Reputation Before Action
```
+house/status Atreides/reputation
# Review effects before diplomatic mission
```

## Status Change Guidelines

| Event Type | Status Change |
|------------|---------------|
| Minor event | ±1 to ±3 |
| Moderate event | ±4 to ±7 |
| Major event | ±8 to ±15 |
| Catastrophic | ±16 to ±30 |

### Events That Increase Status
- Military victories
- Successful diplomacy
- New territories/resources
- Cultural achievements
- Beneficial alliances
- Major project completions

### Events That Decrease Status
- Military defeats
- Diplomatic failures
- Lost territories
- Internal strife
- Exposed scandals
- Failed ventures

## Reputation Effects in Play

### Feeble (Desperate)
- NPCs are dismissive or predatory
- Attacks are likely
- Very hard to gain allies
- Focus on survival

### Weak (Wounded)
- NPCs see opportunity
- Must rebuild carefully
- Existing allies may waver
- Recovery is possible

### Respected (Stable)
- NPCs treat as equals
- Standard operations
- Balanced position
- Most Houses here

### Strong (Ascendant)
- NPCs are respectful
- Easier to act
- Success breeds success
- Good position

### Problematic (Ambitious)
- NPCs are wary
- Easy to be aggressive
- Hard to be diplomatic
- Others plotting

### Dangerous (Threatening)
- NPCs are hostile
- Powerful but isolated
- All actions generate Threat
- Multiple enemies

## House Type Transitions

### Nascent → Minor House
- Reach status 30
- GM approval
- Type changes, status stays

### Minor → Major House
- Status 60+ required
- Control entire planet
- Major story achievement
- Rare transition

### Major → Great House
- Status 80+ required
- Multiple planets
- Epic storyline
- Campaign-level event

## Staff Quick Notes

### When to Adjust
✓ Major military outcomes
✓ Significant diplomacy
✓ Story arc conclusions
✓ Territory changes
✓ House-wide scandals

✗ Individual character scenes
✗ Minor interactions
✗ Routine operations
✗ Single failed rolls

### Balancing Tips
- Keep Houses within 20-30 status of each other
- "Respected" is the baseline
- Status 80+ should be rare
- Status below 15 is crisis mode
- Always explain changes to players

### Common Adjustments
```
+house/status House/adjust=+5    # Won battle
+house/status House/adjust=+10   # Major diplomatic victory
+house/status House/adjust=-8    # Lost important territory
+house/status House/adjust=-15   # Major scandal exposed
```

## Integration Notes

### With Skills
- Communicate: Most affected by reputation modifiers
- Battle: Gets bonuses at Problematic/Dangerous
- Discipline: Harder at extremes of status

### With Domains
- Political: More opportunities to affect status
- Military: Military events have bigger impact
- Espionage: Can mitigate status losses
- Cultural: Achievements boost status

### With Threat
- Problematic: +1 Threat when discussed
- Dangerous: +1 Threat per action
- Use for enemy plots and complications

## Reputation Color Codes

When displayed in game:
- **Feeble:** Red (|r)
- **Weak:** Yellow (|y)
- **Respected:** Green (|g)
- **Strong:** Cyan (|c)
- **Problematic:** Magenta (|m)
- **Dangerous:** Bright Red (|R)

---

**Need more detail?** See `HOUSE_STATUS_REPUTATION_README.md` for complete documentation.

