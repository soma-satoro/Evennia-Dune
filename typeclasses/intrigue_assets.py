"""
Intrigue Assets Data

This module defines all Intrigue Assets available in Dune.
These can be used to create Asset objects with the correct properties.
"""

# Intrigue Assets organized by category
INTRIGUE_ASSETS = {
    # Favors
    "Debtor": {
        "asset_type": "Intrigue",
        "keywords": ["Desperate", "Frightened", "Paranoid"],
        "quality": 0,
        "description": "Someone owes you. Whether it is cash, drugs, or whatever they have borrowed from you in some way. When needed, you can call in that debt and force them to provide you with something in return. You can do this gradually, always insinuating that the loan you extended to them is about to be withdrawn, or you can do it suddenly, demanding payment now! Of course, as necessary as this might be, it tends to cost an agent their asset. Once burned, or once the favor has been called in and revealed to be a quid pro quo, the relationship between the agent and their asset is usually done. Burned. In a few cases, with the most subtle and most expert of agents—those with Mentat training perhaps—it might be possible to avoid such terminal consequences, but this is rare.",
        "special": "As an Asset: A sudden, vital resource can be elicited, when needed. Funds, a safe-house, something. When the situation is bleak and options are few, this can be a life-saving option."
    },
    
    "Old Friendship": {
        "asset_type": "Intrigue",
        "keywords": ["Faithful", "Reliable", "Wily"],
        "quality": 0,
        "description": "A favor provided by an agent to someone, in the hope they might become an asset, leaves no trace. An unexpected sum of money is suspicious. It draws attention to itself, or it makes its owner act foolishly. A knife leaves marks, or, worse, a dead body which must be hidden or explained. These are clumsy methods. A true agent, an agent worthy of the trust placed in them, does not leave such obvious paths for a hunter to follow. Where is the harm in a favor, however? It's simply a friend trying to help a friend, after all. A perfectly normal, natural thing to want to do. Of course, gaining trust and building a relationship is not easy. It involves work, carefully assessing the intended target and determining what it is that they wish they could have, what it is that they need. But once you have this knowledge, with care, you can maintain this friendship for years if necessary.",
        "special": "As an Asset: A companion you've known for some time, carefully compiling information on them and acting as their friend. They can provide you with information, spy on a target, or hide you when things become dangerous."
    },
    
    "Service": {
        "asset_type": "Intrigue",
        "keywords": ["Reliable", "Valuable"],
        "quality": 0,
        "description": "Everything comes with a price. The universe depends on trade. Everything depends on commerce. But for those who are truly powerful, or those who understand how true power works and where it lies, currency is worthless. Favors… now, favors have value. Favors are the only currency, outside of spice, that holds its worth, that isn't susceptible to the fluctuations of market prices. You provide these services to large organizations and in return, you get to know where they send the resources you offer. They know they can call on you when things get tough. And you know you can call on them.",
        "special": "As an Asset: A large organization is in your pocket and, within reason, you can gain as much of a different asset as you require."
    },
    
    # Valuables
    "Land Rights": {
        "asset_type": "Intrigue",
        "keywords": ["Land", "Production"],
        "quality": 0,
        "description": "A step up from simply trading raw materials, access to the land where these materials are produced can be traded if the price is good enough, allowing whomever has access to generate as much of that raw material as they want… so long as they're willing to do the work. This can be something of a double-edged sword—everyone wants spice, but few are willing to face the dangers and difficulties of harvesting and refining it—but it can serve as part of a lucrative deal and create great opportunities for influence.",
        "special": "As an Asset: Leasing land rights to another can be lucrative, and place another party in a position where they're more open to other deals because they cannot afford to turn you down… but there's risk, because you're giving up some of your capacity to produce those same materials to another. (Plus other keywords according to the type of material, such as Scarce or Abundant.)"
    },
    
    "Manufactured Goods": {
        "asset_type": "Intrigue",
        "keywords": ["Manufactured", "Trade Goods"],
        "quality": 0,
        "description": "Your House manufactures something valuable, or you've managed to obtain some valuable goods which someone is likely to need. This might be technology or crafted items, such as shields, weapons, or vehicles, or it might be a refined substance ready for use, such as the various useful forms and substances that spice can be transformed into.",
        "special": "As an Asset: The ability to manufacture goods can expose you to the influence of whomever provides the raw materials, but finished goods are highly valuable cargo and access to them can open doors that might otherwise remain closed. (Plus other keywords according to the goods, such as Scarce or Abundant.)"
    },
    
    "Raw Materials": {
        "asset_type": "Intrigue",
        "keywords": ["Raw Materials", "Trade Goods"],
        "quality": 0,
        "description": "You have access to a large quantity of the raw materials needed to produce other goods. This may vary from minerals and construction materials such as wood or metals, to raw foodstuffs such as particular kinds of meat or plant matter, and it may vary in rarity from commonplace (but needed in vast quantities) to extremely rare (but precious such as the spice melange). Access to quantities of materials can be useful for trade if you're dealing with someone who needs or wants those materials for something, but anyone skilled in business will be looking for a better deal.",
        "special": "As an Asset: Trading raw materials is an easy way to get embroiled in an intrigue, and the ability to produce and distribute resources can be a powerful way to gain influence. (Plus other keywords according to the type of material, such as Scarce or Abundant.)"
    },
    
    "Supply Contract": {
        "asset_type": "Intrigue",
        "keywords": ["Long-term", "Production", "Trade"],
        "quality": 0,
        "description": "A one-off sale of goods is one thing, but a long-term contract can be a powerful tool in the halls where politics and trade align. A contract to produce goods for another faction can forge a lasting relationship with that faction and help turn their wealth to your advantage. In turn, contracting another faction to supply something to you can ensure you never lack for the resources you need. Either way, there's a lasting connection between both parties, which can allow for greater influence at a later date.",
        "special": "As an Asset: It's difficult to take hostile action against someone who supplies goods to you, or who you supply; these kinds of entanglements help preserve a semblance of peace in the Imperium, tying the interests of competing Houses together. A cunning player of this grand game can use that to their advantage. (Plus other keywords according to of goods, such as Scarce or Abundant.)"
    },
    
    "Valuable Item": {
        "asset_type": "Intrigue",
        "keywords": ["Fragile", "Portable", "Precious"],
        "quality": 0,
        "description": "While not necessarily on the scale of trade contracts and land rights, individual valuable items can be potent assets in trade and intrigue. Items of artistic merit, unique creations of historical or religious value, and similar precious objects are highly sought-after, and their ownership often changes during times of political strife and turmoil, frequently serving as leverage for those possessed of great power, great ambition, and expensive tastes.",
        "special": "As an Asset: Valuable items are often relatively easy to move and trade, as they are frequently small and lightweight compared to their value. This makes them an excellent way of moving value from place to place discretely, which in turn makes them a useful tool during trade and negotiations."
    },
    
    # Blackmail
    "Hostage": {
        "asset_type": "Intrigue",
        "keywords": ["Frightened", "Trapped", "Valuable"],
        "quality": 0,
        "description": "For those prepared to truly commit their resources to such a thing, blackmail can go far. The kidnap of a loved one, a family member, or a close friend—and the threat of harm being committed against them—can be enough to break even the most devoted of servants to a House. Some Mentats even hypothesize that such an extreme approach might be sufficient to shatter the Imperial conditioning. Of course, no one has ever had chance to test such an outlandish theory, but it nevertheless persists. While shame, ridicule, exile, or death are powerful motivators—of the kind that threaten those subject to exposure from more traditional modes of blackmail—the ongoing torture of a loved one might be sufficient to make a person do anything to achieve its cessation. Only the mind of a particularly twisted variety of Mentat is even capable of conjecturing such things, but nevertheless, such creatures do exist.",
        "special": "As an Asset: Kidnapped, imprisoned, and fearful, a hostage is an extremely potent form of leverage, but also carries commensurately high risks. Keeping the hostage well can be difficult, and preventing them from escaping can also require resources."
    },
    
    "Illicit Recording": {
        "asset_type": "Intrigue",
        "keywords": ["Damaging", "Embarrassing"],
        "quality": 0,
        "description": "It is human nature to want things. It is human nature to want things that one isn't allowed to have. Drugs, flesh, money… whatever the laws of the Landsraad forbid, or the rules of a House prohibit, human nature desires more. And when have laws and other such trivialities ever prevented people from doing precisely what they wish? After all, there are always those willing to give into forbidden desires and those prepared to profit from it. Not simply through fulfilling the desire and taking payment, of course. Many are prepared to do just that, but some special individuals are prepared to go a little further… 'accidentally' recording such illicit activities in one form or another, before filing it away, ready and waiting for the moment when it becomes useful.",
        "special": "As an Asset: Recordings, visual or audible, of an asset's illegal (or at least extremely embarrassing) practices. Can be related to drugs, sex, or other activities an agent's target wants to remain hidden."
    },
    
    "Stolen File": {
        "asset_type": "Intrigue",
        "keywords": ["Damaging", "Illicit", "Subtle"],
        "quality": 0,
        "description": "Politics requires its players to wear different masks at different times, depending on the circumstances they find themselves in. A staunch ally of the Atreides today may become the bosom companion of the Harkonnens tomorrow. It's the way of things and entirely accepted, so long as no one can ever prove those previous allegiances. As long as no one has, say, a record of payments made to an assassin to kill a Harkonnen aide. Or the footage of an asset stealing from the Atreides spice supply. Of course, getting hold of such proofs can be difficult, but worth it. Most definitely worth it.",
        "special": "As an Asset: Proof of a target's various machinations against a current employer; extracted from the personal files of the target, these are powerful inducements to ensure a target's continued good behavior."
    },
    
    # Contacts
    "Black Market Trader": {
        "asset_type": "Intrigue",
        "keywords": ["Experienced", "Resourceful", "Well-known"],
        "quality": 0,
        "description": "You need things, naturally. Some of those things are easy to obtain, purchasable in any bazaar, any market, any shop. Other things require sourcing more carefully. That's what black market contacts are for. Anything you need, they can usually find. Yes, they charge a lot, but you get what you pay for. And you might end up looking for some very obscure and illegal stuff. So, you're going to need someone trustworthy, or at least, trustworthy enough.",
        "special": "As an Asset: Someone with one foot in the mercantile world and the other in the underworld. They can get you what you need when you need it. No questions asked, so long as the money is right. Note: All Contacts will also need to be created as NPC objects along with assets."
    },
    
    "Courtesan": {
        "asset_type": "Intrigue",
        "keywords": ["Attractive", "Cunning", "Resourceful"],
        "quality": 0,
        "description": "Sex is always a powerful lure, and a courtesan of any gender is a useful contact. People are rarely as guarded when undressed, and a skilled courtesan can learn much, both from conversation and from a quick study of what a person keeps in their pockets—and what company they keep. The courtesan is an ally and a contact of the highest usefulness, provided you can find one prepared to offer such information. The risk of being caught, and the punishment involved for a courtesan selling information, is much higher than that for any other role. The rewards must therefore be much greater.",
        "special": "As an Asset: A trained courtesan with access to the bedchambers of the wealthy and influential, capable of discovering a great deal if handled carefully. Note: All Contacts will also need to be created as NPC objects along with assets."
    },
    
    "Ex-Agent": {
        "asset_type": "Intrigue",
        "keywords": ["Experienced", "Intelligent", "Wily"],
        "quality": 0,
        "description": "As long as the Landsraad has worked to undermine each other, as long as the Padishah Emperor has watched the affairs of the Houses with paranoid panic, there have been agents. They work to collect information, to spy on the comings and goings of the Houses, to influence the fate of worlds. A few of these agents retire, some are driven out, and some escape. Some even survive outside of their House. But some never entirely escape the life, and remain at its periphery, calling upon their old training and network of contacts to remain viable and to turn their former experience into profit. Ex-agents inevitably know other former or even active agents, and can call on them now and then, for advice, for direction, for the kind of favors old agents understand better than anyone else. However, due to the nature of the game, these are not the most trustworthy people, and should be utilized with caution.",
        "special": "As an Asset: This is a former agent encountered and trusted in in the past, able to be called on for a safe place to hide or tips on the moves being made by opponents. Note: All Contacts will also need to be created as NPC objects along with assets."
    },
    
    # Courtiers
    "Ambitious Newcomer": {
        "asset_type": "Intrigue",
        "keywords": ["Ambitious", "Eager", "Pushy"],
        "quality": 0,
        "description": "Gaining access to the court of the Padishah Emperor can be difficult, even for experienced and well-connected agents. Finding someone who understands the right hand signals, the right gestures to gain admittance to this sanctum, to that library, is a vital step for anyone hoping to situate themselves at the ultimate nexus of power. It is not simply about admission, either. Without the right guide to the myriad factions and shifting allegiances of the Imperial court, even the most sagacious agent can become entirely lost. Newcomers to court with the connections to make their way swiftly up the ranks are ideal targets for agents trying to infiltrate the court—potentially powerful, but inexperienced enough to be taken in by a quick enough tongue.",
        "special": "As an Asset: Recently arrived at the Emperor's court, this scion of a House or otherwise well-connected youngster wants to rise quickly in the eyes of the court. Note: All Courtiers will also need to be created as NPC objects along with assets."
    },
    
    "Confidant of the Emperor": {
        "asset_type": "Intrigue",
        "keywords": ["Cunning", "Paranoid", "Ruthless"],
        "quality": 0,
        "description": "Those fortunate few who have gained the Emperor's favor are always on the lookout for novelty, for something to amuse or surprise the Padishah Emperor, and for someone who might one day be a useful scapegoat. There is little loyalty in the Imperial court; the Padishah Emperor's whims are far too changeable for that and, as a result, friendships and allegiances tend to be brief, though plentiful. An enemy in the morning might be a bosom companion by the evening and an attempted assassin by the time the sun has set. The Emperor's favorites rarely last long and use any means necessary to retain their position. This can be used by the cunning to their advantage, but it can also spell disaster…",
        "special": "As an Asset: Having risen high in the Emperor's esteem, this asset can get you in places and give you information few others can. But this comes with risks; they might be imprisoned or executed for displeasing the Emperor without warning, drawing you into the purge. Note: All Courtiers will also need to be created as NPC objects along with assets."
    },
    
    "House Retainer": {
        "asset_type": "Intrigue",
        "keywords": ["Familiar", "Loyal"],
        "quality": 0,
        "description": "Any House, by its nature, has a wide variety of associated and loyal personnel who serve the House's members and its best interests. The nature, quality, and responsibilities of these individuals varies dramatically, but all are extensions of the House itself, and as such are considered as assets.",
        "special": "As an Asset: Chapter 3: Creating Your House covers the creation of a House and establishes guidelines for creating retainer assets, before and during play. Note: All Courtiers will also need to be created as NPC objects along with assets."
    },
    
    "Indebted Landowner": {
        "asset_type": "Intrigue",
        "keywords": ["Fallen", "Indebted", "Loyal"],  # Can also be "Disloyal"
        "quality": 0,
        "description": "Not all who bear titles are wealthy, and due to the whims of the market or through political connivance, it is entirely possible that a landowner may be relatively poor, either inhabiting a shell of a former estate—hollowed out by the necessity of selling possessions to survive—or subsisting entirely on a wave of debt incurred to maintain the illusion of prosperity. At the end of the day when the accounting is complete, however, the House, and particularly its head, is in debt.",
        "special": "As an Asset: Indebted landowners are potentially the most extreme of courtier assets, as they may range from fiercely loyal and hoping to better their status within the House ruling over them, to embittered has-beens who blame those above them for their sorry state, and can be utilized against the House by its enemies. (Pick either Loyal or Disloyal as a keyword.) Note: All Courtiers will also need to be created as NPC objects along with assets."
    },
    
    "Politician": {
        "asset_type": "Intrigue",
        "keywords": ["Cunning", "Intelligent", "Wily"],
        "quality": 0,
        "description": "A politician is an essential guide to precisely who is in favor, who is about to be in favor and who is about to experience a precipitous fall. Such information is utterly invaluable, enabling agents to plot strategies to ingratiate themselves with one faction at the expense of another. It is in the back-and-forth of courtier politics that the grand fiefs are handed out to those the Emperor wishes to reward (or to punish), and only those politicians intimately tied to the moods of the court, and to the rise and fall of individuals in the Emperor's favor, can predict certain upcoming changes. When Count Fenring was sent to Arrakis to inspect the Harkonnen operation, the move was common knowledge amongst the various politicians at court long before it began to filter through to the Landsraad.",
        "special": "As an Asset: A long-serving member of the court, having seen it all and survived various coup attempts, this asset knows everything and everyone, and is wily enough to avoid the worst of the fallout. Note: All Courtiers will also need to be created as NPC objects along with assets."
    }
}


def create_intrigue_asset(asset_name, character=None):
    """
    Create an Intrigue Asset object.
    
    Args:
        asset_name (str): Name of the asset to create
        character (Character, optional): Character to give the asset to
        
    Returns:
        Asset: The created Asset object, or None if asset_name not found
    """
    from evennia import create_object
    from typeclasses.assets import Asset
    
    if asset_name not in INTRIGUE_ASSETS:
        return None
    
    asset_data = INTRIGUE_ASSETS[asset_name]
    
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


def get_all_intrigue_asset_names():
    """
    Get a list of all Intrigue Asset names.
    
    Returns:
        list: List of asset names
    """
    return sorted(INTRIGUE_ASSETS.keys())

