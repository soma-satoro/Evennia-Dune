# Places System Guide

## Overview

The Places system allows you to create sub-locations within a room where players can have private conversations. This is perfect for creating distinct social spaces like tables in a restaurant, corners of a bar, or different seating areas in a lounge.

## Core Concepts

### What is a Place?

A **place** is a designated area within a room where characters can gather and communicate privately. Characters at a place can see and hear each other using table talk, while characters elsewhere in the room cannot hear these conversations.

### How It Works

1. **Places are room-based**: Each room maintains its own list of places
2. **Characters join places**: A character can join one place at a time
3. **Communication is private**: Table talk only reaches people at the same place
4. **Dynamic creation**: Players can create places on-the-fly
5. **No room modification needed**: The system works with standard Evennia rooms

## Command Reference

### Creating Places

```
+place/create <name>[=<description>]
```

Creates a new place in the current room.

**Examples:**
```
+place/create Corner Table
+place/create Bar=A long mahogany bar with leather-padded stools
+place/create Fireplace Nook=A cozy alcove with overstuffed chairs facing a crackling fire
```

### Joining Places

```
+place/join <name>
```

Join an existing place. If you're already at another place, you'll automatically leave it.

**Examples:**
```
+place/join Corner Table
+place/join Bar
```

### Leaving Places

```
+place/leave
```

Leave your current place and return to the general room.

### Viewing Places

```
+place/list
```

Lists all places in the current room, showing who's at each place.

**Example Output:**
```
Places in The Rusty Anchor Tavern:

┌─────────────────┬───────────────────┬────────────────────────┐
│ Place Name      │ People            │ Description            │
├─────────────────┼───────────────────┼────────────────────────┤
│ Corner Table    │ Jakob, Sarah      │ A cozy corner with...  │
│ Bar             │ Marcus, Elena     │ A long mahogany bar... │
│ Fireplace Nook  │ (empty)           │ A cozy alcove with...  │
└─────────────────┴───────────────────┴────────────────────────┘
```

### Checking Who's at a Place

```
+place/who [<name>]
```

Without a name, shows who's at your current place. With a name, shows who's at that specific place.

**Examples:**
```
+place/who                  # Shows who's at your place
+place/who Corner Table     # Shows who's at Corner Table
```

### Checking Your Current Place

```
+place
```

Shows information about your current place.

### Managing Places

```
+place/desc <name>=<description>
```

Sets or changes a place's description. You must be the creator or a staff member.

**Example:**
```
+place/desc Corner Table=A dark corner with a scarred wooden table
```

```
+place/delete <name>
```

Deletes a place. You must be the creator or a staff member. Everyone at the place will be removed from it.

**Example:**
```
+place/delete Corner Table
```

## Table Talk Commands

Once you've joined a place, use the `tt` command to communicate with others at your place.

### Basic Syntax

```
tt <message>         # Say something
tt :<message>        # Pose an action
tt \<message>        # Emit a message
```

### Examples

**Saying something:**
```
tt Hello everyone!
```
Output: `At Corner Table, Jakob says, "Hello everyone!"`

**Posing an action:**
```
tt :smiles warmly at the group.
```
Output: `At Corner Table, Jakob smiles warmly at the group.`

**Emitting a message:**
```
tt \The conversation grows more animated.
```
Output: `At Corner Table, The conversation grows more animated.`

### Language Support

Table talk supports the same language features as regular communication:

```
tt "~Bonjour mes amis." Hello everyone.
tt :"~Bonjour," he says with a smile.
```

The `~` marker indicates speech in your set language. Only those who understand the language will see the actual words.

## Usage Scenarios

### Scenario 1: Restaurant Tables

```
> +place/create Table 1=A two-person table by the window
> +place/create Table 2=A four-person booth in the corner
> +place/create Table 3=A large round table in the center

> +place/join Table 2
You join Table 2.

> tt Hey, did you hear about the mayor?
At Table 2, Jakob says, "Hey, did you hear about the mayor?"
```

Characters at other tables won't hear this conversation.

### Scenario 2: Bar Seating

```
> +place/create Bar Stools=The main bar with a dozen stools
> +place/create Back Booth=A discrete booth in the back

> +place/join Bar Stools
You join Bar Stools.

> tt :leans over to the bartender
At Bar Stools, Sarah leans over to the bartender.

> tt "~I need some information." whispers quietly.
At Bar Stools, Sarah whispers quietly, "I need some information."
```

### Scenario 3: Meeting Spaces

```
> +place/create Council Circle=A circle of ornate chairs
> +place/join Council Circle
You join Council Circle.

> tt \The council members gather closely.
At Council Circle, The council members gather closely.

> tt :addresses the group solemnly
At Council Circle, Marcus addresses the group solemnly.
```

## Best Practices

### For Players

1. **Create descriptive places**: Give places evocative descriptions to enhance immersion
2. **Join before talking**: Remember to join a place before using table talk
3. **Use regular commands for public speech**: Use `say`, `pose`, and `emit` for room-wide communication
4. **Clean up**: Delete places you created when done, or leave them for others

### For Staff

1. **Pre-create common places**: Set up standard places in frequently-used rooms
2. **Monitor place usage**: Check if players are creating appropriate places
3. **Set examples**: Use descriptive place descriptions to set the tone

### For Storytellers

1. **Use places for scene management**: Organize large scenes by separating groups
2. **Create temporary places**: Make special places for specific events
3. **Combine with regular RP**: Use places for private conversations while keeping main action public

## Technical Details

### Data Storage

- **Room level**: Places are stored in `room.db.places` as a dictionary
- **Character level**: Current place is tracked in `character.db.place` as a string
- **No database changes**: Works with standard Evennia objects

### Persistence

- Places persist as long as the room exists
- Characters lose their place assignment when they disconnect (automatic cleanup)
- Empty places remain until explicitly deleted

### Permissions

- **Anyone** can create, join, and leave places
- **Creators and staff** can modify or delete places
- Place ownership is tracked by character ID

## Troubleshooting

### "You must be at a place to use table talk"

You need to join a place first:
```
+place/list          # See available places
+place/join <name>   # Join a place
```

### "There's no one at this place to talk to"

You're at a place but alone. Others need to join:
- Wait for others to join
- Invite others IC to come to your place
- Leave and join a different place

### "A place called '...' already exists"

That place name is taken. Either:
- Join the existing place: `+place/join <name>`
- Choose a different name: `+place/create <different name>`

### Can't delete a place

You can only delete places you created or you need staff permissions:
- If you're staff, you can delete any place
- If not, ask the creator or a staff member
- Or simply leave the place and create a new one

## Integration with Other Systems

### Language System

Places fully support the language system. Characters at a place will only understand speech in languages they know, just like in regular RP.

### Pose Breaks

Table talk includes pose breaks (visual separators) to distinguish speakers, just like regular poses.

### OOC Areas

In OOC areas, pose breaks are automatically disabled to keep things cleaner.

### Watch System

Staff using the watch system can see all table talk, even at places they're not at.

## Examples of Creative Uses

### Private Investigations
```
+place/create Shadowy Corner=A dimly lit corner far from prying eyes
+place/join Shadowy Corner
tt :passes a folded note across the table
tt "~Meet me at midnight," whispers in coded language.
```

### Multiple Conversations
```
# At Table 1
tt :discusses the upcoming ball with excitement

# Meanwhile at Table 2
tt :argues quietly about recent political developments

# Both happening simultaneously in the same room!
```

### Dynamic Scene Splitting
```
# Start together
say Let's split up and search for clues.

# Create separate investigation areas
+place/create Study Desk
+place/create Bookshelf Area
+place/create Filing Cabinets

# Each group investigates separately
+place/join Study Desk
tt :carefully searches through the papers
```

## Conclusion

The Places system adds depth to your RP by allowing multiple simultaneous conversations in the same room. Use it to create intimate moments, organize large scenes, or simply enhance the sense of physical space in your game world.

For technical support or questions, contact game staff or refer to the CommonMux README.md file.

