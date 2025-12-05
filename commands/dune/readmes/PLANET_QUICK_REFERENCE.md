# Planet Command Quick Reference

## Viewing
```
+planet <name>                              View planet information
+planet/list                                List all planets
```

## Creation & Destruction (Builder+)
```
+planet/create <name>                       Create new planet
+planet/destroy <name>                      Destroy planet
```

## Basic Properties (Builder+)
```
+planet/set <planet>/habitability=<type>    Set habitability type
+planet/set <planet>/type=<world type>      Set world type
+planet/set <planet>/star=<system>          Set star system
+planet/set <planet>/affiliation=<house>    Set political affiliation
+planet/set <planet>/population=<number>    Set population
+planet/set <planet>/lifestyle=<text>       Set lifestyle
+planet/set <planet>/industries=<text>      Set industries
+planet/set <planet>/military=<text>        Set military power
+planet/set <planet>/notes=<text>           Set planet notes
+planet/set <planet>/other=<text>           Set other notes
```

## Houses on Planets (Builder+)
```
+planet/house <planet>/list                 List houses on planet
+planet/house <planet>/add=<house>          Add house to planet
+planet/house <planet>/remove=<house>       Remove house from planet
```

## Organizations on Planets (Builder+)
```
+planet/org <planet>/list                   List organizations on planet
+planet/org <planet>/add=<org>              Add organization to planet
+planet/org <planet>/remove=<org>           Remove organization from planet
```

## Habitability Types
- Uninhabitable
- Habitable
- Asteroid
- Terran

## World Types
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

## Quick Setup Example
```
+planet/create Arrakis
+planet/set Arrakis/habitability=Habitable
+planet/set Arrakis/type=Arid World
+planet/set Arrakis/star=Canopus
+planet/set Arrakis/population=4000000
+planet/set Arrakis/industries=Spice mining
+planet/set Arrakis/military=Planetary shields, space fleet
+planet/set Arrakis/affiliation=House Atreides
+planet/org Arrakis/add=Spacing Guild
+planet/set Arrakis/notes=A harsh desert world, only source of the spice melange.
+planet Arrakis
```

