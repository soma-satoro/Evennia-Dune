"""
Warfare Assets Data

This module defines all Warfare Assets available in Dune.
Asset data is stored separately from typeclass logic.
"""

# Warfare Assets organized by category
WARFARE_ASSETS = {
    # Shields & Emplacements
    "Strategic/House Shield": {
        "asset_type": "Warfare",
        "keywords": ["Atomic", "Impenetrable", "Strategic"],
        "quality": 0,
        "description": "Strategic or House Holtzman shields, which derive their name from the Holtzman effect, are large shields that project an energy field around strategic sites. Personal shields also exist, but they cannot begin to compare to the strength of these massive defenses that would require energy levels like that of a crashing spaceship, comet, or meteorite to cause the shield to fail. They are used to defend massive fortresses and small cities from all forms of high-speed projectiles, from bombardments down to small arms fire.",
        "special": "As an Asset: A shield is a House-level asset whose control can change the tide of a battle. Widely used throughout the Imperium, on Arrakis they are only used within the Imperial Basin, as sandworms are not found there; if used elsewhere on the planet, sandworms would be attracted to their vibrations and attack."
    },
    
    "Fortress": {
        "asset_type": "Warfare",
        "keywords": ["Defensive", "Heavy Cover", "Strategic"],
        "quality": 0,
        "description": "Because they can be defended by strategic shields, fortified locations like castles and fortresses—places that rely on defensive architecture designed to impede melee armed ground troops—have become the standard form of defense of strategic locations throughout the Imperium and even on Arrakis. On Arrakis, only the Imperial Basin combines fortresses with shields, but the various Fremen sietches throughout the planet are also fortified against both conventional and nonconventional attacks.",
        "special": "As an Asset: Another strategic asset, fortresses and their control play a major role in who controls a planet, and who can lay claim to ownership of a territory in front of the Landsraad and the Emperor. They are designed to impede and kill attackers while still allowing access for regular business during peaceful times."
    },
    
    "Bunker": {
        "asset_type": "Warfare",
        "keywords": ["Defensive", "Heavy Cover", "Tactical"],
        "quality": 0,
        "description": "Bunkers, pillboxes, entrenched positions, or any sort of fortified location, shielded or not, are smaller defensive structures intended to slow or stop attackers. They are smaller than fortresses and can be created quickly with an entrenching tool. At times, more complex permanent bunkers are built in a place too small to secure with a full-sized fortress—for example, at a bridge with limited banks on either side suitable for construction. Bunkers are also used to defend temporary systems like undermining operations designed to penetrate shielded fortresses from below the ground.",
        "special": "As an Asset: A bunker is a tactical asset used to secure and give a bonus to defensive units and characters. It defends a smaller but critical location, like the only bridge that crosses a river for miles, or temporary defenses built to hold difficult ground recently won in a battle."
    },
    
    # Soldiers
    "Conscript": {
        "asset_type": "Warfare",
        "keywords": ["Expendable", "Poor Training", "Unshielded"],  # Default keywords, can choose 3
        "quality": 0,
        "description": "Conscripts are the lowest of the low. Soldiers assembled with little to no training and bad or non-existent equipment. They almost never have shields and are armed with a combination of ranged weapons and shoddy melee weapons. These soldiers could be used to represent rebelling peasants, escaped slaves, or conscripted prisoners meant to tie up enemy forces while other soldiers maneuver into flanking positions.",
        "special": "As an Asset: Used to distract, hinder, or slow down an enemy force, or to attack unprepared enemy locations only defended by noncombatants. Keywords (choose three): Expendable, Poor Training, Ranged Weapons, or Unshielded. Quality: 0 (larger units may have higher Quality)."
    },
    
    "Shield Infantry": {
        "asset_type": "Warfare",
        "keywords": ["Formation", "Melee Weapons", "Shielded"],
        "quality": 1,
        "description": "These are the standard line infantry used throughout the Imperium: shielded soldiers armed with melee weapons and trained to fight efficiently in large formations of a thousand men or more. They learn how to defend quickly and attack slowly, move in formation together, and pin and flank other formations.",
        "special": "As an Asset: This asset represents a trained unit from a small squad up to a large brigade of soldiers. Quality: 1 (larger units may have higher Quality)."
    },
    
    # Transports
    "Personnel Carrier": {
        "asset_type": "Warfare",
        "keywords": ["All-terrain", "Shielded", "Troop Transport"],
        "quality": 0,
        "description": "These massive shielded vehicles are designed to ferry troops across planetary surfaces and are as varied and unique as the planets they are designed to traverse. Most are wheel-based, although walkers, treaded, and even anti-gravity variants are not uncommon. These also range in size from squad-based carriers to massive shielded land ships that carry companies or even a full regiment of soldiers.",
        "special": "As an Asset: A fleet of these vehicles is usually maintained by a House so that they can transport troops quickly to various strategic places within their territory. Smaller vehicles are more common. Quality: Larger carriers carry more troops."
    },
    
    "Anti-Grav Platform": {
        "asset_type": "Warfare",
        "keywords": ["Anti-gravity", "Flatbed", "Shielded"],
        "quality": 0,
        "description": "Not originally a weapon of war, anti-gravity platforms, or just grav platforms, were adopted centuries ago into modern Imperial warfare. Most are shielded like personnel carriers, but their grav systems allow them to be used as ways to overcome fortress walls, deliver troops in tight spaces, work as elevators along unprepared cliff faces, or ferry people and equipment across rivers or other impassable terrain. These vary in size, but most are designed to comfortably carry an entire squad of soldiers, their equipment, and a pilot/operator. As they incorporate a Holtzman effect to function, they are rare on Arrakis, although Glossu Rabban Harkonnen used one as bait when he hunted a sandworm.",
        "special": "As an Asset: These can be used as short-range transportation for troops or other supplies, and often are little more than a platform built with a shield, anti-gravity generators, and a control console."
    },
    
    "Naval Transport": {
        "asset_type": "Warfare",
        "keywords": ["Naval", "Shielded"],
        "quality": 0,
        "description": "Naval transports carry troops and supplies across large bodies of water or up rivers at times when traveling by air or orbital transports would be strategically unsound. These ships have changed little from the eras before humanity took the stars. The major difference is the inclusion of a shield to discourage attacks. They can range from small patrol boats to massive cargo transports designed to carry tens of thousands of troops.",
        "special": "As an Asset: These can be used as waterborne transportation for troops or other supplies when air or orbital travel is unwise or prohibited."
    },
    
    "Ornithopter - Scout": {
        "asset_type": "Warfare",
        "keywords": ["Fast", "Flying", "Glide", "Quiet", "Size: Small"],
        "quality": 0,
        "description": "These advanced flying machines use huge wings to fly like dragonflies. This allows them to take off and land vertically and glide to preserve fuel. They are quiet in flight and far less polluting than a traditional jet engine. It also makes them incredibly agile. Scout variants are small one- or two-person craft designed for reconnaissance.",
        "special": "As an Asset: Ornithopters can be used to gather intelligence in warfare as well as move troops and attack both air and ground targets. As espionage devices they allow quiet observation of a target as well as providing a fast and subtle way to escape an area."
    },
    
    "Ornithopter - Troop Transport": {
        "asset_type": "Warfare",
        "keywords": ["Fast", "Flying", "Glide", "Quiet", "Size: Squad"],
        "quality": 0,
        "description": "These advanced flying machines use huge wings to fly like dragonflies. This allows them to take off and land vertically and glide to preserve fuel. They are quiet in flight and far less polluting than a traditional jet engine. It also makes them incredibly agile. Troop transport variants can carry an entire squad of soldiers.",
        "special": "As an Asset: Ornithopters can be used to gather intelligence in warfare as well as move troops and attack both air and ground targets."
    },
    
    "Ornithopter - Supply Carrier": {
        "asset_type": "Warfare",
        "keywords": ["Fast", "Flying", "Glide", "Jet-assisted", "Size: Company"],
        "quality": 0,
        "description": "These advanced flying machines use huge wings to fly like dragonflies. This allows them to take off and land vertically and glide to preserve fuel. They are quiet in flight and far less polluting than a traditional jet engine. Supply carrier variants are larger craft designed to carry troops and supplies for company-sized units, and may use jet engines to assist with speed and lift.",
        "special": "As an Asset: Ornithopters can be used to gather intelligence in warfare as well as move troops and attack both air and ground targets."
    },
    
    "Ornithopter - Attack/Arrakis": {
        "asset_type": "Warfare",
        "keywords": ["Fast", "Flying", "Glide", "Guns", "Missiles", "Quiet", "Rockets", "Size: Small"],
        "quality": 0,
        "description": "These advanced flying machines use huge wings to fly like dragonflies. This allows them to take off and land vertically and glide to preserve fuel. They are quiet in flight and far less polluting than a traditional jet engine. Attack variants are armed with guns, rockets, and missiles to work as close air support and air superiority. On Arrakis, they fill an expanded role beyond just recon and transport, weather permitting.",
        "special": "As an Asset: Ornithopters can be used to gather intelligence in warfare as well as move troops and attack both air and ground targets. On Arrakis, attack ornithopters can be armed with guns, rockets, and missiles to work as close air support and air superiority."
    },
    
    "Carryall": {
        "asset_type": "Warfare",
        "keywords": ["Cargo Space", "Flying", "Shielded", "Size: Large to Gargantuan"],
        "quality": 0,
        "description": "Most often seen as air transport for spice harvesters on Arrakis, carryalls are the air transportation workhorse of the Imperium military and civilian sectors. These massive craft, essentially large-scale ornithopters, use a variety of flight systems—from modified ornithopter wings, to jet, rocket, and anti-gravity systems—to quickly travel across the skies of the planets of the Imperium. Designs of carryalls vary based on their intended cargo. Personnel carryalls appear much like massed civilian air transports. Internal cargo carryalls have similar but bulkier builds compared to personnel carryalls, while external cargo carryalls, like the ones used on Arrakis to pick up and transport spice harvesters, appear to be not much more than a large frame with flight systems attached and various cargo clamps for holding the specialty cargo during transport. Cargo carryalls as used in spice mining usually have room for only four crew: two pilots and two journeymen attachers.",
        "special": "As an Asset: Depending on the design of a carryall, they excel at transporting cargo or personnel across planets at suborbital altitudes. These workhorses are employed by spice smugglers on Arrakis to quickly come and go from illicit spice harvesting operations in the deep deserts."
    },
    
    # Artillery & Anti-Aircraft
    "Artillery": {
        "asset_type": "Warfare",
        "keywords": ["Crew-served", "Long-ranged", "Shell Varieties"],
        "quality": 0,
        "description": "Artillery guns are massive cannons, often mounted on a vehicle platform, that fire explosive shells over kilometers to soften up unshielded infantry and fortified positions. Nearly obsolete, artillery is only employed in the rare instances when a military force is fighting against unshielded rebels or on Arrakis, where the inability to use shields on most of the planet makes their use a viable military strategy.",
        "special": "As an Asset: These guns need to be crewed by a group of soldiers trained in their use, but if this is done they are very effective and can deploy a variety of warheads from air-burst and explosive rounds designed to eviscerate unshielded soldiers, to armor-piercing, bunker buster, and even gas and toxin shells that can spread deadly pathogens or poisonous gases across the battlefield."
    },
    
    "RPG": {
        "asset_type": "Warfare",
        "keywords": ["Armor-piercing", "Explosive", "Portable", "Single-use", "Unguided"],
        "quality": 0,
        "description": "Rocket-propelled grenades are one-man disposable rocket weapons. Much like artillery, rocket and missile launchers have nearly gone extinct with the widespread adoption of shields. However, they continue to be of use on Arrakis and against unshielded targets on other planets.",
        "special": "As an Asset: These have been used to great success by various factions on Arrakis over the centuries. Fremen employ rocket-propelled grenades during raids targeting spice harvesters and other vulnerable targets."
    },
    
    "MPAD": {
        "asset_type": "Warfare",
        "keywords": ["Anti-aircraft", "Armor-piercing", "Explosive", "Guided", "Portable", "Single-use"],
        "quality": 0,
        "description": "Man-Portable Air Defense systems are guided missile systems designed for anti-aircraft roles. They are portable and single-use, allowing individual soldiers to engage enemy aircraft.",
        "special": "As an Asset: These guided missile systems are deployed in anti-aircraft roles and have been effectively used on Arrakis and against unshielded targets."
    },
    
    "Mortar": {
        "asset_type": "Warfare",
        "keywords": ["Anti-personnel", "Arcing Fire", "Armor-piercing", "Explosive", "Two-person Crew"],
        "quality": 0,
        "description": "Mortars are portable artillery weapons that fire explosive shells in an arcing trajectory. They require a two-person crew and are effective against infantry and light fortifications.",
        "special": "As an Asset: Mortars provide indirect fire support and are useful for engaging targets behind cover or at various ranges."
    },
    
    "Rocket Launcher": {
        "asset_type": "Warfare",
        "keywords": ["Arcing", "Armor-piercing", "Explosive", "Ground Vehicle", "Mass Fire", "Unguided"],
        "quality": 0,
        "description": "Large vehicle-mounted rocket launcher systems designed to launch masses of 'dumb' rockets at a variety of unshielded targets. These systems provide saturation fire against enemy positions.",
        "special": "As an Asset: The Harkonnen effectively used rocket and missile launchers against the Atreides when they seized power on Arrakis. These systems provide devastating mass fire against unshielded targets."
    },
    
    "Missile Launcher": {
        "asset_type": "Warfare",
        "keywords": ["Anti-aircraft", "Armor-piercing", "Explosive", "Ground Vehicle", "Guided", "Mass Fire"],
        "quality": 0,
        "description": "Large vehicle-mounted missile launcher systems designed to launch guided missiles. These systems can be used for anti-aircraft defense or ground attack against unshielded targets.",
        "special": "As an Asset: Guided missile systems are deployed in anti-aircraft roles and against ground targets. The Harkonnen effectively used these systems against the Atreides when they seized power on Arrakis."
    },
    
    # Other Vehicles
    "Spice Harvester": {
        "asset_type": "Warfare",
        "keywords": ["Designed for Carryall Transport", "Factory", "Integral Scout Vehicles", "Massive", "Spice-infused", "Wormcall"],
        "quality": 0,
        "description": "The literal factory that supplies the source of Imperial power, spice harvesters are massive mobile mining and refining factories. They are crewed by daring wildcat crews who work furiously to harvest as much spice as possible from spice blows before a sandworm appears. Sandworms always appear as they are drawn to the vibrations of the harvesters. Designs vary, but they are often described as massive beetle-like ground vehicles that are flown into place by a carryall. During a short period of time they send out scout vehicles to search for the incoming worm while drills and scoops extend to draw the spice into the harvester to begin the refining process.",
        "special": "As an Asset: The rulers of Arrakis are nominally the only ones who control spice harvesters, but smugglers and the Fremen employ their own. The Fremen, Imperial-backed rulers, and the smugglers wage an ongoing shadow war, striking at their opponents' spice harvesters whenever they see an opportunity. Thus, they are not infrequently found in the middle of a pitched battle."
    },
    
    "Orbital Transport": {
        "asset_type": "Warfare",
        "keywords": ["Cargo", "Guild/House Design", "Shielded", "Spacecraft", "Staterooms"],
        "quality": 0,
        "description": "To reach Spacing Guild Heighliners, the Spacing Guild has countless large craft that travel to and from orbital space. Each Guild craft can carry thousands of individuals and millions of tons of goods for planetary markets and exchanges. Some Landsraad Houses own their own orbital transports and prefer to stay aboard their own transports for security and comfort reasons, and these craft vary in size from single- or two-person affairs up to the size of Guild craft. Incidents in space are almost unheard of because of the prohibitions placed on space warfare by the Spacing Guild; although rare events do happen, they are generally limited. More frequently, transports may find themselves engulfed in a mobile battle when landed near a strategic location, or when unloading troops transported to a planet.",
        "special": "As an Asset: As with the spice-harvester, these transports are more strategic targets than tools or weapons in their own right. However, cunning characters like Baron Harkonnen have discovered ways to employ them as weapons."
    },
    
    "Heighliner": {
        "asset_type": "Warfare",
        "keywords": ["Carrier", "FTL Travel", "Immense", "Navigator Pilot Required", "Spacecraft"],
        "quality": 0,
        "description": "The Imperium exists because of spice and the Holtzman engine. The engine makes instantaneous jumps from one location in space to another by folding the space in between. The spice allows Spacing Guild Navigators and Steersmen to navigate this jump through space while controlling moon-like spacecraft called Heighliners. These immense craft often reach 20 kilometers in length and can house hundreds of orbital transports of all sizes at any one time. Each day multiple Heighliners travel routes to every planet of the Empire to keep trade flowing throughout. With one of these ships one could easily find themselves halfway across the Empire in a day.",
        "special": "As an Asset: To wrest control of a Heighliner from the Spacing Guild would be to commit one of the highest crimes against the Empire, and one would need to control the specialized and mutated Navigator to even transport the ship anywhere else. But stranger things have happened."
    }
}

