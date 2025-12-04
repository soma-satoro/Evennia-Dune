# Conflict Mechanics Overview

This document describes the general conflict mechanics that apply to all conflict types (Dueling, Skirmish, Espionage, Warfare, Intrigue).

## Core Concepts

### Assets
- **Tangible Assets**: Physical items (weapons, vehicles, troops, surveillance devices)
- **Intangible Assets**: Non-physical resources (positioning, information, leverage, rumors)
- **Quality**: Rated 0-4, affects effectiveness
- Assets can be used across different conflict types

### Zones
- Conflict areas divided into distinct zones
- Zones can be physical (rooms, terrain) or abstract (people, groups, places)
- Zones may have special effects (traits)
- Some zones may be objectives

## Turn Order and Initiative

### Basic Turn Structure
1. Characters take turns in order
2. Each character takes one action per turn
3. Once all characters have acted, a new round begins
4. First turn of each round goes to the initiative holder

### Keeping Initiative
- **Cost**: 2 Momentum (or add 2 Threat for NPCs)
- **Effect**: 
  - Take an extra action immediately (+1 Difficulty to any test)
  - OR allow an allied character to act before opponents
- **Restriction**: Can only be done once per round, and only after at least one enemy has acted

### Turn Passing
- After your turn, you can:
  - Pass to an opposing side (they choose who acts next)
  - Keep the Initiative (spend 2 Momentum)

## Actions

### Move
Move one asset (or character) from current location to an adjacent zone.

**Options:**
- **Normal Movement**: Move to adjacent zone
- **Extra Movement**: Spend 2 Momentum to move one additional zone OR move a second asset
- **Subtle Movement**: Skill test (Difficulty 2)
  - Success: Move asset, reduce Keep Initiative cost to 0
  - Failure: Cannot spend Momentum on extra movement, one enemy may move an asset
- **Bold Movement**: Skill test (Difficulty 2)
  - Success: Move asset, then move one opposing asset
  - Failure: Cannot spend Momentum on extra movement, one enemy may move an asset

### Use an Asset
Use an asset to achieve a goal. Always requires a skill test.

**Common uses:**
- Attack an opponent
- Target an opponent's asset
- Create a trait or asset
- Overcome an obstacle
- Gain information
- Aid a defeated ally

**Contests vs. Skill Tests:**
- Actions affecting opponents are **contests** (opponent resists)
- Other actions are **skill tests**
- Final Difficulty of contests is influenced by defender's assets

## Attacks, Defeat, and Recovery

### Making an Attack
1. Choose asset to use
2. Choose appropriate skill and drive
3. Roll contest against target
4. If successful, determine outcome

### Attack Outcomes

**Minor Characters:**
- Successful attack = immediate defeat

**Notable/Major Characters or Player Characters:**
- Defeat is an **extended task**
- Requirement = target's most appropriate skill
- Points scored = 2 + Quality of asset used
- Can spend 2 Momentum to add +1 Quality for that attack only
- Once requirement is reached, character is defeated

### Defensive Assets
- Each defensive asset in target's zone increases attacker's Difficulty by +1
- Quality of defensive asset is added to extended task requirement
- Some defensive assets can move (half-shields, parrying weapons)
- Most are immobile (armor, full shields)

### Defeat Consequences
- Defeated characters cannot participate in the conflict
- Recovery may require time, ally action, or specific conditions
- Some defeats may be permanent (death, serious injury)
- Spend 2 Momentum after defeating opponent to inflict lasting injury

## Targeting Assets

### Removing Opponent's Assets
- **Skill Test**: Difficulty 2 (or contest if asset is wielded directly)
- **Intangible Assets**: Destroyed when targeted
- **Tangible Assets**: Set aside, can be recovered as an action or at end of scene

## Creating Traits or Assets

### Creating a Trait
- Skill test, Difficulty 2
- Represents new facts, advantages, or circumstances

### Creating an Asset
- Skill test, Difficulty 2
- Created assets have Quality 0
- Must be useful in current conflict type
- Can be intangible (positioning, information) or tangible (concealed items, found objects)
- **Temporary**: Ceases to exist at end of scene
- **Permanent**: Spend 2 Momentum to make permanent (added to character sheet)

## Overcoming Obstacles

### Obstacle Types
- **Physical**: Terrain features, barriers, difficult ground
- **Social/Political**: Access restrictions, isolation, security

### Resolution
- Skill test (Difficulty usually 1, can be higher)
- Appropriate skill depends on obstacle type:
  - Physical: Move, Battle, Discipline
  - Social: Communicate, Understand
- Success: Pass obstacle unhindered
- Failure: Stopped, must find different method

## Gaining Information

### Basic Information Gathering
- Skill test, Difficulty 0 (base)
- Difficulty increases for classified/restricted/obscure information
- Appropriate skills: Understand, Battle, Communicate (depending on context)

### Using Momentum
- Spend 1 Momentum per question to ask the gamemaster
- Momentum can create traits representing advantages
- Momentum can remove concealment/deception traits
- Momentum can be saved for later (up to usual limit)

### Special Cases
- **Questioning Characters**: Contest against character being questioned
- **Converting NPCs**: Extended task (requirement = NPC's Discipline)
- **Piecing Together Information**: Extended task across multiple sources

## Aiding an Ally

### Removing Traits
- Skill test, Difficulty 2
- Removes complications or impairments

### Preventing Lasting Effects
- Skill test, Difficulty 2
- Prevents permanent consequences (death, lasting injury, character traits)
- Ally is still defeated but lasting effect is prevented

### Recovering Defeat
- Extended task
- Requirement = 4 + Quality of asset that defeated the ally
- If completed, ally can rejoin the scene

## Extended Tasks

### When Used
- Defeating non-minor characters
- Complex objectives requiring multiple actions
- Piecing together information from multiple sources

### Mechanics
- **Requirement**: Number of points needed (usually based on target's skill)
- **Points per Success**: 2 + Quality of asset used
- **Momentum**: Can spend 2 Momentum to add +1 Quality for that action
- **Completion**: Once requirement is reached, task is complete

## Conflict Commands

### General Conflict Command (`+conflict`)
- `+conflict/turn` - Show whose turn it is
- `+conflict/next` - Pass to next character
- `+conflict/initiative` - Keep the initiative (spend 2 Momentum)
- `+conflict/move` - Move asset (delegates to conflict-specific command)
- `+conflict/use` - Use asset (shows available actions)
- `+conflict/attack` - Attack with asset
- `+conflict/target` - Target opponent's asset
- `+conflict/create` - Create trait or asset
- `+conflict/obstacle` - Overcome obstacle
- `+conflict/info` - Gain information
- `+conflict/aid` - Aid defeated ally

### Conflict-Specific Commands
Each conflict type has its own command set:
- `+duel` - Dueling conflicts
- `+skirmish` - Skirmish conflicts
- `+espionage` - Espionage conflicts
- `+warfare` - Warfare conflicts
- `+intrigue` - Intrigue conflicts

## Implementation Notes

### Base Conflict Class
The `BaseConflict` class (`typeclasses/conflicts.py`) provides common mechanics:
- Turn order management
- Initiative tracking
- Extended task management
- Point calculation

### Conflict-Specific Classes
Each conflict type extends or implements its own mechanics:
- `Duel` - One-on-one combat
- `Skirmish` - Small-scale multi-combatant conflicts
- `Espionage` - Information-based conflicts
- `Warfare` - Large-scale military conflicts
- `Intrigue` - Social/political conflicts

All conflict types share the general mechanics described above, but implement them in ways appropriate to their specific context.

