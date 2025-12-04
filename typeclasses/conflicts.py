"""
Base Conflict System for Dune 2d20

Provides common conflict mechanics shared across all conflict types:
- Turn order and initiative
- Basic actions (move, use asset, attack, etc.)
- Extended tasks
- Asset targeting
- Trait/asset creation
"""

from evennia.objects.objects import DefaultObject
from .objects import ObjectParent


class BaseConflict(ObjectParent, DefaultObject):
    """
    Base class for all conflict types.
    
    Provides common mechanics:
    - Turn order and initiative
    - Basic actions
    - Extended tasks
    - Asset management
    """
    
    def at_object_creation(self):
        """Initialize base conflict state"""
        super().at_object_creation()
        
        # Participants
        self.db.participants = []  # List of character objects
        
        # Turn order
        self.db.turn_order = []  # List of characters in turn order
        self.db.current_turn_index = 0  # Index of current turn
        self.db.current_round = 1  # Current round number
        self.db.turns_taken_this_round = []  # Characters who have acted this round
        
        # Initiative
        self.db.initiative_holder = None  # Character who has initiative
        self.db.initiative_kept = False  # Whether initiative was kept this round
        
        # Extended tasks
        # Format: {task_id: {"requirement": int, "points": int, "participants": [character_ids]}}
        self.db.extended_tasks = {}
        
        # Conflict state
        self.db.status = "active"  # active, concluded
        self.db.winners = []
        self.db.defeated = []  # List of defeated characters
        
        # Room where conflict takes place
        self.db.location = None
    
    def add_participant(self, character):
        """Add a participant to the conflict"""
        if character not in self.db.participants:
            self.db.participants.append(character)
            return True
        return False
    
    def initialize_turn_order(self, first_character=None):
        """
        Initialize turn order for the conflict.
        
        Args:
            first_character: Character to take first turn (defaults to first participant)
        """
        if not self.db.participants:
            return
        
        # Start with first participant or specified character
        if first_character and first_character in self.db.participants:
            self.db.turn_order = [first_character]
            remaining = [c for c in self.db.participants if c != first_character]
            self.db.turn_order.extend(remaining)
        else:
            self.db.turn_order = list(self.db.participants)
        
        self.db.current_turn_index = 0
        self.db.current_round = 1
        self.db.turns_taken_this_round = []
        self.db.initiative_holder = self.db.turn_order[0] if self.db.turn_order else None
        self.db.initiative_kept = False
    
    def get_current_turn(self):
        """Get whose turn it is"""
        if not self.db.turn_order:
            return None
        
        if self.db.current_turn_index >= len(self.db.turn_order):
            return None
        
        return self.db.turn_order[self.db.current_turn_index]
    
    def next_turn(self):
        """Move to next turn"""
        if not self.db.turn_order:
            return None
        
        current_char = self.get_current_turn()
        if current_char:
            if current_char not in self.db.turns_taken_this_round:
                self.db.turns_taken_this_round.append(current_char)
        
        # Move to next character
        self.db.current_turn_index += 1
        
        # Check if round is complete
        if self.db.current_turn_index >= len(self.db.turn_order):
            # All characters have taken a turn
            return self._start_new_round()
        
        return self.get_current_turn()
    
    def _start_new_round(self):
        """Start a new round"""
        self.db.current_round += 1
        self.db.turns_taken_this_round = []
        self.db.current_turn_index = 0
        self.db.initiative_kept = False
        
        # First turn of new round goes to initiative holder
        if self.db.initiative_holder:
            # Find index of initiative holder
            if self.db.initiative_holder in self.db.turn_order:
                self.db.current_turn_index = self.db.turn_order.index(self.db.initiative_holder)
        
        return self.get_current_turn()
    
    def keep_initiative(self, character, momentum_cost=2, add_threat=False):
        """
        Keep the initiative (take extra action or allow ally to act).
        
        Args:
            character: Character keeping initiative
            momentum_cost: Cost in Momentum (default 2)
            add_threat: If True, add to Threat instead of spending Momentum
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if self.db.initiative_kept:
            return (False, "Initiative has already been kept this round.")
        
        # Check if character can afford it
        # In full implementation, would check Momentum/Threat pools
        
        self.db.initiative_kept = True
        self.db.initiative_holder = character
        
        return (True, f"{character.name} keeps the initiative!")
    
    def set_extended_task(self, task_id, requirement, participants=None):
        """
        Set up an extended task.
        
        Args:
            task_id: Unique identifier for the task
            requirement: Number of points needed
            participants: List of characters contributing
            
        Returns:
            dict: Task status
        """
        if not self.db.extended_tasks:
            self.db.extended_tasks = {}
        
        self.db.extended_tasks[task_id] = {
            "requirement": requirement,
            "points": 0,
            "participants": participants or []
        }
        
        return self.db.extended_tasks[task_id]
    
    def add_extended_task_points(self, task_id, points):
        """
        Add points to an extended task.
        Points = 2 + Quality of asset used.
        
        Args:
            task_id: Task identifier
            points: Points to add
            
        Returns:
            bool: True if task is complete
        """
        if task_id not in self.db.extended_tasks:
            return False
        
        task = self.db.extended_tasks[task_id]
        task["points"] += points
        
        return task["points"] >= task["requirement"]
    
    def get_extended_task_status(self, task_id):
        """Get extended task status"""
        if task_id not in self.db.extended_tasks:
            return None
        
        return self.db.extended_tasks[task_id]
    
    def calculate_attack_points(self, asset_quality, momentum_spent=0):
        """
        Calculate points scored in an extended task attack.
        Base: 2 + Quality
        Can spend 2 Momentum to add +1 Quality for that attack only.
        
        Args:
            asset_quality: Quality of asset used
            momentum_spent: Momentum spent to increase Quality
            
        Returns:
            int: Points scored
        """
        # Each 2 Momentum spent adds +1 Quality
        effective_quality = asset_quality + (momentum_spent // 2)
        return 2 + effective_quality
    
    def conclude_conflict(self, winners=None, defeated=None):
        """Conclude the conflict"""
        self.db.status = "concluded"
        if winners:
            self.db.winners = winners
        if defeated:
            self.db.defeated = defeated

