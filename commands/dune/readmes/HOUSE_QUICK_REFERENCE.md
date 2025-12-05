# House System Quick Reference

## Quick Command List

### Everyone
```
+house <name>        View House information
+house/list          List all Houses
```

### Staff Only (Builder+)

#### Creation
```
+housecreate <name>=<type>
```

#### Basic Setup
```
+houseset <house>/type=<Nascent House|House Minor|House Major|Great House>
+houseset <house>/banner=<color>,<color>
+houseset <house>/crest=<symbol>
+houseset <house>/trait=<trait name>
+houseset <house>/homeworld=<name>
+houseset <house>/desc=<description>
```

#### Domains
```
+housedomain <house>/list
+housedomain <house>/areas
+housedomain <house>/add primary=<area>:<subtype>:<description>
+housedomain <house>/add secondary=<area>:<subtype>:<description>
+housedomain <house>/remove primary|secondary=<#>
```

#### Roles
```
+houserole <house>/list
+houserole <house>/set <role>=<name>[:<desc>][:<traits>]
+houserole <house>/remove <role>
```

#### Enemies
```
+houseenemy <house>/list
+houseenemy <house>/add=<enemy>:<hatred>:<reason>
+houseenemy <house>/remove=<#>
```

#### Members
```
+housemember <character>
+housemember <house>/list
+housemember <house>/add=<character>
+housemember <house>/remove=<character>
```

## House Types

| Type | Threat/Player | Primary | Secondary |
|------|--------------|---------|-----------|
| Nascent | 0 | 0 | 1 |
| Minor | 1 | 1 | 1 |
| Major | 2 | 1 | 2 |
| Great | 3 | 2 | 3 |

## Domain Areas

**Artistic** - Art, poetry, theater
**Espionage** - Spies, intelligence
**Farming** - Agriculture, crops
**Industrial** - Manufacturing, technology
**Kanly** - Assassination, poisons
**Military** - Soldiers, weapons
**Political** - Diplomacy, intrigue
**Religion** - Faith, clergy
**Science** - Research, genetics

## Domain Subtypes

**Machinery** - Equipment
**Produce** - Products
**Expertise** - Leaders
**Workers** - Staff
**Understanding** - Knowledge

## Roles

Ruler, Consort, Advisor, Chief Physician, Councilor, Envoy, Heir, Marshal, Scholar, Spymaster, Swordmaster, Treasurer, Warmaster

## Hatred Levels

**Dislike** - +1 Difficulty
**Rival** - Active opposition
**Loathing** - Plans destruction
**Kanly** - Blood feud

## Enemy Reasons

Competition, Slight, Debt, Ancient Feud, Morality, Servitude, Family Ties, Theft, Jealousy, No Reason

## Example House Creation (5 Minutes)

```bash
# Create House
+housecreate MyHouse=House Minor

# Basic info
+houseset MyHouse/banner=Blue,Silver
+houseset MyHouse/crest=Hawk
+houseset MyHouse/homeworld=MyWorld Prime
+houseset MyHouse/trait=Honorable

# Add domains
+housedomain MyHouse/add primary=Military:Expertise:Elite tacticians
+housedomain MyHouse/add secondary=Political:Produce:Political favors

# Set ruler
+houserole MyHouse/set Ruler=Duke/Duchess Name:Description:Honorable

# Add enemy (optional)
+houseenemy MyHouse/add=Enemy House:Rival:Competition

# Add characters
+housemember MyHouse/add=CharacterName
```

## Tips

1. **Primary domains** automatically add traits
2. **House traits** cost 1 Momentum for characters to use
3. Set **Ruler** role first, then other key positions
4. **Homeworld description** is freeform - be creative!
5. **Enemy reasons** should tell a story
6. Domain **descriptions** can be specific (e.g., "Pundi rice" not just "Crops")

