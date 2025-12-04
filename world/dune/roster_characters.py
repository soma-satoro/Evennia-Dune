"""
Roster Character Creation Script for Dune MUD

This script creates feature/roster characters set during the period after Paul's 
disappearance during the Great Jihad. Alia is Regent, the Imperial Seat is on 
Arrakis, and the twins Leto II and Ghanima are coming of age.

Timeline: Children of Dune era
- Alia Atreides: Regent of the Empire
- Jessica: Bene Gesserit Reverend Mother, still alive
- Duncan Idaho (Hayt): Ghola, resurrected by the Tleilaxu
- Irulan Corrino: Empress, historian and tutor
- Leto II and Ghanima: Pre-born twins, coming of age
- Stilgar: Fremen Naib, guardian to the twins
- Gurney Halleck: Warmaster of House Atreides

To use this script:
1. From in-game as a superuser: @py world.dune.roster_characters.create_all_roster()
2. Or create individual characters: @py world.dune.roster_characters.create_alia()
"""

from evennia import create_object, search_object
from typeclasses.characters import Character


def get_or_create_character(name, typeclass="typeclasses.characters.Character"):
    """
    Get existing character or create new one.
    
    Args:
        name (str): Character name
        typeclass (str): Typeclass path
        
    Returns:
        Character: The character object
    """
    char = search_object(name, typeclass=typeclass)
    if char:
        print(f"Character {name} already exists. Updating stats...")
        return char[0]
    else:
        char = create_object(typeclass, key=name)
        print(f"Created new character: {name}")
        return char


def create_alia():
    """
    ALIA ATREIDES
    Regent of the Imperium
    
    The sister of Paul Muad'Dib, Alia was born "pre-born" with full consciousness
    and ancestral memories due to her mother's spice agony during pregnancy. As
    Regent, she rules the Empire with an iron fist but struggles against the 
    influence of her ancestral memories, particularly the voice of her grandfather,
    Baron Vladimir Harkonnen. She possesses incredible Bene Gesserit powers and
    is both feared and respected throughout the Imperium.
    """
    char = get_or_create_character("Alia Atreides")
    
    # Basic information
    char.db.house = "Atreides"
    char.db.role = "Regent"
    char.db.title = "imperial_regent"  # Custom title
    char.db.gender = "feminine"
    char.db.caste = "Noble"
    
    # Background and personality
    char.db.background = """Born as a pre-born with full ancestral memories, Alia Atreides 
became Regent of the Imperium after her brother Paul's disappearance into the desert. She 
rules from Arrakeen with absolute authority, wielding both political power and terrifying 
Bene Gesserit abilities. However, she wages a constant internal battle against possession 
by her ancestral memories, particularly the insidious voice of Baron Vladimir Harkonnen."""
    
    char.db.personality_traits = """Authoritative, intelligent, and charismatic, but increasingly 
erratic and volatile. She displays flashes of the Harkonnen cruelty she inherited through 
genetic memory. Fiercely protective of her family's legacy while simultaneously struggling 
with her own identity."""
    
    char.db.ambition = "Maintain control of the Empire and resist ancestral possession"
    
    char.db.appearance = """A striking woman in her twenties with the dark hair and green eyes 
of House Atreides. She moves with predatory grace and her gaze seems to look through people. 
She typically wears elaborate robes befitting her station as Regent."""
    
    char.db.reputation_trait = "The Pre-Born Regent"
    
    # Skills (Dune 2d20: Battle, Communicate, Discipline, Move, Understand)
    # Highly skilled, as befitting a major character
    char.set_skill("battle", 4)  # Trained in combat, has ancestral memories
    char.set_skill("communicate", 5)  # Master of Voice and manipulation
    char.set_skill("discipline", 5)  # Immense mental power (though threatened by possession)
    char.set_skill("move", 3)  # Agile and trained
    char.set_skill("understand", 5)  # Pre-born wisdom and ancestral knowledge
    
    # Focuses
    char.db.stats["focuses"] = [
        "Battle: Knife Fighting",
        "Communicate: Voice",
        "Communicate: Intimidation", 
        "Discipline: Bene Gesserit Training",
        "Discipline: Ancestral Memories",
        "Understand: Politics",
        "Understand: Spice Knowledge"
    ]
    
    # Talents (Bene Gesserit abilities and pre-born powers)
    char.db.stats["talents"] = [
        "Bene Gesserit Training",
        "Voice",
        "Prana-Bindu Control",
        "Pre-Born",
        "Reverend Mother Abilities",
        "Mentat-like Computation (ancestral)",
        "Prescient Flashes"
    ]
    
    # Drives (ratings must be 8, 7, 6, 5, 4)
    char.set_drive_rating("power", 8)
    char.set_drive_statement("power", "I will maintain absolute control over the Empire and prove I am worthy of the Atreides legacy")
    
    char.set_drive_rating("duty", 7)
    char.set_drive_statement("duty", "As Regent, I must protect the realm and guide my nephew and niece toward their destiny")
    
    char.set_drive_rating("justice", 6)
    char.set_drive_statement("justice", "I will root out corruption and those who would threaten House Atreides")
    
    char.set_drive_rating("faith", 5)
    
    char.set_drive_rating("truth", 4)
    
    # Resources
    char.db.stress = 0
    char.db.max_stress = 10
    char.db.determination = 3
    
    # Languages
    char.db.languages = ["The Truth", "Fremen Chakobsa", "Galach", "Bene Gesserit Battle Language"]
    char.db.speaking_language = "Galach"
    
    # Relationships
    char.db.relationships = """Sister of Paul Muad'Dib (missing). Aunt to Leto II and Ghanima. 
Daughter of Lady Jessica and Duke Leto. Wife to Duncan Idaho (Hayt). Complex relationship with 
Irulan Corrino."""
    
    print(f"✓ Created Alia Atreides - Regent of the Imperium")
    return char


def create_leto_ii():
    """
    LETO II ATREIDES
    Heir to the Empire
    
    Son of Paul Muad'Dib and Chani, Leto II is a pre-born with full access to 
    ancestral memories from birth. As he comes of age, he begins to see the Golden 
    Path - a terrible future that will ensure humanity's survival but at great cost. 
    He stands at the precipice of a transformation that will make him something more 
    than human.
    """
    char = get_or_create_character("Leto II Atreides")
    
    # Basic information
    char.db.house = "Atreides"
    char.db.role = "Heir"
    char.db.title = "ducal_heir"
    char.db.gender = "masculine"
    char.db.caste = "Noble"
    
    # Background and personality
    char.db.background = """Son of Paul Muad'Dib and Chani, Leto II was born pre-born with 
access to the memories of all his ancestors. Coming of age under the regency of his aunt Alia, 
he has begun to see the Golden Path - a future that requires terrible sacrifice. He stands at 
a crossroads: accept his humanity and a normal life, or embrace a transformation that will make 
him the immortal God Emperor for thousands of years."""
    
    char.db.personality_traits = """Introspective, profoundly wise beyond his years, yet still 
retains flashes of youthful curiosity and emotion. He bears the weight of prescient knowledge 
with grim determination. More willing than his father to pay the terrible price the future demands."""
    
    char.db.ambition = "Follow the Golden Path to ensure humanity's survival, no matter the personal cost"
    
    char.db.appearance = """A teenager with the striking features of House Atreides - dark hair 
and those distinctive green eyes. He has the desert-hardened physique of someone raised among the 
Fremen. When he gazes into the distance, it's as if he's looking through time itself."""
    
    char.db.reputation_trait = "The Pre-Born Heir"
    
    # Skills (High potential but still coming of age)
    char.set_skill("battle", 3)  # Well-trained, Fremen combat skills
    char.set_skill("communicate", 4)  # Natural leader
    char.set_skill("discipline", 5)  # Exceptional mental control
    char.set_skill("move", 4)  # Desert-trained
    char.set_skill("understand", 5)  # Pre-born wisdom and prescience
    
    # Focuses
    char.db.stats["focuses"] = [
        "Battle: Crysknife",
        "Communicate: Leadership",
        "Discipline: Ancestral Memories",
        "Discipline: Prescience",
        "Move: Desert Survival",
        "Understand: Ecology",
        "Understand: Imperial Politics"
    ]
    
    # Talents
    char.db.stats["talents"] = [
        "Pre-Born",
        "Fremen Training",
        "Prescient Visions",
        "Ancestral Wisdom",
        "Voice (learned)",
        "Desert Survival Expert"
    ]
    
    # Drives
    char.set_drive_rating("duty", 8)
    char.set_drive_statement("duty", "I must walk the Golden Path to save humanity from stagnation and extinction")
    
    char.set_drive_rating("truth", 7)
    char.set_drive_statement("truth", "I will see beyond what others can see and understand the terrible necessities of the future")
    
    char.set_drive_rating("justice", 6)
    char.set_drive_statement("justice", "I will ensure that humanity's future is secured, even if the present must suffer")
    
    char.set_drive_rating("power", 5)
    
    char.set_drive_rating("faith", 4)
    
    # Resources
    char.db.stress = 0
    char.db.max_stress = 10
    char.db.determination = 3
    
    # Languages
    char.db.languages = ["Fremen Chakobsa", "Galach", "The Truth"]
    char.db.speaking_language = "Chakobsa"
    
    # Relationships
    char.db.relationships = """Son of Paul Muad'Dib (missing) and Chani (deceased). Twin brother of 
Ghanima. Nephew of Alia Atreides. Grandson of Lady Jessica. Ward of Stilgar. Student of Irulan."""
    
    print(f"✓ Created Leto II Atreides - Heir to the Empire")
    return char


def create_ghanima():
    """
    GHANIMA ATREIDES
    The Wise Twin
    
    Twin sister of Leto II, Ghanima is also pre-born with full ancestral memories.
    She serves as a balance to her brother, sharing his burdens while maintaining 
    her own identity. Strong-willed and perceptive, she understands her brother's 
    terrible destiny and supports him even as she fears for what he must become.
    """
    char = get_or_create_character("Ghanima Atreides")
    
    # Basic information
    char.db.house = "Atreides"
    char.db.role = "Heir"  # Also an heir
    char.db.title = "ducal_heir"
    char.db.gender = "feminine"
    char.db.caste = "Noble"
    
    # Background and personality
    char.db.background = """Daughter of Paul Muad'Dib and Chani, Ghanima was born pre-born like 
her twin brother Leto II. Raised among the Fremen at Sietch Tabr, she combines desert wisdom 
with ancestral knowledge. She shares a deep psychic bond with her brother and understands the 
terrible burden of the Golden Path, providing him emotional support and wisdom."""
    
    char.db.personality_traits = """Strong-willed, perceptive, and deeply compassionate despite 
her ancestral memories. She possesses a sharp wit and often serves as the voice of reason. More 
emotionally expressive than her brother, but equally burdened by prescient knowledge."""
    
    char.db.ambition = "Protect my brother and help guide humanity's future while maintaining my own identity"
    
    char.db.appearance = """A striking teenage girl with the classic Atreides features - dark 
hair and penetrating green eyes. She moves with the fluid grace of a trained Fremen, comfortable 
in stillsuit or formal robes. Her gaze carries ancient wisdom."""
    
    char.db.reputation_trait = "The Wise Twin"
    
    # Skills (Parallel to her brother but with different focus)
    char.set_skill("battle", 3)  # Fremen combat training
    char.set_skill("communicate", 5)  # Exceptional at reading and influencing people
    char.set_skill("discipline", 5)  # Strong mental defenses
    char.set_skill("move", 4)  # Desert-trained
    char.set_skill("understand", 4)  # Wise beyond her years
    
    # Focuses
    char.db.stats["focuses"] = [
        "Battle: Crysknife",
        "Communicate: Empathy",
        "Communicate: Voice",
        "Discipline: Ancestral Memories",
        "Discipline: Mental Barriers",
        "Move: Desert Survival",
        "Understand: Human Nature"
    ]
    
    # Talents
    char.db.stats["talents"] = [
        "Pre-Born",
        "Fremen Training",
        "Prescient Awareness",
        "Ancestral Wisdom",
        "Voice",
        "Desert Survival Expert",
        "Psychic Bond with Twin"
    ]
    
    # Drives
    char.set_drive_rating("duty", 8)
    char.set_drive_statement("duty", "I must support my brother in his terrible task and help preserve what's human in him")
    
    char.set_drive_rating("justice", 7)
    char.set_drive_statement("justice", "I will ensure that in saving humanity, we do not lose our own humanity")
    
    char.set_drive_rating("faith", 6)
    char.set_drive_statement("faith", "I believe in the essential goodness of humanity and the value of individual choice")
    
    char.set_drive_rating("power", 5)
    
    char.set_drive_rating("truth", 4)
    
    # Resources
    char.db.stress = 0
    char.db.max_stress = 10
    char.db.determination = 3
    
    # Languages
    char.db.languages = ["Fremen Chakobsa", "Galach", "The Truth", "Bene Gesserit Battle Language"]
    char.db.speaking_language = "Chakobsa"
    
    # Relationships
    char.db.relationships = """Daughter of Paul Muad'Dib (missing) and Chani (deceased). Twin sister 
of Leto II. Niece of Alia Atreides. Granddaughter of Lady Jessica. Ward of Stilgar. Student of Irulan."""
    
    print(f"✓ Created Ghanima Atreides - The Wise Twin")
    return char


def create_duncan_idaho():
    """
    DUNCAN IDAHO (HAYT)
    Ghola Swordmaster
    
    The legendary Swordmaster of House Atreides, killed during the Harkonnen attack 
    on Arrakis, Duncan Idaho was resurrected by the Tleilaxu as a ghola named Hayt. 
    He has regained most of his original memories and serves House Atreides once more, 
    though he is troubled by his death and resurrection. He is now married to Alia, 
    adding complexity to his loyalties.
    """
    char = get_or_create_character("Duncan Idaho")
    
    # Basic information
    char.db.house = "Atreides"
    char.db.role = "Swordmaster"
    char.db.title = "swordmaster"
    char.db.gender = "masculine"
    char.db.caste = "Retainer"
    
    # Background and personality
    char.db.background = """The legendary Swordmaster of House Atreides, Duncan Idaho died 
defending Paul during the Harkonnen attack. Resurrected by the Tleilaxu as a ghola called Hayt, 
he recovered his original memories and returned to Atreides service. Now married to Alia, he 
struggles with questions of identity, mortality, and loyalty while serving as one of the greatest 
warriors in the Imperium."""
    
    char.db.personality_traits = """Intensely loyal to House Atreides, but troubled by his 
resurrection and the philosophical questions it raises. Stoic and disciplined, with flashes of 
the old warmth and humor. Deeply concerned about Alia's growing instability."""
    
    char.db.ambition = "Serve House Atreides faithfully and protect Alia from the darkness consuming her"
    
    char.db.appearance = """A tall, powerful man in his prime with dark curling hair and 
penetrating blue-within-blue eyes of spice addiction. He moves with the deadly grace of a 
master swordsman. Bears himself with the dignity of House Atreides but with an undercurrent 
of existential unease."""
    
    char.db.reputation_trait = "The Resurrected Swordmaster"
    
    # Skills (Master combatant)
    char.set_skill("battle", 5)  # Legendary swordmaster
    char.set_skill("communicate", 3)  # Competent but not his focus
    char.set_skill("discipline", 4)  # Strong mental discipline
    char.set_skill("move", 5)  # Peak physical conditioning
    char.set_skill("understand", 3)  # Practical wisdom
    
    # Focuses
    char.db.stats["focuses"] = [
        "Battle: Long Blade",
        "Battle: Short Blade",
        "Battle: Shield Fighting",
        "Battle: Multiple Opponents",
        "Discipline: Mentat Training (Tleilaxu gift)",
        "Discipline: Combat Focus",
        "Move: Acrobatics",
        "Move: Infiltration"
    ]
    
    # Talents
    char.db.stats["talents"] = [
        "Master Swordsman",
        "Ginaz Training",
        "Shield Fighter",
        "Tleilaxu Enhancement",
        "Mentat-like Computation (ghola gift)",
        "Martial Reflexes",
        "Combat Awareness"
    ]
    
    # Drives
    char.set_drive_rating("duty", 8)
    char.set_drive_statement("duty", "I am sworn to House Atreides and will protect them with my life - again and again if needed")
    
    char.set_drive_rating("justice", 7)
    char.set_drive_statement("justice", "I will defend the innocent and punish those who betray honor")
    
    char.set_drive_rating("power", 6)
    char.set_drive_statement("power", "I seek to master my own fate and prove I am more than a manufactured copy")
    
    char.set_drive_rating("truth", 5)
    
    char.set_drive_rating("faith", 4)
    
    # Resources
    char.db.stress = 0
    char.db.max_stress = 10
    char.db.determination = 3
    
    # Languages
    char.db.languages = ["Galach", "Chakobsa", "The Truth"]
    char.db.speaking_language = "Galach"
    
    # Relationships
    char.db.relationships = """Husband of Alia Atreides (Regent). Legendary retainer of House 
Atreides. Mentor figure to Leto II and Ghanima. Loyally served Duke Leto (deceased) and Paul 
Muad'Dib (missing). Resurrected by Tleilaxu."""
    
    print(f"✓ Created Duncan Idaho (Hayt) - Ghola Swordmaster")
    return char


def create_irulan():
    """
    PRINCESS IRULAN CORRINO
    Empress and Historian
    
    Daughter of the deposed Emperor Shaddam IV, Irulan was married to Paul Atreides 
    for political purposes. Though the marriage was loveless, she has found purpose 
    as historian of the Muad'Dib legacy and tutor to the twins. A Bene Gesserit with 
    exceptional education and diplomatic skills, she navigates a complex position 
    between her Corrino heritage and Atreides present.
    """
    char = get_or_create_character("Irulan Corrino")
    
    # Basic information
    char.db.house = "Atreides"  # Now by marriage, though born Corrino
    char.db.role = "Consort"
    char.db.title = "empress"
    char.db.gender = "feminine"
    char.db.caste = "Noble"
    
    # Background and personality
    char.db.background = """Eldest daughter of Emperor Shaddam IV, Irulan received the finest 
education in the Imperium and was trained by the Bene Gesserit. Married to Paul Atreides in a 
political union, she was denied children but found purpose as historian and chronicler of the 
Muad'Dib legend. After Paul's disappearance, she serves as tutor to Leto II and Ghanima, seeking 
redemption for past conspiracies against Paul."""
    
    char.db.personality_traits = """Intelligent, cultured, and diplomatic. Haunted by regret over 
past actions and her loveless marriage. She possesses deep compassion masked by imperial dignity. 
Excellent teacher and historian with a gift for seeing patterns in history."""
    
    char.db.ambition = "Redeem myself by serving the Atreides children and preserving the true history of this era"
    
    char.db.appearance = """A statuesque woman in her thirties with the refined beauty of House 
Corrino. Her bearing is regal despite her house's fall from power. She dresses in elegant robes 
that balance Atreides green with hints of Corrino gold. Her eyes reflect both intelligence and 
deep sadness."""
    
    char.db.reputation_trait = "The Historian Empress"
    
    # Skills (Scholar and diplomat more than warrior)
    char.set_skill("battle", 2)  # Basic self-defense
    char.set_skill("communicate", 5)  # Master diplomat and teacher
    char.set_skill("discipline", 4)  # Bene Gesserit training
    char.set_skill("move", 2)  # Adequate but not exceptional
    char.set_skill("understand", 5)  # Brilliant scholar and historian
    
    # Focuses
    char.db.stats["focuses"] = [
        "Communicate: Diplomacy",
        "Communicate: Teaching",
        "Communicate: Voice",
        "Discipline: Bene Gesserit Training",
        "Understand: History",
        "Understand: Politics",
        "Understand: Imperial Protocol",
        "Understand: Writing"
    ]
    
    # Talents
    char.db.stats["talents"] = [
        "Bene Gesserit Training",
        "Voice",
        "Master Historian",
        "Imperial Education",
        "Diplomatic Immunity (status)",
        "Truthsayer Training",
        "Scholar"
    ]
    
    # Drives
    char.set_drive_rating("truth", 8)
    char.set_drive_statement("truth", "I will record the true history of this age, free from propaganda and myth")
    
    char.set_drive_rating("duty", 7)
    char.set_drive_statement("duty", "I must guide Leto and Ghanima to rule wisely and redeem my past failures")
    
    char.set_drive_rating("justice", 6)
    char.set_drive_statement("justice", "I seek to atone for my house's crimes and my own conspiracies against Paul")
    
    char.set_drive_rating("power", 5)
    
    char.set_drive_rating("faith", 4)
    
    # Resources
    char.db.stress = 0
    char.db.max_stress = 10
    char.db.determination = 3
    
    # Languages
    char.db.languages = ["Galach", "The Truth", "Bene Gesserit Battle Language", "Ancient Imperial Tongues"]
    char.db.speaking_language = "Galach"
    
    # Relationships
    char.db.relationships = """Widow of Paul Atreides (missing). Daughter of deposed Emperor 
Shaddam IV. Tutor to Leto II and Ghanima. Trained by Bene Gesserit. Complex relationship with 
Alia (political tensions). Sister to Wensicia Corrino."""
    
    print(f"✓ Created Irulan Corrino - Empress and Historian")
    return char


def create_jessica():
    """
    LADY JESSICA
    Bene Gesserit Reverend Mother
    
    Mother of Paul and Alia, concubine of the late Duke Leto, Jessica is a full 
    Bene Gesserit Reverend Mother who famously defied the Sisterhood by bearing a 
    son. Now returned to Arrakis, she watches with concern as her daughter rules 
    as Regent while battling possession by ancestral memories - the very danger 
    Jessica's disobedience helped create.
    """
    char = get_or_create_character("Lady Jessica")
    
    # Basic information
    char.db.house = "Atreides"
    char.db.role = "Advisor"  # Semi-retired but influential
    char.db.title = "reverend_mother"
    char.db.gender = "feminine"
    char.db.caste = "Noble"  # Elevated from concubine status
    
    # Background and personality
    char.db.background = """Once concubine to Duke Leto Atreides, Jessica is a Bene Gesserit 
Reverend Mother who defied the Sisterhood by bearing a son instead of a daughter. Mother to 
Paul Muad'Dib and Alia, grandmother to Leto II and Ghanima, she carries the weight of seeing 
her choices ripple across the Imperium. Returned to Arrakis to guide her grandchildren and 
attempt to save her daughter from possession."""
    
    char.db.personality_traits = """Wise, calculating, and deeply maternal despite her Bene 
Gesserit training. Carries profound guilt over Alia's pre-born condition. She balances love for 
her family with cold practicality when needed. Master of Voice and Bene Gesserit arts."""
    
    char.db.ambition = "Protect my grandchildren and save Alia from the darkness consuming her"
    
    char.db.appearance = """A woman in her sixties who appears far younger due to Bene Gesserit 
training. She carries herself with the grace and authority of both a Reverend Mother and former 
ducal concubine. Her green Atreides eyes miss nothing, and her presence commands respect."""
    
    char.db.reputation_trait = "The Reverend Mother of Atreides"
    
    # Skills (Bene Gesserit master)
    char.set_skill("battle", 3)  # Bene Gesserit combat training
    char.set_skill("communicate", 5)  # Master of Voice and manipulation
    char.set_skill("discipline", 5)  # Reverend Mother mental powers
    char.set_skill("move", 3)  # Bene Gesserit movement arts
    char.set_skill("understand", 5)  # Deep wisdom and knowledge
    
    # Focuses
    char.db.stats["focuses"] = [
        "Battle: Bene Gesserit Fighting",
        "Communicate: Voice",
        "Communicate: Manipulation",
        "Discipline: Bene Gesserit Training",
        "Discipline: Truthsaying",
        "Discipline: Other Memory",
        "Understand: Politics",
        "Understand: Bene Gesserit Lore"
    ]
    
    # Talents
    char.db.stats["talents"] = [
        "Bene Gesserit Training",
        "Reverend Mother",
        "Voice",
        "Prana-Bindu Control",
        "Truthsayer",
        "Other Memory",
        "Weirding Way Combat",
        "Water of Life Survived"
    ]
    
    # Drives
    char.set_drive_rating("duty", 8)
    char.set_drive_statement("duty", "I must protect my grandchildren and guide them toward a future free from my mistakes")
    
    char.set_drive_rating("faith", 7)
    char.set_drive_statement("faith", "I believe in the Bene Gesserit way, even as I defy the Sisterhood for my family")
    
    char.set_drive_rating("truth", 6)
    char.set_drive_statement("truth", "I will face the consequences of my choices and see clearly through deception")
    
    char.set_drive_rating("power", 5)
    
    char.set_drive_rating("justice", 4)
    
    # Resources
    char.db.stress = 0
    char.db.max_stress = 10
    char.db.determination = 3
    
    # Languages
    char.db.languages = ["Galach", "The Truth", "Bene Gesserit Battle Language", "Chakobsa", "Ancient Tongues"]
    char.db.speaking_language = "Galach"
    
    # Relationships
    char.db.relationships = """Mother of Paul Atreides (missing) and Alia Atreides (Regent). 
Concubine of Duke Leto (deceased). Grandmother of Leto II and Ghanima. Bene Gesserit Reverend 
Mother. Daughter of Baron Harkonnen (secret)."""
    
    print(f"✓ Created Lady Jessica - Bene Gesserit Reverend Mother")
    return char


def create_stilgar():
    """
    STILGAR
    Fremen Naib
    
    Leader of Sietch Tabr and one of the first Fremen to follow Paul Muad'Dib, 
    Stilgar is the guardian and mentor to Leto II and Ghanima. A traditionalist 
    who reveres Paul as a prophet, he struggles to balance Fremen values with 
    the changes sweeping across Arrakis under Imperial rule.
    """
    char = get_or_create_character("Stilgar")
    
    # Basic information
    char.db.house = "Atreides"  # Sworn to Atreides
    char.db.role = "Marshal"  # Military leader
    char.db.title = "naib"
    char.db.gender = "masculine"
    char.db.caste = "Fremen"
    
    # Background and personality
    char.db.background = """Naib of Sietch Tabr and among the first Fremen to recognize Paul 
Muad'Dib's potential, Stilgar has served House Atreides faithfully through the Jihad and beyond. 
Now he serves as guardian to Paul's children, teaching them the old ways while watching his people 
transform from desert warriors to Imperial citizens. He reveres Paul as the prophet but worries 
about what the future holds."""
    
    char.db.personality_traits = """Traditional, honorable, and deeply religious in his belief in 
Muad'Dib's prophecy. Loyal to the bone but increasingly troubled by the changes to Fremen culture. 
He is pragmatic when needed but holds firm to the old ways. Gruff exterior hides deep affection 
for those under his care."""
    
    char.db.ambition = "Preserve Fremen traditions while serving House Atreides and protecting the twins"
    
    char.db.appearance = """A weathered Fremen warrior in his fifties with the distinctive 
blue-within-blue eyes of spice addiction. His face bears the lines of a lifetime in the desert. 
He wears traditional Fremen robes and carries himself with the quiet authority of a naib."""
    
    char.db.reputation_trait = "The Guardian Naib"
    
    # Skills (Desert warrior)
    char.set_skill("battle", 5)  # Master Fremen warrior
    char.set_skill("communicate", 3)  # Blunt but effective leader
    char.set_skill("discipline", 4)  # Desert-hardened will
    char.set_skill("move", 4)  # Desert movement master
    char.set_skill("understand", 3)  # Fremen wisdom
    
    # Focuses
    char.db.stats["focuses"] = [
        "Battle: Crysknife",
        "Battle: Maula Pistol",
        "Battle: Desert Warfare",
        "Communicate: Leadership",
        "Discipline: Pain Resistance",
        "Move: Desert Survival",
        "Move: Sandwalking",
        "Understand: Fremen Lore"
    ]
    
    # Talents
    char.db.stats["talents"] = [
        "Fremen Warrior",
        "Desert Survival Expert",
        "Naib Authority",
        "Crysknife Master",
        "Water Discipline",
        "Sandworm Rider",
        "Fedaykin Veteran"
    ]
    
    # Drives
    char.set_drive_rating("duty", 8)
    char.set_drive_statement("duty", "I am sworn to protect Paul's children and guide them in the ways of the desert")
    
    char.set_drive_rating("faith", 7)
    char.set_drive_statement("faith", "I believe in Muad'Dib's prophecy and the destiny of his line")
    
    char.set_drive_rating("justice", 6)
    char.set_drive_statement("justice", "I will uphold Fremen law and tradition in a changing world")
    
    char.set_drive_rating("power", 5)
    
    char.set_drive_rating("truth", 4)
    
    # Resources
    char.db.stress = 0
    char.db.max_stress = 10
    char.db.determination = 3
    
    # Languages
    char.db.languages = ["Fremen Chakobsa", "Galach"]
    char.db.speaking_language = "Chakobsa"
    
    # Relationships
    char.db.relationships = """Guardian to Leto II and Ghanima. Naib of Sietch Tabr. Faithful 
follower of Paul Muad'Dib (missing). Respected by Alia Atreides. Ally of Duncan Idaho and 
Lady Jessica. Uncle-figure to the twins."""
    
    print(f"✓ Created Stilgar - Fremen Naib")
    return char


def create_gurney_halleck():
    """
    GURNEY HALLECK
    Warmaster of House Atreides
    
    The veteran warrior, musician, and troubadour who has served House Atreides 
    for decades. Scarred by Harkonnen torture, he survived the fall of House 
    Atreides and fought his way back to Paul's side. Now serves as Warmaster, 
    commanding Atreides forces across the Imperium while struggling with the 
    violence of the Jihad he helped enable.
    """
    char = get_or_create_character("Gurney Halleck")
    
    # Basic information
    char.db.house = "Atreides"
    char.db.role = "Warmaster"
    char.db.title = "warmaster"
    char.db.gender = "masculine"
    char.db.caste = "Retainer"
    
    # Background and personality
    char.db.background = """Veteran warrior and troubadour, Gurney Halleck has served House 
Atreides since Duke Leto freed him from Harkonnen slavery. He survived the fall of Arrakis, 
years as a smuggler, and fought in Paul's Jihad across the stars. Now Warmaster of Atreides 
forces, he commands armies while remaining loyal to the ideals of the old Duke. He carries the 
scars of Harkonnen torture and the weight of the Jihad's violence."""
    
    char.db.personality_traits = """Gruff, cynical, but with a deep romantic soul that finds 
expression in music and poetry. Absolutely loyal to House Atreides. Quick to violence when needed 
but haunted by the cost of the Jihad. Mentor figure who balances harsh training with genuine care."""
    
    char.db.ambition = "Serve House Atreides faithfully while preserving some humanity in an age of holy war"
    
    char.db.appearance = """A scarred, weathered man in his fifties with an inkvine scar running 
down his jaw - a memento of Harkonnen torture. Despite his rough appearance, his eyes show both 
intelligence and deep feeling. Often carries a baliset and moves with the controlled economy of 
a master warrior."""
    
    char.db.reputation_trait = "The Troubadour Warrior"
    
    # Skills (Master warrior and strategist)
    char.set_skill("battle", 5)  # Legendary warrior and tactician
    char.set_skill("communicate", 3)  # Effective but rough-edged
    char.set_skill("discipline", 4)  # Hardened by decades of war
    char.set_skill("move", 3)  # Aging but still capable
    char.set_skill("understand", 3)  # Practical wisdom and tactics
    
    # Focuses
    char.db.stats["focuses"] = [
        "Battle: Long Blade",
        "Battle: Shield Fighting",
        "Battle: Military Tactics",
        "Battle: Small Unit Tactics",
        "Communicate: Inspiration",
        "Discipline: Pain Resistance",
        "Understand: Military Strategy",
        "Understand: Music (baliset)"
    ]
    
    # Talents
    char.db.stats["talents"] = [
        "Master Warrior",
        "Military Genius",
        "Troubadour",
        "Veteran of Many Wars",
        "Shield Master",
        "Inspirational Leader",
        "Torture Survivor (mental resilience)"
    ]
    
    # Drives
    char.set_drive_rating("duty", 8)
    char.set_drive_statement("duty", "I serve House Atreides unto death, as I swore to Duke Leto")
    
    char.set_drive_rating("justice", 7)
    char.set_drive_statement("justice", "I will see the Harkonnens and all tyrants brought to account for their crimes")
    
    char.set_drive_rating("faith", 6)
    char.set_drive_statement("faith", "I believe in the old Duke's vision of just rule, even in this age of holy war")
    
    char.set_drive_rating("power", 5)
    
    char.set_drive_rating("truth", 4)
    
    # Resources
    char.db.stress = 0
    char.db.max_stress = 10
    char.db.determination = 3
    
    # Languages
    char.db.languages = ["Galach", "Chakobsa", "Various military dialects"]
    char.db.speaking_language = "Galach"
    
    # Relationships
    char.db.relationships = """Warmaster of House Atreides. Served Duke Leto (deceased) and 
Paul Muad'Dib (missing). Comrade of Duncan Idaho. Respected by Alia (Regent). Friend to Lady 
Jessica. Mentor to younger Atreides soldiers. Former Harkonnen slave."""
    
    print(f"✓ Created Gurney Halleck - Warmaster of House Atreides")
    return char


def create_all_roster():
    """
    Create all roster characters in one batch.
    
    Returns:
        dict: Dictionary of character names to character objects
    """
    print("\n" + "="*70)
    print("CREATING ROSTER CHARACTERS FOR CHILDREN OF DUNE ERA")
    print("="*70 + "\n")
    
    characters = {}
    
    try:
        characters["Alia Atreides"] = create_alia()
        characters["Leto II Atreides"] = create_leto_ii()
        characters["Ghanima Atreides"] = create_ghanima()
        characters["Duncan Idaho"] = create_duncan_idaho()
        characters["Irulan Corrino"] = create_irulan()
        characters["Lady Jessica"] = create_jessica()
        characters["Stilgar"] = create_stilgar()
        characters["Gurney Halleck"] = create_gurney_halleck()
        
        print("\n" + "="*70)
        print(f"SUCCESS: Created {len(characters)} roster characters!")
        print("="*70)
        print("\nCharacters created:")
        for name in characters.keys():
            print(f"  - {name}")
        print("\nUse +sheet <character> to view their complete information.")
        print("="*70 + "\n")
        
        return characters
        
    except Exception as e:
        print(f"\n!!! ERROR creating roster characters: {e}")
        import traceback
        traceback.print_exc()
        return characters


# Quick reference for individual character creation
CREATE_FUNCTIONS = {
    "alia": create_alia,
    "leto": create_leto_ii,
    "leto2": create_leto_ii,
    "ghanima": create_ghanima,
    "duncan": create_duncan_idaho,
    "idaho": create_duncan_idaho,
    "irulan": create_irulan,
    "jessica": create_jessica,
    "stilgar": create_stilgar,
    "gurney": create_gurney_halleck
}


def create_character(name):
    """
    Create a single roster character by name.
    
    Args:
        name (str): Short name of character (e.g., "alia", "duncan", "leto")
        
    Returns:
        Character: The created character object
        
    Example:
        @py world.dune.roster_characters.create_character("alia")
    """
    name_lower = name.lower()
    if name_lower in CREATE_FUNCTIONS:
        return CREATE_FUNCTIONS[name_lower]()
    else:
        print(f"Unknown character: {name}")
        print(f"Available characters: {', '.join(CREATE_FUNCTIONS.keys())}")
        return None

