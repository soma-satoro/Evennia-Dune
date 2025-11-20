"""
Dune Command Set

This cmdset includes all Dune-specific custom commands for the 2d20 system.
"""

from evennia.commands.cmdset import CmdSet

from commands.dune.CmdSheet import CmdSheet, CmdStats, CmdFocus, CmdStress
from commands.dune.CmdRoll import CmdRoll, CmdMomentum, CmdDetermination
from commands.dune.CmdHouse import (
    CmdHouse, CmdHouseCreate, CmdHouseSet, CmdHouseDomain,
    CmdHouseRole, CmdHouseEnemy, CmdHouseMember
)
from commands.dune.CmdRoster import CmdRoster, CmdRosterSet, CmdWho
from commands.dune.CmdOrganization import CmdOrg, CmdOrgCreate, CmdOrgSet, CmdOrgRole


class DuneCmdSet(CmdSet):
    """
    This cmdset includes all Dune custom commands.
    """
    key = "Dune"
    priority = 1

    def at_cmdset_creation(self):
        """
        Populates the cmdset with all Dune commands.
        """
        # Character management commands
        self.add(CmdSheet())
        self.add(CmdStats())
        self.add(CmdFocus())
        self.add(CmdStress())
        
        # Dice and mechanics commands
        self.add(CmdRoll())
        self.add(CmdMomentum())
        self.add(CmdDetermination())
        
        # House management commands (builder+ only for creation/editing)
        self.add(CmdHouse())
        self.add(CmdHouseCreate())
        self.add(CmdHouseSet())
        self.add(CmdHouseDomain())
        self.add(CmdHouseRole())
        self.add(CmdHouseEnemy())
        self.add(CmdHouseMember())
        
        # Roster management commands
        self.add(CmdRoster())
        self.add(CmdRosterSet())
        self.add(CmdWho())
        
        # Organization management commands (builder+ only for creation/editing)
        self.add(CmdOrg())
        self.add(CmdOrgCreate())
        self.add(CmdOrgSet())
        self.add(CmdOrgRole())

