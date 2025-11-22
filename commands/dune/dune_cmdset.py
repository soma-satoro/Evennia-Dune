"""
Dune Command Set

This cmdset includes all Dune-specific custom commands for the 2d20 system.
"""

from evennia.commands.cmdset import CmdSet

from commands.dune.CmdSheet import CmdSheet, CmdStats, CmdStress
from commands.dune.CmdRoll import CmdRoll, CmdMomentum, CmdDetermination
from commands.dune.CmdPool import CmdPool
from commands.dune.CmdComplication import CmdComplication
from commands.dune.CmdThreat import CmdThreat
from commands.dune.CmdExtendedTask import CmdExtendedTask
from commands.dune.CmdHouse import CmdHouse
from commands.dune.CmdRoster import CmdRoster, CmdRosterSet, CmdWho
from commands.dune.CmdOrganization import CmdOrg
from commands.dune.CmdPlanet import CmdPlanet
from commands.dune.CmdRoom import CmdRoom
from commands.dune.CmdInventory import CmdInventory
from commands.dune.CmdAsset import CmdAsset
from commands.dune.CmdChargen import CmdChargen
from commands.dune.CmdBio import CmdBio


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
        self.add(CmdStress())
        self.add(CmdComplication())
        self.add(CmdInventory())
        self.add(CmdAsset())
        self.add(CmdChargen())
        self.add(CmdBio())
        
        # Dice and mechanics commands
        self.add(CmdRoll())
        self.add(CmdMomentum())
        self.add(CmdDetermination())
        self.add(CmdPool())
        self.add(CmdThreat())
        self.add(CmdExtendedTask())
        
        # House management command (builder+ only for creation/editing)
        self.add(CmdHouse())
        
        # Roster management commands
        self.add(CmdRoster())
        self.add(CmdRosterSet())
        self.add(CmdWho())
        
        # Organization management command (builder+ only for creation/editing)
        self.add(CmdOrg())
        
        # Planet management command (builder+ only for creation/editing)
        self.add(CmdPlanet())
        
        # Room management command (builder+ only)
        self.add(CmdRoom())

