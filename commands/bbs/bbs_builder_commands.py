#commands/bbs/bbs_builder_commands.py


from evennia import default_cmds
from evennia.commands.default.muxcommand import MuxCommand
from evennia import create_object
from typeclasses.bbs_controller import BBSController
from typeclasses.groups import Group, get_group_by_name, get_character_groups

class CmdCreateBoard(MuxCommand):
    """
    Create a new board.

    Usage:
      +bbs/create <name> = <description> / public | private [/group=<group_name1>,<group_name2>...]
      
    Examples:
      +bbs/create Announcements = Game announcements / public
      +bbs/create Supernatural = Supernatural discussion / private /group=Vampire,Werewolf
    """
    key = "+bbs/create"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +bbs/create <name> = <description> / public | private [/group=<group_name1>,<group_name2>...]")
            return

        # Split into name_desc and privacy/group parts
        name_desc, remainder = self.args.split("=", 1)
        parts = remainder.split("/")
        
        if len(parts) < 2:
            self.caller.msg("Usage: +bbs/create <name> = <description> / public | private [/group=<group_name1>,<group_name2>...]")
            return
            
        description = parts[0].strip()
        privacy = parts[1].strip().lower()
        public = privacy == "public"
        
        # Check for group specification
        group_names = []
        if len(parts) > 2:
            for part in parts[2:]:
                if part.strip().lower().startswith("group="):
                    group_list = part.split("=")[1].strip()
                    group_names = [g.strip() for g in group_list.split(",")]
                    
                    # Verify all groups exist
                    for group_name in group_names:
                        group = get_group_by_name(group_name)
                        if not group:
                            self.caller.msg(f"Error: Group '{group_name}' does not exist.")
                            return

        name = name_desc.strip()

        # Ensure BBSController exists
        try:
            controller = BBSController.objects.get(db_key="BBSController")
        except BBSController.DoesNotExist:
            controller = create_object(BBSController, key="BBSController")
            controller.db.boards = {}  # Initialize with an empty boards dictionary if needed
            self.caller.msg("BBSController created.")

        # Create the board
        controller.create_board(name, description, public, group_names=group_names)
        msg = f"Board '{name}' created as {'public' if public else 'private'}"
        if group_names:
            msg += f" (restricted to groups: {', '.join(group_names)})"
        msg += f" with description: {description}"
        self.caller.msg(msg)

class CmdDeleteBoard(MuxCommand):
    """
    Delete a board and all its posts.

    Usage:
      +bbs/deleteboard <board_name>
    """
    key = "+bbs/deleteboard"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: +bbs/deleteboard <board_name>")
            return
        board_name = self.args.strip()

        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        board = controller.get_board(board_name)
        if not board:
            self.caller.msg(f"No board found with the name '{board_name}'.")
            return

        controller.delete_board(board_name)
        self.caller.msg(f"Board '{board_name}' and all its posts have been deleted.")

class CmdRevokeAccess(MuxCommand):
    """
    Revoke access to a private board.

    Usage:
      +bbs/revokeaccess <board_name> = <character_name>
    """
    key = "+bbs/revokeaccess"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +bbs/revokeaccess <board_name> = <character_name>")
            return
        board_name, character_name = [arg.strip() for arg in self.args.split("=", 1)]

        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        board = controller.get_board(board_name)
        if not board:
            self.caller.msg(f"No board found with the name '{board_name}'.")
            return
        if board['public']:
            self.caller.msg(f"Board '{board_name}' is public; access control is not required.")
            return
        if character_name not in board['access_list']:
            self.caller.msg(f"{character_name} does not have access to board '{board_name}'.")
            return
        controller.revoke_access(board_name, character_name)
        self.caller.msg(f"Access for {character_name} has been revoked from board '{board_name}'.")

class CmdListAccess(MuxCommand):
    """
    List all users who have access to a private board.

    Usage:
      +bbs/listaccess <board_name>
    """
    key = "+bbs/listaccess"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: +bbs/listaccess <board_name>")
            return
        board_name = self.args.strip()

        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        board = controller.get_board(board_name)
        if not board:
            self.caller.msg(f"No board found with the name '{board_name}'.")
            return
            
        output = []
        
        # Show group restrictions if any
        group_names = board.get('group_names', [])
        if group_names:
            output.append(f"Board '{board_name}' is restricted to members of the following groups:")
            
            # Get current group members for each group
            for group_name in group_names:
                output.append(f"\nGroup: {group_name}")
                group = get_group_by_name(group_name)
                if group:
                    members = group.members
                    if members:
                        output.append("Current group members with access:")
                        for member in members:
                            output.append(f"- {member.name}")
                    else:
                        output.append("No members in this group.")
                else:
                    output.append(f"Warning: Group '{group_name}' no longer exists!")
        
        # Show individual access list
        if board['public']:
            output.append(f"\nBoard '{board_name}' is public; individual access list is not applicable.")
        else:
            access_list = board.get('access_list', {})
            if not access_list:
                output.append(f"\nNo users have individual access to the private board '{board_name}'.")
            else:
                output.append("\nUsers with individual access:")
                for user, access_type in access_list.items():
                    output.append(f"- {user} ({access_type})")
        
        self.caller.msg("\n".join(output))

class CmdLockBoard(MuxCommand):
    """
    Lock a board to prevent new posts.

    Usage:
      +bbs/lockboard <board_name>
    """
    key = "+bbs/lockboard"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: +bbs/lockboard <board_name>")
            return
        board_name = self.args.strip()

        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        board = controller.get_board(board_name)
        if not board:
            self.caller.msg(f"No board found with the name '{board_name}'.")
            return

        if board.get('locked', False):
            self.caller.msg(f"Board '{board_name}' is already locked.")
            return

        controller.lock_board(board_name)
        self.caller.msg(f"Board '{board_name}' has been locked. No new posts can be made.")

class CmdPinPost(MuxCommand):
    """
    Pin a post to the top of a board.

    Usage:
      +bbs/pinpost <board_name_or_number>/<post_number>
    """
    key = "+bbs/pinpost"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "/" not in self.args:
            self.caller.msg("Usage: +bbs/pinpost <board_name_or_number>/<post_number>")
            return
        board_ref, post_number = [arg.strip() for arg in self.args.split("/", 1)]

        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        # Determine if board_ref is a name or a number
        try:
            board_ref = int(board_ref)
        except ValueError:
            pass

        board = controller.get_board(board_ref)
        if not board:
            self.caller.msg(f"No board found with the name or number '{board_ref}'.")
            return

        try:
            post_number = int(post_number)
        except ValueError:
            self.caller.msg("Post number must be an integer.")
            return
        posts = board['posts']
        if post_number < 1 or post_number > len(posts):
            self.caller.msg(f"Invalid post number. Board '{board['name']}' has {len(posts)} posts.")
            return

        controller.pin_post(board['id'], post_number - 1)
        self.caller.msg(f"Post {post_number} in board '{board['name']}' has been pinned to the top.")


class CmdUnpinPost(MuxCommand):
    """
    Unpin a pinned post from the top of a board.

    Usage:
      +bbs/unpinpost <board_name_or_number>/<post_number>
    """
    key = "+bbs/unpinpost"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "/" not in self.args:
            self.caller.msg("Usage: +bbs/unpinpost <board_name_or_number>/<post_number>")
            return
        board_ref, post_number = [arg.strip() for arg in self.args.split("/", 1)]

        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        # Determine if board_ref is a name or a number
        try:
            board_ref = int(board_ref)
        except ValueError:
            pass

        board = controller.get_board(board_ref)
        if not board:
            self.caller.msg(f"No board found with the name or number '{board_ref}'.")
            return

        try:
            post_number = int(post_number)
        except ValueError:
            self.caller.msg("Post number must be an integer.")
            return
        posts = board['posts']
        if post_number < 1 or post_number > len(posts):
            self.caller.msg(f"Invalid post number. Board '{board['name']}' has {len(posts)} posts.")
            return

        controller.unpin_post(board['id'], post_number - 1)
        self.caller.msg(f"Post {post_number} in board '{board['name']}' has been unpinned.")


class CmdEditBoard(MuxCommand):
    """
    Edit the settings or description of a board.

    Usage:
      +bbs/editboard <board_name> = <field>, <new_value>

    Fields:
      description - Change the board's description
      public - Set to true/false to change board visibility

    Example:
      +bbs/editboard Announcements = description, A board for official announcements.
      +bbs/editboard Announcements = public, true
    """
    key = "+bbs/editboard"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +bbs/editboard <board_name> = <field>, <new_value>")
            return
        board_name, updates = [arg.strip() for arg in self.args.split("=", 1)]
        field, new_value = [arg.strip() for arg in updates.split(",", 1)]
        field = field.lower()

        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        board = controller.get_board(board_name)
        if not board:
            self.caller.msg(f"No board found with the name '{board_name}'.")
            return

        if field == "description":
            board['description'] = new_value
            msg = f"Description set to '{new_value}'"
        elif field == "public":
            board['public'] = new_value.lower() in ["true", "yes", "1"]
            msg = f"Public status set to {board['public']}"
        else:
            self.caller.msg(f"Invalid field '{field}'. You can edit 'description' or 'public'.")
            return

        controller.save_board(board_name, board)
        self.caller.msg(f"Board '{board_name}' has been updated. {msg}.")

class CmdEditBoardGroups(MuxCommand):
    """
    Edit the group restrictions of a board.

    Usage:
      +bbs/editboard/groups <board_name> = <group_name1> [,<group_name2>...]
      +bbs/editboard/groups <board_name> =    # Clear all group restrictions

    Examples:
      +bbs/editboard/groups Supernatural = Vampire,Werewolf,Mage
      +bbs/editboard/groups Supernatural =    # Remove all group restrictions
    """
    key = "+bbs/editboard/groups"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +bbs/editboard/groups <board_name> = <group_name1> [,<group_name2>...]")
            return

        board_name, group_list = [arg.strip() for arg in self.args.split("=", 1)]
        
        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        board = controller.get_board(board_name)
        if not board:
            self.caller.msg(f"No board found with the name '{board_name}'.")
            return

        # Handle empty value to clear group restrictions
        if not group_list:
            board['group_names'] = []
            controller.save_board(board_name, board)
            self.caller.msg(f"Cleared all group restrictions from board '{board_name}'.")
            return

        # Process group list
        group_names = [g.strip() for g in group_list.split(",") if g.strip()]
        
        # Verify all groups exist
        for group_name in group_names:
            group = get_group_by_name(group_name)
            if not group:
                self.caller.msg(f"Error: Group '{group_name}' does not exist.")
                return

        # Update board with new group list
        board['group_names'] = group_names
        controller.save_board(board_name, board)
        self.caller.msg(f"Updated group restrictions for board '{board_name}' to: {', '.join(group_names)}")

class CmdGrantAccess(MuxCommand):
    """
    Grant access to a private board.

    Usage:
      +bbs/grantaccess <board_name> = <character_name> [/readonly]

    This command grants full access to a character by default. If "/readonly" is specified,
    the character is granted read-only access instead.

    Examples:
      +bbs/grantaccess Announcements = John
      +bbs/grantaccess Announcements = John /readonly
    """
    key = "+bbs/grantaccess"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +bbs/grantaccess <board_name> = <character_name> [/readonly]")
            return
        board_name, args = [arg.strip() for arg in self.args.split("=", 1)]
        character_name, *options = [arg.strip() for arg in args.split(" ")]

        # Determine access level
        access_level = "read_only" if "/readonly" in options else "full_access"

        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return

        board = controller.get_board(board_name)
        if not board:
            self.caller.msg(f"No board found with the name '{board_name}'.")
            return

        controller.grant_access(board_name, character_name, access_level=access_level)
        access_type = "read-only" if access_level == "read_only" else "full access"
        self.caller.msg(f"Granted {access_type} to {character_name} for board '{board_name}'.")

class CmdAddGroup(MuxCommand):
    """
    Add a group restriction to a board.

    Usage:
      +bbs/addgroup <board_name> = <group_name>
    """
    key = "+bbs/addgroup"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +bbs/addgroup <board_name> = <group_name>")
            return
            
        board_name, group_name = [arg.strip() for arg in self.args.split("=", 1)]
        
        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return
            
        result = controller.add_group_to_board(board_name, group_name)
        self.caller.msg(result)

class CmdRemoveGroup(MuxCommand):
    """
    Remove a group restriction from a board.

    Usage:
      +bbs/removegroup <board_name> = <group_name>
    """
    key = "+bbs/removegroup"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +bbs/removegroup <board_name> = <group_name>")
            return
            
        board_name, group_name = [arg.strip() for arg in self.args.split("=", 1)]
        
        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return
            
        result = controller.remove_group_from_board(board_name, group_name)
        self.caller.msg(result)

class CmdListGroups(MuxCommand):
    """
    List all groups associated with a board.

    Usage:
      +bbs/listgroups <board_name>
    """
    key = "+bbs/listgroups"
    locks = "cmd:perm(Builder)"
    help_category = "Event & Bulletin Board"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: +bbs/listgroups <board_name>")
            return
            
        board_name = self.args.strip()
        
        controller = BBSController.objects.get(db_key="BBSController")
        if not controller:
            self.caller.msg("BBSController not found.")
            return
            
        board = controller.get_board(board_name)
        if not board:
            self.caller.msg(f"No board found with the name '{board_name}'.")
            return
            
        group_names = controller.get_board_groups(board_name)
        if not group_names:
            self.caller.msg(f"Board '{board_name}' has no group restrictions.")
        else:
            self.caller.msg(f"Board '{board_name}' is restricted to the following groups:")
            for group_name in group_names:
                group = get_group_by_name(group_name)
                if group:
                    member_count = group.get_member_count()
                    self.caller.msg(f"- {group_name} ({member_count} members)")
                else:
                    self.caller.msg(f"- {group_name} (WARNING: Group no longer exists!)")
