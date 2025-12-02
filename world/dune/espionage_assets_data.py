"""
Espionage Assets Data

This module defines all Espionage Assets available in Dune.
Asset data is stored separately from typeclass logic.
"""

# Espionage Assets organized by category
ESPIONAGE_ASSETS = {
    # Weapons
    "Shigawire Garrote": {
        "asset_type": "Espionage",
        "keywords": ["Common", "Melee Weapon", "Subtle"],
        "quality": 0,
        "description": "Shigawire comes from the Narvi narviium ground vine found on Salusa Secundus and III Delta Kaising. Its primary use is in holding and transmitting messages. However, the Sardaukar were the first ones to use the strong, thin filaments as garrotes. They now carry them as standard issue, often blended into one's hair or concealed elsewhere.",
        "special": "As an Asset: Shigawire isn't hard to find in the Imperium, considering its varied uses in communications. If an individual wants one for offense or defense, it's almost always close at hand. That also means that an opponent has easy access, as well."
    },
    
    "Slip-Tip": {
        "asset_type": "Espionage",
        "keywords": ["Archaic", "Melee Weapon", "Small"],
        "quality": 0,
        "description": "A slip-tip can render even the strongest opponent powerless just by scratching the skin. This weapon emerged from the world of shield-fighting, where combatants carry blades in both hands. In a traditional match, the slip-tip is the shorter, poison-coated blade held in the left hand. Those who use them outside the shield-fighting arena are usually making a statement by using the archaic weapons.",
        "special": "As an Asset: Though these blades have a long-established history in the Imperium and originated from ritual combat, some with dangerous intent carry them in day-to-day life. Depending on the poisons chosen, these thin blades can result in a quick, quiet death or a long, torturous one."
    },
    
    # Drugs
    "Chaumas and Chaumurky": {
        "asset_type": "Espionage",
        "keywords": ["Expensive", "Ingestible", "Stealthy"],
        "quality": 0,
        "description": "Poisoning a friend, foe, or family member through food and drink is a time-honored practice in the Imperium. Chaumas refers to poison administered through comestibles, while chaumurky is the category of poisoned beverages. These terms include both fast-acting and slow-acting poisons.",
        "special": "As an Asset: Those who are members of the Landsraad are wary of both chaumas and chaumurky and make liberal use of poison snoopers. Those who implement chaumas and chaumurky often need to find ways to avoid poison snoopers and the various methods of scanning for and identifying different poisons."
    },
    
    "Elacca": {
        "asset_type": "Espionage",
        "keywords": ["Bloodlust", "Drug", "Inexpensive", "Orange-tinged Skin"],
        "quality": 0,
        "description": "On Ecaz, a planet in Alpha Centauri B, they burn elacca wood to create this potent narcotic. It sends users into an intense rage that suppresses an individual's survival instincts and changes their skin to a peculiar carrot-colored hue. Few in the Imperium choose to take this drug of their own free will. The most common application of this narcotic is in drugging slave-combatants for the gladiatorial arenas. However, some soldiers do choose to ingest it before a battle to harden their resolve.",
        "special": "As an Asset: Despite the Imperium generally frowning on the practice, some commanders have dosed their troops to eliminate the risk of desertion before or during an engagement. Some also suggest using it to send an unsuspecting individual on a rampage against a target to deflect suspicion. In the past, unwittingly drugged victims died at the hands of those defending themselves against elacca-enraged individuals."
    },
    
    "Residual Poison": {
        "asset_type": "Espionage",
        "keywords": ["Drug", "Expensive", "Unobtrusive"],
        "quality": 0,
        "description": "The twisted Mentat Piter de Vries created a system of dependence in which an individual must receive periodic antidotes or the poison coursing through their body will kill them over time. The victim may or may not know about the death waiting for them. This is a savage, but effective, method of control.",
        "special": "As an Asset: Residual poison may be used as blackmail or a failsafe. The victim may act out of character to make sure they get their antidotes on time. A victim who doesn't know about the residual poison may simply not receive the antidote when their usefulness runs out."
    },
    
    "Semuta": {
        "asset_type": "Espionage",
        "keywords": ["Addictive", "Euphoric", "Expensive", "Ingestible"],
        "quality": 0,
        "description": "Ecaz's valuable elacca tree also produces semuta, a highly addictive narcotic. As opposed to the frenzy that the elacca drug causes in its users, semuta evokes a euphoric bliss when paired with atonal semuta music. A semuta user can counteract the effects with an antidote.",
        "special": "As an Asset: Many choose to use semuta as a way to relax. However, others take advantage of the associated addiction as a means of manipulating others through blackmail, withholding the drug, or offering copious amounts of the narcotic to an addict. Having a steady, reliable supply can lead to extreme loyalty. Semuta is also a popular currency for bribery."
    },
    
    "Shere": {
        "asset_type": "Espionage",
        "keywords": ["Expensive", "Ingestive", "Obscuring", "Uncommon"],
        "quality": 0,
        "description": "A drug taken by anyone fearing that they will be subjected to an Ixian probe. This obscures the neural processes that the probe reads, making collection and duplication of the subject's thoughts, memories, and emotions impossible. Upon death, a subject using shere suffers rapid neural disintegration, eliminating any possibility of future copying. The risk of side effects such as nerve damage make taking this drug a substance of last resort.",
        "special": "As an Asset: A subject that has consumed shere is immune to the effects of an Ixian probe while alive or dead. The later T-Probe, however, is unhindered by the drug."
    },
    
    "Truthsayer Drug": {
        "asset_type": "Espionage",
        "keywords": ["Expensive", "Ingestible", "Poisonous", "Spice-derived"],
        "quality": 0,
        "description": "By falling into a truthtrance, some remarkable Bene Gesserit Reverend Mothers have the ability to distinguish truth from falsehood in even the most practiced liars. Though not all Reverend Mothers need them, truthsayer drugs allow them to enter the truthtrance. Without the control afforded by prana-bindu training, anyone lacking the conditioning of the Bene Gesserit taking a truthsayer drug dies a painful death.",
        "special": "As an Asset: For those possessing both the confidence to believe themselves exceptional and the desire to practice the mystical Bene Gesserit arts, the truthsayer drugs are a powerful temptation. As such, the truthsayer drugs can be used as currency, poison, or on a Bene Gesserit who can enter the truthtrance."
    },
    
    "Verite": {
        "asset_type": "Espionage",
        "keywords": ["Expensive", "Ingestible", "Narcotic"],
        "quality": 0,
        "description": "Yet another specialty product of Ecaz, verite is a plant that grows on only that planet. After a specific processing technique, it becomes a narcotic. Verite smashes through a user's willpower, compelling them to tell the truth. It is impossible to resist.",
        "special": "As an Asset: Verite is a viable alternative to a Bene Gesserit Truthsayer. This narcotic is also an effective interrogation tactic or an intelligence-gathering tool for dosed unknowingly."
    },
    
    # Communication & Information
    "Distrans": {
        "asset_type": "Espionage",
        "keywords": ["Animal", "Courier", "Stealth"],
        "quality": 0,
        "description": "While the specific technology varies by planet and subject, distrans enable a user to implant information in an animal and turn it into an unknown accomplice in conveying messages. The recipient of the animal retrieves the message by using a code. The animal relays the message through chirps, screeches, and other noises that approximate words. Birds are frequently used as couriers, with bats being the most sought after for their nocturnal abilities.",
        "special": "As an Asset: Distrans ensure private and secure communication."
    },
    
    "Intelligence": {
        "asset_type": "Espionage",
        "keywords": ["Secret Information"],
        "quality": 0,
        "description": "Illicit information comes in many forms in the Imperium. Tiny minimic films made from shigawire, Bene Gesserit coded dots, decoders, intercepted communications, spy-eyes, spies, and traitors can all provide different insights into the trundling gears of the Imperium. Ixian dampers and cones of silence exist in the Imperium for good reason. Trust no one.",
        "special": "As an Asset: Intelligence gathering goes both ways. Those searching for secrets might be giving away valuable details themselves."
    },
    
    "Interrogation": {
        "asset_type": "Espionage",
        "keywords": ["Secret Information"],
        "quality": 0,
        "description": "The Harkonnens in particular are known for their success in wringing intelligence out of unwilling captives. Torture, verite, and all manner of brutal methods are common and accepted in the Imperium.",
        "special": "As an Asset: Interrogation is effective. Using it or resisting it will require mental, physical, and spiritual fortitude."
    },
    
    "Map": {
        "asset_type": "Espionage",
        "keywords": ["Secret information"],
        "quality": 0,
        "description": "Guild bribery, intentional deceit, financial dishonesty, and geographical fraud all contribute to flawed or incomplete maps of the various planets and systems within the Imperium. Accurate maps are helpful for survival and planning but finding them is not always easy. Many Houses and communities have their reasons to hide this kind of information.",
        "special": "As an Asset: A reliable map can reveal a lot about a planet, the people, and the local Houses... and what they're hiding. Resources, weapons, technology, warehouses, or sweeping changes to a planet's environment might all be things that different factions want to keep to themselves."
    },
    
    "Shigawire": {
        "asset_type": "Espionage",
        "keywords": ["Common", "Inexpensive", "Physical Item"],
        "quality": 0,
        "description": "An organic product of the Narvi narviium ground vine found on Salusa Secundus and III Delta Kaising, shigawire is critical for communication across the Imperium. Though the Sardaukar sometimes use the strong, thin wire as a garrote, it's more often found in recording and transmitting devices. Tiny, unobtrusive minimic films and the mnemonic pulse-imprinted filmbooks are two common uses of this vine.",
        "special": "As an Asset: Minimic films are only one micron in diameter, making them easy to smuggle and hide. Encrypted shigawire reels also act as ways to send messages."
    },
    
    # Contacts and Agents
    "Assassin": {
        "asset_type": "Espionage",
        "keywords": ["Cunning", "Dangerous", "Elusive"],
        "quality": 0,
        "description": "Knowledgeable in the rules, regulations, and permissible techniques from the Assassins' Handbook, assassins are not rogue actors working outside the system but rather a critical part of how the Imperium functions. By adhering to the restrictions set out in the War of Assassins under the Great Convention and Guild Peace, assassins help to keep warfare between the Houses of the Landsraad civil... or at least with minimal civilian casualties. Assassins are clever, dangerous, and often placed in positions of power within the Great Houses.",
        "special": "As an Asset: An assassin has certain skills and an understanding of how society works that not all are privy to. They're a good friend to have and a cruel foe to face. With their contacts spread among the underbelly of the Imperium as well as the highest ranks of nobility, they often have intelligence others don't."
    },
    
    "Corporate Spy": {
        "asset_type": "Espionage",
        "keywords": ["Elusive", "Knowledgeable"],
        "quality": 0,
        "description": "House Vernius, House Harkonnen, and others all have large organizations that they run. They provide technology, weapons, and other resources to the rest of the Imperium. Many Houses also have shares in the Empire-wide economic syndicate CHOAM, the Combine Honnete Ober Advancer Mercantiles. As a result, many Houses, CHOAM itself, the Bene Gesserit, and other factions throughout the Imperium have embedded spies throughout these institutions.",
        "special": "As an Asset: Spies may know about, or know how to find, secret schematics, exclusive technology, confidential formulas, and other valuable information. They may also have access to sensitive details about their employers, giving anyone who gets their hands on a spy the chance to turn the tables on a rival."
    },
    
    "Face Dancer": {
        "asset_type": "Espionage",
        "keywords": ["Elusive", "Genetically Programmed", "Indistinguishable"],
        "quality": 0,
        "description": "These genetically-engineered humanoids cultivated by the Bene Tleilax are unrivaled in the arena of spycraft. With their ability to change their appearance and even secondary sex characteristics, Face Dancers can mimic their targets to an almost undetectable degree. If a Face Dancer has infiltrated an organization, they may be almost impossible to root out. This gives the Bene Tleilax incredible power in the Imperium, despite the general disdain toward them as a people.",
        "special": "As an Asset: Face Dancers can sneak into almost any location, organization, or government without notice. However, they are programmed with loyalty to the Bene Tleilax, so turning one against their masters or toward independence is not a simple task. Their devotion to their Bene Tleilax masters may become a liability in the field. A Face Dancer may also come to believe that they are the person whose life they assumed, if left in place for too long, and in some cases can break free of their Tleilaxu masters."
    },
    
    "Mentat Master of Assassins": {
        "asset_type": "Espionage",
        "keywords": ["Human Computer", "Intelligent", "Tricky"],
        "quality": 0,
        "description": "After the ban on thinking machines in the Imperium, Mentats (or 'human computers') took over the assessment and forecasting tasks that the thinking machines once performed. Mentats are often trained to fight and kill as well. The title Master of Assassins goes to the Mentat who serves a House Major. They mastermind the strategies in a War of Assassins against and for their House. Houses place a high value on their Masters of Assassins.",
        "special": "As an Asset: Mentats have incredible abilities that allow them to evaluate situations while considering vast amounts of data. They can often predict upcoming offensives and determine the best course of action for their Houses. A Mentat Master of Assassins is a dangerous and clever opponent."
    },
    
    "Political Spy": {
        "asset_type": "Espionage",
        "keywords": ["Elusive", "Knowledgeable", "Tricky"],
        "quality": 0,
        "description": "The Landsraad represents all the Houses Major and Minor in the Imperium but is only one of its ruling bodies. With so many different parts to the Imperium affecting wide-ranging policy, political spies are rampant. Many Houses try to infiltrate the Padishah Emperor's own government. Others attempt to blackmail rival or lesser Houses with the information they gather. For a member of a House, it is difficult to determine who to trust even within one's own family.",
        "special": "As an Asset: A political spy can provide information on a War of Assassins, blackmail material, or plans for Landsraad proposals. Catching a spy can result in new information about a known enemy or an unknown adversary. Protecting one's spies and defending against hostile spies is a never-ending battle for the Houses of the Imperium."
    }
}

