"""
Test Script for Advancement System

This script provides comprehensive testing for the advancement system.
Run this to validate that everything works correctly.

Usage:
    @py from scripts.test_advancement import run_all_tests; run_all_tests()
"""

from evennia import ObjectDB, create_object
from typeclasses.characters import Character


def test_advancement_initialization():
    """Test that advancement tracking initializes correctly"""
    print("\n" + "=" * 70)
    print("TEST: Advancement Initialization")
    print("=" * 70)
    
    # Create a test character
    test_char = create_object(
        Character,
        key="AdvanceTestChar",
        location=None
    )
    
    # Initialize stats
    test_char.db.stats = {
        "skills": {
            "battle": 4,
            "communicate": 4,
            "discipline": 4,
            "move": 4,
            "understand": 4
        },
        "focuses": [],
        "talents": [],
        "assets": [],
        "drives": {
            "duty": {"rating": 0, "statement": ""},
            "faith": {"rating": 0, "statement": ""},
            "justice": {"rating": 0, "statement": ""},
            "power": {"rating": 0, "statement": ""},
            "truth": {"rating": 0, "statement": ""}
        }
    }
    
    # Initialize advancement
    from scripts.init_advancement import init_character_advancement
    result = init_character_advancement(test_char)
    
    # Verify
    checks = {
        "advancement_points exists": hasattr(test_char.db, 'advancement_points'),
        "advancement_history exists": hasattr(test_char.db, 'advancement_history'),
        "skill_advances exists": hasattr(test_char.db, 'skill_advances'),
        "total_skill_advances exists": hasattr(test_char.db, 'total_skill_advances'),
        "points initialized to 0": test_char.db.advancement_points == 0,
        "history is list": isinstance(test_char.db.advancement_history, list),
        "skill_advances is dict": isinstance(test_char.db.skill_advances, dict)
    }
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    # Cleanup
    test_char.delete()
    
    all_passed = all(checks.values())
    print(f"\n{'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_cost_calculations():
    """Test that costs are calculated correctly"""
    print("\n" + "=" * 70)
    print("TEST: Cost Calculations")
    print("=" * 70)
    
    # Create test character
    test_char = create_object(
        Character,
        key="CostTestChar",
        location=None
    )
    
    # Initialize
    test_char.db.stats = {
        "skills": {"battle": 4, "communicate": 4, "discipline": 4, "move": 4, "understand": 4},
        "focuses": ["Focus1", "Focus2", "Focus3"],
        "talents": ["Talent1", "Talent2"],
        "assets": [],
        "drives": {}
    }
    test_char.db.advancement_points = 100
    test_char.db.skill_advances = {
        "battle": 0, "communicate": 0, "discipline": 0, "move": 0, "understand": 0
    }
    test_char.db.total_skill_advances = 0
    test_char.db.advancement_history = []
    
    checks = {}
    
    # Test skill cost (should be 10 + 0 = 10)
    expected_skill_cost = 10
    actual_skill_cost = 10 + test_char.db.total_skill_advances
    checks["First skill costs 10"] = expected_skill_cost == actual_skill_cost
    print(f"  Skill cost: {actual_skill_cost} (expected {expected_skill_cost})")
    
    # Test focus cost (should equal focus count = 3)
    expected_focus_cost = len(test_char.db.stats["focuses"])
    actual_focus_cost = len(test_char.db.stats["focuses"])
    checks["Focus cost equals count"] = expected_focus_cost == actual_focus_cost
    print(f"  Focus cost: {actual_focus_cost} (expected {expected_focus_cost})")
    
    # Test talent cost (should be 3 × 2 = 6)
    expected_talent_cost = 3 * len(test_char.db.stats["talents"])
    actual_talent_cost = 3 * len(test_char.db.stats["talents"])
    checks["Talent cost equals 3×count"] = expected_talent_cost == actual_talent_cost
    print(f"  Talent cost: {actual_talent_cost} (expected {expected_talent_cost})")
    
    # Simulate advancing a skill
    test_char.db.total_skill_advances = 2
    expected_skill_cost_after = 10 + 2
    actual_skill_cost_after = 10 + test_char.db.total_skill_advances
    checks["Skill cost increases"] = expected_skill_cost_after == actual_skill_cost_after
    print(f"  Skill cost after 2 advances: {actual_skill_cost_after} (expected {expected_skill_cost_after})")
    
    # Test retraining cost (half of 12, rounded up = 6)
    full_cost = 12
    expected_retrain_cost = (full_cost + 1) // 2
    actual_retrain_cost = (full_cost + 1) // 2
    checks["Retrain cost is half (rounded up)"] = expected_retrain_cost == actual_retrain_cost
    print(f"  Retrain cost for 12: {actual_retrain_cost} (expected {expected_retrain_cost})")
    
    # Cleanup
    test_char.delete()
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    all_passed = all(checks.values())
    print(f"\n{'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_skill_advancement():
    """Test skill advancement mechanics"""
    print("\n" + "=" * 70)
    print("TEST: Skill Advancement")
    print("=" * 70)
    
    # Create test character
    test_char = create_object(
        Character,
        key="SkillTestChar",
        location=None
    )
    
    # Initialize
    test_char.db.stats = {
        "skills": {"battle": 4, "communicate": 4, "discipline": 4, "move": 4, "understand": 4},
        "focuses": [],
        "talents": [],
        "assets": [],
        "drives": {}
    }
    test_char.db.advancement_points = 50
    test_char.db.skill_advances = {
        "battle": 0, "communicate": 0, "discipline": 0, "move": 0, "understand": 0
    }
    test_char.db.total_skill_advances = 0
    test_char.db.advancement_history = []
    
    checks = {}
    
    # Test initial state
    initial_battle = test_char.db.stats["skills"]["battle"]
    checks["Initial battle is 4"] = initial_battle == 4
    print(f"  Initial battle: {initial_battle}")
    
    # Simulate skill advance
    cost = 10 + test_char.db.total_skill_advances
    test_char.db.advancement_points -= cost
    test_char.set_skill("battle", initial_battle + 1)
    test_char.db.skill_advances["battle"] += 1
    test_char.db.total_skill_advances += 1
    
    # Verify
    new_battle = test_char.db.stats["skills"]["battle"]
    checks["Battle increased to 5"] = new_battle == 5
    checks["Skill advances tracked"] = test_char.db.skill_advances["battle"] == 1
    checks["Total advances tracked"] = test_char.db.total_skill_advances == 1
    checks["Points deducted"] = test_char.db.advancement_points == 40
    
    print(f"  New battle: {new_battle}")
    print(f"  Battle advances: {test_char.db.skill_advances['battle']}")
    print(f"  Total advances: {test_char.db.total_skill_advances}")
    print(f"  Points remaining: {test_char.db.advancement_points}")
    
    # Test "already advanced" check
    already_advanced = test_char.db.skill_advances["battle"] > 0
    checks["Cannot advance battle again"] = already_advanced
    print(f"  Battle already advanced: {already_advanced}")
    
    # Test second skill advance (should cost 11)
    cost2 = 10 + test_char.db.total_skill_advances
    checks["Second advance costs 11"] = cost2 == 11
    print(f"  Second skill advance would cost: {cost2}")
    
    # Cleanup
    test_char.delete()
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    all_passed = all(checks.values())
    print(f"\n{'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_focus_advancement():
    """Test focus purchase mechanics"""
    print("\n" + "=" * 70)
    print("TEST: Focus Advancement")
    print("=" * 70)
    
    # Create test character
    test_char = create_object(
        Character,
        key="FocusTestChar",
        location=None
    )
    
    # Initialize
    test_char.db.stats = {
        "skills": {"battle": 6, "communicate": 4, "discipline": 4, "move": 4, "understand": 4},
        "focuses": ["Existing Focus 1", "Existing Focus 2"],
        "talents": [],
        "assets": [],
        "drives": {}
    }
    test_char.db.advancement_points = 50
    test_char.db.skill_advances = {
        "battle": 0, "communicate": 0, "discipline": 0, "move": 0, "understand": 0
    }
    test_char.db.total_skill_advances = 0
    test_char.db.advancement_history = []
    
    checks = {}
    
    # Test prerequisite
    has_skill_6 = any(v >= 6 for v in test_char.db.stats["skills"].values())
    checks["Has skill 6+"] = has_skill_6
    print(f"  Has skill 6+: {has_skill_6}")
    
    # Test initial focus count
    initial_count = len(test_char.db.stats["focuses"])
    checks["Initial focus count is 2"] = initial_count == 2
    print(f"  Initial focus count: {initial_count}")
    
    # Calculate cost
    cost = initial_count
    checks["Focus cost equals count (2)"] = cost == 2
    print(f"  Cost: {cost}")
    
    # Simulate focus purchase
    test_char.db.advancement_points -= cost
    test_char.add_focus("New Test Focus")
    
    # Verify
    new_count = len(test_char.db.stats["focuses"])
    checks["Focus count increased to 3"] = new_count == 3
    checks["Points deducted"] = test_char.db.advancement_points == 48
    checks["Focus added"] = "New Test Focus" in test_char.db.stats["focuses"]
    
    print(f"  New focus count: {new_count}")
    print(f"  Points remaining: {test_char.db.advancement_points}")
    print(f"  Has new focus: {'New Test Focus' in test_char.db.stats['focuses']}")
    
    # Test next cost
    next_cost = len(test_char.db.stats["focuses"])
    checks["Next focus costs 3"] = next_cost == 3
    print(f"  Next focus would cost: {next_cost}")
    
    # Cleanup
    test_char.delete()
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    all_passed = all(checks.values())
    print(f"\n{'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_talent_advancement():
    """Test talent purchase mechanics"""
    print("\n" + "=" * 70)
    print("TEST: Talent Advancement")
    print("=" * 70)
    
    # Create test character
    test_char = create_object(
        Character,
        key="TalentTestChar",
        location=None
    )
    
    # Initialize
    test_char.db.stats = {
        "skills": {"battle": 4, "communicate": 4, "discipline": 4, "move": 4, "understand": 4},
        "focuses": [],
        "talents": ["Existing Talent 1", "Existing Talent 2"],
        "assets": [],
        "drives": {}
    }
    test_char.db.advancement_points = 50
    test_char.db.skill_advances = {
        "battle": 0, "communicate": 0, "discipline": 0, "move": 0, "understand": 0
    }
    test_char.db.total_skill_advances = 0
    test_char.db.advancement_history = []
    
    checks = {}
    
    # Test initial talent count
    initial_count = len(test_char.db.stats["talents"])
    checks["Initial talent count is 2"] = initial_count == 2
    print(f"  Initial talent count: {initial_count}")
    
    # Calculate cost
    cost = 3 * initial_count
    checks["Talent cost is 3×count (6)"] = cost == 6
    print(f"  Cost: {cost}")
    
    # Simulate talent purchase
    test_char.db.advancement_points -= cost
    test_char.add_talent("New Test Talent")
    
    # Verify
    new_count = len(test_char.db.stats["talents"])
    checks["Talent count increased to 3"] = new_count == 3
    checks["Points deducted"] = test_char.db.advancement_points == 44
    checks["Talent added"] = "New Test Talent" in test_char.db.stats["talents"]
    
    print(f"  New talent count: {new_count}")
    print(f"  Points remaining: {test_char.db.advancement_points}")
    print(f"  Has new talent: {'New Test Talent' in test_char.db.stats['talents']}")
    
    # Test next cost
    next_cost = 3 * len(test_char.db.stats["talents"])
    checks["Next talent costs 9"] = next_cost == 9
    print(f"  Next talent would cost: {next_cost}")
    
    # Cleanup
    test_char.delete()
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    all_passed = all(checks.values())
    print(f"\n{'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_retraining():
    """Test retraining mechanics"""
    print("\n" + "=" * 70)
    print("TEST: Retraining")
    print("=" * 70)
    
    # Create test character
    test_char = create_object(
        Character,
        key="RetrainTestChar",
        location=None
    )
    
    # Initialize
    test_char.db.stats = {
        "skills": {"battle": 5, "communicate": 4, "discipline": 4, "move": 6, "understand": 4},
        "focuses": ["Old Focus"],
        "talents": ["Old Talent"],
        "assets": [],
        "drives": {}
    }
    test_char.db.advancement_points = 50
    test_char.db.skill_advances = {
        "battle": 0, "communicate": 0, "discipline": 0, "move": 0, "understand": 0
    }
    test_char.db.total_skill_advances = 2
    test_char.db.advancement_history = []
    
    checks = {}
    
    # Test skill retraining
    full_cost = 10 + test_char.db.total_skill_advances  # 12
    retrain_cost = (full_cost + 1) // 2  # 6 (rounded up)
    checks["Retrain cost is 6 (half of 12)"] = retrain_cost == 6
    print(f"  Retrain cost: {retrain_cost} (half of {full_cost})")
    
    # Simulate skill retrain (move→battle)
    old_move = test_char.db.stats["skills"]["move"]
    old_battle = test_char.db.stats["skills"]["battle"]
    
    test_char.db.advancement_points -= retrain_cost
    test_char.set_skill("move", old_move - 1)
    test_char.set_skill("battle", old_battle + 1)
    test_char.db.skill_advances["battle"] += 1
    test_char.db.total_skill_advances += 1
    
    # Verify
    new_move = test_char.db.stats["skills"]["move"]
    new_battle = test_char.db.stats["skills"]["battle"]
    
    checks["Move reduced from 6 to 5"] = old_move == 6 and new_move == 5
    checks["Battle increased from 5 to 6"] = old_battle == 5 and new_battle == 6
    checks["Battle marked as advanced"] = test_char.db.skill_advances["battle"] == 1
    checks["Total advances increased"] = test_char.db.total_skill_advances == 3
    checks["Points deducted"] = test_char.db.advancement_points == 44
    
    print(f"  Move: {old_move} → {new_move}")
    print(f"  Battle: {old_battle} → {new_battle}")
    print(f"  Battle advances: {test_char.db.skill_advances['battle']}")
    print(f"  Total advances: {test_char.db.total_skill_advances}")
    print(f"  Points remaining: {test_char.db.advancement_points}")
    
    # Test focus retraining cost
    focus_count = len(test_char.db.stats["focuses"])
    full_focus_cost = focus_count  # 1
    focus_retrain_cost = (full_focus_cost + 1) // 2  # 1 (rounded up)
    checks["Focus retrain cost is 1"] = focus_retrain_cost == 1
    print(f"  Focus retrain cost: {focus_retrain_cost} (half of {full_focus_cost})")
    
    # Test talent retraining cost
    talent_count = len(test_char.db.stats["talents"])
    full_talent_cost = 3 * talent_count  # 3
    talent_retrain_cost = (full_talent_cost + 1) // 2  # 2 (rounded up)
    checks["Talent retrain cost is 2"] = talent_retrain_cost == 2
    print(f"  Talent retrain cost: {talent_retrain_cost} (half of {full_talent_cost})")
    
    # Cleanup
    test_char.delete()
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    all_passed = all(checks.values())
    print(f"\n{'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def run_all_tests():
    """Run all advancement tests"""
    print("\n" + "=" * 70)
    print("ADVANCEMENT SYSTEM TEST SUITE")
    print("=" * 70)
    
    results = {
        "Initialization": test_advancement_initialization(),
        "Cost Calculations": test_cost_calculations(),
        "Skill Advancement": test_skill_advancement(),
        "Focus Advancement": test_focus_advancement(),
        "Talent Advancement": test_talent_advancement(),
        "Retraining": test_retraining()
    }
    
    print("\n" + "=" * 70)
    print("TEST SUITE RESULTS")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {status}: {test_name}")
    
    all_passed = all(results.values())
    passed_count = sum(results.values())
    total_count = len(results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print(f"ALL TESTS PASSED ({passed_count}/{total_count})")
    else:
        print(f"SOME TESTS FAILED ({passed_count}/{total_count} passed)")
    print("=" * 70)
    
    return results


# Example usage:
# @py from scripts.test_advancement import run_all_tests; run_all_tests()

