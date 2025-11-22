"""
Personal Assets Data

This module defines all Personal Assets available in Dune.
These can be used to create Asset objects with the correct properties.
"""

# Personal Assets organized by category
PERSONAL_ASSETS = {
    # Ranged Weapons
    "Lasgun": {
        "asset_type": "Personal",
        "keywords": ["Laser", "Ranged Weapon"],
        "quality": 0,
        "description": "The most commonly used firearm in the Imperium. These continuous wave-laser projectors are fitted into either pistols or rifles, enhancing their range. The beam forms a tight, narrow laser that can be widened, reducing the strength while increasing the area impacted. Lasguns use an energy cell capable of firing 30 shots before needing to be replaced. The number of shots is based on the narrow beam setting, and wider beams require additional energy. The universe is filled with lasguns, befitting the planet, culture, and group using them, making countless variants available for purchase. They are expensive and sometimes unreliable, and the reaction with shields makes them often undesirable in mass combat, when a stray shot could have catastrophic results.",
        "special": "As an Asset: Lasguns are the conventional method of combat and can be used to destroy obstacles."
    },
    
    "Maula Pistol": {
        "asset_type": "Personal",
        "keywords": ["Concealable", "Ranged Weapon", "Quiet"],
        "quality": 0,
        "description": "The maula pistol is an assassin's weapon. These pistols have a spring-loaded trigger and can launch poison darts or other projectiles with considerable accuracy up to 40 meters. They originate from change to beginning of the Faufreluches' period and are closely related to stunners. The needle gun is a variant of the maula pistol.",
        "special": "As an Asset: The silent nature of the maula pistol makes it an excellent choice for assassinations."
    },
    
    # Melee Weapons
    "Blade": {
        "asset_type": "Personal",
        "keywords": ["Melee Weapon"],
        "quality": 0,
        "description": "Blades are as ancient as Old Terra and are just as critical for defense now as then. The creation of the personal shield has elevated them into common use. Blades come in a variety of shapes, sizes, and forms. Types of blades include daggers, swords, and rapiers, but many other specialized or culturally specific blades exist. Since ancient times, numerous new versions of traditional blades have arisen, sometimes crafted from new material, sometimes combined with new technology. Most modern blades are crafted with plasteel or damasteel.",
        "special": "As an Asset: If used correctly, can penetrate a shield, and thus are a common part of a hand-to-hand combat attack. Some blades are presented as parts of ceremonies, used to signify rank and status. Historically they are known to be given as a diplomatic gift between warring factions. (Different sizes and forms of blade may have additional keywords.)"
    },
    
    "Bodkin": {
        "asset_type": "Personal",
        "keywords": ["Concealable", "Melee Weapon", "Quiet"],
        "quality": 0,
        "description": "These tiny, well-crafted blades are used for personal defense and are commonly used by assassins. While not useful for cutting, they are exceptional for stabbing attacks. Several noted cutpurses use them as an aid in their crimes.",
        "special": "As an Asset: The bodkin is easily concealed in a wrist sheath and easily disposed of before capture."
    },
    
    "Crysknife": {
        "asset_type": "Personal",
        "keywords": ["Melee Weapon", "Sacred"],
        "quality": 1,  # Even the least crysknives has a Quality 1
        "description": "This sacred blade of the Fremen is crafted from the tooth of a dead sandworm. An average crysknife possesses a 0.2-meter curved milky-white double blade with a finger-ridged handle. Sometimes the tip of the blade is coated with a deadly, fast-acting poison. Part of the Fremen tradition surrounding the blade states that one can never be re-sheathed without first drawing blood. Additionally, outsiders are not allowed to view these blades, and if they do, the blade is cleansed through a long ritual or the outsider being put to death. Crysknives come primarily in two types: unfixed and fixed. Unfixed blades must stay close to a person's electrical field, or they will disintegrate. Fixed blades are treated with a unique process that allows them to be stored.",
        "special": "As an Asset: A crysknife is a status symbol for an outsider among Fremen to show that one is a friend. They are an effective weapon against shielded opponents. Quality: Even the least crysknives has a Quality 1, and the poison used may increase the Quality further."
    },
    
    "Kindjal": {
        "asset_type": "Personal",
        "keywords": ["Long Blade", "Melee Weapon", "Traditional"],
        "quality": 0,
        "description": "These large curve-bladed knives range from 18–22 cm long. Their use is common among all noble houses who have been taught in their use since the earliest days of the Faufreluches. The ability of these blades to safely bypass shields has increased their popularity to the point that they are commonplace.",
        "special": "As an Asset: The kindjal can cut through personal shields and can be used in artistic displays of sword use. Many noble Houses engrave the hilts with their House emblem."
    },
    
    "Pulse-Sword": {
        "asset_type": "Personal",
        "keywords": ["Disruptive", "Melee Weapon", "Vibro-blade"],
        "quality": 0,
        "description": "The pulse-sword is a melding of two different worlds: the medieval and the technologically advanced. These blades use vibrations to amplify the attacking power of the sword wielder, but as a result are rarely used on Arrakis due to the possibility of attracting sandworms.",
        "special": "As an Asset: The vibration effect of the blade disrupts thinking machine gelcircuitry."
    },
    
    # Armor and Dress
    "Jubba Cloak": {
        "asset_type": "Personal",
        "keywords": ["Adaptable", "Fashion", "Survival"],
        "quality": 0,
        "description": "These durable and versatile cloaks are a boon to survivalists. The jubba cloak is a flowing cloak with various styles and functions. The cloaks are easily converted into a hammock or make-shift tent and regulate temperatures by absorbing or radiating heat.",
        "special": "As an Asset: The compact cloak appears like any other cloak and goes unnoticed until used. While mainly a survival tool, the cloaks are sometimes woven with intricate designs and worn as a status symbol."
    },
    
    "Shield": {
        "asset_type": "Personal",
        "keywords": ["Atomic", "Impervious", "Static Defense"],
        "quality": 0,
        "description": "The Holtzman shield is named for the creator of the Holtzman effect, used to create a protective field of energy around a larger area such as a castle, or in some cases a planet. Shields are a common defense for facilities and make the use of lasguns deadly for all sides engaging in the battle, due to the unpredictable interaction of the resultant explosion. A shield can provide protection for more substantial areas, making them much harder to penetrate.",
        "special": "As an Asset: Shields are affordable for those of means, and always a factor when determining strategies against House operatives and soldiers. Their use on Arrakis is limited, as the vibration attracts the worms in a violent rage. Special: No high-velocity attack can bypass a shield, and it requires colossal amounts of firepower to overwhelm one. Lasguns are as risky to use against emplaced shields as against personal ones."
    },
    
    "Personal Shield": {
        "asset_type": "Personal",
        "keywords": ["Atomic", "Defense", "Protection"],
        "quality": 0,
        "description": "The Holtzman shield was named for the creator of the Holtzman Effect, and, unfortunately, not for his assistant, Norma Cenva, who actually discovered its use before Holtzman took over the project. This effect is used to create a protective field of energy around a person. The shields quickly became commonly used for personal defense. While shields provide incredible protection, they allow slow-moving objects to pass through them, otherwise, the users would suffocate without atmospheric gasses such as oxygen. The evolution of the shields has allowed them to protect one side or one half of the body. To date, no one has been able to have the shields protect only a single limb or appendage. Shields are affordable for most Houses and are commonplace with nobles and their retainers, with even some merchants able to have one. Holtzman shields are the primary reason for the move to more medieval forms of combat involving melee weapons. Their use on Arrakis is limited, as the vibration attracts the sandworms and puts them in a violent rage.",
        "special": "As an Asset: Shields are used for defense and can be used to threaten someone with a lasgun if activated. Special: Ranged attacks cannot harm a character protected by a personal shield. If a shield is struck by a lasgun, either the shield or the lasgun (randomly determined) will produce an atomic explosion; using such methods of destruction upon a human population is strictly forbidden."
    },
    
    "Semi Shield": {
        "asset_type": "Personal",
        "keywords": ["Atomic", "Defense", "Protection"],
        "quality": 0,
        "description": "A variant of the personal shield, the semi-shield is a shield built to protect only a part of the body, usually the upper torso or half of the upper torso and one leg. Also called a half-shield. These are often used in gladiatorial games or with light sparring, where an additional level of skill is utilized to strike areas not covered by the semi-shield.",
        "special": "As an Asset: As with regular shields, semi-shields are used for defense and can be used to threaten someone with a lasgun if activated. Special: It is more difficult to harm a character armed with a semi-shield with ranged combat, and special care must be taken to strike the portion not protected by the shield. In each case, the Difficulty is increased by +1 step. If a shield is struck by a lasgun, either the shield or the lasgun (randomly determined) will produce an atomic explosion; using such methods of destruction upon a human population is strictly forbidden. As a semi-shield doesn't protect the whole body unlike most defensive assets it can be moved into any personal zone of the user as they shift position to make the best use of its protection."
    },
    
    "Stillsuit": {
        "asset_type": "Personal",
        "keywords": ["Arrakis", "Fremen", "Survival"],
        "quality": 0,
        "description": "These full-body suits are essential for survival on Arrakis outside the cities. Their primary function is to preserve the body's moisture by absorbing sweat, urine, and other body fluids. The stillsuit processes these fluids by filtering impurities, recycling captured fluids into drinkable water collected in catchpockets, which is drunk through a tube. The key components of the stillsuit are filt-plug (collects moisture from exhaled air), faceflap (face mask that protects the wearer from fine dust), catchtube (connects the catchpockets), and stillsuit cap or hood.",
        "special": "As an Asset: An operable stillsuit allows the wearer to function for weeks in the desert by collecting water as it is lost by the body. Each stillsuit is finely-crafted, with multiple plated layers. The average stillsuit wearer loses 2.7 ml of water per day. Better Quality suits can reduce this."
    },
    
    # Communication and Information
    "Communinet": {
        "asset_type": "Personal",
        "keywords": ["Communication", "Information", "Universal"],
        "quality": 0,
        "description": "The planetary universal system that connects communications.",
        "special": "As an Asset: Communinet is essential in relaying information on a universal scale. The communication system can be hacked and used as a weapon against other Houses."
    },
    
    "Ixian Damper": {
        "asset_type": "Personal",
        "keywords": ["Countermeasure", "Privacy", "Technology"],
        "quality": 0,
        "description": "The secrecy of the Ixians led to the creation of these devices to nullify eavesdroppers. These small tools usually cover a dome of roughly a 10-meter area. Larger Ixian dampers increase the dome's sphere of influence and counteract countermeasures.",
        "special": "As an Asset: The damper ensures the privacy of conversations (as a defensive asset against listening agents of devices). It can also be employed offensively if used while an opponent is attempting to communicate with distant allies."
    },
    
    "Emergency Transmitter": {
        "asset_type": "Personal",
        "keywords": ["Communication", "Concealable", "Tiny"],
        "quality": 0,
        "description": "Emergency transmitters are small, coin-sized devices possessing limited range to alert others that the user needs help. The devices are frequently worn by nobles and high-ranking officials when they are in the field. More paranoid wearers always keep them on hand, with a security contingent ready to respond. The signal is sent back to a relay station or communicator possessed by the reinforcements. The larger the relay station, the more range the signal has.",
        "special": "As an Asset: The emergency transmitter is a useful tool for alerting others or calling in reinforcements. Smaller groups frequently carry multiple transmitters and receivers to minimize lack of communication. Special: Use of an emergency transmitter is often a good justification for creating assets that represent extra troops."
    },
    
    "Filmbook": {
        "asset_type": "Personal",
        "keywords": ["Mnemonic", "Shigawire", "Training"],
        "quality": 0,
        "description": "The filmbook is an imprint of shigawire that uses mnemonic pulses to train students. The exact subject varies per book, though shigawire is only found on Salusa Secundus and III Delta Kaising.",
        "special": "As an Asset: Noble Houses and other elite people use them for training their younger House and Guild members."
    },
    
    "Memocorder": {
        "asset_type": "Personal",
        "keywords": ["Infiltration", "Secrecy", "Technology"],
        "quality": 0,
        "description": "The technological masters of Ix built these tiny handheld black squares to store written messages. The originator writes a message on the square with a needle, one word on top of the next until the message is compete as the box absorbs each word. The message is read by nerve receptors, with the recipient seeing the message flash before their eyes.",
        "special": "As an Asset: The devices can only be cracked by extremely advanced technology."
    },
    
    "Ridulian Crystal": {
        "asset_type": "Personal",
        "keywords": ["Crystal", "Knowledge", "Skills"],
        "quality": "Special",  # Quality depends on contents
        "description": "Ridulian crystals redefined books, as each sheet of a page made of this crystal is only a few molecules thick. Due to the compressed state of the book, they can only be used with an automatic page-turner in the spine of the book. A single volume of a book with an excess of thousands of pages would be a little over 1 cm thick.",
        "special": "As an Asset: A useful tool to convey large amounts of information without requiring much space to accommodate it. Also, for easy transport and disposal of the data if needed. Quality: Special (the Quality depends on the contents of the book and the usefulness of the information it contains)."
    },
    
    # Tools and Equipment
    "Baradye Pistol": {
        "asset_type": "Personal",
        "keywords": ["Arrakis", "Fremen", "Signaling"],
        "quality": 0,
        "description": "Baradye pistols are produced on Arrakis by the Fremen to communicate. The pistol fires a static charge capable of turning a large, 20-meter-diameter area orange (or another color if programmed). The charge retains the coloration for several hours before disappearing. The zone has many uses, from signaling traders or spice raiders to capturing sandworms.",
        "special": "As an Asset: The baradye pistol is a covert weapon useful in relaying messages and distracting others."
    },
    
    "Cibus Hood": {
        "asset_type": "Personal",
        "keywords": ["Disguise", "Infiltration", "Technology"],
        "quality": 0,
        "description": "A malleable, flexible black mask created by the Ixians. When placed over a wearer's face, it completely conceals all their features. The device does not emit any energy readings. When using the hood, the wearer appears as a regular person in passing and looks different when viewed a second or third time.",
        "special": "As an Asset: A cibus hood enables its user to easily escape notice and blend into crowds."
    },
    
    "Dew Collector": {
        "asset_type": "Personal",
        "keywords": ["Arrakis", "Survival", "Water"],
        "quality": 0,
        "description": "These devices are commonly found on Arrakis. The dew collector is a small egg-shaped tool that collects the morning dew for later use.",
        "special": "As an Asset: Dew collectors are one of the ways to maintain life on the planet."
    },
    
    "Fremkit": {
        "asset_type": "Personal",
        "keywords": ["Desert", "Fremen", "Survival"],
        "quality": 0,
        "description": "A desert survival kit created by the Fremen. The kit has all the tools need to survive for roughly a month on Arrakis. It commonly includes a manual, paracompass, stilltent, maker hooks, emergency stillsuit patches, and thumper.",
        "special": "As an Asset: The kit's primary purpose is to allow someone to survive in the desert for a short period. The emergency stillsuit patches can be used to temporarily repair tears in a stillsuit for roughly a day."
    },
    
    "Glowglobe": {
        "asset_type": "Personal",
        "keywords": ["Hovering", "Light"],
        "quality": 0,
        "description": "These small devices use the Holtzman effect to hover near the user, providing illumination. The color of the light differs based on when it was constructed, and it is powered by an organic battery. They are easily switched on or off with a touch.",
        "special": "As an Asset: Glowglobes are used to illuminate areas of darkness, as distractions, and possibly as a concealable explosive delivery system."
    },
    
    "Krimskel Fiber Rope": {
        "asset_type": "Personal",
        "keywords": ["Capture", "Prisoners", "Utility"],
        "quality": 0,
        "description": "Ecaz hufuf vine is woven together from strands to form Krimskel fiber. When pulled, the fiber will 'claw' itself together into a tighter and stronger composite. Attempting to escape being bound with the fiber instead reinforces the bonds.",
        "special": "As an Asset: A Krimskel fiber rope can be used to bind prisoners or even as a device to secure doors when tried to pull open."
    },
    
    "Maker Hooks": {
        "asset_type": "Personal",
        "keywords": ["Fremen", "Sandworm", "Transportation"],
        "quality": 0,
        "description": "These narrow metallic shafts are used to open a gap within a sandworm's ring segments, exposing the less armored hide beneath to the elements. Once pried open, the sandworm rolls onto its side to avoid sand getting in between the exposed flesh between the ring segments. This allows the user to get on top of the sandworm and guide the beast to wherever the rider wishes.",
        "special": "As an Asset: Maker hooks can be used to guide sandworms into enemy locations or travel great distances across Arrakis."
    },
    
    "Palm Lock": {
        "asset_type": "Personal",
        "keywords": ["Encoded", "Security", "Tool"],
        "quality": 0,
        "description": "These small-to-medium-sized locks are usable on objects up to the size of a warehouse door. Each lock is keyed to a specific person's palm or a genetic type (such as a Bene Gesserit). Anyone else must pick the lock to open it. Higher Quality locks are more challenging to pick.",
        "special": "As an Asset: A palm lock is a versatile tool to secure locks and can aid in escapes by locking a door while escaping."
    },
    
    "Paracompass": {
        "asset_type": "Personal",
        "keywords": ["Navigation", "Survival"],
        "quality": 0,
        "description": "The paracompass uses magnetic anomalies in a planet's magnetic field to determine directions by measuring instabilities. The device is a small handheld circular object that fits firmly in the palm.",
        "special": "As an Asset: Paracompasses are essential to locate directions and determine which way to travel in the wilds."
    },
    
    "Poison Snooper": {
        "asset_type": "Personal",
        "keywords": ["Detection", "Security", "Technology"],
        "quality": 0,
        "description": "Poison has long been the preferred assassination method of nobles since Old Terra. It is hard to detect, difficult to identify who one's actual enemy is, and tougher still to prove who used it. Poisons typically come in two forms: food (chaumas) and drink (chaumurky). Countless deaths from poisoning led to the invention of poison snoopers that replaced food tasters. These mechanical devices scan edible substances before they are ingested. Both Ix and Richese are the primary manufacturers of poisons snoopers; however, the continued Ixian propaganda has most of the public believing their models are more sensitive. Poison snoopers come in two forms. The first is a portable version that is a handheld box with an extendable hose that is placed over the substance. An alarm sounds if the snooper detects poison. More advanced models have the option to vibrate rather than emit an audible noise, facilitating concealed use. A larger form of poison snooper is installed on rooftops, usually above eating rooms, and is always active. Fixed alarms continuously emit an ear-piercing sound elevating in frequency every minute.",
        "special": "As an Asset: Poison snoopers are excellent for defense and for use in safeguarding endangered people. Quality: To make matter easier the gamemaster may rule that a poison snooper automatically detects any poison asset in play of the same or lower Quality."
    },
    
    "Ixian Probe": {
        "asset_type": "Personal",
        "keywords": ["Ixian", "Knowledge", "Secret Information", "Technology"],
        "quality": 0,
        "description": "A device wrought by the folk of Ix, the Ixian probe allows the user to scan and replicate the electrochemical signals in a human brain—living or dead—making a copy of personality traits, sense experience, and memory for later reference. The probe itself is a moderately-sized device, and requires sensors be attached to the intended subject, and an operator working while the process is ongoing. The stored information is compiled into a simulacrum, a digital 'duplicate' of the original subject, which responds to stimulus in the same fashion, answering queries or providing answers. These simulacrums are often disoriented, and if created without permission, can be angry and uncooperative. It is rumored that this technology allows Tleilaxu to create gholas, copies of living persons whose minds have been copied with Ixian probes. Note that the simulacrum is not a thinking machine in and of itself but is in fact merely a means of recovering information and responses. Simulacrums are necessarily limited in their ability to have original thoughts and to learn, unable to form neural pathways that duplicate human learning and actual cognitive development. Many within the Imperium feel that the distinction is irrelevant, and that the device skirts the limits of what is allowed under the Butlerian Edicts. Due to its immense potential for espionage, the Ixian probe is considered a loathsome innovation to most civilized people and is not generally used, even by the most amoral of spymasters. The most reliable means of circumventing duplication by an Ixian probe is consuming a drug called shere, which disrupts the probe's ability to collect information, rendering the data useless. Upon death, shere also causes rapid deterioration of the nervous system of the one who took it, rending all further attempts impossible. Shere has no other practical applications and due to its side effects, is not commonly used as a precaution, despite its efficacy. A later innovation, the T-Probe, is able to copy the memories of a person even if they have consumed shere, but causes incredible, frequently lethal amounts of pain to its subject.",
        "special": "As an Asset: An Ixian probe can copy a living or recently-deceased human being and allow access to a digital simulacrum of them, as if speaking to them in person."
    },
    
    "Sapho": {
        "asset_type": "Personal",
        "keywords": ["Addictive", "Mentat", "Stimulant"],
        "quality": 0,
        "description": "A juice created from the roots of plants on the planet Ecaz. The juice is refined into a high-energy drink that amplifies mental powers.",
        "special": "As an Asset: Sapho is addictive if used repeatedly and leaves tell-tale signs by staining one's mouth and lips a ruby color. It is favored by Mentats."
    },
    
    "Stilltent": {
        "asset_type": "Personal",
        "keywords": ["Fremen", "Sealed", "Survival"],
        "quality": 0,
        "description": "This airtight tent works similar to the stillsuit by capturing the humidity inside of it and gathering it for use by the tenant. These are frequently used under a layer or two of sand. The tents use sandsnorks (installed air tubes) to provide air to the interior of the tent.",
        "special": "As an Asset: Stilltents are essential for traveling on the surface of Arrakis and are commonly used by Fremen."
    },
    
    "Personal Suspensor": {
        "asset_type": "Personal",
        "keywords": ["Anti-gravity", "Holtzman", "Mobility"],
        "quality": 0,
        "description": "Personal suspensors are frequently placed into belts, chairs, and other portable objects. These devices operate on the secondary (low drain) phase of the Holtzman field generator and nullify local gravity. The height and mass of the energy consumed is based on the weight of the object lifted. Personal suspensors do not have the power to allow flight or stop falls from very high distances before running out of power. This application of the field was pioneered by Norma Cenva in the creation of the glowglobes during her tenure working for Tio Holtzman.",
        "special": "As an Asset: Personal suspensors can be used as transportation, for carrying heavy objects, or moving large forms of ordinance."
    },
    
    "Thumper": {
        "asset_type": "Personal",
        "keywords": ["Arrakis", "Sandworm"],
        "quality": 0,
        "description": "A simple device used to summon sandworms on Arrakis. The thumper is composed of a spring-loaded clapper on a short stake that repeatedly strikes the ground. Delayed thumpers exist which have a candle attached to them that burns for one hour before activating the thumper. Longer candles can be used to extend the duration, with an increased change of failure for each additional fifteen minutes.",
        "special": "As an Asset: The thumper is useful in calling or distracting sandworms. The device can be used to cause mass destruction by having the sandworm appear in an area."
    }
}


def create_personal_asset(asset_name, character=None):
    """
    Create a Personal Asset object.
    
    Args:
        asset_name (str): Name of the asset to create
        character (Character, optional): Character to give the asset to
        
    Returns:
        Asset: The created Asset object, or None if asset_name not found
    """
    from evennia import create_object
    from typeclasses.assets import Asset
    
    if asset_name not in PERSONAL_ASSETS:
        return None
    
    asset_data = PERSONAL_ASSETS[asset_name]
    
    # Create the asset object
    asset = create_object(
        Asset,
        key=asset_name,
        location=character if character else None
    )
    
    # Set asset properties
    asset.set_asset_type(asset_data["asset_type"])
    asset.set_quality(asset_data["quality"])
    asset.set_description(asset_data["description"])
    asset.set_special(asset_data["special"])
    
    # Add keywords
    for keyword in asset_data["keywords"]:
        asset.add_keyword(keyword)
    
    return asset


def get_all_personal_asset_names():
    """
    Get a list of all Personal Asset names.
    
    Returns:
        list: List of asset names
    """
    return sorted(PERSONAL_ASSETS.keys())

