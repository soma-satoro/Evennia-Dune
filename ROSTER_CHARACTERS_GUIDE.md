# Roster Characters Guide
## Children of Dune Era Feature Characters

### Timeline Setting

This game is set shortly after **Paul Muad'Dib's disappearance** into the desert during the Great Jihad. The key facts of this period:

- **Alia Atreides** serves as Regent of the Imperium
- The **Imperial Seat** is on Arrakis (moved from Kaitain)
- **Leto II** and **Ghanima**, Paul's twin children, are coming of age (approximately 9-12 years old but pre-born)
- This is **before** Leto II's transformation into the God Emperor
- **Lady Jessica** has returned to Arrakis
- **Duncan Idaho** has been resurrected as a ghola and restored his memories
- **Princess Irulan** serves as historian and tutor to the twins

This corresponds roughly to the period covered in Frank Herbert's novel "Children of Dune."

---

## Creating the Roster Characters

### Method 1: Create All at Once (Recommended)

From in-game as a superuser or admin:

```
@py world.dune.roster_characters.create_all_roster()
```

This will create all 8 major roster characters in one batch.

### Method 2: Create Individual Characters

To create specific characters:

```
@py world.dune.roster_characters.create_character("alia")
@py world.dune.roster_characters.create_character("duncan")
@py world.dune.roster_characters.create_character("leto")
```

Available character shortcuts:
- `alia` - Alia Atreides
- `leto`, `leto2` - Leto II Atreides  
- `ghanima` - Ghanima Atreides
- `duncan`, `idaho` - Duncan Idaho (Hayt)
- `irulan` - Princess Irulan Corrino
- `jessica` - Lady Jessica
- `stilgar` - Stilgar
- `gurney` - Gurney Halleck

### Method 3: Direct Function Calls

For more control:

```
@py world.dune.roster_characters.create_alia()
@py world.dune.roster_characters.create_leto_ii()
@py world.dune.roster_characters.create_ghanima()
```

---

## The Roster Characters

### 1. ALIA ATREIDES
**Title:** Regent of the Imperium  
**Role:** Imperial Regent, Pre-Born  
**House:** Atreides

**Background:**  
Sister of Paul Muad'Dib, Alia was born "pre-born" - with full consciousness and access to all her ancestral memories due to her mother's spice agony during pregnancy. This makes her both incredibly powerful and dangerously vulnerable to possession by her ancestors, particularly Baron Vladimir Harkonnen. As Regent, she rules the Empire with absolute authority but fights a constant internal battle against the Baron's personality attempting to take control.

**Key Stats:**
- Skills: Battle 4, Communicate 5, Discipline 5, Move 3, Understand 5
- Major Talents: Bene Gesserit Training, Voice, Pre-Born, Reverend Mother Abilities, Prescient Flashes
- Drives: Power 8, Duty 7, Justice 6, Faith 5, Truth 4

**Roleplay Notes:**
- Increasingly volatile and unpredictable due to ancestral possession
- Displays both Atreides nobility and Harkonnen cruelty
- Married to Duncan Idaho but their relationship is strained
- Fiercely protective of her family's legacy

---

### 2. LETO II ATREIDES
**Title:** Heir to the Empire  
**Role:** Pre-Born Heir  
**House:** Atreides

**Background:**  
Son of Paul Muad'Dib and Chani, Leto II was born pre-born with access to all ancestral memories. Unlike his aunt Alia, he has learned to manage these voices. As he comes of age, he begins to see the "Golden Path" - a future that will ensure humanity's survival but requires him to undergo a transformation that will make him an immortal tyrant for thousands of years. He stands at a crossroads between humanity and apotheosis.

**Key Stats:**
- Skills: Battle 3, Communicate 4, Discipline 5, Move 4, Understand 5
- Major Talents: Pre-Born, Fremen Training, Prescient Visions, Ancestral Wisdom, Desert Survival Expert
- Drives: Duty 8, Truth 7, Justice 6, Power 5, Faith 4

**Roleplay Notes:**
- Profoundly wise beyond his years but still shows flashes of youth
- Shares a deep psychic bond with his twin Ghanima
- Wrestling with the terrible knowledge of what he must become
- Trained in both Imperial politics and Fremen desert ways

---

### 3. GHANIMA ATREIDES
**Title:** The Wise Twin  
**Role:** Pre-Born Heir  
**House:** Atreides

**Background:**  
Twin sister of Leto II, Ghanima is also pre-born with full ancestral memories. She serves as a balance to her brother, sharing his burdens while maintaining her own strong identity. She understands the terrible destiny Leto faces and supports him even as she fears for what he must become. More emotionally expressive than her brother, she often serves as the voice of reason and humanity.

**Key Stats:**
- Skills: Battle 3, Communicate 5, Discipline 5, Move 4, Understand 4
- Major Talents: Pre-Born, Fremen Training, Prescient Awareness, Voice, Desert Survival Expert, Psychic Bond with Twin
- Drives: Duty 8, Justice 7, Faith 6, Power 5, Truth 4

**Roleplay Notes:**
- Strong-willed and perceptive with sharp wit
- Deep empathy despite ancestral memories
- Protective of her brother and their humanity
- Balances Fremen traditions with Imperial responsibilities

---

### 4. DUNCAN IDAHO (HAYT)
**Title:** Ghola Swordmaster  
**Role:** Swordmaster of House Atreides  
**House:** Atreides

**Background:**  
The legendary Swordmaster of House Atreides, Duncan Idaho was killed defending Paul during the Harkonnen attack on Arrakis. He was resurrected by the Tleilaxu as a ghola (clone) called "Hayt" and has since recovered his original memories. Now married to Alia, he serves House Atreides while struggling with profound questions about identity, mortality, and the nature of his existence. He is deeply troubled by Alia's growing instability.

**Key Stats:**
- Skills: Battle 5, Communicate 3, Discipline 4, Move 5, Understand 3
- Major Talents: Master Swordsman, Ginaz Training, Shield Fighter, Tleilaxu Enhancement, Mentat-like Computation
- Drives: Duty 8, Justice 7, Power 6, Truth 5, Faith 4

**Roleplay Notes:**
- Unwaveringly loyal to House Atreides
- Troubled by existential questions about his resurrection
- One of the greatest swordsmen in the Imperium
- Concerned about Alia's mental state and seeking to protect her

---

### 5. PRINCESS IRULAN CORRINO
**Title:** Empress and Historian  
**Role:** Imperial Consort, Historian  
**House:** Atreides (by marriage), born Corrino

**Background:**  
Eldest daughter of the deposed Emperor Shaddam IV, Irulan received the finest education in the Imperium and was trained by the Bene Gesserit. She was married to Paul Atreides in a loveless political union and denied children. After Paul's disappearance, she has found purpose as historian of the Muad'Dib legend and tutor to Leto II and Ghanima, seeking redemption for past conspiracies against Paul.

**Key Stats:**
- Skills: Battle 2, Communicate 5, Discipline 4, Move 2, Understand 5
- Major Talents: Bene Gesserit Training, Voice, Master Historian, Imperial Education, Truthsayer Training, Scholar
- Drives: Truth 8, Duty 7, Justice 6, Power 5, Faith 4

**Roleplay Notes:**
- Brilliant scholar and master diplomat
- Haunted by regret over her loveless marriage and past actions
- Excellent teacher and chronicler of history
- Navigates complex position between Corrino heritage and Atreides present

---

### 6. LADY JESSICA
**Title:** Bene Gesserit Reverend Mother  
**Role:** Advisor, Matriarch  
**House:** Atreides

**Background:**  
Mother of Paul and Alia, concubine of the late Duke Leto, Jessica is a full Bene Gesserit Reverend Mother who famously defied the Sisterhood by bearing a son instead of a daughter. This act of love set in motion the events that led to Paul's rise and the Jihad. Now returned to Arrakis, she watches with concern and guilt as her daughter Alia battles the very curse Jessica's disobedience helped create.

**Key Stats:**
- Skills: Battle 3, Communicate 5, Discipline 5, Move 3, Understand 5
- Major Talents: Reverend Mother, Voice, Prana-Bindu Control, Truthsayer, Other Memory, Weirding Way Combat
- Drives: Duty 8, Faith 7, Truth 6, Power 5, Justice 4

**Roleplay Notes:**
- Master of Bene Gesserit arts, particularly Voice
- Deeply maternal despite her training in emotional control
- Carries profound guilt over Alia's pre-born condition
- Torn between loyalty to family and the Sisterhood

---

### 7. STILGAR
**Title:** Fremen Naib  
**Role:** Marshal, Guardian  
**House:** Atreides (sworn)

**Background:**  
Naib (leader) of Sietch Tabr and among the first Fremen to recognize Paul Muad'Dib's potential, Stilgar has served House Atreides faithfully through the Jihad and its aftermath. He now serves as guardian and mentor to Paul's children, teaching them the old Fremen ways while watching his people transform from desert warriors to Imperial citizens. He reveres Paul as a prophet but is troubled by what the future holds.

**Key Stats:**
- Skills: Battle 5, Communicate 3, Discipline 4, Move 4, Understand 3
- Major Talents: Fremen Warrior, Desert Survival Expert, Naib Authority, Crysknife Master, Sandworm Rider, Fedaykin Veteran
- Drives: Duty 8, Faith 7, Justice 6, Power 5, Truth 4

**Roleplay Notes:**
- Traditional Fremen warrior and leader
- Deeply religious belief in Muad'Dib's prophecy
- Troubled by changes to Fremen culture under Imperial rule
- Gruff exterior but deep affection for those under his care

---

### 8. GURNEY HALLECK
**Title:** Warmaster  
**Role:** Warmaster of House Atreides  
**House:** Atreides

**Background:**  
Veteran warrior, musician, and troubadour who has served House Atreides for decades. Freed from Harkonnen slavery by Duke Leto, he survived the fall of House Atreides and fought his way back to Paul's side. Now serves as Warmaster commanding Atreides forces across the Imperium while struggling with the violence of the Jihad he helped enable. Carries the scars of Harkonnen torture and the weight of the holy war.

**Key Stats:**
- Skills: Battle 5, Communicate 3, Discipline 4, Move 3, Understand 3
- Major Talents: Master Warrior, Military Genius, Troubadour, Shield Master, Inspirational Leader
- Drives: Duty 8, Justice 7, Faith 6, Power 5, Truth 4

**Roleplay Notes:**
- Gruff and cynical but with a romantic soul (plays baliset)
- Absolutely loyal to House Atreides
- Haunted by the cost of the Jihad
- Mentor figure who balances harsh training with genuine care

---

## Using Roster Characters

### Viewing Character Sheets

After creation, view any character's full sheet:

```
+sheet Alia Atreides
+sheet Duncan Idaho
+sheet "Leto II Atreides"
```

### Assigning Players to Roster Characters

If you want to let players take over roster characters:

1. Create a player account if needed:
   ```
   @charcreate <playername>:<password>
   ```

2. Transfer the character to the player:
   ```
   @force <playername> = @ic Alia Atreides
   ```

3. Or use the roster system (if implemented):
   ```
   +rosterset Atreides/add "Alia Atreides"=Regent:Pre-born Regent of the Imperium
   ```

### Making Characters Available

To make these characters available at character selection:

1. Move them to a holding room:
   ```
   @tel Alia Atreides = #<room_id>
   @tel Duncan Idaho = #<room_id>
   ```

2. Set them as roster characters (if using a roster app):
   ```
   @set Alia Atreides/ROSTER = 1
   ```

### Modifying Characters

Characters can be further customized using standard commands:

```
@desc Alia Atreides = <new description>
+bio/personality Alia Atreides = <new personality>
+asset/create <asset_name> (when controlling the character)
```

---

## Additional Roster Character Ideas

### Imperial Characters

**Count Hasimir Fenring**
- Master assassin and genetic eunuch
- Close friend of deposed Emperor Shaddam IV
- Skills: Communicate 5, Battle 4, Discipline 5

**Wensicia Corrino**
- Sister of Irulan, plotter against House Atreides
- Schemes to restore House Corrino to power
- Skills: Communicate 5, Understand 5, Discipline 3

**Farad'n Corrino**
- Wensicia's son, potential heir to Corrino throne
- Young nobleman trained in intrigue
- Skills: Communicate 4, Understand 4, Battle 3

### Fremen Characters

**Harah**
- Fremen woman, caretaker to Paul's children
- Former wife of Jamis (killed by Paul)
- Skills: Move 3, Communicate 3, Understand 2

**Ghadhean al-Fali**
- Fremen Naib and former Fedaykin
- Advocates for Lady Jessica's return to power
- Skills: Battle 4, Communicate 3, Discipline 4

**Alia's Amazons**
- Elite female warriors serving Alia directly
- Fanatically loyal to the Regent
- Skills vary but Battle-focused

### Bene Gesserit Characters

**Reverend Mother Gaius Helen Mohiam**
- Former Imperial Truthsayer (if still alive in your timeline)
- Trained Jessica and Irulan
- Skills: Discipline 5, Communicate 5, Understand 5

**Other Reverend Mothers**
- Various Bene Gesserit operatives
- Each with specialized missions

### Guild & CHOAM

**Spacing Guild Navigator**
- Mutated by spice, able to fold space
- Dependent on continuous spice consumption
- Skills: Understand 5, Discipline 5

**CHOAM Director**
- Corporate power broker
- Controls spice trade contracts
- Skills: Communicate 5, Understand 5

---

## Timeline Notes

### Recent Past (Before Game Start)
- Paul Muad'Dib has walked into the desert after being blinded
- Chani died giving birth to the twins
- Duncan Idaho resurrected and memory restored
- Alia assumed the Regency

### Current Situation (Game Setting)
- Alia rules as Regent from Arrakeen
- The twins are coming of age (9-12 years old)
- Fremen culture is changing under Imperial influence
- Various factions plot against House Atreides
- Alia's mental stability is deteriorating

### Near Future (Potential Plot Threads)
- Leto II's transformation approaches
- House Corrino plots restoration
- Bene Gesserit schemes involving the twins
- Jessica's attempts to save Alia
- The question of Paul's return

---

## Roleplaying Guidelines

### Political Tensions

**House Atreides Internal:**
- Alia vs. Jessica (control and Alia's stability)
- Traditionalists vs. Reformers
- Fremen integration into Imperial structure

**External Threats:**
- House Corrino seeking restoration
- Bene Gesserit manipulation
- Spacing Guild dependence on spice
- Other Great Houses seeking advantage

### Themes to Explore

1. **Identity & Humanity**
   - What makes you human when you carry thousands of other memories?
   - Duncan's struggle with being a copy
   - Alia's battle against possession

2. **Power & Responsibility**
   - The burden of prescient knowledge
   - Ruling vs. Being ruled
   - The cost of the Jihad

3. **Tradition vs. Change**
   - Fremen cultural transformation
   - Imperial adaptation to Atreides rule
   - Old ways vs. new realities

4. **Sacrifice & Destiny**
   - Leto II's terrible choice
   - What are you willing to give up for humanity?
   - Personal happiness vs. greater good

---

## Technical Notes

### Character Stats Explanation

**Skills (0-5):**
- **Battle:** Combat, warfare, tactics
- **Communicate:** Social interaction, persuasion, Voice
- **Discipline:** Mental fortitude, focus, Bene Gesserit powers
- **Move:** Physical movement, athletics, agility
- **Understand:** Knowledge, comprehension, wisdom

**Drives (ratings 4-8, one of each):**
- **Duty:** Obligations and responsibilities
- **Faith:** Beliefs and principles  
- **Justice:** Sense of right and wrong
- **Power:** Ambitions and goals
- **Truth:** Quest for knowledge

Drives rated 6+ require statements describing what that drive means to the character.

### Special Abilities

**Pre-Born:**
- Access to ancestral memories from birth
- Risk of possession by ancestor personalities
- Immense knowledge but psychological danger

**Bene Gesserit Training:**
- Voice (command through vocal tones)
- Prana-Bindu (perfect body control)
- Truthsaying (detect lies)
- Fighting arts (Weirding Way)

**Fremen Abilities:**
- Desert survival expertise
- Water discipline
- Crysknife mastery
- Sandworm riding

---

## Story Hooks & Plots

### Major Plot Threads

1. **Alia's Possession**
   - Can Alia be saved from the Baron's influence?
   - Who will intervene and how?
   - What happens if she falls completely?

2. **Leto's Transformation**
   - Will Leto embrace the sandtrout?
   - Who supports or opposes this choice?
   - What are the immediate consequences?

3. **Corrino Restoration**
   - House Corrino plots to retake the throne
   - Assassination attempts on Atreides
   - Political marriages and alliances

4. **The Preacher**
   - Is the mysterious Preacher actually Paul?
   - What is his message?
   - How does this affect Alia's legitimacy?

### Side Quests & Storylines

1. **Fremen Traditionalists**
   - Resistance to Imperial changes
   - Water conflicts and cultural preservation
   - Naib politics

2. **Spice Smuggling**
   - Black market spice trade
   - Guild navigation monopoly
   - Desert raids

3. **Bene Gesserit Schemes**
   - Breeding program adjustments
   - Attempts to control the twins
   - Political manipulation

4. **Personal Dramas**
   - Duncan and Alia's troubled marriage
   - Irulan's search for purpose
   - Jessica's guilt over Alia
   - The twins' coming of age

---

## Commands Quick Reference

```bash
# View character
+sheet <character>

# Create all roster characters
@py world.dune.roster_characters.create_all_roster()

# Create individual character
@py world.dune.roster_characters.create_character("alia")

# Add character to House roster (if using roster system)
+rosterset Atreides/add "<character>"=<title>:<description>

# Teleport character
@tel <character> = <location>

# Set character as puppetable
@ic <character> (when possessing as player)

# Force character to perform action (admin only)
@force <character> = <command>
```

---

## Credits & Sources

Based on Frank Herbert's *Dune* series, specifically:
- *Dune Messiah* (ending)
- *Children of Dune* (primary setting)

Character stats adapted for the Modiphus 2d20 Dune RPG system as implemented in this Evennia codebase.

---

*For questions or issues with roster characters, contact your game admin.*

