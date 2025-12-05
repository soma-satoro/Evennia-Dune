# Roster Characters - Corrected Focuses

This document lists the corrected focuses for each roster character, using only valid focuses from the game's DUNE_FOCUSES list.

## Valid Focus Format

Focuses must match entries from CmdSheet.py DUNE_FOCUSES exactly. Some focuses require specification with "/" (Music, Secret Language, Survival, Pilot, Faction Lore).

---

## ALIA ATREIDES

**OLD (Invalid):**
```
+stats/focus add=Battle: Knife Fighting
+stats/focus add=Communicate: Voice
+stats/focus add=Communicate: Intimidation
+stats/focus add=Discipline: Bene Gesserit Training
+stats/focus add=Discipline: Ancestral Memories
+stats/focus add=Understand: Politics
+stats/focus add=Understand: Spice Knowledge
```

**NEW (Corrected):**
```
+stats/focus add=Short Blades
+stats/focus add=Intimidation
+stats/focus add=Composure
+stats/focus add=Resolve
+stats/focus add=Imperial Politics
+stats/focus add=House Politics
+stats/focus add=Botany
```

---

## LETO II ATREIDES

**OLD (Invalid):**
```
+stats/focus add=Battle: Crysknife
+stats/focus add=Communicate: Leadership
+stats/focus add=Discipline: Ancestral Memories
+stats/focus add=Discipline: Prescience
+stats/focus add=Move: Desert Survival
+stats/focus add=Understand: Ecology
+stats/focus add=Understand: Imperial Politics
```

**NEW (Corrected):**
```
+stats/focus add=Short Blades
+stats/focus add=Inspiration
+stats/focus add=Composure
+stats/focus add=Resolve
+stats/focus add=Survival: Desert
+stats/focus add=Ecology
+stats/focus add=Imperial Politics
```

---

## GHANIMA ATREIDES

**OLD (Invalid):**
```
+stats/focus add=Battle: Crysknife
+stats/focus add=Communicate: Empathy
+stats/focus add=Communicate: Voice
+stats/focus add=Discipline: Ancestral Memories
+stats/focus add=Discipline: Mental Barriers
+stats/focus add=Move: Desert Survival
+stats/focus add=Understand: Human Nature
```

**NEW (Corrected):**
```
+stats/focus add=Short Blades
+stats/focus add=Empathy
+stats/focus add=Persuasion
+stats/focus add=Composure
+stats/focus add=Resolve
+stats/focus add=Survival: Desert
+stats/focus add=Physical Empathy
```

---

## DUNCAN IDAHO

**OLD (Invalid):**
```
+stats/focus add=Battle: Long Blade
+stats/focus add=Battle: Short Blade
+stats/focus add=Battle: Shield Fighting
+stats/focus add=Battle: Multiple Opponents
+stats/focus add=Discipline: Mentat Training (Tleilaxu gift)
+stats/focus add=Discipline: Combat Focus
+stats/focus add=Move: Acrobatics
+stats/focus add=Move: Infiltration
```

**NEW (Corrected):**
```
+stats/focus add=Long Blades
+stats/focus add=Short Blades
+stats/focus add=Shield Fighting
+stats/focus add=Tactics
+stats/focus add=Infiltration
+stats/focus add=Composure
+stats/focus add=Acrobatics
+stats/focus add=Stealth
```

---

## IRULAN CORRINO

**OLD (Invalid):**
```
+stats/focus add=Communicate: Diplomacy
+stats/focus add=Communicate: Teaching
+stats/focus add=Communicate: Voice
+stats/focus add=Discipline: Bene Gesserit Training
+stats/focus add=Understand: History
+stats/focus add=Understand: Politics
+stats/focus add=Understand: Imperial Protocol
+stats/focus add=Understand: Writing
```

**NEW (Corrected):**
```
+stats/focus add=Diplomacy
+stats/focus add=Teaching
+stats/focus add=Persuasion
+stats/focus add=Composure
+stats/focus add=Cultural Studies
+stats/focus add=Imperial Politics
+stats/focus add=Etiquette
+stats/focus add=Linguistics
```

---

## LADY JESSICA

**OLD (Invalid):**
```
+stats/focus add=Battle: Bene Gesserit Fighting
+stats/focus add=Communicate: Voice
+stats/focus add=Communicate: Manipulation
+stats/focus add=Discipline: Bene Gesserit Training
+stats/focus add=Discipline: Truthsaying
+stats/focus add=Discipline: Other Memory
+stats/focus add=Understand: Politics
+stats/focus add=Understand: Bene Gesserit Lore
```

**NEW (Corrected):**
```
+stats/focus add=Unarmed Combat
+stats/focus add=Persuasion
+stats/focus add=Deceit
+stats/focus add=Composure
+stats/focus add=Observe
+stats/focus add=Resolve
+stats/focus add=Imperial Politics
+stats/focus add=Faction Lore: Bene Gesserit
```

---

## STILGAR

**OLD (Invalid):**
```
+stats/focus add=Battle: Crysknife
+stats/focus add=Battle: Maula Pistol
+stats/focus add=Battle: Desert Warfare
+stats/focus add=Communicate: Leadership
+stats/focus add=Discipline: Pain Resistance
+stats/focus add=Move: Desert Survival
+stats/focus add=Move: Sandwalking
+stats/focus add=Understand: Fremen Lore
```

**NEW (Corrected):**
```
+stats/focus add=Short Blades
+stats/focus add=Pistols
+stats/focus add=Tactics
+stats/focus add=Inspiration
+stats/focus add=Resolve
+stats/focus add=Survival: Desert
+stats/focus add=Stealth
+stats/focus add=Faction Lore: Fremen
```

---

## GURNEY HALLECK

**OLD (Invalid):**
```
+stats/focus add=Battle: Long Blade
+stats/focus add=Battle: Shield Fighting
+stats/focus add=Battle: Military Tactics
+stats/focus add=Battle: Small Unit Tactics
+stats/focus add=Communicate: Inspiration
+stats/focus add=Discipline: Pain Resistance
+stats/focus add=Understand: Military Strategy
+stats/focus add=Understand: Music (baliset)
```

**NEW (Corrected):**
```
+stats/focus add=Long Blades
+stats/focus add=Shield Fighting
+stats/focus add=Strategy
+stats/focus add=Tactics
+stats/focus add=Inspiration
+stats/focus add=Resolve
+stats/focus add=Imperial Politics
+stats/focus add=Music: baliset
```

---

## Key Changes Made

### Invalid Focuses Removed:
- **Voice** - This is a Talent, not a Focus
- **Bene Gesserit Training** - This is a Talent, not a Focus
- **Mentat Training** - This is a Talent, not a Focus
- **Ancestral Memories** - Not a valid focus
- **Prescience** - Not a valid focus
- **Truthsaying** - This is a Talent, not a Focus
- **Other Memory** - This is a Talent, not a Focus
- **Multiple Opponents** - Not in valid list
- **Desert Warfare** - Not in valid list
- **Combat Focus** - Not in valid list

### Corrections Applied:
- "Battle: Knife Fighting" → "Short Blades"
- "Battle: Crysknife" → "Short Blades"
- "Battle: Long Blade" → "Long Blades"
- "Battle: Short Blade" → "Short Blades"
- "Battle: Maula Pistol" → "Pistols"
- "Battle: Military Tactics" → "Strategy" or "Tactics"
- "Communicate: Leadership" → "Inspiration"
- "Discipline: Mental Barriers" → "Resolve"
- "Discipline: Pain Resistance" → "Resolve"
- "Move: Desert Survival" → "Survival: Desert"
- "Move: Sandwalking" → "Stealth"
- "Move: Infiltration" → "Infiltration" (under Discipline, not Move!)
- "Understand: Spice Knowledge" → "Botany"
- "Understand: Human Nature" → "Physical Empathy"
- "Understand: Fremen Lore" → "Faction Lore: Fremen"
- "Understand: Bene Gesserit Lore" → "Faction Lore: Bene Gesserit"
- "Understand: History" → "Cultural Studies"
- "Understand: Politics" → "Imperial Politics" or "House Politics"
- "Understand: Military Strategy" → "Imperial Politics" (representing strategic knowledge)
- "Understand: Music (baliset)" → "Music: baliset" (under Communicate)

### Valid Focus Categories:
- **Battle:** Assassination, Atomics, Dirty Fighting, Dueling, Evasive Action, Lasgun, Long Blades, Pistols, Rifle, Shield Fighting, Short Blades, Sneak Attacks, Strategy, Tactics, Unarmed Combat
- **Communicate:** Acting, Bartering, Charm, Deceit, Diplomacy, Disguise, Empathy, Gossip, Innuendo, Inspiration, Interrogation, Intimidation, Linguistics, Listening, Music/type, Neurolinguistics, Persuasion, Secret Language/type, Teaching
- **Discipline:** Command, Composure, Espionage, Infiltration, Observe, Precision, Resolve, Self-Control, Survival/type
- **Move:** Acrobatics, Body Control, Climb, Dance, Distance Running, Drive, Escaping, Grace, Pilot/type, Stealth, Swift, Swim, Unobtrusive, Worm Rider
- **Understand:** Advanced Technology, Botany, CHOAM Bureaucracy, Cultural Studies, Danger Sense, Data Analysis, Deductive Reasoning, Ecology, Emergency Medicine, Etiquette, Faction Lore/type, Genetics, Geology, House Politics, Imperial Politics, Infectious Diseases, Kanly, Philosophy, Physical Empathy, Physics, Poison, Psychiatry, Religion, Smuggling, Surgery, Traps, Virology

---

**Note:** When adding focuses with "/" (like "Music: baliset"), the game requires the format `+stats/focus add=Music/baliset` (using slash, not colon).

