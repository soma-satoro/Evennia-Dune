# House Skills System

## Overview

House Skills represent the capabilities and resources of a Noble House across five key areas. Unlike character skills, these represent the collective power, influence, and abilities of the entire House organization.

## The Five House Skills

### Battle
**Military Power and Tactical Skill**

Represents the quality of the House's military forces, training, equipment, and leadership. This includes:
- Spacecraft and weapons systems
- Quality and discipline of soldiers
- Tactical acumen of generals and lieutenants
- Strategic positioning of military assets
- Overall combat readiness

**Used when:** The House goes to war, defends territory, or engages in military operations.

**Example Domains:** Military (all subtypes), Kanly (Machinery, Workers)

### Communicate
**Diplomatic Reputation and Influence**

Measures the House's standing in the Landsraad and the Imperium at large. This includes:
- Diplomatic reputation and favors owed
- Acumen of envoys, spies, and diplomats
- Network of contacts and informants
- Court influence and political capital
- Communication infrastructure

**Used when:** Exerting influence in court, negotiating with other Houses, gathering intelligence.

**Example Domains:** Political (all subtypes), Espionage (Expertise, Workers)

### Discipline
**Loyalty and Internal Stability**

Shows the loyalty and reliability of the House's people and forces. This includes:
- Loyalty of subjects and retainers
- Resistance to infiltration and subversion
- Internal cohesion and morale
- Trust between leadership and followers
- Effectiveness of internal security

**Note:** Both House Atreides and House Harkonnen command high Discipline—Atreides through love, Harkonnen through fear.

**Used when:** Ensuring mission security, resisting espionage, maintaining order, verifying loyalty before major actions.

**Example Domains:** Religion (Workers, Understanding), Military (Workers)

### Move
**Response Time and Crisis Management**

Measures the House's ability to respond quickly to crises and opportunities. This includes:
- Well-placed agents across the Imperium
- Resource distribution and accessibility
- Communication speed and efficiency
- Diplomatic response capability
- Rapid deployment of assets

**Note:** Move applies to both military and civilian responses—a well-placed diplomat can respond to allegations as quickly as a military force can respond to a threat.

**Used when:** Responding to crises, seizing opportunities, deploying resources rapidly.

**Example Domains:** Espionage (all subtypes), Political (Workers)

### Understand
**Academic Excellence and Innovation**

Shows the level of academic, scientific, and artistic excellence the House commands. This includes:
- Scientific research capabilities
- Technological advancement
- Advanced arts and crafts
- Academic institutions and scholars
- Innovation and development capacity

**Used when:** Developing new projects, upgrading technology, conducting research, advancing the arts.

**Example Domains:** Science (all subtypes), Artistic (Understanding), Industrial (Understanding)

## Starting Skill Values

When creating a House, assign the following values to the five skills in any order:

### Great House
**Values:** 9, 8, 7, 6, 5

Great Houses control multiple planets and have vast resources at their disposal.

**Examples:** House Atreides, House Harkonnen, House Corrino

### House Major
**Values:** 8, 7, 6, 5, 4

Major Houses rule entire planets and command significant power in the Landsraad.

**Examples:** House Richese, House Vernius (before its fall)

### House Minor
**Values:** 7, 6, 6, 5, 4

Minor Houses control portions of planets and serve as vassals to Major or Great Houses.

**Examples:** Most player-created Houses will start here

### Nascent House
**Values:** 6, 5, 5, 4, 4

Nascent Houses have just achieved Minor House status and are building their power base.

**Examples:** Newly recognized noble families

## Skill Assignment Guidelines

Consider your House's domains and concept when assigning values:

### Military House
- High Battle (8-9)
- High Discipline (7-8)
- Moderate Move (5-6)
- Lower Communicate and Understand

### Diplomatic/Political House
- High Communicate (8-9)
- High Move (7-8) for rapid diplomatic response
- Moderate Discipline (6)
- Lower Battle and Understand

### Scientific/Industrial House
- High Understand (8-9)
- High Battle or Communicate (7-8) to protect/market research
- Moderate Discipline (6)
- Lower Move

### Espionage House
- High Move (8-9) for rapid intelligence deployment
- High Communicate (7-8) for information networks
- High Discipline (6-7) to resist counter-espionage
- Lower Battle and Understand

### Balanced House
- Distribute values relatively evenly
- Focus two skills based on primary domains
- Keep no skill below 4

## Commands

### View Default Values
```
+house/skill <house>/values
```
Shows recommended starting values for the House's type, current skill levels, and descriptions.

**Example:**
```
+house/skill Molay/values
```

### Initialize All Skills
```
+house/skill <house>/init=<battle>,<communicate>,<discipline>,<move>,<understand>
```
Set all five skills at once using comma-separated values.

**Example:**
```
+house/skill Molay/init=7,6,6,5,4
```

### Set Individual Skill
```
+house/skill <house>/set <skill>=<value>
```
Modify a single skill value.

**Example:**
```
+house/skill Molay/set Battle=8
+house/skill Atreides/set Communicate=9
```

### View House Skills
```
+house <house>
```
The main House display now includes skill values and descriptions.

**Example:**
```
+house Molay
```

## Gameplay Usage

### Skill Tests
When the House takes an action, the GM may call for a House skill test:
- **Target Number:** Typically 10-15 depending on difficulty
- **Dice Pool:** 2d20 + House Skill + any modifiers
- **Success:** Roll under the Target Number
- **Momentum:** Generated on successful rolls for follow-up actions

### Examples of House Actions

#### Battle
- Defending a planet from invasion
- Launching a military campaign
- Positioning forces strategically
- Military logistics and supply

#### Communicate
- Negotiating a treaty
- Swaying Landsraad opinion
- Gathering intelligence through diplomacy
- Managing public relations

#### Discipline
- Preventing infiltration
- Maintaining troop morale
- Ensuring operational security before a mission
- Resisting bribes and corruption

#### Move
- Responding to a sudden crisis
- Deploying assets to a distant location
- Rapid diplomatic intervention
- Emergency resource allocation

#### Understand
- Researching new technology
- Developing improved equipment
- Analyzing enemy capabilities
- Creating artistic masterworks

### Skill Improvement

House skills can be improved through:
1. **Ventures** (see House projects system)
2. **Investment** of Wealth and resources
3. **Major story achievements** at GM discretion
4. **Domain expansion** (adding relevant domains may justify +1 to related skill)

**Note:** House skills cost Wealth to maintain. Without investment, they may gradually drop.

## Integration with Domains

Your House's domains should influence skill assignment:

| Domain Type | Related Skills |
|------------|----------------|
| Artistic | Understand, Communicate |
| Espionage | Move, Communicate, Discipline |
| Farming | Understand, Discipline |
| Industrial | Understand, Battle |
| Kanly | Battle, Move, Discipline |
| Military | Battle, Discipline, Move |
| Political | Communicate, Move |
| Religion | Discipline, Communicate |
| Science | Understand, Move |

## Complete House Creation Example

### House Molay (House Minor)

**Step 1: Create the House**
```
+house/create Molay=House Minor
```

**Step 2: Assign Skills**
```
+house/skill Molay/values
# Review recommendations: 7, 6, 6, 5, 4

+house/skill Molay/init=6,7,5,4,6
# Battle: 6 (adequate defense)
# Communicate: 7 (political and artistic connections)
# Discipline: 5 (moderate loyalty)
# Move: 4 (slower response)
# Understand: 6 (artistic excellence)
```

**Step 3: Verify Skills Match Domains**
```
+house/domain Molay/add primary=Artistic:Produce:Renowned poetry
# Artistic domain supports Understand: 6

+house/domain Molay/add secondary=Kanly:Workers:Hidden assassins
# Kanly domain supports Battle: 6
```

**Reasoning:** House Molay focuses on arts (high Understand) and political connections (high Communicate), with adequate military forces (Battle 6) enhanced by secret assassins. They're not particularly quick to respond (Move 4) and have moderate internal loyalty (Discipline 5).

## Advanced: Skill Focuses

**Note:** House skills do not normally have focuses like character skills. However, the GM may allow a focus if the House has sufficient experts and resources in a very specific area.

**Example:**
- House Molay might have "Battle (Assassination)" if their Kanly domain is particularly strong
- House Richese might have "Understand (Technology)" due to their industrial excellence

**Requirements for a Focus:**
- Relevant primary domain in that area
- Multiple experts or role-holders with that specialty
- Significant House trait supporting it
- GM approval

## Staff Notes

### Creating Balanced Houses

When creating NPC Houses or reviewing player Houses:

1. **Verify skill totals match House type**
   - Great: 35 total (9+8+7+6+5)
   - Major: 30 total (8+7+6+5+4)
   - Minor: 28 total (7+6+6+5+4)
   - Nascent: 24 total (6+5+5+4+4)

2. **Check domain alignment**
   - Primary domains should justify 1-2 high skills
   - Secondary domains should support remaining skills
   - No skill should be orphaned without domain support

3. **Consider enemy relationships**
   - Military rivals → should have comparable Battle scores
   - Political rivals → should have comparable Communicate scores
   - If one House dominates all skills, adjust Threat accordingly

4. **Story integration**
   - Skills should reflect House history and reputation
   - Recent events might justify temporary +1/-1 modifiers
   - Long-term campaigns can permanently change skills

## Future Enhancements

Planned additions to the skills system:

1. **Ventures System**: Projects to improve skills over time
2. **Status and Reputation**: How skills affect House standing
3. **Wealth Costs**: Maintaining high skills requires resources
4. **Skill Degradation**: Skills may decrease without maintenance
5. **Domain Bonuses**: Certain domains provide +1 to related skill tests
6. **Role Bonuses**: Key roles (Warmaster, Spymaster) provide benefits to related skills

---

*"Power requires skill in its application. A great House wields five blades: the sword, the word, the will, the movement, and the mind."*

