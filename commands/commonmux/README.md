# CommonMux - Custom Commands

This directory contains all custom CommonMux commands. They are fairly generic MUSH-style commands like page, +who, +where, but also includes some other elements that could be game-specific such as languages and language code, pools that match Chronicles of Darkness (blood, willpower, glamour, essence, etc.), weather, and more.

I've described any modifications that need to be made to these files or others in order to get them to work if you are using this code outside of the PyReach file structure.

## Command Set

All commands in this directory are organized into the `CommonMuxCmdSet` commandset, which can be imported and added to other commandsets easily.

### Usage

Add the following to your default_cmdsets.py file in the import section near the top:
```python
from commands.commonmux.commonmux_cmdset import CommonMuxCmdSet
```

In your cmdset's at_cmdset_creation method add the following:
```python
self.add(CommonMuxCmdSet())
```

## Available Commands

### Character & Roleplay Commands
- **CmdAlias** - Set and manage character aliases
- **CmdAlts** - Manage alternate characters
- **CmdEmit** - Emit messages to a room
- **CmdPlace** - Create and manage places within a room
- **CmdPose** - Pose/emote actions
- **CmdSay** - Say something in character
- **CmdShortDesc** - Set a short description for your character
- **CmdTableTalk** - Talk only to people at your place (requires places)

### Communication Commands
- **CmdPage** - Send private messages to other players (by character name)
- **CmdText** - Text/SMS-style messages

### Information & Social Commands
- **CmdStaff** - Display staff roster
- **CmdWatch** - Watch/monitor players
- **CmdWeather** - Display or set weather information
- **CmdWho** - List connected players
- **CmdCensus** - Display player census information

### Game Mechanics Commands
- **CmdPool** - Manage power point pools
- **CmdSpend** - Spend pool points
- **CmdGain** - Gain pool points
- **CmdLanguage** - Handle multi-language communication

## File Structure

```
commonmux/
├── __init__.py                 # Package initialization
├── commonmux_cmdset.py         # Main commandset containing all commands
├── README.md                   # This file
├── CmdAlias.py                 # Alias management
├── CmdAlts.py                  # Alt character management
├── CmdEmit.py                  # Room emits
├── CmdFinger.py                # OOC/IC Character information
├── CmdLanguage.py              # Language system
├── CmdPage.py                  # Private messaging
├── CmdPlace.py                 # Places management system
├── CmdPool.py                  # Resource/power point management
├── CmdPose.py                  # Posing/emoting
├── CmdSay.py                   # In-character speech
├── CmdShortDesc.py             # Short character descriptions
├── CmdStaff.py                 # Staff roster
├── CmdTableTalk.py             # Table talk at places
├── CmdTxt.py                   # Text messages
├── CmdWatch.py                 # Watching/monitoring
├── CmdWeather.py               # Weather system
├── CmdWho.py                   # Who list and census
└── notes.py                    # Set notes on characters
```

## Integration

The `CommonMuxCmdSet` is integrated into the main `CharacterCmdSet` in `commands/default_cmdsets.py`, making all these commands available to all characters in the game.

### File Specific Integration

#### **CmdWeather.py Updates**
CmdWeather requires some additional modification in order for it to start working. Weather utilizes two APIs from outside sources: one from tidesandcurrents.noaa.gov, and another from openweather.org. To get this to work properly, one must set up a new API link as found on the NOAA and Open Weather websites. Just make sure to change this link:
```python
    def get_tide_info(self):
        tide_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=9410170&product=predictions&datum=STND&time_zone=lst_ldt&interval=hilo&units=english&format=json" # Example API key
```
and to modify the following information starting on line 142 and ending on 144:
```python
            # OpenWeatherMap API call
            api_key = "549ac137ad7db9fb5d6f68b590d488a6" # Example API key
            city_id = "5391811"  # San Diego city ID
```
The links to the Open Weather API are designed to be updated based on the attributes above, so no need to modify them.

CmdPose, CmdSay and CmdEmit have a language mixin to allow people to utilize the language code. If you are not using the language code, comment out the following lines:

#### **CmdPose.py: Lines 115-120**
```python
# Check if there's a language-tagged speech and set speaking language
 if "~" in self.args:
     speaking_language = caller.get_speaking_language()
     if not speaking_language:
         caller.msg("You need to set a speaking language first with +language <language>")
         return
```
#### **CmdSay.py: lines 58, 86-107**
Line 58 is directly linked to language processing. Lines 86-107 is what catches language code being used and checks to see if the receiver understands the language.

Optionally, instead of commenting out anything, you can replace lines 98-103 with the following code:
```python
if receiver != caller:
    _, msg_understand, _, _ = caller.prepare_say(speech, viewer=receiver, skip_english=True)
    receiver.msg(msg_understand)
else:
    msg_self, _, _, _ = caller.prepare_say(speech, viewer=receiver, skip_english=True)
    receiver.msg(msg_self)
```
This will make messages seen by the receiver marked as msg_understand, bypassing language entirely.

#### **CmdEmit.py: lines 50-55**
The following lines control the language requirement checks.
```python
# Check if there's a language-tagged speech and set speaking language
 if "~" in processed_args or 'language' in self.switches:
     speaking_language = caller.get_speaking_language()
     if not speaking_language:
         caller.msg("You need to set a speaking language first with +language <language>")
         return
```

Another option is to have each command ignore the tilde )(~) key, which is what indicates that a language is being used, as it will always default to English.

Language commands are stored in the core PyReach folder, with a database file located in pyreach/world/utils. If you are not using this code with PyReach, you obviously cannot use the language files.

#### **CmdPlace.py & CmdTableTalk.py - Places System**

**What are Places?**

Places are like "quasi-rooms" that exist within the structure of a room, allowing for players to communicate with one another without being overheard by other players occupying the same room. An example usage would be having specific tables in a restaurant, where players can communicate through tabletalk to all players who occupy their table, or they can use the standard say/emit/pose commands to communicate with the rest of the room.

**How Places Work:**

The Places system is now built directly into CommonMux with the `CmdPlace` command, which provides a full suite of place management tools:

**Available Place Commands:**
- `+place/create <name>[=<description>]` - Create a new place in the current room
- `+place/join <name>` - Join an existing place
- `+place/leave` - Leave your current place
- `+place/list` - See all places in the room and who's at each one
- `+place/who [<name>]` - See who's at a specific place (or your current place)
- `+place/desc <name>=<description>` - Set or change a place's description
- `+place/delete <name>` - Delete a place (creator or staff only)
- `+place` - Show your current place

**Integration:**

Places are stored as a dictionary on the room object (`location.db.places`), and each character tracks which place they're at via `character.db.place`. The system is completely self-contained and requires no additional room typeclass modifications to work.

**Using Table Talk:**

Once you've joined a place using `+place/join <name>`, you can use the `tt` (table talk) command to communicate only with people at your place:

- `tt <message>` - Say something (like the say command)
- `tt :<message>` - Pose something (like the pose command)
- `tt \<message>` - Emit something (like the @emit command)

Table talk supports all the same language features as regular say/pose/emit commands.

**Example Usage:**
```
+place/create Corner Table=A cozy corner with plush chairs and dim lighting
+place/join Corner Table
tt Hello everyone at this table!
tt :smiles warmly at the group
tt \The conversation grows animated.
+place/leave
```

**Disabling Places:**

If you don't want to use the places system, you can safely disable both commands by commenting them out in `commonmux_cmdset.py`:
```python
        #self.add(CmdPlace())
        #self.add(CmdTableTalk())
```

#### CmdPage.py

For page, since there are some conflicts with base evennia files in the most recent build, you must specifically identify the command in your default_cmdsets.py file and make sure it is added at the account level so as to override the existing Evennia 'tell' system.

This is what that looks like:
In your imports, specify the following:
```python
from commands.commonmux.CmdPage import CmdPage
```

Then your account level commands should have something like this (as well as any other account-level commands you might identify, such as if you're using the mail contrib)

```python
class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(CmdPage())
```

The reason this command exists like this is that on Evennia, a 'tell' (page, in MUSH language) is used for account-to-account communication. It doesn't allow for emotes as it's intended to just be OOC to OOC communication.

Pages are intended as OOC communication, however most traditional MUSHers are used to being able to type 'p :some emote' and have it show up as an action on the other person's end. Additionally, since account names and character names could differ wildly and might be confusing for a player, the puppeted character name is shown instead of the account name. If your account name is Soma, for example, but your character's name is Jakob, then using 'p jim=Hello!' will show 'From afar, Jakob pages 'Hello!''. 

If this is not something you feel is necessary, then just ignore the above instructions as the Evennia-level command will override secondary cmdsets.

#### CmdText.py

You can disable this command in default_cmdsets.py if your game does not take place in the modern day. Nothing else is reliant on this command and it should not break anything to remove it.

#### CmdPool

As far as I know, this requires the characters.py typeclass from PyReach since all pools are based around Chronicles of Darkness 1st and 2nd editions. We derive most of the values for these pools from stats, which is done through the caller.db.stats.get() method. Willpower is derived from the sum of attributes Resolve + Composure, and each power stat pool (blood, essence, mana, etc.) is derived based on the supernatural power advantage. If you are not using PyReach, disable these commands.

## Adding New Commands

To add a new command to the CommonMux command set:

1. Create your command file in this directory (e.g., `CmdNewCommand.py`)
2. Add the import to `commonmux_cmdset.py`
3. Add the command instance to the `at_cmdset_creation` method in `CommonMuxCmdSet`
4. The command will automatically be available to all characters

Example:
```python
# In commonmux_cmdset.py
from commands.commonmux.CmdNewCommand import CmdNewCommand

class CommonMuxCmdSet(CmdSet):
    # ...
    def at_cmdset_creation(self):
        # ... other commands ...
        self.add(CmdNewCommand())
```

## Command Categories

Commands are organized by functionality in the commandset for better maintainability:
- Character and roleplay commands (alias, alts, emit, pose, say, etc.)
- Communication commands (page, text)
- Information and social commands (staff, finger, watch, weather, who, census)
- Game mechanics commands (pool, spend, gain, language)

## See Also

- [Default CommandSets](../default_cmdsets.py) - Main commandset integration
- [BBS CommandSet](../bbs/bbs_cmdset.py) - Similar pattern for BBS commands

