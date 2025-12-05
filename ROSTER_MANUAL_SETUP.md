# Roster Characters - Manual Setup Guide

This guide shows you how to manually set up roster character accounts using in-game commands. This gives you more control and allows players to apply for and take over these characters with their own passwords.

## Overview

For each character, you'll:
1. Create an Account
2. Create a Character object linked to that account
3. Set up stats using `+stats` commands
4. Set up biography using `+bio` commands
5. Set home location and permissions

---

## Step-by-Step Setup

### 1. CREATE ACCOUNTS & CHARACTERS

First, create accounts for all roster characters:

```python
# Create accounts (run as superuser)
@charcreate/account Alia_Atreides:default_password
@charcreate/account Leto_Atreides:default_password
@charcreate/account Ghanima_Atreides:default_password
@charcreate/account Duncan_Idaho:default_password
@charcreate/account Irulan_Corrino:default_password
@charcreate/account Lady_Jessica:default_password
@charcreate/account Stilgar:default_password
@charcreate/account Gurney_Halleck:default_password
```

**Note:** If you already created the Character objects with Python, you need to link them to accounts instead:

```python
# Find and link existing characters to new accounts
@py from evennia import create_account, search_object
@py account = create_account("Alia_Atreides", email="alia@roster.dune", password="default_password")
@py char = search_object("Alia Atreides")[0]
@py char.locks.add(f"puppet:pid({account.id}) or pperm(Builder)")
@py account.db._playable_characters = [char]
@py account.msg("Character linked!")
```

---

## Character Setup Commands

### ALIA ATREIDES - Regent of the Imperium

**Step 1: Basic Info**
```
@ic Alia Atreides
+bio/house Atreides
+bio/role Regent
+bio/caste Noble
+bio/gender feminine
```

**Step 2: Skills (Discipline 8, Communicate 7, Understand 5, Battle 4, Move 4) = 28 points**
```
+stats discipline=8
+stats communicate=7
+stats understand=5
+stats battle=4
+stats move=4
```

**Step 3: Focuses**
```
+stats/focus add=Short Blades
+stats/focus add=Intimidation
+stats/focus add=Composure
+stats/focus add=Resolve
+stats/focus add=Imperial Politics
+stats/focus add=House Politics
+stats/focus add=Botany
```

**Step 4: Talents**
```
+stats/talent add=Bene Gesserit Training
+stats/talent add=Voice
+stats/talent add=Prana-Bindu Control
+stats/talent add=Pre-Born
+stats/talent add=Reverend Mother Abilities
+stats/talent add=Mentat-like Computation (ancestral)
+stats/talent add=Prescient Flashes
```

**Step 5: Drives (8,7,6,5,4)**
```
+stats/drive power=8
+stats/drive power/statement=I will maintain absolute control over the Empire and prove I am worthy of the Atreides legacy
+stats/drive duty=7
+stats/drive duty/statement=As Regent, I must protect the realm and guide my nephew and niece toward their destiny
+stats/drive justice=6
+stats/drive justice/statement=I will root out corruption and those who would threaten House Atreides
+stats/drive faith=5
+stats/drive truth=4
```

**Step 6: Biography**
```
+bio/personality Authoritative, intelligent, and charismatic, but increasingly erratic and volatile. She displays flashes of the Harkonnen cruelty she inherited through genetic memory. Fiercely protective of her family's legacy while simultaneously struggling with her own identity.

+bio/ambition Maintain control of the Empire and resist ancestral possession

+bio/appearance A striking woman in her twenties with the dark hair and green eyes of House Atreides. She moves with predatory grace and her gaze seems to look through people. She typically wears elaborate robes befitting her station as Regent.

+bio/trait The Pre-Born Regent

+bio/relationships Sister of Paul Muad'Dib (missing). Aunt to Leto II and Ghanima. Daughter of Lady Jessica and Duke Leto. Wife to Duncan Idaho (Hayt). Complex relationship with Irulan Corrino.
```

**Step 7: Languages**
```
+language/add The Truth
+language/add Fremen Chakobsa
+language/add Galach
+language/add Bene Gesserit Battle Language
+language/set Galach
```

**Step 8: Final Setup**
```
+determination/set 3
@ooc
```

---

### LETO II ATREIDES - Heir to the Empire

```
@ic Leto II Atreides
+bio/house Atreides
+bio/role Heir
+bio/caste Noble
+bio/gender masculine

+stats discipline=8
+stats understand=7
+stats move=5
+stats battle=4
+stats communicate=4

+stats/focus add=Short Blades
+stats/focus add=Inspiration
+stats/focus add=Composure
+stats/focus add=Resolve
+stats/focus add=Survival/Desert
+stats/focus add=Ecology
+stats/focus add=Imperial Politics

+stats/talent add=Pre-Born
+stats/talent add=Fremen Training
+stats/talent add=Prescient Visions
+stats/talent add=Ancestral Wisdom
+stats/talent add=Voice (learned)
+stats/talent add=Desert Survival Expert

+stats/drive duty=8
+stats/drive duty/statement=I must walk the Golden Path to save humanity from stagnation and extinction
+stats/drive truth=7
+stats/drive truth/statement=I will see beyond what others can see and understand the terrible necessities of the future
+stats/drive justice=6
+stats/drive justice/statement=I will ensure that humanity's future is secured, even if the present must suffer
+stats/drive power=5
+stats/drive faith=4

+bio/personality Introspective, profoundly wise beyond his years, yet still retains flashes of youthful curiosity and emotion. He bears the weight of prescient knowledge with grim determination. More willing than his father to pay the terrible price the future demands.

+bio/ambition Follow the Golden Path to ensure humanity's survival, no matter the personal cost

+bio/appearance A teenager with the striking features of House Atreides - dark hair and those distinctive green eyes. He has the desert-hardened physique of someone raised among the Fremen. When he gazes into the distance, it's as if he's looking through time itself.

+bio/trait The Pre-Born Heir

+bio/relationships Son of Paul Muad'Dib (missing) and Chani (deceased). Twin brother of Ghanima. Nephew of Alia Atreides. Grandson of Lady Jessica. Ward of Stilgar. Student of Irulan.

+language/add Fremen Chakobsa
+language/add Galach
+language/add The Truth
+language/set Chakobsa

+determination/set 3
@ooc
```

---

### GHANIMA ATREIDES - The Wise Twin

```
@ic Ghanima Atreides
+bio/house Atreides
+bio/role Heir
+bio/caste Noble
+bio/gender feminine

+stats communicate=8
+stats discipline=7
+stats understand=5
+stats battle=4
+stats move=4

+stats/focus add=Short Blades
+stats/focus add=Empathy
+stats/focus add=Persuasion
+stats/focus add=Composure
+stats/focus add=Resolve
+stats/focus add=Survival/Desert
+stats/focus add=Physical Empathy

+stats/talent add=Pre-Born
+stats/talent add=Fremen Training
+stats/talent add=Prescient Awareness
+stats/talent add=Ancestral Wisdom
+stats/talent add=Voice
+stats/talent add=Desert Survival Expert
+stats/talent add=Psychic Bond with Twin

+stats/drive duty=8
+stats/drive duty/statement=I must support my brother in his terrible task and help preserve what's human in him
+stats/drive justice=7
+stats/drive justice/statement=I will ensure that in saving humanity, we do not lose our own humanity
+stats/drive faith=6
+stats/drive faith/statement=I believe in the essential goodness of humanity and the value of individual choice
+stats/drive power=5
+stats/drive truth=4

+bio/personality Strong-willed, perceptive, and deeply compassionate despite her ancestral memories. She possesses a sharp wit and often serves as the voice of reason. More emotionally expressive than her brother, but equally burdened by prescient knowledge.

+bio/ambition Protect my brother and help guide humanity's future while maintaining my own identity

+bio/appearance A striking teenage girl with the classic Atreides features - dark hair and penetrating green eyes. She moves with the fluid grace of a trained Fremen, comfortable in stillsuit or formal robes. Her gaze carries ancient wisdom.

+bio/trait The Wise Twin

+bio/relationships Daughter of Paul Muad'Dib (missing) and Chani (deceased). Twin sister of Leto II. Niece of Alia Atreides. Granddaughter of Lady Jessica. Ward of Stilgar. Student of Irulan.

+language/add Fremen Chakobsa
+language/add Galach
+language/add The Truth
+language/add Bene Gesserit Battle Language
+language/set Chakobsa

+determination/set 3
@ooc
```

---

### DUNCAN IDAHO - Ghola Swordmaster

```
@ic Duncan Idaho
+bio/house Atreides
+bio/role Swordmaster
+bio/caste Retainer
+bio/gender masculine

+stats battle=8
+stats move=7
+stats discipline=5
+stats communicate=4
+stats understand=4

+stats/focus add=Long Blades
+stats/focus add=Short Blades
+stats/focus add=Shield Fighting
+stats/focus add=Tactics
+stats/focus add=Infiltration
+stats/focus add=Composure
+stats/focus add=Acrobatics
+stats/focus add=Stealth

+stats/talent add=Master Swordsman
+stats/talent add=Ginaz Training
+stats/talent add=Shield Fighter
+stats/talent add=Tleilaxu Enhancement
+stats/talent add=Mentat-like Computation (ghola gift)
+stats/talent add=Martial Reflexes
+stats/talent add=Combat Awareness

+stats/drive duty=8
+stats/drive duty/statement=I am sworn to House Atreides and will protect them with my life - again and again if needed
+stats/drive justice=7
+stats/drive justice/statement=I will defend the innocent and punish those who betray honor
+stats/drive power=6
+stats/drive power/statement=I seek to master my own fate and prove I am more than a manufactured copy
+stats/drive truth=5
+stats/drive faith=4

+bio/personality Intensely loyal to House Atreides, but troubled by his resurrection and the philosophical questions it raises. Stoic and disciplined, with flashes of the old warmth and humor. Deeply concerned about Alia's growing instability.

+bio/ambition Serve House Atreides faithfully and protect Alia from the darkness consuming her

+bio/appearance A tall, powerful man in his prime with dark curling hair and penetrating blue-within-blue eyes of spice addiction. He moves with the deadly grace of a master swordsman. Bears himself with the dignity of House Atreides but with an undercurrent of existential unease.

+bio/trait The Resurrected Swordmaster

+bio/relationships Husband of Alia Atreides (Regent). Legendary retainer of House Atreides. Mentor figure to Leto II and Ghanima. Loyally served Duke Leto (deceased) and Paul Muad'Dib (missing). Resurrected by Tleilaxu.

+language/add Galach
+language/add Chakobsa
+language/add The Truth
+language/set Galach

+determination/set 3
@ooc
```

---

### IRULAN CORRINO - Empress and Historian

```
@ic Irulan Corrino
+bio/house Atreides
+bio/role Consort
+bio/caste Noble
+bio/gender feminine

+stats understand=8
+stats communicate=7
+stats discipline=5
+stats battle=4
+stats move=4

+stats/focus add=Diplomacy
+stats/focus add=Teaching
+stats/focus add=Persuasion
+stats/focus add=Composure
+stats/focus add=Cultural Studies
+stats/focus add=Imperial Politics
+stats/focus add=Etiquette
+stats/focus add=Linguistics

+stats/talent add=Bene Gesserit Training
+stats/talent add=Voice
+stats/talent add=Master Historian
+stats/talent add=Imperial Education
+stats/talent add=Diplomatic Immunity (status)
+stats/talent add=Truthsayer Training
+stats/talent add=Scholar

+stats/drive truth=8
+stats/drive truth/statement=I will record the true history of this age, free from propaganda and myth
+stats/drive duty=7
+stats/drive duty/statement=I must guide Leto and Ghanima to rule wisely and redeem my past failures
+stats/drive justice=6
+stats/drive justice/statement=I seek to atone for my house's crimes and my own conspiracies against Paul
+stats/drive power=5
+stats/drive faith=4

+bio/personality Intelligent, cultured, and diplomatic. Haunted by regret over past actions and her loveless marriage. She possesses deep compassion masked by imperial dignity. Excellent teacher and historian with a gift for seeing patterns in history.

+bio/ambition Redeem myself by serving the Atreides children and preserving the true history of this era

+bio/appearance A statuesque woman in her thirties with the refined beauty of House Corrino. Her bearing is regal despite her house's fall from power. She dresses in elegant robes that balance Atreides green with hints of Corrino gold. Her eyes reflect both intelligence and deep sadness.

+bio/trait The Historian Empress

+bio/relationships Widow of Paul Atreides (missing). Daughter of deposed Emperor Shaddam IV. Tutor to Leto II and Ghanima. Trained by Bene Gesserit. Complex relationship with Alia (political tensions). Sister to Wensicia Corrino.

+language/add Galach
+language/add The Truth
+language/add Bene Gesserit Battle Language
+language/add Ancient Imperial Tongues
+language/set Galach

+determination/set 3
@ooc
```

---

### LADY JESSICA - Bene Gesserit Reverend Mother

```
@ic Lady Jessica
+bio/house Atreides
+bio/role Advisor
+bio/caste Noble
+bio/gender feminine

+stats discipline=8
+stats communicate=7
+stats understand=5
+stats battle=4
+stats move=4

+stats/focus add=Unarmed Combat
+stats/focus add=Persuasion
+stats/focus add=Deceit
+stats/focus add=Composure
+stats/focus add=Observe
+stats/focus add=Resolve
+stats/focus add=Imperial Politics
+stats/focus add=Faction Lore/Bene Gesserit

+stats/talent add=Bene Gesserit Training
+stats/talent add=Reverend Mother
+stats/talent add=Voice
+stats/talent add=Prana-Bindu Control
+stats/talent add=Truthsayer
+stats/talent add=Other Memory
+stats/talent add=Weirding Way Combat
+stats/talent add=Water of Life Survived

+stats/drive duty=8
+stats/drive duty/statement=I must protect my grandchildren and guide them toward a future free from my mistakes
+stats/drive faith=7
+stats/drive faith/statement=I believe in the Bene Gesserit way, even as I defy the Sisterhood for my family
+stats/drive truth=6
+stats/drive truth/statement=I will face the consequences of my choices and see clearly through deception
+stats/drive power=5
+stats/drive justice=4

+bio/personality Wise, calculating, and deeply maternal despite her Bene Gesserit training. Carries profound guilt over Alia's pre-born condition. She balances love for her family with cold practicality when needed. Master of Voice and Bene Gesserit arts.

+bio/ambition Protect my grandchildren and save Alia from the darkness consuming her

+bio/appearance A woman in her sixties who appears far younger due to Bene Gesserit training. She carries herself with the grace and authority of both a Reverend Mother and former ducal concubine. Her green Atreides eyes miss nothing, and her presence commands respect.

+bio/trait The Reverend Mother of Atreides

+bio/relationships Mother of Paul Atreides (missing) and Alia Atreides (Regent). Concubine of Duke Leto (deceased). Grandmother of Leto II and Ghanima. Bene Gesserit Reverend Mother. Daughter of Baron Harkonnen (secret).

+language/add Galach
+language/add The Truth
+language/add Bene Gesserit Battle Language
+language/add Chakobsa
+language/add Ancient Tongues
+language/set Galach

+determination/set 3
@ooc
```

---

### STILGAR - Fremen Naib

```
@ic Stilgar
+bio/house Atreides
+bio/role Marshal
+bio/caste Fremen
+bio/gender masculine

+stats battle=8
+stats understand=6
+stats discipline=6
+stats move=4
+stats communicate=4

+stats/focus add=Short Blades
+stats/focus add=Pistols
+stats/focus add=Tactics
+stats/focus add=Inspiration
+stats/focus add=Resolve
+stats/focus add=Survival/Desert
+stats/focus add=Stealth
+stats/focus add=Faction Lore/Fremen

+stats/talent add=Fremen Warrior
+stats/talent add=Desert Survival Expert
+stats/talent add=Naib Authority
+stats/talent add=Crysknife Master
+stats/talent add=Water Discipline
+stats/talent add=Sandworm Rider
+stats/talent add=Fedaykin Veteran

+stats/drive duty=8
+stats/drive duty/statement=I am sworn to protect Paul's children and guide them in the ways of the desert
+stats/drive faith=7
+stats/drive faith/statement=I believe in Muad'Dib's prophecy and the destiny of his line
+stats/drive justice=6
+stats/drive justice/statement=I will uphold Fremen law and tradition in a changing world
+stats/drive power=5
+stats/drive truth=4

+bio/personality Traditional, honorable, and deeply religious in his belief in Muad'Dib's prophecy. Loyal to the bone but increasingly troubled by the changes to Fremen culture. He is pragmatic when needed but holds firm to the old ways. Gruff exterior hides deep affection for those under his care.

+bio/ambition Preserve Fremen traditions while serving House Atreides and protecting the twins

+bio/appearance A weathered Fremen warrior in his fifties with the distinctive blue-within-blue eyes of spice addiction. His face bears the lines of a lifetime in the desert. He wears traditional Fremen robes and carries himself with the quiet authority of a naib.

+bio/trait The Guardian Naib

+bio/relationships Guardian to Leto II and Ghanima. Naib of Sietch Tabr. Faithful follower of Paul Muad'Dib (missing). Respected by Alia Atreides. Ally of Duncan Idaho and Lady Jessica. Uncle-figure to the twins.

+language/add Fremen Chakobsa
+language/add Galach
+language/set Chakobsa

+determination/set 3
@ooc
```

---

### GURNEY HALLECK - Warmaster

```
@ic Gurney Halleck
+bio/house Atreides
+bio/role Warmaster
+bio/caste Retainer
+bio/gender masculine

+stats battle=8
+stats communicate=6
+stats discipline=6
+stats move=4
+stats understand=4

+stats/focus add=Long Blades
+stats/focus add=Shield Fighting
+stats/focus add=Strategy
+stats/focus add=Tactics
+stats/focus add=Inspiration
+stats/focus add=Resolve
+stats/focus add=Imperial Politics
+stats/focus add=Music/baliset

+stats/talent add=Master Warrior
+stats/talent add=Military Genius
+stats/talent add=Troubadour
+stats/talent add=Veteran of Many Wars
+stats/talent add=Shield Master
+stats/talent add=Inspirational Leader
+stats/talent add=Torture Survivor (mental resilience)

+stats/drive duty=8
+stats/drive duty/statement=I serve House Atreides unto death, as I swore to Duke Leto
+stats/drive justice=7
+stats/drive justice/statement=I will see the Harkonnens and all tyrants brought to account for their crimes
+stats/drive faith=6
+stats/drive faith/statement=I believe in the old Duke's vision of just rule, even in this age of holy war
+stats/drive power=5
+stats/drive truth=4

+bio/personality Gruff, cynical, but with a deep romantic soul that finds expression in music and poetry. Absolutely loyal to House Atreides. Quick to violence when needed but haunted by the cost of the Jihad. Mentor figure who balances harsh training with genuine care.

+bio/ambition Serve House Atreides faithfully while preserving some humanity in an age of holy war

+bio/appearance A scarred, weathered man in his fifties with an inkvine scar running down his jaw - a memento of Harkonnen torture. Despite his rough appearance, his eyes show both intelligence and deep feeling. Often carries a baliset and moves with the controlled economy of a master warrior.

+bio/trait The Troubadour Warrior

+bio/relationships Warmaster of House Atreides. Served Duke Leto (deceased) and Paul Muad'Dib (missing). Comrade of Duncan Idaho. Respected by Alia (Regent). Friend to Lady Jessica. Mentor to younger Atreides soldiers. Former Harkonnen slave.

+language/add Galach
+language/add Chakobsa
+language/add Various military dialects
+language/set Galach

+determination/set 3
@ooc
```

---

## Post-Setup Tasks

After setting up all characters:

### 1. Set Roster Availability
```python
@tag/add Alia Atreides = roster_character:character_type
@tag/add Alia Atreides = available:roster
# Repeat for all characters
```

### 2. Move to Starting Location
```python
@tel Alia Atreides = Arrakeen Palace - Throne Room
@tel Duncan Idaho = Arrakeen Palace - Throne Room
@tel Leto II Atreides = Sietch Tabr
# etc.
```

### 3. Set Homes
```python
@py from evennia import search_object
@py char = search_object("Alia Atreides")[0]
@py location = search_object("Arrakeen Palace - Throne Room")[0]
@py char.home = location
# Repeat for all characters
```

### 4. Verify Setup
```
@ic Alia Atreides
+sheet
@ooc
```

---

## Quick Copy-Paste Block

For rapid setup, you can copy each character's block above and paste it directly into your game. Each block includes:
- All stats
- All focuses
- All talents
- All drives with statements
- Complete biography
- Languages

Just puppet each character (`@ic <name>`) and paste the commands!

---

## Batch Script Alternative

If you prefer, you can create a text file with all commands and run:
```
@batchcommand <path_to_file>
```

---

## Tips

1. **Test as you go**: After each character, test with `+sheet` to make sure everything looks right
2. **Adjust as needed**: These are suggestions - feel free to modify stats or backgrounds
3. **Set passwords**: Remember to set secure passwords for roster accounts
4. **Document changes**: Keep notes on any modifications you make
5. **Backup**: Use `@examine <character>` to save character data

---

## Troubleshooting

**Commands not working?**
- Make sure you're logged in with proper permissions
- Use `@ic <character>` before setting their stats

**Stats not saving?**
- Some commands require being puppeted as the character
- Check that character object exists first

**Can't find character?**
- Use `@find <name>` to locate them
- Make sure they're created first

---

*This manual approach gives you complete control over roster character setup using standard in-game commands!*

