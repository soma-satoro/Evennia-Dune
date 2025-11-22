# Domain Spaces System

## Overview

The Domain Spaces system creates a territorial and economic foundation for Noble Houses by linking their **domains** to physical **spaces** on **planets**. This system models how Houses control exploitable territory to support their areas of expertise, generating wealth and power.

## Core Concepts

### What are Spaces?

**Spaces** represent exploitable territory on a planet or moon—areas that can be cleared, developed, and made ready for holdings, mines, industries, or other domain activities. They are abstract units that represent:
- Agricultural land for Farming domains
- Industrial zones for Industrial/Science domains
- Urban areas for Political/Artistic domains
- Training grounds for Military/Kanly domains
- Research facilities for Science domains

###Typical Space Availability

- **Planets:** 80 spaces (average)
- **Moons:** 30 spaces (average)
- **Custom:** Staff can adjust based on planetary size and nature

These numbers represent "easy" exploitable territory. Houses can expand beyond this with consequences (see Space Expansion below).

### Space Requirements by House Type

Different House types typically control different amounts of territory:

| House Type | Typical Spaces | Notes |
|------------|---------------|-------|
| **Nascent House** | 10 | Just starting out, limited holdings |
| **House Minor** | 35 | Established presence, ~1/3 of a planet |
| **House Major** | 60 | Controls most/all of a planet |
| **Great House** | 100+ | Multiple planets, vast holdings |

**Important:** These are typical values. Actual space control varies based on:
- Number and quality of planets controlled
- Political situation and alliances
- Military strength and expansion
- Story developments and ventures

## Domain Space Requirements

Each domain a House maintains requires dedicated spaces to operate:

### Primary Domain: 25 Spaces
Primary domains represent major investments in expertise, infrastructure, and personnel. They require:
- Large-scale facilities (factories, bases, academies)
- Significant workforce
- Supporting infrastructure
- Supply chains and logistics

**Examples:**
- **Military Primary:** Bases, training grounds, armories, vehicle depots
- **Industrial Primary:** Factories, shipyards, refineries, warehouses
- **Political Primary:** Palace complexes, embassy networks, administrative centers
- **Science Primary:** Research labs, universities, testing grounds

### Secondary Domain: 10 Spaces
Secondary domains are smaller but still significant operations:
- Moderate facilities
- Specialist workforce
- Focused infrastructure
- Limited but effective operations

**Examples:**
- **Espionage Secondary:** Safe houses, communications networks, training facilities
- **Farming Secondary:** Agricultural estates, processing facilities
- **Artistic Secondary:** Theaters, studios, performance venues

### Calculating Requirements

```
Total Required Spaces = (Primary Domains × 25) + (Secondary Domains × 10)
```

**Example: House Minor**
- 1 Primary Domain (Military): 25 spaces
- 1 Secondary Domain (Political): 10 spaces
- **Total Required:** 35 spaces

**Example: Great House**
- 2 Primary Domains: 50 spaces
- 3 Secondary Domains: 30 spaces
- **Total Required:** 80 spaces

## Multi-House Planets

Planets can be divided among multiple Houses, creating complex political situations:

### Shared Control Scenarios

**House Major + Minor Houses (Common)**
```
Planet Caladan (80 spaces total)
- House Atreides (Major): 60 spaces
- House Molay (Minor, vassal): 15 spaces
- House Verdan (Minor, vassal): 5 spaces
```

**Multiple Equal Minor Houses (Rare)**
```
Planet Contested (80 spaces total)
- House Ordos: 40 spaces
- House Richese: 40 spaces
(Neither has clear dominance, political tension)
```

**Great House with Scattered Holdings**
```
House Corrino controls:
- Kaitain (homeworld): 90 spaces
- Salusa Secundus: 60 spaces
- Minor holdings on 5 other planets: 10 spaces each
Total: 200 spaces
```

### Political Affiliation vs. Space Control

- **Political Affiliation:** Which House officially rules the planet
- **Space Control:** Actual territorial holdings

A planet may be politically affiliated with one House but have spaces controlled by multiple Houses (vassals, allies, or contested territories).

## Space Surplus and Deficit

### Surplus Spaces
When a House controls more spaces than required for domains:

**Benefits:**
- **Expansion capacity:** Can add new domains
- **Wealth generation:** Excess spaces can generate income (future system)
- **Strategic reserve:** Buffer against losses
- **Political leverage:** Can grant spaces to allies or vassals

**Example:**
```
House Minor
- Controlled Spaces: 50
- Required for Domains: 35
- Surplus: 15 spaces (can add 1 more secondary domain or save for primary)
```

### Deficit Spaces
When domain requirements exceed controlled spaces:

**Consequences:**
- **Undermanned operations:** Domains don't function at full capacity
- **Reduced efficiency:** Domain benefits are lessened
- **Staff concern:** GM may impose penalties
- **Storyline:** Must acquire more territory or reduce domains

**Example:**
```
House Minor (ambitious)
- Controlled Spaces: 30
- Required for Domains: 45 (1 primary, 2 secondary)
- Deficit: -15 spaces (operations are stretched thin)
```

**House Response to Deficit:**
1. **Acquire more territory** - conquest, purchase, negotiation
2. **Remove a domain** - downsize operations
3. **Reduce domain from primary to secondary** - scale back
4. **Space expansion** (drastic measure, see below)

## Space Expansion (Drastic Measures)

Houses can exceed a planet's "typical" space limit through aggressive development:

### Methods
- **Reduce living space for population:** Pack people more densely
- **Destroy natural habitats:** Clear forests, drain wetlands, level mountains
- **Develop inhospitable areas:** Desert reclamation, ocean platforms, underground complexes
- **Militarize civilian areas:** Convert towns to military bases

### Consequences

**Population Unrest:**
- Unhappy populace works against the nobility
- Increased crime and resistance
- Reduced loyalty (affects Discipline skill)
- Potential for rebellion or sabotage

**Environmental Degradation:**
- Planet becomes polluted
- Unpleasant to live on
- Reduced attractiveness for trade and diplomacy
- May affect tourism or cultural endeavors

**Mechanical Effects (Future):**
- Status penalties
- Discipline skill tests harder
- Communicate skill penalties when dealing with other Houses
- Potential random events (protests, accidents, environmental disasters)

**When Worth It:**
Houses may accept these consequences when:
- Desperate for more domains
- Pursuing aggressive expansion
- At war and need military capacity
- Wealthy enough to manage discontent

### Example
```
Planet Veridia (normally 80 spaces)
House Harkonnen expands to 95 spaces
- Population unhappy (living in cramped industrial zones)
- Planet polluted (factories everywhere)
- Harkonnen can support 3 primary domains instead of 2
- But: Discipline -1 for tests involving Veridia forces
```

## Commands

### Planet Space Management (Staff Only)

#### View Space Allocations
```
+planet/spaces <planet>
```
Shows total spaces, allocations by House, and available spaces.

**Example:**
```
+planet/spaces Arrakis

=================== Space Allocations for Arrakis ====================

Total Spaces: 80
Allocated: 60
Available: 20

Allocations by House:
  House Atreides: 60 spaces (75.0%)

Commands:
  +planet/spaces Arrakis/total=<number>
  +planet/spaces Arrakis/allocate=<house>:<spaces>
  +planet/spaces Arrakis/deallocate=<house>
```

#### Set Total Spaces
```
+planet/spaces <planet>/total=<number>
```
Set the total number of exploitable spaces on a planet.

**Examples:**
```
+planet/spaces Arrakis/total=80
+planet/spaces Giedi Prime/total=90
+planet/spaces Small Moon/total=25
```

**Note:** Cannot reduce total below currently allocated spaces.

#### Allocate Spaces to House
```
+planet/spaces <planet>/allocate=<house>:<spaces>
```
Allocate (or adjust) spaces for a House on a planet.

**Examples:**
```
+planet/spaces Arrakis/allocate=House Atreides:60
+planet/spaces Caladan/allocate=House Molay:15
```

**Behavior:**
- Creates new allocation if House has none on this planet
- Updates existing allocation if House already present
- Automatically adds House to planet's Houses list
- Checks available space before allocating

#### Remove House Allocation
```
+planet/spaces <planet>/deallocate=<house>
```
Remove all space allocations for a House on a planet.

**Example:**
```
+planet/spaces Arrakis/deallocate=House Harkonnen
```

### House Space Management (Staff Only)

#### View House Spaces
```
+house/spaces <house>
```
Shows House's total spaces, requirements, surplus/deficit, and planet allocations.

**Example:**
```
+house/spaces Molay

================ Space Allocations for House Molay ===================

House Type: House Minor (Typical: 35 spaces)
Total Spaces Controlled: 35
Domain Requirements: 35 spaces
Surplus: 0 spaces available

Domain Space Requirements:
  Primary (Artistic): 25 spaces
  Secondary (Kanly): 10 spaces

Planet Allocations:
  Molay Prime: 35 spaces (100.0%)

Commands:
  +house/spaces Molay/allocate=<planet>:<spaces>
  +house/spaces Molay/deallocate=<planet>
```

#### Allocate Spaces (from House perspective)
```
+house/spaces <house>/allocate=<planet>:<spaces>
```
Allocate spaces to this House on a planet.

**Examples:**
```
+house/spaces Atreides/allocate=Arrakis:60
+house/spaces Molay/allocate=Molay Prime:35
```

**Same effect as planet command, just different perspective.**

#### Remove Allocation (from House perspective)
```
+house/spaces <house>/deallocate=<planet>
```
Remove House's allocation on a planet.

**Example:**
```
+house/spaces Harkonnen/deallocate=Arrakis
```

## Integration with Existing Systems

### Skills
Space control affects House skills:

- **Battle:** Military domains require spaces for bases and training
- **Understand:** Science/Artistic domains require spaces for research/culture
- **Discipline:** Space deficits or expansion may penalize Discipline
- **Communicate:** Environmental degradation may penalize diplomatic efforts

### Status and Reputation
Space control can affect status:
- Acquiring new territory → Status increase
- Losing territory → Status decrease
- Space expansion at population's expense → Potential Status penalties
- Efficient use of spaces → No effect
- Major deficit → Status concerns from peers

### Domains
Domains **require** spaces to function:
- Cannot add domain without sufficient spaces
- Must maintain space allocations
- Deficit means domains are undermanned
- Surplus means expansion capacity

### Planets
Planets track their space allocations:
- Shows which Houses control territory
- Multiple Houses can co-exist
- Political affiliation ≠ space control necessarily
- Display now shows space breakdowns

## Complete House Creation with Spaces

### Step-by-Step Example: House Molay (House Minor)

```
# 1. Create House
+house/create Molay=House Minor
# Status: 25 (Respected)

# 2. Set Skills
+house/skill Molay/init=6,7,5,4,6

# 3. Create Homeworld Planet
+planet/create Molay Prime
+planet/set Molay Prime/habitability=Habitable
+planet/set Molay Prime/type=Forested World
+planet/set Molay Prime/population=2000000
+planet/set Molay Prime/affiliation=House Molay

# 4. Set Planet Spaces (default is 80, adjust if needed)
+planet/spaces Molay Prime/total=80

# 5. Allocate Spaces to House
# House Minor typically has 35 spaces
+house/spaces Molay/allocate=Molay Prime:35

# Check allocation
+house/spaces Molay
# Shows: 35 spaces controlled, 0 required (no domains yet), 35 surplus

# 6. Add Domains
+house/domain Molay/add primary=Artistic:Produce:Poetry
# Now requires 25 spaces, surplus = 10

+house/domain Molay/add secondary=Kanly:Workers:Assassins
# Now requires 35 spaces, surplus = 0 (perfect fit!)

# 7. View Complete Setup
+house Molay
# Shows all information including Territory and Domains section

+planet Molay Prime
# Shows House Molay controls 35/80 spaces (45 available)
```

### Example: Multi-Planet Great House

```
# House Corrino (Great House, 100 spaces typical)

# Homeworld: Kaitain
+house/spaces Corrino/allocate=Kaitain:70

# Prison Planet: Salusa Secundus
+house/spaces Corrino/allocate=Salusa Secundus:20

# Minor holdings
+house/spaces Corrino/allocate=Harmonthep:10

# Total: 100 spaces
# 2 Primary domains (50) + 3 Secondary domains (30) = 80 required
# Surplus: 20 spaces
```

## Future Enhancements

### Phase 1: Spaces Foundation (COMPLETED)
- ✅ Space tracking on planets
- ✅ Space allocations by House
- ✅ Domain space requirements
- ✅ Surplus/deficit calculations
- ✅ Management commands
- ✅ Display integration

### Phase 2: Space Expansion Mechanics (NEXT)
- Drastic measures to gain more spaces
- Population unhappiness tracking
- Environmental degradation effects
- Mechanical penalties for over-expansion
- Status impacts

### Phase 3: Wealth Generation
- Spaces generate wealth based on domain type
- Surplus spaces provide bonus income
- Deficit spaces reduce income
- Planet type affects wealth generation
- Integration with treasury system

### Phase 4: Role Actions
- Specific roles can initiate space expansion
- Treasurer can manage space efficiency
- Marshal can militarize civilian areas
- Scholar can research space-saving technologies
- Warmaster can conquer new territories

### Phase 5: Subfief System
- Planets can be divided into subfiefs
- Each subfief has own space allocation
- Minor Houses as vassals control subfiefs
- Wealth and resources split accordingly
- Complex vassal relationships

### Phase 6: Territory Ventures
- Ventures to acquire new spaces
- Development projects
- Terraforming and reclamation
- Space optimization
- Cost-benefit analysis

## Staff Guidelines

### Assigning Starting Spaces

When creating a new House:

1. **Determine House Type**
   - Use typical spaces as baseline

2. **Create or Assign Homeworld**
   - Set total spaces (80 for planets, 30 for moons)
   - Adjust if unusual planet size

3. **Allocate Initial Spaces**
   - Match typical value for House type
   - Can adjust based on story
   - Ensure alignment with planned domains

4. **Plan Domain Requirements**
   - Calculate: (Primary × 25) + (Secondary × 10)
   - Ensure House has enough spaces
   - Small surplus is ideal (5-10 spaces)

### Balancing Multi-House Planets

When multiple Houses share a planet:

**Guidelines:**
- Major House should control 60-80% of spaces
- Minor Houses get remainder
- Leave 10-20% unallocated for future expansion
- Political affiliation usually = largest space holder
- Contested planets can be 50/50 splits

**Example Distributions:**
```
80-space planet with House Major + 2 Minors:
- Major House: 50 spaces (62.5%)
- Minor House A: 15 spaces (18.75%)
- Minor House B: 10 spaces (12.5%)
- Unallocated: 5 spaces (6.25%)
```

### Adjusting Spaces During Play

**Increase spaces when:**
- House conquers territory (+10 to +30 spaces)
- House negotiates land grants (+5 to +15 spaces)
- House completes development venture (+5 to +10 spaces)
- House acquires new planet (varies)

**Decrease spaces when:**
- House loses territory in war (-10 to -40 spaces)
- House cedes land in treaty (-5 to +20 spaces)
- Environmental disaster (-5 to -15 spaces)
- Rebellion/uprising (-10 to -25 spaces)

**Always:**
- Inform players of changes
- Explain narrative reason
- Check if affects domain requirements
- Update both House and Planet records

### Handling Space Deficits

If a House has space deficit:

1. **Immediate:** Inform player
2. **Short-term:** Give grace period (1-2 story arcs)
3. **Consequences:** 
   - Domains operate at reduced capacity
   - May impose skill test penalties
   - Status concerns from peers
4. **Resolution options:**
   - Acquire more territory (conquest, purchase, negotiation)
   - Remove a domain
   - Downgrade primary to secondary
   - Space expansion (with consequences)

### Space Expansion Approval

When players want to expand beyond planet's typical spaces:

**Consider:**
- Is House desperate enough?
- Can House handle the consequences?
- Does it fit the story?
- Will it create interesting RP?

**If approved:**
- Set new total (typically +10 to +20 spaces max)
- Note population unrest in planet description
- Note environmental issues
- Apply mechanical penalties:
  - Discipline tests involving that planet: +1 Difficulty
  - Communicate tests when planet mentioned: +1 Difficulty
- Create potential story hooks (protests, accidents, etc.)

---

*"Territory is power. A House without land is a House without teeth. But land without people is a desert, and people without hope are a rebellion waiting to happen."*

