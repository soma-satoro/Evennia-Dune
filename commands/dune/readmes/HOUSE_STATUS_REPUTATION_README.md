# House Status and Reputation System

## Overview

The Status and Reputation system tracks a House's political standing in the Landsraad and the broader Imperium. Status is measured on a scale of 0-100, and determines the House's Reputation level, which has significant mechanical and narrative effects on House actions.

## Status: The 0-100 Scale

**Status** represents the House's political power, influence, and standing among its peers. It's a fluid measure that changes based on:
- Military victories and defeats
- Diplomatic successes and failures
- Major events and storylines
- Alliances made and broken
- Economic success or hardship
- Scandals and triumphs

### Status Range
- **Minimum:** 0 (complete collapse of influence)
- **Maximum:** 100 (pinnacle of power for House type)
- **Dynamic:** Status changes throughout play based on House actions

## Reputation Levels

Reputation is **derived from Status** and varies by House type. There are six reputation levels, each with distinct mechanical effects:

### 1. Feeble
**The House is alone and vulnerable.**

The House is considered isolated, without allies, and facing inevitable attacks. Any attempt to secure new allies or take aggressive action faces severe penalties.

**Mechanical Effects:**
- Aggressive actions: **+2 Difficulty penalty**
- Gaining allies/favor: **+2 Difficulty penalty**
- Attacks by other Houses are inevitable
- Very difficult to negotiate from this position

**Narrative:** The House is seen as weak prey. Vultures circle. Other Houses see opportunity in the House's collapse.

### 2. Weak
**The House has taken losses but survives.**

The House has recently suffered setbacks but still has some friends. Its word doesn't carry the weight it once did, and all aggressive actions face penalties.

**Mechanical Effects:**
- All aggressive actions: **+1 Difficulty penalty**
- Gaining allies/favor: **+1 Difficulty penalty**
- Existing allies may reconsider their support

**Narrative:** The House is recovering from recent defeats. Reputation is tarnished but not destroyed. Careful diplomacy can rebuild standing.

### 3. Respected
**Everything is as it should be.**

The House occupies exactly the space in the Imperium its peers expect. This is the "neutral" reputation—the House is stable, reliable, and predictable.

**Mechanical Effects:**
- **No modifiers** to any actions
- The baseline for House operations

**Narrative:** The House maintains its traditional position. No one is surprised by the House's actions. The status quo is maintained.

### 4. Strong
**The House is thriving within its boundaries.**

The House is doing very well without overreaching. Its people are confident and enthusiastic. Other Houses take notice of its success and may seek alliance or trade.

**Mechanical Effects:**
- All House actions: **-1 Difficulty reduction**
- People of the House are more confident and enthusiastic
- Better recruitment and morale

**Narrative:** The House is on the rise but not threateningly so. Success breeds success. This is a good position to be in.

### 5. Problematic
**The House is too ambitious.**

The House is getting a little too ambitious for comfort. It may be planning moves for greater power, making other Houses nervous. While aggressive actions are easier, diplomacy becomes harder.

**Mechanical Effects:**
- Aggressive actions: **-2 Difficulty reduction**
- Diplomatic actions: **+1 Difficulty penalty**
- Gaining favor/alliance: **+1 Difficulty penalty**
- Other Houses discussing what to do about you: **+1 Threat**

**Narrative:** The House is reaching beyond its traditional bounds. Others are watching carefully and discussing intervention. Success is easier but comes with political cost.

### 6. Dangerous
**The House threatens the established order.**

The House is doing far too well and clearly has designs on resources above its station. Several peers (and possibly the Emperor) are actively plotting its downfall.

**Mechanical Effects:**
- House actions: **-2 Difficulty reduction**
- All diplomatic actions: **+2 Difficulty penalty**
- Any House action or venture: **+1 Threat**
- Active plots against the House by peers

**Narrative:** The House has become a threat to the existing power structure. Every action generates opposition. The House is powerful but isolated and under constant threat.

## Status Thresholds by House Type

The relationship between Status and Reputation varies by House type. A Minor House can be "Dangerous" at a much lower status than a Great House.

### House Minor (including Nascent Houses)

| Status Range | Reputation | Notes |
|--------------|------------|-------|
| 0-10 | Feeble | Nearly destroyed |
| 11-20 | Weak | Recovering from defeat |
| 21-40 | Respected | Normal standing |
| 41-50 | Strong | Doing well |
| 51-70 | Problematic | Overreaching |
| 71+ | Dangerous | Too powerful for a Minor House |

**Notes:** 
- Minor Houses "level out" at Respected (21-40) relatively easily
- A Minor House at 71+ is considered dangerously ambitious
- Nascent Houses start at status 15 (Weak)
- Minor Houses start at status 25 (Respected)

### House Major

| Status Range | Reputation | Notes |
|--------------|------------|-------|
| 0-20 | Feeble | Crisis situation |
| 21-40 | Weak | Weakened position |
| 41-60 | Respected | Expected standing |
| 61-70 | Strong | Prospering |
| 71-80 | Problematic | Ambitious moves |
| 81+ | Dangerous | Threatening Great House status |

**Notes:**
- Major Houses have a wider "normal" range
- Status 81+ suggests the House is making a play for Great House status
- Major Houses start at status 45 (Respected)

### Great House

| Status Range | Reputation | Notes |
|--------------|------------|-------|
| 0-40 | Feeble | Catastrophic decline |
| 41-60 | Weak | Major losses |
| 61-70 | Respected | Maintaining position |
| 71-80 | Strong | Ascendant |
| 81-90 | Problematic | Imperial concern |
| 91+ | Dangerous | Threat to the Emperor |

**Notes:**
- Great Houses have the widest ranges—they're harder to shake
- Status 91+ means the House could challenge the Emperor
- Even "Feeble" (0-40) represents massive resources by Minor House standards
- Great Houses start at status 65 (Respected)

## Starting Status by House Type

When a House is created, it receives a default starting status:

- **Nascent House:** 15 (Weak)
- **House Minor:** 25 (Respected)
- **House Major:** 45 (Respected)
- **Great House:** 65 (Respected)

Most Houses start at "Respected" for their type—occupying their expected place in the hierarchy.

## Changing Status

Status changes through gameplay, staff decisions, and major events:

### Reasons for Status Increase
- Military victories
- Successful diplomatic initiatives
- Acquiring new territories or resources
- Major cultural or scientific achievements
- Favorable marriages or alliances
- Successful completion of major ventures
- Public triumphs and celebrations

### Reasons for Status Decrease
- Military defeats
- Diplomatic failures or scandals
- Loss of territory or resources
- Internal strife or betrayal
- Unfavorable exposure of secrets
- Failed ventures or projects
- Public humiliations

### Rate of Change
Status should change **slowly** in most cases:
- Minor events: ±1-3 status
- Moderate events: ±4-7 status
- Major events: ±8-15 status
- Catastrophic events: ±16-30 status

**Important:** Status changes should be rare enough to feel significant. Not every scene should affect status.

## Commands

### View Current Status
```
+house <house name>
```
The main House display shows current status and reputation.

### View Detailed Status
```
+house/status <house>
```
Shows current status, reputation, effects, and available commands.

**Example:**
```
+house/status Molay

================================= Status for House Molay ==================================

House Type: House Minor
Current Status: 25/100
Reputation: Respected

Effects: No modifiers

Commands:
  +house/status Molay/set=<value>
  +house/status Molay/adjust=<+/-amount>
  +house/status Molay/reputation
```

### Set Status (Staff Only)
```
+house/status <house>/set=<value>
```
Set status to a specific value (0-100).

**Examples:**
```
+house/status Molay/set=30
+house/status Atreides/set=75
```

### Adjust Status (Staff Only)
```
+house/status <house>/adjust=<+/-amount>
```
Increase or decrease status by a relative amount.

**Examples:**
```
+house/status Molay/adjust=+5
+house/status Harkonnen/adjust=-10
```

### View Reputation Details (Staff Only)
```
+house/status <house>/reputation
```
Shows detailed reputation information including:
- Current status and reputation
- Full description of what the reputation means
- Mechanical effects
- Reputation thresholds for the House type

**Example:**
```
+house/status Molay/reputation
```

## Gameplay Integration

### Using Reputation in Scenes

**GM Guidance:**

1. **Check Reputation Before Major House Actions**
   - Before a House takes an action, note its reputation
   - Apply the appropriate difficulty modifiers
   - Narrate how other Houses react based on reputation

2. **Reputation Affects NPC Reactions**
   - **Feeble/Weak:** NPCs are dismissive, contemptuous, opportunistic
   - **Respected:** NPCs treat you as equals
   - **Strong:** NPCs are respectful, seek favor
   - **Problematic/Dangerous:** NPCs are wary, defensive, plotting

3. **Generate Threat Based on Reputation**
   - Problematic and Dangerous reputations generate Threat
   - Use this Threat for complications and enemy actions

### Example Scenarios

#### Scenario 1: Minor House Seeking Alliance (Respected)
```
House Molay (Status 30, Respected) approaches House Vernius for trade alliance.
- Reputation: Respected
- Modifier: None
- Roll: 2d20 + Communicate skill
- Difficulty: Standard (based on situation)
```

#### Scenario 2: Major House at War (Problematic)
```
House Ordos (Status 75, Problematic) launches military campaign.
- Reputation: Problematic
- Modifier: -2 Difficulty for aggressive action
- Roll: 2d20 + Battle skill
- Difficulty: Reduced by 2
- Side Effect: +1 Threat (other Houses plotting)
```

#### Scenario 3: Weakened Great House Negotiating (Weak)
```
House Moritani (Status 50, Weak for Great House) seeks Landsraad support.
- Reputation: Weak
- Modifier: +1 Difficulty penalty for gaining favor
- Roll: 2d20 + Communicate skill
- Difficulty: Increased by 1
- Narrative: Other Houses sense weakness, demand concessions
```

## Status Progression and House Type Changes

### Nascent House → House Minor
When a Nascent House reaches **status 30**, it can transition to House Minor:
- Still uses Minor House reputation table
- Now eligible for more domains and roles
- Represents official recognition of increased standing

**Process:**
1. Reach status 30
2. GM approval based on story
3. Change House type to "House Minor"
4. Status remains the same (now in "Respected" range)

### House Minor → House Major
A rare and significant transition requiring:
- Status of **60+** (reaching Strong/Problematic range)
- Control of an entire planet (not just territory)
- Multiple domains and strong skills
- Significant story achievements
- GM approval

**Process:**
1. Meet requirements above
2. Major story arc justifying ascension
3. Change House type to "House Major"
4. Status usually adjusted down to 45-50 (Respected for Major House)
5. Gain access to additional domains

### House Major → Great House
An epic transition requiring:
- Status of **80+** (Dangerous territory for Major House)
- Control of multiple planets/systems
- Vast resources and military might
- Major historical events and story arcs
- GM and staff approval
- Campaign-level significance

**Process:**
1. Extended storyline over multiple arcs
2. Acquisition of second planet/major holdings
3. Political maneuvering in Landsraad
4. Possible opposition from existing Great Houses
5. Change House type to "Great House"
6. Status adjusted to 65-70 (Respected for Great House)
7. Access to maximum domains

## Maintaining Status

### Natural Decay (Optional Rule)
GMs may implement slow status decay for inactive Houses:
- Houses that don't engage in actions slowly lose status
- Rate: -1 status per [time period - GM choice]
- Minimum: Won't fall below "Weak" threshold unless events dictate
- Represents loss of relevance and influence over time

### Status Maintenance Through Action
Houses maintain and increase status by:
- **Regular engagement** in House-level scenes and plots
- **Successful ventures** (future system)
- **Active diplomacy** with other Houses
- **Military readiness** and occasional action
- **Cultural contributions** to the Imperium

## Staff Guidelines

### When to Adjust Status

**Do Adjust Status For:**
- Major military victories or defeats (±5 to ±15)
- Significant diplomatic achievements or failures (±3 to ±10)
- Major story arc conclusions (±5 to ±20)
- House-wide scandals or triumphs (±5 to ±15)
- Territory gained or lost (±5 to ±10)

**Don't Adjust Status For:**
- Individual character scenes (unless House-wide impact)
- Minor diplomatic interactions
- Routine operations
- Failed individual actions (unless catastrophic)

### Balancing Multiple Houses

When multiple player Houses exist:
- Keep status relatively balanced unless story justifies gaps
- Status 20-40 for Minor Houses is reasonable
- Status 40-60 for Major Houses is reasonable
- Status 60-80 for Great Houses is reasonable

Avoid:
- One House at 80+ while others languish at 20
- All Houses at exactly the same status (boring)
- Wild swings in status without justification

### Communication

**Always inform players when status changes:**
```
+house/status Molay/adjust=+8
Status changed by +8 (25 → 33). Reputation remains Respected.

[Send mail to House Molay members explaining why]
```

**Explain the narrative reason:**
- What event caused the change?
- How do other Houses react?
- What does this mean going forward?

## Integration with Other Systems

### Skills
Reputation affects skill tests:
- **Communicate skill:** Directly affected by reputation modifiers
- **Battle skill:** Problematic/Dangerous Houses get bonuses to aggressive actions
- **Discipline:** May be harder to maintain at very high or low status
- **Move:** Unaffected directly
- **Understand:** Unaffected directly

### Domains
Domains can affect status changes:
- **Political domains:** Provide opportunities to increase status through diplomacy
- **Military domains:** Military victories have greater status impact
- **Espionage domains:** Can prevent status loss from scandals
- **Scientific/Artistic domains:** Cultural triumphs increase status

### Threat
Reputation directly generates Threat:
- **Problematic:** +1 Threat when other Houses discuss you
- **Dangerous:** +1 Threat for any House action or venture
- Use Threat for complications, enemy actions, and dramatic tension

## Future Enhancements

Planned additions to the Status system:

1. **Status Events System**
   - Automated events triggered by reputation thresholds
   - Random events affecting status
   - Status-based plot hooks

2. **Alliance Effects**
   - Allies can help maintain or boost status
   - Allied Houses share reputation bonuses
   - Alliance networks affect status changes

3. **Wealth and Status**
   - Wealth generation affected by status
   - Higher status = more trade opportunities
   - "Feeble" Houses face economic penalties

4. **Landsraad Voting Power**
   - Status determines votes in Landsraad
   - Great Houses have more influence
   - Dangerous Houses face voting penalties

5. **Enemy Interactions**
   - Enemy Houses more likely to act against Dangerous Houses
   - Feeble Houses are easier targets
   - Status affects enemy actions and plots

---

*"In the Landsraad, reputation is everything. A House's standing determines not just what it can do, but what others will allow it to do."*

