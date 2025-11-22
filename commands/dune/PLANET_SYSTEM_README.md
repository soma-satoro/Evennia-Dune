# Planet System

This document describes the Planet system for the Dune MUSH, including the `+planet` command and Planet typeclass.

## Overview

The Planet system allows staff to create and manage planetary bodies in the Dune universe. Each planet can have various characteristics including habitability, population, industries, and political affiliations with Houses. Rooms can be set to be on specific planets to inherit planet-specific features.

## Staff Commands

### Viewing Planets

**List all planets:**
```
+planet/list
```

**View a specific planet:**
```
+planet <planet name>
```

Example:
```
+planet Arrakis
+planet Vallabhi
```

### Creating and Destroying Planets

**Create a new planet:**
```
+planet/create <planet name>
```

Example:
```
+planet/create Vallabhi
```

**Destroy a planet:**
```
+planet/destroy <planet name>
```

Example:
```
+planet/destroy OldPlanet
```

### Setting Planet Properties

**Set habitability type:**
```
+planet/set <planet>/habitability=<type>
```

Habitability Types: `Uninhabitable`, `Habitable`, `Asteroid`, `Terran`

Example:
```
+planet/set Vallabhi/habitability=Habitable
```

**Set world type:**
```
+planet/set <planet>/type=<world type>
```

World Types:
- Gas giant
- Rocky world
- Moon planetoid
- Ice Giant
- Toxic Atmosphere
- Furnace
- Volcanic
- Asteroid
- Ice Asteroid
- Mineral Rich Asteroid
- Alpine World
- Mineral World
- Frozen World
- Ocean World
- Arid World
- Forested World
- Tropical World
- Savanna World
- Mined-Out World
- Earth-Like

Example:
```
+planet/set Vallabhi/type=Mineral World
```

**Set star system:**
```
+planet/set <planet>/star=<star system name>
```

Example:
```
+planet/set Vallabhi/star=Beta Tucanae IV
```

**Set political affiliation:**
```
+planet/set <planet>/affiliation=<house name>
```

This automatically adds the house to the planet if not already present.

Example:
```
+planet/set Vallabhi/affiliation=House Nagara
```

**Set population:**
```
+planet/set <planet>/population=<number>
```

Numbers can include commas for readability.

Example:
```
+planet/set Vallabhi/population=3,300,000
+planet/set Arrakis/population=3000000
```

**Set lifestyle:**
```
+planet/set <planet>/lifestyle=<text>
```

Example:
```
+planet/set Vallabhi/lifestyle=Mining communities and trade centers
```

**Set industries:**
```
+planet/set <planet>/industries=<text>
```

Example:
```
+planet/set Vallabhi/industries=Ore-refining of local metals and gems
```

**Set military power:**
```
+planet/set <planet>/military=<text>
```

Example:
```
+planet/set Vallabhi/military=Ground forces, space fleet, basic planetary defenses
```

**Set planet notes:**
```
+planet/set <planet>/notes=<text>
```

This sets the main descriptive notes about the planet.

**Text Formatting:** Planet notes support special character substitutions:
- `%r` = newline/carriage return
- `%t` = tab character

Example:
```
+planet/set Vallabhi/notes=Vallabhi is a mountainous world with deep valleys.%r%rIt has vast lakes rather than seas, and many islands. These islands are dangerous to live on due to unpredictable and violent tides, but fishermen and smugglers from minor Houses make a home here.
```

**Set other notes:**
```
+planet/set <planet>/other=<text>
```

This sets additional tangential information about the planet. Also supports `%r` and `%t` formatting.

Example:
```
+planet/set Vallabhi/other=House Nagara's home city of Kyotashi is set upon one of the broad mountain terraces that make up the Rinumian Ridge.%r%rThe dramatic landscape has also inspired poets, who are drawn to the training halls of House Molay.
```

### Managing Houses on Planets

**List houses on a planet:**
```
+planet/house <planet>/list
```

Example:
```
+planet/house Vallabhi/list
```

**Add a house to a planet:**
```
+planet/house <planet>/add=<house name>
```

Example:
```
+planet/house Vallabhi/add=House Nagara
+planet/house Vallabhi/add=House Molay
+planet/house Vallabhi/add=House Arcuri
```

**Remove a house from a planet:**
```
+planet/house <planet>/remove=<house name>
```

Example:
```
+planet/house Vallabhi/remove=House Molay
```

### Managing Organizations on Planets

**List organizations on a planet:**
```
+planet/org <planet>/list
```

Example:
```
+planet/org Vallabhi/list
```

**Add an organization to a planet:**
```
+planet/org <planet>/add=<organization name>
```

Example:
```
+planet/org Vallabhi/add=Spacing Guild
+planet/org Vallabhi/add=Bene Gesserit School
```

**Remove an organization from a planet:**
```
+planet/org <planet>/remove=<organization name>
```

Example:
```
+planet/org Vallabhi/remove=Spacing Guild
```

## Planet Display

The planet display uses green ANSI coloration and shows all planet information in an organized format:

```
================================================================================

                                VALLABHI                                      

                            BETA TUCANAE IV

================================================================================

Habitability: Habitable     Type: Mineral World    Affiliation: House Nagara

--------------------------------------------------------------------------------

Population:       3,300,000 inhabitants

Industries:       Ore-refining of local metals and gems

Military Power:   Ground forces, space fleet, basic planetary defenses

Houses:           Nagara, Molay, Arcuri

Organizations:    Bene Gesserit School, Spacing Guild

--------------------------------------------------------------------------------

Planet Notes:

Vallabhi is a mountainous world with deep valleys. It has vast lakes rather than
seas, and many islands. These islands are dangerous to live on due to
unpredictable and violent tides, but fishermen and smugglers from minor Houses
make a home here.


Other Notes:

House Nagara's home city of Kyotashi is set upon one of the broad mountain
terraces that make up the Rinumian Ridge, a chain of mountains that are
extensively mined. However the dramatic landscape has also inspired poets, who
are drawn to the training halls of the other minor House Molay.

================================================================================
```

## Complete Example: Creating Vallabhi

Here's a complete example of creating the planet Vallabhi from scratch:

```
+planet/create Vallabhi
+planet/set Vallabhi/habitability=Habitable
+planet/set Vallabhi/type=Mineral World
+planet/set Vallabhi/star=Beta Tucanae IV
+planet/set Vallabhi/population=3300000
+planet/set Vallabhi/industries=Ore-refining of local metals and gems
+planet/set Vallabhi/military=Ground forces, space fleet, basic planetary defenses
+planet/set Vallabhi/affiliation=House Nagara
+planet/house Vallabhi/add=House Molay
+planet/house Vallabhi/add=House Arcuri
+planet/org Vallabhi/add=Bene Gesserit School
+planet/org Vallabhi/add=Spacing Guild
+planet/set Vallabhi/notes=Vallabhi is a mountainous world with deep valleys. It has vast lakes rather than seas, and many islands. These islands are dangerous to live on due to unpredictable and violent tides, but fishermen and smugglers from minor Houses make a home here.
+planet/set Vallabhi/other=House Nagara's home city of Kyotashi is set upon one of the broad mountain terraces that make up the Rinumian Ridge, a chain of mountains that are extensively mined. House Nagara manages the mineral wealth of the planet, with the assistance of the minor House Arcuri. However the dramatic landscape has also inspired poets, who are drawn to the training halls of the other minor House Molay.
```

Then view the completed planet:
```
+planet Vallabhi
```

## Complete Example: Creating Arrakis

Here's another example creating the famous planet Arrakis:

```
+planet/create Arrakis
+planet/set Arrakis/habitability=Habitable
+planet/set Arrakis/type=Arid World
+planet/set Arrakis/star=Canopus
+planet/set Arrakis/population=4000000
+planet/set Arrakis/industries=Spice mining and processing, water reclamation
+planet/set Arrakis/military=Planetary shields, space fleet, desert patrols
+planet/set Arrakis/affiliation=House Atreides
+planet/house Arrakis/add=House Atreides
+planet/org Arrakis/add=Spacing Guild
+planet/org Arrakis/add=Bene Gesserit School
+planet/set Arrakis/notes=Arrakis, also known as Dune, is a harsh desert world where water is the most precious resource. The planet is the only known source of the spice melange, the most valuable substance in the universe. Giant sandworms dominate the deep desert, while the Fremen people have adapted to survive in this extreme environment.
+planet/set Arrakis/other=The spice melange extends life, expands consciousness, and is essential for space navigation. Control of Arrakis means control of the spice, and control of the spice means power in the Imperium. The Fremen possess deep ecological knowledge of the planet and have their own plans for its transformation.
```

## Planet Typeclass

### Attributes

The Planet typeclass (`typeclasses.planets.Planet`) stores the following attributes:

- `habitability_type`: One of Uninhabitable, Habitable, Asteroid, or Terran
- `world_type`: Type of planet (Gas giant, Rocky world, Earth-Like, etc.)
- `star`: Name of the star system
- `political_affiliation`: House object that controls the planet
- `population`: Integer number of inhabitants
- `lifestyle`: General lifestyle description
- `industries`: Industries present or what the planet is known for
- `military_power`: Description of military capabilities
- `houses`: List of House objects present on the planet
- `organizations`: List of Organization objects present on the planet
- `planet_notes`: Main descriptive notes about the planet
- `other_notes`: Additional tangential information

### Methods

The Planet typeclass provides several useful methods:

- `format_population()`: Returns formatted population string with commas
- `get_affiliation_name()`: Returns the name of the affiliated House or "Independent"
- `add_house(house)`: Add a House presence to the planet
- `remove_house(house)`: Remove a House from the planet
- `add_organization(org)`: Add an Organization presence to the planet
- `remove_organization(org)`: Remove an Organization from the planet
- `get_display()`: Returns the formatted planet display (green-themed)

### Locks

Planets use the following locks:
- `view:all()` - Anyone can view planet information
- `edit:perm(Builder)` - Only Builders+ can edit planets
- `delete:perm(Admin)` - Only Admins can delete planets

## Future Integration with Rooms

In the future, rooms can be set to be on specific planets, allowing them to inherit planet-specific features such as:

- Atmospheric conditions
- Gravity effects
- Local time and weather
- Political context
- Available resources

To set a room's planet (when implemented):
```
@set here/planet = Vallabhi
```

## Tips

1. **Create planets before setting affiliations**: Create the planet first, then add houses and set the political affiliation.

2. **Use commas in population**: Population numbers can include commas for readability: `3,300,000`

3. **Political affiliation automatically adds house**: When you set a planet's political affiliation, the house is automatically added to the planet's house list if not already present.

4. **Word wrapping**: Long notes are automatically word-wrapped to 80 characters while preserving paragraph breaks.

5. **Multiple houses**: Planets can have multiple houses present - one as the political affiliation (ruling house) and others as minor presences.

6. **Multiple organizations**: Planets can have multiple organizations present, representing their influence on the world.

7. **List format**: Use `+planet/list` to see all planets at a glance with their key stats.

## Permission Requirements

- **Viewing**: Any player can view planet information
- **Creating/Editing**: Requires Builder permission or higher
- **Destroying**: Requires Admin permission (due to default Planet locks)

