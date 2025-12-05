# House Skills Quick Reference

## The Five Skills

| Skill | Represents | Used For |
|-------|-----------|----------|
| **Battle** | Military power & tactics | War, defense, military operations |
| **Communicate** | Diplomacy & influence | Court politics, negotiations, intelligence |
| **Discipline** | Loyalty & stability | Security, morale, resisting infiltration |
| **Move** | Response time | Crisis management, rapid deployment |
| **Understand** | Academic excellence | Research, technology, innovation |

## Starting Values by House Type

| House Type | Skill Values |
|-----------|--------------|
| **Great House** | 9, 8, 7, 6, 5 |
| **House Major** | 8, 7, 6, 5, 4 |
| **House Minor** | 7, 6, 6, 5, 4 |
| **Nascent House** | 6, 5, 5, 4, 4 |

## Commands

```
+house/skill <house>/values              Show recommended values
+house/skill <house>/init=b,c,d,m,u     Initialize all skills
+house/skill <house>/set <skill>=<#>    Set individual skill
+house <house>                           View skills in house display
```

## Quick Examples

### Military House (Minor)
```
+house/skill Garrison/init=8,4,7,5,4
Battle: 8, Communicate: 4, Discipline: 7, Move: 5, Understand: 4
```

### Diplomatic House (Minor)
```
+house/skill Envoy/init=4,8,6,7,4
Battle: 4, Communicate: 8, Discipline: 6, Move: 7, Understand: 4
```

### Scientific House (Major)
```
+house/skill Technius/init=6,7,5,4,8
Battle: 6, Communicate: 7, Discipline: 5, Move: 4, Understand: 8
```

### Balanced House (Minor)
```
+house/skill Balanced/init=6,7,6,5,4
Battle: 6, Communicate: 7, Discipline: 6, Move: 5, Understand: 4
```

## Domain-Skill Relationships

| Domain | Primary Skills | Secondary Skills |
|--------|---------------|------------------|
| **Artistic** | Understand, Communicate | - |
| **Espionage** | Move, Communicate | Discipline |
| **Farming** | Understand | Discipline |
| **Industrial** | Understand | Battle |
| **Kanly** | Battle, Move | Discipline |
| **Military** | Battle, Discipline | Move |
| **Political** | Communicate | Move |
| **Religion** | Discipline | Communicate |
| **Science** | Understand | Move |

## Assignment Tips

1. **Match domains**: High skills should align with your primary domains
2. **Concept first**: Let House concept drive skill allocation
3. **Balance vs. Specialization**: 
   - Specialized: One skill 8-9, others lower
   - Balanced: More even distribution
4. **No orphans**: Every high skill should have domain support
5. **Story matters**: Skills should reflect House reputation

## Skill Descriptions (Expanded)

### Battle
- Quality of soldiers, spacecraft, weapons
- Tactical and strategic leadership
- Military positioning and readiness
- **Not just numbers**: Even small forces with high Battle are deadly

### Communicate
- Diplomatic reputation and favors
- Spy networks and intelligence
- Court influence
- **Both overt and covert**: Includes espionage alongside diplomacy

### Discipline
- Loyalty through love OR fear (both work!)
- Internal security and cohesion
- Resistance to infiltration
- **Pre-mission check**: Often tested before important operations

### Move
- Agent placement across Imperium
- Rapid response to crises
- **Not just military**: Includes diplomatic speed
- Resource accessibility

### Understand
- Scientific research and innovation
- Technological advancement
- Artistic and craft excellence
- **Development key**: Vital for House projects and upgrades

## Common Mistakes to Avoid

❌ **Don't:** Assign all high values to combat skills
✓ **Do:** Consider political and economic needs

❌ **Don't:** Ignore domain relationships
✓ **Do:** Ensure skills match your domains

❌ **Don't:** Make all skills equal
✓ **Do:** Create a distinctive profile

❌ **Don't:** Forget Discipline
✓ **Do:** Remember internal loyalty matters

❌ **Don't:** Skimp on Understand if you want tech/arts
✓ **Do:** Invest in innovation if that's your path

## Staff Commands Only

All skill management requires Builder+ permission:
- `/skill` - All skill-related commands
- View skills with `+house <name>` (available to all)

## Maintenance Notes

- Skills require Wealth to maintain (future system)
- Skills can improve through Ventures (future system)
- Without investment, skills may degrade over time
- Major story achievements may grant +1 to a skill

---

**Need more detail?** See `HOUSE_SKILLS_README.md` for complete documentation.

