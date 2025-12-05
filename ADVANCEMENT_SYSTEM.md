# Character Advancement System

This document describes the character advancement system for the Dune 2d20 MUSH, implementing the Modiphius rules for character growth and improvement.

## Overview

Characters gain **Advancement Points** through play and can spend them to improve their abilities. Players may only purchase **one advance per adventure**, and each type of advancement has specific costs and restrictions.

## Gaining Advancement Points

Characters can earn advancement points through the following means:

### 1. **Adversity**

Advancement comes from facing difficult situations, making mistakes, and suffering consequences:

- **Pain**: Gain **1 point** when defeated during conflict
  - Command: `+xp/pain <character>`
  
- **Failure**: Gain **1 point** when failing a test with Difficulty 3 or higher
  - Command: `+xp/failure <character>`
  
- **Peril**: Gain **1 point** when the GM spends 4 or more Threat points at once
  - Command: `+xp/peril <character>`

### 2. **Ambition**

Characters gain points when succeeding at actions that support their ambition:

- **Minor Contribution**: **1 point** for minor progress toward ambition
  - Command: `+xp/ambition <character>`
  
- **Major Contribution**: **3 points** for major progress toward ambition
  - Command: `+xp/ambition/major <character>`

*Note: This does not require a skill test, but if one is involved, it must succeed.*

### 3. **Impressing the Group**

- Gain **1 point** for especially good plans, roleplay, or noteworthy contributions
- **Maximum once per session**
- Command: `+xp/impress <character>`

### 4. **Custom Awards**

Staff can award custom amounts for special circumstances:
- Command: `+xp/custom <character>=<amount>`

## Spending Advancement Points

View your advancement options with: `+advance`

Characters may purchase **ONE advance per adventure**. Available advances:

### 1. Skill Increase

**Cost**: 10 + (previous skill advances)
- Increase any skill by +1
- Maximum skill value: **8**
- **Each skill can only be advanced once**
- First skill advance costs **10 points**
- Second skill advance costs **11 points**
- Third skill advance costs **12 points**, etc.

**Command**: `+advance/spend skill/<skillname>`

**Example**:
```
+advance/spend skill/battle
```

### 2. Focus

**Cost**: Equal to current number of focuses
- Purchase a new focus for a skill
- **Requires at least one skill at 6 or higher**
- If you have 3 focuses, the next costs **3 points**
- If you have 7 focuses, the next costs **7 points**

**Command**: `+advance/spend focus/<focusname>`

**Examples**:
```
+advance/spend focus/Tactics
+advance/spend focus/music/baliset
+advance/spend focus/survival/desert
```

### 3. Talent

**Cost**: 3 × current number of talents
- Purchase a new talent
- If you have 2 talents, the next costs **6 points**
- If you have 5 talents, the next costs **15 points**

**Command**: `+advance/spend talent/<talentname>`

**Example**:
```
+advance/spend talent/Mentat Training
```

### 4. Asset

**Cost**: 3 points (permanent) or 2 × new Quality (improve)
- Make a temporary asset permanent: **3 points**
- Improve asset Quality by +1: **2 × new Quality points**
  - Improving from Quality 2 to 3 costs **6 points**
  - Improving from Quality 3 to 4 costs **8 points**

**Commands**:
```
+advance/spend asset/<assetname>              # Make permanent
+advance/spend asset/<assetname>/quality      # Improve quality (not yet implemented)
```

## Retraining

Characters can retrain abilities at **half cost (rounded up)**, but must sacrifice an existing ability:

### Skill Retraining

- **Cost**: (10 + previous advances) ÷ 2, rounded up
- Must reduce another skill by 1 (minimum 4)
- Still counts as having advanced a skill (can only do once per skill)

**Command**: `+advance/retrain skill=<oldskill>/<newskill>`

**Example**:
```
+advance/retrain skill=move/battle
```
*Reduces Move by 1, increases Battle by 1*

### Focus Retraining

- **Cost**: (current focus count) ÷ 2, rounded up
- Must remove an existing focus

**Command**: `+advance/retrain focus=<oldfocus>/<newfocus>`

**Example**:
```
+advance/retrain focus=Charm/Tactics
```

### Talent Retraining

- **Cost**: (3 × current talent count) ÷ 2, rounded up
- Must remove an existing talent

**Command**: `+advance/retrain talent=<oldtalent>/<newtalent>`

**Example**:
```
+advance/retrain talent=Old Talent Name/New Talent Name
```

## Commands Reference

### Player Commands

| Command | Description |
|---------|-------------|
| `+advance` | View advancement points and purchase options |
| `+advance/spend skill/<name>` | Spend points to increase a skill |
| `+advance/spend focus/<name>` | Spend points to purchase a focus |
| `+advance/spend talent/<name>` | Spend points to purchase a talent |
| `+advance/spend asset/<name>` | Spend points to make asset permanent |
| `+advance/retrain skill=<old>/<new>` | Retrain a skill (half cost) |
| `+advance/retrain focus=<old>/<new>` | Retrain a focus (half cost) |
| `+advance/retrain talent=<old>/<new>` | Retrain a talent (half cost) |
| `+advance/history` | View detailed advancement history |

### Staff Commands

| Command | Description |
|---------|-------------|
| `+xp/pain <character>` | Award 1 point (defeated in conflict) |
| `+xp/failure <character>` | Award 1 point (failed D3+ test) |
| `+xp/peril <character>` | Award 1 point (GM spent 4+ Threat) |
| `+xp/ambition <character>` | Award 1 point (minor ambition) |
| `+xp/ambition/major <character>` | Award 3 points (major ambition) |
| `+xp/impress <character>` | Award 1 point (impressed group) |
| `+xp/custom <character>=<amount>` | Award custom amount |
| `+advance/award <character>=<points>` | Award points directly |
| `+advance/reset <character>` | Reset advancement tracking |
| `+xp/session` | View current session awards |
| `+xp/session/list` | List all session awards |
| `+xp/session/clear` | Clear session tracking (new session) |

## Examples

### Example 1: Gaining and Spending Points

**Scenario**: Jessica fails a Difficult 3 test and is awarded a point:

```
> +xp/failure Jessica
[XP] Failure: Awarded 1 advancement point to Jessica
Reason: Failed Difficulty 3+ test
New total: 12 points
```

Jessica decides to spend her points on a new focus:

```
> +advance
Available Advancement Points: 12

What You Can Purchase:
...
Focus: 7 points (Requires skill 6+)
  Current focuses: 7

> +advance/spend focus/Poison
Purchased focus: Poison!
Cost: 7 points, Remaining: 5 points
```

### Example 2: Retraining

**Scenario**: Duncan wants to shift focus from Move to Battle:

```
> +advance
Available Advancement Points: 8

Skills:
  battle      (Current: 7) - 11 points (already advanced)
  move        (Current: 6) - 11 points
  ...

> +advance/retrain skill=move/battle
Retrained skills!
  Move: 6 → 5
  Battle: 7 → 8
Cost: 6 points (half of 11), Remaining: 2 points
```

### Example 3: Major Ambition

**Scenario**: Paul makes a major contribution to his ambition:

```
> +xp/ambition/major Paul
[XP] Ambition (Major): Awarded 3 advancement points to Paul
Reason: Major contribution to ambition
New total: 15 points
```

## Important Rules

1. **One Advance Per Adventure**: Characters can only purchase ONE advance after each adventure
2. **Skill Advances Are Once Per Skill**: Each skill can only be advanced once through the advancement system
3. **Maximum Skill Value**: Skills cannot exceed 8
4. **Focus Requirement**: Must have at least one skill at 6+ to purchase focuses
5. **Retraining Costs Half**: All retraining costs half the normal cost (rounded up)
6. **Retraining Requires Sacrifice**: Must remove/reduce an existing ability to retrain

## Advancement Point Costs Summary

| Advance Type | Cost Formula | Example |
|--------------|--------------|---------|
| Skill (first time) | 10 + skill advances | 10, 11, 12, 13... |
| Focus | Current focus count | 0, 1, 2, 3, 4... |
| Talent | 3 × current talents | 0, 3, 6, 9, 12... |
| Asset (permanent) | 3 | 3 |
| Asset (improve) | 2 × new Quality | 4, 6, 8, 10... |
| Retrain Skill | (10 + advances) ÷ 2 ↑ | 5, 6, 6, 7, 7... |
| Retrain Focus | (focus count) ÷ 2 ↑ | 0, 1, 1, 2, 2... |
| Retrain Talent | (3 × talents) ÷ 2 ↑ | 0, 2, 3, 5, 6... |

*↑ = rounded up*

## GM Guidelines

### When to Award Points

- **Automatically**: Pain (defeat), Failure (D3+), Peril (4+ Threat spent)
- **Session-Based**: Impressing the Group (max once per session)
- **Discretionary**: Ambition contributions (judge minor vs. major)

### Session Tracking

Use `+xp/session` commands to track awards during a session:

```
> +xp/session/list
Shows all awards this session

> +xp/session/clear
Clears tracking for new session
```

### Ambition Judgement

- **Minor**: Small steps, partial progress, indirect support
  - Example: Gathering information relevant to ambition
  - Example: Making an alliance that might help later
  
- **Major**: Significant progress, direct achievement, critical milestones
  - Example: Completing a major phase of the ambition
  - Example: Achieving a key objective that directly advances the goal

### Adventure Definition

An "adventure" is typically:
- A complete story arc or mission
- A significant in-game time period (varies by game pace)
- GM discretion based on story pacing

Characters can only purchase **one advance** per adventure to prevent rapid power growth.

## Technical Implementation

The system tracks:
- `advancement_points`: Current available points
- `advancement_history`: Complete log of awards and purchases
- `skill_advances`: Per-skill tracking of how many times advanced
- `total_skill_advances`: Total count for cost calculation

All data is stored on the character object and persists across sessions.

## See Also

- `help +advance` - In-game help for advancement commands
- `help +xp` - In-game help for awarding points
- Character Sheet (`+sheet`) - View current stats
- Character Generation (`help chargen`) - Initial character creation

