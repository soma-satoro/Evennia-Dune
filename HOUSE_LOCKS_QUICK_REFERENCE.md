# House Lock Functions - Quick Reference

## Basic Syntax

```
@lock/traverse <exit> = <lock_function>
@fail <exit> = <message when denied>
```

## Lock Functions

| Function | Usage | Description |
|----------|-------|-------------|
| `house(Name)` | `house(Atreides)` | Specific House only |
| `hashouse()` | `hashouse()` | Any House member |
| `nohouse()` | `nohouse()` | No House affiliation |
| `housetype(Type)` | `housetype(Major)` | Specific House type |
| `housemintype(Type)` | `housemintype(Minor)` | Minimum House type |
| `houseor(H1,H2,...)` | `houseor(Atreides,Molay)` | Multiple Houses |
| `not_house(Name)` | `not_house(Harkonnen)` | Exclude specific House |
| `houserole(Role)` | `houserole(Ruler)` | Specific House role |

## House Types

- **Nascent House** or **Nascent**
- **House Minor** or **Minor**
- **House Major** or **Major**
- **Great House** or **Great**

Hierarchy: Nascent < Minor < Major < Great

## House Roles

Ruler, Consort, Advisor, Chief Physician, Councilor, Envoy, Heir, Marshal, Scholar, Spymaster, Swordmaster, Treasurer, Warmaster

## Quick Examples

### Single House Access
```
@lock/traverse palace = house(Atreides)
@fail palace = Only House Atreides members may enter.
```

### Any Noble Access
```
@lock/traverse landsraad = hashouse()
@fail landsraad = This area is restricted to noble Houses.
```

### Multiple House Access (Allies)
```
@lock/traverse coalition = houseor(Atreides, Molay, Vernius)
@fail coalition = Only coalition members may enter.
```

### Minimum House Type
```
@lock/traverse court = housemintype(Major)
@fail court = Only Major Houses and above may attend.
```

### Exclude Enemy
```
@lock/traverse territory = not_house(Harkonnen)
@fail territory = Harkonnen agents are not welcome here.
```

### Role-Based
```
@lock/traverse vault = houserole(Treasurer)
@fail vault = Only the Treasurer may access the vault.
```

### Complex Combination
```
@lock/traverse secure = house(Atreides) AND houserole(Warmaster)
@fail secure = Restricted to House Atreides military leadership.
```

## Common Patterns

### House Palace
```
@lock/traverse entrance = house(YourHouse)
@lock/traverse throne = houserole(Ruler) OR houserole(Heir)
@lock/traverse war_room = house(YourHouse) AND houserole(Warmaster)
@lock/traverse treasury = houserole(Treasurer)
```

### Diplomatic Area
```
@lock/traverse hall = housemintype(Minor)
@lock/traverse vip_room = housemintype(Major)
@lock/traverse imperial = housetype(Great)
```

### Hostile Territory
```
@lock/traverse checkpoint = house(YourHouse) OR perm(Builder)
@lock/traverse inner = house(YourHouse) AND not_house(Enemy)
```

## Combining Locks

| Operator | Example | Meaning |
|----------|---------|---------|
| **AND** | `house(A) AND houserole(Ruler)` | Both must be true |
| **OR** | `house(A) OR house(B)` | Either can be true |
| **NOT** | `NOT house(Harkonnen)` | Inverse/opposite |

**Complex:**
```
(house(A) OR house(B)) AND NOT house(C)
```
House A or B, but never House C.

## Always Include Staff Bypass

```
@lock/traverse area = <your_lock> OR perm(Builder)
```

This ensures staff can always access for testing/admin.

## Testing

```
@examine <exit>              # View lock
@examine/locks <exit>        # Detailed lock info
@lock/del/traverse <exit>    # Remove lock
```

## Tips

1. **Case-insensitive:** `house(Atreides)` = `house(atreides)`
2. **Partial names work:** `house(Atreides)` can match "House Atreides"
3. **Test thoroughly:** Use different characters with various affiliations
4. **Clear fail messages:** Tell players WHY they can't pass
5. **Layer security:** Multiple checkpoints with escalating restrictions

## Common Issues

| Problem | Solution |
|---------|----------|
| Everyone blocked | Add `OR perm(Builder)` for staff |
| Wrong House | Check spelling, check character's house |
| Role doesn't work | Verify character has role in House |
| Syntax error | Check parentheses and spelling |

## Full Example: House Complex

```
# Main Gate
@dig Palace = palace_gate, out
@lock/traverse palace_gate = house(Atreides) OR perm(Builder)
@fail palace_gate = The guards cross their spears. "House Atreides only."

# Public Hall (guests allowed)
@open hall
@lock/traverse hall = hashouse()
@fail hall = This area is for nobles only.

# Private Wing
@open private
@lock/traverse private = house(Atreides)
@fail private = This wing is restricted to House members.

# War Room
@open warroom
@lock/traverse warroom = house(Atreides) AND houserole(Warmaster)
@fail warroom = Restricted to the Warmaster.

# Treasury
@open vault
@lock/traverse vault = houserole(Treasurer)
@fail vault = Only the Treasurer may enter.

# Throne Room
@open throne
@lock/traverse throne = houserole(Ruler) OR houserole(Consort)
@fail throne = Only the Duke and Duchess may enter.
```

---

**See:** `HOUSE_LOCKS_GUIDE.md` for detailed documentation and advanced usage.

