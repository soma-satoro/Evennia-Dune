"""
Talents for Dune Character Generation

Talents are special abilities that characters can possess.
Some talents are restricted to specific factions, and some
require parameters (skill or drive).
"""

# Talent categories
TALENT_CATEGORIES = {
    "General": "General talents available to all characters",
    "Bene Gesserit": "Talents restricted to Bene Gesserit Sisterhood",
    "Fremen": "Talents restricted to Fremen",
    "Mentat": "Talents restricted to Mentat Academies",
    "Spacing Guild": "Talents restricted to Spacing Guild",
    "Suk Doctor": "Talents restricted to Suk Doctors",
    "CHOAM": "Talents restricted to CHOAM",
    "Sardaukar": "Talents restricted to Sardaukar Legions",
    "Face Dancer": "Talents restricted to Tleilaxu Face Dancers",
    "Swordmaster": "Talents restricted to Swordmasters of Ginaz",
    "House Jongleur": "Talents restricted to House Jongleur",
    "Spice (Physical)": "Talents related to spice consumption (physical effects)",
    "Spice (Mental)": "Talents related to spice consumption (mental effects)",
}

# All talents with their metadata
TALENTS = {
    # GENERAL TALENTS
    "Advisor": {
        "category": "General",
        "requires_parameter": "skill",
        "description": "You've got a knack for guiding others through problems. When you choose this talent, select a single skill. Whenever you assist an ally and you use that skill, the ally you assist may re-roll a single d20 in their dice pool.",
    },
    "Binding Promise": {
        "category": "General",
        "description": "Whether through your demeanor, your reputation, or the method of your persuasion, you have a way of making people reluctant to break faith with you. When you succeed at a Communicate test to persuade someone to agree to a promise or agreement, you may spend one, two, or three points of Momentum to make that agreement binding.",
    },
    "Bold": {
        "category": "General",
        "requires_parameter": "skill",
        "description": "When you take calculated risks, you tend to succeed more often than seems reasonable. When you select this talent, choose a single skill. When you attempt a test using the chosen skill, and you buy additional d20s by generating Threat for the gamemaster, you may re-roll a single d20 in that dice pool.",
    },
    "Bolster": {
        "category": "General",
        "description": "Your certainty and resolve are a beacon to others, who might waver without your example. Once per scene, when an ally fails a skill test, you may immediately spend 2 points of Momentum or add 2 to Threat to allow that ally to re-roll their dice pool.",
    },
    "Cautious": {
        "category": "General",
        "requires_parameter": "skill",
        "description": "You are patient and circumspect, acting only when the odds are in your favor. When you select this talent, choose a single skill. When you attempt a test using that skill, and you buy additional d20s by spending Momentum, you may re-roll a single d20 in that dice pool.",
    },
    "Collaboration": {
        "category": "General",
        "requires_parameter": "skill",
        "description": "You've coached your allies to capitalize on your expertise, and that effort has paid off. When you select this talent, choose a single skill with a rating of 6 or more. Whenever an ally attempts a test using that skill, and you can communicate with them, you may spend 2 points of Momentum to allow them to use your score for that skill.",
    },
    "Constantly Watching": {
        "category": "General",
        "description": "You're vigilant, bordering on paranoid… and little catches you off-guard. Whenever you attempt a skill test to detect danger or hidden enemies, you reduce the Difficulty by 2, to a minimum of 0.",
    },
    "Cool Under Pressure": {
        "category": "General",
        "requires_parameter": "skill",
        "description": "When the situation gets tough, you take a deep breath and get the job done. When you select this talent, choose a single skill. When you attempt a test using that skill, before rolling you may spend a Determination point to automatically succeed at that test, but you generate no Momentum.",
    },
    "Decisive Action": {
        "category": "General",
        "description": "You take risks in combat, often ones that seem foolhardy or needless. You have a knack for making those gambles pay off. In a conflict, when you succeed at a Battle test to remove an opponent's assets, and you bought one or more dice by generating Threat, you may spend 2 points of Momentum to remove a second enemy asset.",
    },
    "Dedication": {
        "category": "General",
        "description": "Your commitment to a cause is unwavering, and this has carried you through many a tough situation. At the start of a scene, if there is no Momentum in the group pool, roll 1d20. If you roll equal to or less than your Discipline score, add 1 to the group Momentum pool.",
    },
    "Deliberate Motion": {
        "category": "General",
        "description": "Every step you take is considered, and you are exceptionally sure-footed. When you attempt a Move test and suffer one or more complications, you may spend Momentum to ignore some or all of those complications; this costs 1 point of Momentum per complication ignored.",
    },
    "Direct": {
        "category": "General",
        "description": "Your will and presence can drive others to act swiftly and efficiently. Once per scene, you may command an ally or subordinate to act. This requires no test from you, but the commanded ally may immediately attempt an action of their own.",
    },
    "Driven": {
        "category": "General",
        "description": "Your determination does not waver. After you spend a point of Determination, roll 1d20. If you roll equal to or under your Discipline rating (by itself), you immediately regain that point of Determination.",
    },
    "Dual Fealty": {
        "category": "General",
        "description": "You owe your service and your life to two different factions equally, and you have the trust of both. Choose two factions to be loyal to. Both factions are aware of your loyalties to both and expect that you will not betray one to the other.",
    },
    "Find Trouble": {
        "category": "General",
        "description": "You know where to find the criminal element wherever you go. Wherever you are, once per adventure, you can always contact the criminal underworld or black market (as long as there is one in that area).",
    },
    "Hidden Motives": {
        "category": "General",
        "description": "You are a master at concealing your intentions and motivations. Few truly know what drives you, even if they think they understand you. When an opponent fails an Understand or Communicate test against you, you may immediately create a trait which reflects a mistaken belief they have about you.",
    },
    "Improved Resources": {
        "category": "General",
        "description": "You are entrusted with greater access to the tools and resources you need to achieve your goals. You may increase the number of assets you possess by +1. This talent may be purchased multiple times.",
    },
    "Improvised Weapon": {
        "category": "General",
        "description": "You are able to turn the most innocuous items into deadly weapons at a moment's notice. Once per scene you may create a Quality 0 asset (at no cost) that you can use in a personal or skirmish conflict.",
    },
    "Intense Study": {
        "category": "General",
        "description": "You are extremely well-read, with vast amounts of knowledge about a wide range of subjects. Once per scene, you may use your Understand skill on a single skill test instead of any other skill, and you are counted as having a focus for that test.",
    },
    "Make Haste": {
        "category": "General",
        "description": "There is value in speed, even if there are consequences. When you attempt a Move test, you may choose to suffer one additional complication in exchange for scoring one automatic success on the test.",
    },
    "Mask of Power": {
        "category": "General",
        "description": "You can intimate that you know more than you do about an enemy's secrets. Once per scene you may create an asset (at no cost) such as blackmail evidence or an owed favor that will allow you to initiate an intrigue or espionage conflict with a person of your choosing.",
    },
    "Master-at-Arms": {
        "category": "General",
        "description": "Your expertise in battle is considerable, and few can match your effectiveness in combat. At the start of a duel, skirmish, or battle scene, select a single asset that represents a melee weapon or a unit of troops. Due to your prowess, you may spend 1 Momentum to improve that asset's Quality by 1 for the next conflict in this scene.",
    },
    "Masterful Innuendo": {
        "category": "General",
        "description": "You have a special knack for saying more than one thing at once, conveying one message with the literal meaning of your words and another with innuendo, allusions, and signals that only the intended recipients will understand.",
    },
    "Nimble": {
        "category": "General",
        "description": "You're quick on your feet, and few obstacles can impede you. When attempting a Move test to move over, around, or through difficult terrain or similar physical obstacles, you may reduce the Difficulty of the test by 2.",
    },
    "Passive Scrutiny": {
        "category": "General",
        "description": "You are quick to notice details which may be of importance later. When you enter a scene, you may ask one question of the gamemaster as if you'd spent Momentum to Obtain Information.",
    },
    "Performer": {
        "category": "General",
        "description": "Your skill with music or poetry helps to soothe and inspire your comrades. Once per scene you may entertain the group with a short performance. Once the performance is over you may add 1 to the group's Momentum pool.",
    },
    "Putting Theory into Practice": {
        "category": "General",
        "description": "You've learned how to quickly turn newfound knowledge into a practical advantage. Once per scene, when you Obtain Information, you may create a trait for free, which must represent an advantage, opportunity, or weakness you've identified.",
    },
    "Ransack": {
        "category": "General",
        "description": "When time is of the essence, you prioritize getting the work done over covering your tracks. When you attempt an Understand test to search an area, you may add 2 to Threat to reduce the difficulty of the test by 1, and to halve the amount of time the test takes to attempt.",
    },
    "Rapid Maneuver": {
        "category": "General",
        "description": "You're fast, able to cross ground, find the shortest route, and bring your tools to bear quicker than most. When attempting a skill test to reach a destination quickly when moving on foot or in a vehicle, reduce the Difficulty by 1.",
    },
    "Rapid Recovery": {
        "category": "General",
        "description": "You return to fighting form quickly after being injured, even when it may be risky to return to the fray. Once per scene, at the start of your turn, you may add +2 to Threat to remove a complication which represents an injury.",
    },
    "Resilience": {
        "category": "General",
        "requires_parameter": "skill",
        "description": "It takes a lot to put you down in a conflict. You get back up more often than most. Usually you may only 'Resist Defeat' once per scene. You can do so twice per scene, but only when in a conflict using the listed skill.",
    },
    "Rigorous Control": {
        "category": "General",
        "description": "You are an island of calm amidst the chaos of the universe, maintaining control over yourself when you cannot control anything else. Whenever you are attempting an extended task where the requirement is based on one of your skills, at the cost of 1 Momentum you may use your Discipline for that requirement instead of the skill normally used.",
    },
    "Specialist": {
        "category": "General",
        "description": "Your duties require you to manage a greater type of a specific kind of asset. You may purchase this talent multiple times. Each time you select this talent, choose a single category of asset from the following list: dueling, warfare, espionage, or intrigue. You increase the number of assets you possess by +2, but those two additional assets must be from the chosen category.",
    },
    "Stirring Rhetoric": {
        "category": "General",
        "description": "You are an able public speaker, and your words carry weight and purpose. When you succeed at a Communicate test to address a group of people, you may select a number of those people equal to your Communicate skill. Those characters may re-roll a single d20 on the next test they attempt.",
    },
    "Subtle Step": {
        "category": "General",
        "description": "You're well-versed in methods of avoiding notice, and you reveal little that you do not intend to. When you attempt a Move test to sneak or otherwise pass unseen through an area, or when you attempt to move an asset subtly during a conflict, the first extra d20 you purchase for the test is free.",
    },
    "Subtle Words": {
        "category": "General",
        "description": "You are skilled at swaying others with a few quiet words spoken in the right place at the right time. Even they may not realize what influence your words have had. When you attempt a Communicate test, and you buy one or more dice by spending Momentum, you may create a new trait for free upon the character you have spoken to.",
    },
    "The Reason I Fight": {
        "category": "General",
        "requires_parameter": "drive",
        "description": "Skill is not the only factor in determining victory; those who want it more, and those who are driven by a greater sense of purpose, may triumph when they should have failed. When you select this talent, choose a single drive rated 6 or higher. When you attempt a Battle test using the chosen drive, and the drive's statement aligns with the action being attempted, you may re-roll 1d20.",
    },
    "The Slow Blade": {
        "category": "General",
        "description": "The slow blade pierces the shield. You're well-versed in the subtle ways of avoiding an opponent's defenses. When you make an attack during a duel or a skirmish using a melee weapon, and you buy one or more dice by spending Momentum, you may choose one of the enemy's assets in the same zone as your attack; you can ignore that asset during your attack.",
    },
    "To Fight Someone Is to Know Them": {
        "category": "General",
        "requires_parameter": "skill",
        "description": "You are an expert in studying your foes in conflict, learning how they think and gleaning secrets from them based on how they move, attack, and defend. When you select this talent, choose a skill. When you win a conflict using the chosen skill, you gain two bonus Momentum points.",
    },
    "Unquestionable Loyalty": {
        "category": "General",
        "description": "Your loyalty to your House is such that it can drive you to action even in the direst of circumstances. At the start of each adventure, you begin with one additional point of Determination. This extra point can only be used on an action which is in direct service to your House.",
    },
    
    # BENE GESSERIT TALENTS
    "Hyperawareness": {
        "category": "Bene Gesserit",
        "description": "Your training has honed your awareness to an incredible degree, allowing you to notice details too small for others to perceive. Whenever you spend Momentum to Obtain Information about the current situation, your current location, or a person you can currently observe, you may ask two questions for the first point of Momentum spent.",
    },
    "Other Memory": {
        "category": "Bene Gesserit",
        "description": "You have undergone the Agony attended by another Reverend Mother, and now you can draw upon the memories and wisdom of all your ancestors. In doing so, you have become a Reverend Mother of the Bene Gesserit. Whenever you attempt a test where knowledge of past events—even those which may have occurred many generations ago—would be beneficial, you score three automatic successes.",
    },
    "Prana-bindu Conditioning": {
        "category": "Bene Gesserit",
        "description": "You have absolute control over your body. Every muscle and every nerve is under your control, and you have even mastered your own body chemistry and metabolism. Whenever you attempt a Move or Discipline test which relies on your control of your body, you may re-roll a single d20.",
    },
    "Voice": {
        "category": "Bene Gesserit",
        "description": "You have been trained to modulate your voice to influence the subconscious minds of others. With this skill you can subtly manipulate others, alter motivations and moods, or even compel action from the unwilling. When you use Voice, you may add one, two, or three points to Threat to score the same number of automatic successes on any Communicate test made to influence your chosen target.",
    },
    "Lightning Reflexes": {
        "category": "Bene Gesserit",
        "description": "Your command of your muscles is so powerful you can move like lightning. You may spend 1 Momentum to take your action first in any given round, regardless of the actual initiative order.",
    },
    
    # FREMEN TALENTS
    "Chosen of Shai-Hulud": {
        "category": "Fremen",
        "requires_parameter": "skill",
        "description": "To ride the worm is to prove your mastery of the desert. Whether it is talent or that you are favored by Shai-Hulud, you have a knack for capturing and riding the great worms. There are three tests that need to be made to capture a sandworm: Move, Discipline, and Understand. Pick one of those skills. When making a test with that skill when attempting to mount or ride a sandworm, you may reduce the Difficulty of the test by 2. This talent may be taken up to three times with a different skill chosen each time.",
    },
    "Crysknife Master": {
        "category": "Fremen",
        "description": "Crysknives are immediately recognizable, in part due to their distinctive opalescent color and to their jagged surface. When making an attack during a skirmish or a duel, when using a crysknife, you may automatically generate 1 free point of Momentum whenever you succeed.",
    },
    "Desert Walker": {
        "category": "Fremen",
        "description": "Accustomed to the privations of life on Arrakis, the Fremen know how to exploit every advantage they possess to ensure their survival. You may ignore the detrimental effects of one environmental trait that is active in the scene as long as it relates to deserts, heat, thirst, or Arrakis.",
    },
    "Fremen Technology": {
        "category": "Fremen",
        "description": "Stillsuits, stilltents, deathstills, thumpers. All these items of Fremen technology require careful understanding, if they are to be maintained to the standards needed to survive the heat and aridity of Arrakis. When making an Obtain Information spend about a piece of Fremen technology or attempting to repair such, you may re-roll 1d20 in your pool.",
    },
    "Jacurutu": {
        "category": "Fremen",
        "description": "Not every sietch lives harmoniously together. Some tribes have performed such dark deeds they are outcast from Fremen society and their names struck from all records. You are descended from such outcasts and have hidden in Fremen society for years but remained loyal to your true tribe. The Difficulty for you to deceive any Fremen is reduced by 1.",
    },
    "Peace of Shai-Hulud": {
        "category": "Fremen",
        "description": "The sandworm, Shai-Hulud, is seen by the Fremen as a form or manifestation of god itself. You may reduce the Difficulty to see wormsign by 1. If you do see a worm you always know which direction it is going in and how long it will take to get there.",
    },
    "Walk Without Rhythm": {
        "category": "Fremen",
        "description": "The Maker is attracted by rhythm, by the consistent thud of feet against the surface of the sand. The Fremen have evolved a means of constantly varying and shifting their progress across the desert. When crossing an open stretch of sand, you do not need to make a test to see if you can avoid attracting a worm with your movements.",
    },
    "Tooth Crafter": {
        "category": "Fremen",
        "description": "The secrets of creating a crysknife are kept by only a few craftsmen among the Fremen. You know the secrets of crafting a crysknife. If you are present to collect the teeth of a worm you may make a Difficulty 4 Discipline test. If successful, you may spend 1 Momentum to craft one crysknife.",
    },
    "Water Wisdom": {
        "category": "Fremen",
        "description": "The collection and preservation of water is one of the central aspects of Fremen life and culture. You are adept at managing your water rations. As such you may ignore the effects of any one trait relating to thirst or water loss in a scene.",
    },
    "Ways of the Ichwan Bedwine": {
        "category": "Fremen",
        "description": "The Fremen eschew most forms of writing. Instead, they rely on their own oral records, a history of vast length and scope maintained almost entirely unchanged. When you use this talent, you gain one automatic success when making a test to Understand anything relating to the Fremen's history or culture.",
    },
    "Fanatic Killer": {
        "category": "Fremen",
        "description": "Specializing in close-quarter combat, you are an astonishingly efficient killer. Even as you land mortal blows, you are pivoting into position to make your next strike. You gain 1 Momentum each time you attack a foe you have not yet engaged with in this scene.",
    },
    "Silent Attack": {
        "category": "Fremen",
        "description": "You move like the wind and strike in silence. Few enemies who fail to see you approach survive your first strike. If your target is unaware of you, then your initial attack dice pool is 3d20 rather than 2d20 for your first attack.",
    },
    "Strike From the Shadows": {
        "category": "Fremen",
        "description": "You are as silent as the night and adept at flanking your enemies and ambushing them. If you are making a stealth test with the express purpose of getting close to a target to make an attack, the Difficulty is reduced by 1.",
    },
    
    # MENTAT TALENTS
    "Calculated Prediction": {
        "category": "Mentat",
        "description": "Using the facts and figures you have memorized and your ability to process information, you can attempt to predict the future. You may spend a few minutes to meditate upon predicting the future. This requires an Understand test with a Difficulty of 4; if successful, you may ask the Gamemaster to state something that is likely to occur in the future.",
    },
    "Mentat Discipline": {
        "category": "Mentat",
        "description": "Intense mental conditioning and extensive training have developed your intellect into a potent and valuable thing. You can retain and process vast amounts of information at extraordinary speeds. You have almost perfect recall, for even the most complex data. When making an Understand test that applies to recalling data, one of the D20s in your pool may be considered to have rolled a 1 instead of rolling it.",
    },
    "Mind Palace": {
        "category": "Mentat",
        "description": "You have exceptional recall and can reconstruct events and places you have experienced with perfect accuracy, allowing you to revisit them later. You may attempt a Difficulty 0 Understand test to recall a past event or a place you have previously been to.",
    },
    "Twisted Mentat": {
        "category": "Mentat",
        "description": "Your Mentat abilities were shaped and engineered by the Bene Tleilax to leave you unencumbered by such petty things as morality, taboo, or decency. Whenever you attempt an Understand test, you generate one bonus Momentum point for each die you bought by adding to Threat. This Talent may only be chosen in character creation.",
    },
    "Verify": {
        "category": "Mentat",
        "description": "You have so much data at your fingertips you can see where it contradicts and determine where falsehoods lie. You may spend a point of Momentum to ask the gamemaster if a piece of information you have is true or false.",
    },
    "Calculated Distress": {
        "category": "Mentat",
        "description": "When you make plans, you are able to ensure they cause the most stress and upset to your target. When a plan you are part of (usually with an Intrigue or Espionage conflict) is resolved, you may impose a negative emotional trait on one of your opponents to represent the stress you have caused them.",
    },
    "Exit Trance": {
        "category": "Mentat",
        "description": "You can enter a deep trance and disassociate your body and mind to avoid interrogation. You give yourself a complex mental problem (such as calculating pi to a million digits) and give your mind over wholly to the task.",
    },
    "Mental Map": {
        "category": "Mentat",
        "description": "You can keep in your mind the image of a map you have seen, while performing other functions. If you have seen a map of the area you are in, you may call it to mind to gain the trait 'Knows the Area' for the current scene.",
    },
    "Never Forget a Face": {
        "category": "Mentat",
        "description": "You have made a study of the Houses of the Landsraad and know the leaders and powers of the Great Houses. You may spend 1 Momentum to recognize any member of the ruling family of a noble House.",
    },
    "Triumph of Reason": {
        "category": "Mentat",
        "description": "You are aware that emotion is not always a logical response, and you can conquer it. If you are able to meditate for around twenty minutes, you may remove a single emotional trait you have, either permanently or for the next scene.",
    },
    "True Agenda": {
        "category": "Mentat",
        "description": "You are adept at collating what people say with their circumstances to gauge their true needs and desires. When a negotiation opponent makes their initial statements, you may Obtain Information about their true intentions and needs (regardless of what they actually say they need) once for no cost.",
    },
    
    # SPACING GUILD TALENTS
    "Failed Navigator": {
        "category": "Spacing Guild",
        "description": "You underwent trials to become a Guild Navigator, but you failed to meet the standards required… yet, for one brief moment, your consciousness became one with the universe. Whenever you spend a point of Determination, the gamemaster will grant you an additional insight.",
    },
    "Guildsman": {
        "category": "Spacing Guild",
        "description": "You have connections to the Spacing Guild, granting you more access to their resources than most. Once per adventure, you may call upon your Spacing Guild connection to use Guild facilities or resources, or to organize a meeting with important persons within the Guild.",
    },
    "Code of Secrecy": {
        "category": "Spacing Guild",
        "description": "The Spacing Guild takes its promise of client confidentiality seriously and enforces it through a regimen of indoctrination and mental conditioning in its key agents. Any attempt to get you to reveal confidential information about a client is one Difficulty level higher.",
    },
    "Guild Peace": {
        "category": "Spacing Guild",
        "description": "The neutrality of the Guild can be a powerful tool in the right hands. Some agents are good at reminding others that the Guild will not stand for violence. For the cost of 1 Momentum, you may add the trait 'Guild Peace' to a scene.",
    },
    "Guild Upbringing": {
        "category": "Spacing Guild",
        "description": "You were brought up on spacecraft, moving around the galaxy. Stepping aboard a spacecraft is like coming home to familiar ground. When you step aboard a Guild Heighliner, or leave a planetary atmosphere, you gain 1 Momentum.",
    },
    "Methodical Efficiency": {
        "category": "Spacing Guild",
        "description": "The Spacing Guild has the best auditors, bankers, and commerce experts in the Known Universe because of their mathematical ability and their training in methodical, well-tested analytical techniques. When making an Understand test that applies to finance, commerce, or bureaucracy, you may re-roll one of the d20s in your pool.",
    },
    "Minor Spice Mutation": {
        "category": "Spacing Guild",
        "description": "Though you were unable to complete the Navigator training, your early exposure to a hyper-rich spice-laden environment caused your body and consciousness to mutate enough to mark you as of the Guild. You gain the trait 'Mutated' that may not be removed to represent this minor deformity.",
    },
    "Nose for Cargo": {
        "category": "Spacing Guild",
        "description": "You have a knack for spotting irregularities in cargo holds or on manifests. Whenever you attempt a skill test to detect contraband or locate a specific item or substance in a collection of cargo, you reduce the Difficulty by 1, to a minimum of 0.",
    },
    "Play Both Ends Against the Middle": {
        "category": "Spacing Guild",
        "description": "The Spacing Guild is often compared to a parasite, as it has a reputation for carefully feeding off other entities instead of seeking leadership on its own. If you are involved as a neutral party in a conflict between two other parties, you may spend 4 Momentum (from the group pool) to gain 1 point of Determination.",
    },
    "Power of Neutrality": {
        "category": "Spacing Guild",
        "description": "Though the Spacing Guild has no troops, weapons, or other military power of its own, its carefully cultivated neutrality serves as a powerful safety net. If you are recognizably a Guild agent, enemies must spend 2 Momentum (or Threat) to attack you or move against you directly in a physical challenge.",
    },
    "Space Power": {
        "category": "Spacing Guild",
        "description": "You hold a position of respect and power within the Guild and may request its assistance in military matters. This talent adds access to a Guild-only asset, a Heighliner. You do not command it and cannot compel it to appear at will, but you have the means of requesting one.",
    },
    "Spacer": {
        "category": "Spacing Guild",
        "description": "You've grown up in space, and the tug of gravity hangs upon you like shackles when you're on a planetary surface. Once away from gravity's pull, you become yourself. While in zero-gravity or light-gravity environments, you may re-roll 1d20 for any Move test.",
    },
    "The Cylinder Must Get Through": {
        "category": "Spacing Guild",
        "description": "Spacing Guild couriers undergo a harsh program of indoctrination to ensure their accuracy, loyalty, and punctuality. When taking actions directly related to delivering a message you've been tasked with, you may re-roll a single d20 in your dice pool.",
    },
    "Check the Books": {
        "category": "Spacing Guild",
        "description": "You know all the secrets of 'creative accounting' and can spot when others are using them. When you are looking over financial records of any kind and spend a point of Momentum to Obtain Information, you may ask two questions for the first point of Momentum spent, rather than one.",
    },
    "Deep Pockets": {
        "category": "Spacing Guild",
        "description": "You can always lay your hands on extra solaris. Once per session you may create an asset of Wealth to use in trade deals or just make purchases. This temporary asset is lost at the end of the scene and cannot be made permanent.",
    },
    
    # SUK DOCTOR TALENTS
    "Adrenaline Shot": {
        "category": "Suk Doctor",
        "description": "You are adept at getting people back on their feet, even if you only make them forget their pain for a moment. By using an action, the character can remove the effects of any physical complication from a character who is in the same zone. This complication is not removed and returns at the end of the scene unless otherwise removed.",
    },
    "Combat Medic": {
        "category": "Suk Doctor",
        "description": "You are skilled at offering rapid medical attention, even during a battle. When an ally in combat has suffered points towards the requirement to defeat them, you may spend 1 point of Momentum to reduce that point total by 2 as an action.",
    },
    "Imperial Conditioning": {
        "category": "Suk Doctor",
        "description": "Through intense psychological conditioning, you cannot take a human life, or cause a human to come to harm. This is a necessary step, for those with power and status must be free of the fear that their physicians might be assassins. You cannot willingly inflict harm upon or kill a human being.",
    },
    "Bedside Manner": {
        "category": "Suk Doctor",
        "description": "The symbol of the Suk School and Imperial conditioning makes you innately trustworthy. When attempting to gain the trust of someone or ingratiate yourself with them, you may reduce the Difficulty of the test by 1.",
    },
    "Empathetic Diagnostics": {
        "category": "Suk Doctor",
        "description": "You need no medical devices to be able to diagnose an illness or medical issue. By using your sense of touch and intuition you can examine a patient and diagnose the problem without the need of medical scanners or lab equipment.",
    },
    "Improvised Medicine": {
        "category": "Suk Doctor",
        "description": "You need very little to create medicine or make improvised equipment to serve patients even in the most primitive conditions. You can create medicine from common household chemicals or natural flora and fauna to heal most afflictions or battlefield wounds, including the effects of poisons.",
    },
    
    # CHOAM TALENTS
    "Audit": {
        "category": "CHOAM",
        "description": "As an agent of CHOAM you have the right to check the accounts of those who trade with the organization. You may spend 1 Momentum to insist a House or other CHOAM trade member show you the records of their recent trade dealings.",
    },
    "Check the Books": {
        "category": "CHOAM",
        "description": "You know all the secrets of 'creative accounting' and can spot when others are using them. When you are looking over financial records of any kind and spend a point of Momentum to Obtain Information, you may ask two questions for the first point of Momentum spent, rather than one.",
    },
    "Deep Pockets": {
        "category": "CHOAM",
        "description": "You can always lay your hands on extra solaris. Once per session you may create an asset of Wealth to use in trade deals or just make purchases. This temporary asset is lost at the end of the scene and cannot be made permanent.",
    },
    "Dirty Money": {
        "category": "CHOAM",
        "description": "Every House has its secrets. You know where the real money has been earned and where it has gone. When facing any sort of challenge or test relating to concealing the source of wealth or any illegitimate financial transactions, with a successful Discipline test you may spend 1+ Momentum to transform one illegal asset into a legitimate and thoroughly legal asset.",
    },
    "Hand of CHOAM": {
        "category": "CHOAM",
        "description": "You can flex your influence over the trade affairs of the Imperium. When you are involved (acting or assisting) in a test dealing with planetary or galactic trade, you may use your influence as a member of CHOAM. Once per session on such a test you may apply the effects of spending a point of Determination on the Trade test.",
    },
    "Master of Coin": {
        "category": "CHOAM",
        "description": "You know how to wring every last solari out of a deal. Whenever making a financial- or economic-related skill test, you may re-roll 1d20 if it is not a success, specifically when dealing with circumstances when CHOAM's influence would be relevant.",
    },
    "Report Malfeasance": {
        "category": "CHOAM",
        "description": "You can make accusations of financial misdealing that will be taken seriously by CHOAM and investigated. You may at any time give another character the complication 'Reported to CHOAM'. This represents your having sent a report to CHOAM of illegal or unfair trading or financial affairs on the part of the target.",
    },
    
    # SARDAUKAR TALENTS
    "Blood Ritual": {
        "category": "Sardaukar",
        "description": "The blood of your enemies grants you power over them. To anoint yourself with their blood when you have defeated them will make you victorious in your next fight. If you spend an action to anoint yourself with the blood of an enemy you have killed in this scene, you gain 2 Momentum/Threat.",
    },
    "Fanatic Killer": {
        "category": "Sardaukar",
        "description": "Specializing in close-quarter combat, you are an astonishingly efficient killer. Even as you land mortal blows, you are pivoting into position to make your next strike. You gain 1 Momentum each time you attack a foe you have not yet engaged with in this scene.",
    },
    "Fearsome Spectacle": {
        "category": "Sardaukar",
        "description": "The tactics and strikes preferred by the Sardaukar are not merely efficient, they are calculated to sow terror among those who would stand against the will of the Emperor. If a Sardaukar defeats an enemy, the next attack action taken against that Sardaukar in the current scene automatically fails.",
    },
    "Hidden Blade": {
        "category": "Sardaukar",
        "description": "Sardaukar are never unarmed. Anything can be a weapon in their hands, no matter how small. You may spend an action to create a blade asset (for yourself only) in any circumstance, without the need for a test of Momentum/Threat spend.",
    },
    "Killer Reputation": {
        "category": "Sardaukar",
        "description": "Your Sardaukar reputation casts a long shadow over all the people of the Known Universe. Few are brave enough to take up arms against you or those under your protection. You may substitute your Battle skill in place of Communicate or Discipline when attempting to dissuade someone from making an attack on you or those under your immediate protection.",
    },
    "Loyal Unto Death": {
        "category": "Sardaukar",
        "description": "The Sardaukar do not accept defeat; even in death, they prevail. You are prepared to give up your own life at a moment's notice in order to thwart the enemies of the Emperor. If you are defeated in melee combat, you may make a single strike against your attacker to attempt to defeat them as well.",
    },
    "Military Counselor": {
        "category": "Sardaukar",
        "description": "The bashars and bursegs of the Sardaukar are peerless commanders. Having overseen multiple campaigns on behalf of the corps, they are veteran experts in virtually every type of combat known to humanity. If you (or those you advise) take the time to consider a plan of attack or defense in an upcoming Duel, Skirmish, or Warfare conflict, you may move one asset to an adjacent zone before the first round begins.",
    },
    "Sacrifice": {
        "category": "Sardaukar",
        "description": "As a Sardaukar, only you are worth sparing in any battle. The rest are simply pawns to be used to gain victory. By sacrificing them, you might gain advantage against your enemies. You may give any allied non-Sardaukar a 'Wounded' trait during a physical conflict to gain 2 Momentum/Threat.",
    },
    "Silent Attack": {
        "category": "Sardaukar",
        "description": "You move like the wind and strike in silence. Few enemies who fail to see you approach survive your first strike. If your target is unaware of you, then your initial attack dice pool is 3d20 rather than 2d20 for your first attack.",
    },
    "Strike From the Shadows": {
        "category": "Sardaukar",
        "description": "You are as silent as the night and adept at flanking your enemies and ambushing them. If you are making a stealth test with the express purpose of getting close to a target to make an attack, the Difficulty is reduced by 1.",
    },
    
    # FACE DANCER TALENTS
    "Copy": {
        "category": "Face Dancer",
        "description": "You are adept at memorizing the mannerisms and body language of a single target. In this way you can convincingly replicate them. If the Face Dancer is able to observe a target closely for a scene, they may make an Average (D1) Understand test to memorize their modes of speech and mannerisms.",
    },
    "Facedance": {
        "category": "Face Dancer",
        "description": "You were crafted by the Bene Tleilax before birth to be able to change your form and face. At the start of a scene, you may choose to alter your form. You may make yourself taller or shorter, heavier or thinner, alter your skin color, your apparent age, or even whether you appear to be masculine or feminine.",
    },
    "Innocent Form": {
        "category": "Face Dancer",
        "description": "You are able to make yourself look so average you fade into the background, or so innocent and naïve you can't be a threat or a suspect. You can take a form that is either unobtrusive or innocent looking (choose which upon taking the form).",
    },
    "Lightning Reflexes": {
        "category": "Face Dancer",
        "description": "Your command of your muscles is so powerful you can move like lightning. You may spend 1 Momentum to take your action first in any given round, regardless of the actual initiative order.",
    },
    "Lock Features": {
        "category": "Face Dancer",
        "description": "You have mastered a way to lock your muscles in one set form. You can maintain the last form you took, even when unconscious or dead. You do not revert to the 'formless' appearance of a Face Dancer.",
    },
    "Muscular Conditioning": {
        "category": "Face Dancer",
        "description": "You have absolute control over your body. Every muscle and every nerve is under your control. Whenever you attempt a Move or Discipline test which relies on your control of your body, you may re-roll a single d20.",
    },
    "The Right Moment": {
        "category": "Face Dancer",
        "description": "With your disguise skills and your ability to understand a target's body language, you are adept at getting closer to them than most people allow. If the Face Dancer is not under suspicion and is not considered a threat by anyone in the scene, they gain a bonus if they initiate a combat.",
    },
    "Unobtrusive Change": {
        "category": "Face Dancer",
        "description": "When in a crowd, you are adept at making subtle and quick changes in your appearance to make yourself hard to follow or spot. Trying to chase a Face Dancer with this Talent is one Difficulty level harder if they are in a reasonably crowded place.",
    },
    
    # SWORDMASTER TALENTS
    "Always Armed": {
        "category": "Swordmaster",
        "description": "Anything you hold can be a weapon. You can make any item you pick up deadly in your hands. If you are unarmed in a scene, you may create a Quality 0 melee weapon asset for free and with no test or action costs during any conflict.",
    },
    "Blur of Blades": {
        "category": "Swordmaster",
        "description": "You enter a fray with unbelievable speed, striking so quickly and decisively that your attacks seem to come from nowhere, and everywhere, at once. You are so adept at swordfighting and fencing that you can move your melee weapon (typically a sword) back and forth between guard zones — right or left — instantly.",
    },
    "Battle Perception": {
        "category": "Swordmaster",
        "description": "You have an almost psychic awareness of when a fight is imminent, even when you cannot see your opponent. You cannot be surprised or ambushed in combat. You always get an action on any round you are being attacked and suffer no penalty for being caught off guard.",
    },
    "Blademaster": {
        "category": "Swordmaster",
        "description": "You know how to get the best out of any weapon you use. Any melee weapon asset you use gains +1 Quality while it is in your hands. This bonus applies even if the weapon does not have a Quality bonus, but the Quality cannot be improved beyond 4.",
    },
    "Combat Meditation": {
        "category": "Swordmaster",
        "description": "Those facing you are at a disadvantage as your defenses and movement seem as reckless as your attacks are deadly. When in combat, you can instinctually move between the three stages of combat meditation — funestus, partus, and novellus — becoming a whirling and unpredictable engine of destructive force.",
    },
    "Lightning Strike": {
        "category": "Swordmaster",
        "description": "You are so attuned to combat, you know when an attack is imminent. Your blade is in your hand before your opponent has even thought to draw their own. If you are not surprised or being ambushed, you have a free action you may take on the first round of combat before anyone else.",
    },
    "Master of Battle": {
        "category": "Swordmaster",
        "description": "More than a mere duelist, the Swordmaster excels in all the arts of war, as adept at logistics as field repairs or piloting a grav tank. At the onset of any skirmish or warfare conflict, the Swordmaster may observe the situation, the intended foes, and the field where the conflict will occur.",
    },
    "Soul of a Swordmaster": {
        "category": "Swordmaster",
        "description": "The soul of a Swordmaster never dies but is instead reborn into the body of another worthy candidate. Your own spirit is that of a great Swordmaster of old, remembered by many, inspiring you from within. Note: This Talent is only available to full Swordmasters, official graduates of the Ginaz School.",
    },
    "Steel Focus": {
        "category": "Swordmaster",
        "description": "The moment a conflict begins, your training kicks in and your mind gains a razor-sharp focus. As soon as a physical conflict (Duel, Skirmish, or Warfare) begins, you gain a bonus point of Determination. This point is removed at the end of the conflict, whether it has been spent or not.",
    },
    "Weapon Focus": {
        "category": "Swordmaster",
        "description": "The Ginaz School relentlessly drilled you in swordfighting, from short-blades, rapiers, long-blades, and pulse-swords, to even the mighty two-handed blades favored in times gone by. When making an attack while using any sword in combat, you may substitute any one d20 in your dice pool for a result of 1, without rolling.",
    },
    
    # HOUSE JONGLEUR TALENTS
    "Project Emotion": {
        "category": "House Jongleur",
        "description": "By pitching your voice at just the right level, you can inspire a broad emotional state in an audience. This can only apply to simple emotions like sadness, happiness, or anger, and these feelings don't consume the audience. This ability gives, to anyone who can hear the Jongleur speak, an emotional trait of the Jongleur's choice for the remainder of the scene.",
    },
    "Targeted Emotion": {
        "category": "House Jongleur",
        "description": "Your skills to affect peoples' feelings can be focused to affect a single individual with a more-powerful emotion. This power can incite rage or love, pushing people to do things they might not otherwise consider. This ability only works on a single target who must be engaged in conversation with the Jongleur for a few minutes.",
    },
    
    # QIZARATE TALENT
    "Holy Presence of Muad'Dib": {
        "category": "General",
        "description": "You carry the authority and presence of the Qizarate, the religious bureaucracy of the Atreides Empire. Your words carry the weight of religious authority, and those who follow the teachings of Muad'Dib are more likely to listen to your guidance.",
    },
    
    # SPICE TALENTS (PHYSICAL)
    "Spice Lore": {
        "category": "Spice (Physical)",
        "description": "How good is the spice you're buying? How many times has it been refined? What's it worth? These are vital questions for anyone seeking to survive in the ruthless business of spice dealing. Whenever your character attempts an Understand test related to the spice melange, you may re-roll up to two d20s, once per scene.",
    },
    "Spice Refinement": {
        "category": "Spice (Physical)",
        "description": "The procedures used to harvest spice, process and purify it, and render it ready for the palates of the Imperial elite are closely guarded secrets. Your character understands the methods and techniques to harvest and refine spice. Whenever your character is attempting a task relating to the mechanics and logistics of spice production or refinement you gain one free d20 for your roll.",
    },
    "Improved Healing": {
        "category": "Spice (Physical)",
        "description": "Take spice into your system, and you suddenly feel tougher, more resilient, more able to withstand pain. This isn't simply the euphoria of a spice high, it is a genuine effect of the melange. Your character must be taking spice regularly to use this talent. This talent allows you once per scene to re-roll one d20 that results in a complication, if the potential complication is an injury.",
    },
    "Enhanced Lifespan": {
        "category": "Spice (Physical)",
        "description": "The geriatric qualities of the spice melange are well known, and widely sought after. These properties keep regular spice users alive for up to triple the expected lifespan of a human. Your character must be taking spice regularly to use this talent. As such, any complication or trait they have due to old age can be ignored at the cost of 1 Momentum.",
    },
    
    # SPICE TALENTS (MENTAL)
    "Foresight": {
        "category": "Spice (Mental)",
        "description": "The prescience granted to the Bene Gesserit by their use of spice derivatives is well known, but the use of high doses of spice can, sometimes, trigger visions of the future even in those who do not otherwise understand the full properties of melange. Using this talent requires your character to consume two spice assets. At the beginning of a scene, you may ask the gamemaster two questions about the nature of the scene about to play out.",
    },
    "Shortening the Way": {
        "category": "Spice (Mental)",
        "description": "The Guild utilize the spice to enable their Navigators to plot routes for space freighters, folding space without being ripped apart by the titanic stresses of the cosmos. On a smaller scale, spice can grant vital insight into the flow of movement in the universe. To use this talent, your character must consume one spice asset. For the remainder of the scene all Move tests they make are one step of Difficulty lower.",
    },
    "Voice of the Inner Dark": {
        "category": "Spice (Mental)",
        "description": "The process by which the venerable Bene Gesserit Sisterhood inducts its members into a full consciousness of their power is a painful process—often terminally so. Those who survive become Reverend Mothers. But some without training can gain a taste of this ability at great risk to themselves with enough spice. To use this talent, your character must consume one spice asset. Doing so unlocks some of the wisdom of their past memories to grant them clarity.",
    },
    
    # ADDITIONAL GENERAL TALENTS
    "Academic Excellence": {
        "category": "General",
        "description": "Years of diligent studying have made you proficient in all areas of academic performance. For any task requiring studying, it takes you only half the time to learn it, and the Difficulty is reduced by one for any test involving a task you can study for.",
    },
    "Cybernetic Surgeon": {
        "category": "General",
        "description": "You have been trained in the surgery and procedures to augment the human body with machine parts. Once per scene you can repair or fix any damaged cybernetics to full functionality. Additionally, in extended game time you can perform the surgery needed to implant cybernetics.",
    },
    "Medical Director": {
        "category": "General",
        "description": "You are an expert in dealing with large scale medical services. During a Warfare conflict where you serve as a medical director, you may restore one unit asset to the conflict at the cost of 1 Momentum.",
    },
    "Researcher": {
        "category": "General",
        "description": "You can use your extensive training in analysis to solve even the most complex problems. In any extended research task you perform, you may add +1 to the Quality of the asset you use for the duration of the test.",
    },
}


def get_talent(name):
    """Get a talent by name (case-insensitive)."""
    name_lower = name.lower()
    for key, talent in TALENTS.items():
        if key.lower() == name_lower:
            return talent
    return None


def get_talents_by_category(category):
    """Get all talents in a specific category."""
    return [name for name, talent in TALENTS.items() if talent.get("category") == category]


def get_talents_by_faction(faction_name):
    """Get all talents available to a specific faction."""
    faction_category_map = {
        "Bene Gesserit Sisterhood": "Bene Gesserit",
        "Fremen": "Fremen",
        "Mentat Academies": "Mentat",
        "Spacing Guild": "Spacing Guild",
        "Suk Doctors": "Suk Doctor",
        "CHOAM": "CHOAM",
        "Sardaukar Legions": "Sardaukar",
        "Tleilaxu Face Dancer": "Face Dancer",
        "Swordmasters of Ginaz": "Swordmaster",
        "House Jongleur": "House Jongleur",
    }
    
    category = faction_category_map.get(faction_name)
    if not category:
        return []
    
    return get_talents_by_category(category)


def can_character_take_talent(character, talent_name):
    """
    Check if a character can take a specific talent.
    
    Args:
        character: The character to check
        talent_name: Name of the talent
        
    Returns:
        tuple: (can_take: bool, reason: str)
    """
    talent = get_talent(talent_name)
    if not talent:
        return (False, f"Unknown talent: {talent_name}")
    
    category = talent.get("category", "General")
    
    # General talents are available to all
    if category == "General":
        return (True, "Available to all characters")
    
    # Spice talents are available to all (but require spice consumption)
    if "Spice" in category:
        return (True, "Available to all characters (requires spice consumption)")
    
    # Check faction-specific talents
    faction = character.db.faction
    if not faction:
        return (False, f"This talent is restricted to {category}. You must be a member of the appropriate faction.")
    
    faction_category_map = {
        "Bene Gesserit Sisterhood": "Bene Gesserit",
        "Fremen": "Fremen",
        "Mentat Academies": "Mentat",
        "Spacing Guild": "Spacing Guild",
        "Suk Doctors": "Suk Doctor",
        "CHOAM": "CHOAM",
        "Sardaukar Legions": "Sardaukar",
        "Tleilaxu Face Dancer": "Face Dancer",
        "Swordmasters of Ginaz": "Swordmaster",
        "House Jongleur": "House Jongleur",
    }
    
    required_category = faction_category_map.get(faction)
    if required_category != category:
        return (False, f"This talent is restricted to {category}. Your faction ({faction}) does not have access to this talent.")
    
    return (True, f"Available to {category}")


def get_all_talent_names():
    """Get a list of all talent names."""
    return sorted(TALENTS.keys())

