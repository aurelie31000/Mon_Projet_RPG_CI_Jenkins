# tests/test_character.py
# Make sure to import the Character class from the src folder
import pytest
from src.character import Character

# Test 1: Verify character initialization with default health
def test_character_initialization():
    """
    Test that a character is initialized with a name and default health (10 HP).
    """
    player = Character("Hero")
    assert player.name == "Hero"
    assert player.health == 10
    assert player.is_alive is True

# Test 2: Verify that character takes damage
def test_character_takes_damage():
    """
    Test that a character's health decreases correctly when taking damage.
    """
    player = Character("Hero", health=10)
    player.take_damage(3)
    assert player.health == 7
    assert player.is_alive is True

# Test 3: Verify character dies at zero or less HP
def test_character_dies_at_zero_health():
    """
    Test that a character is marked as dead when their health drops to 0 or below.
    """
    player = Character("Hero", health=1)
    player.take_damage(1)
    assert player.health == 0
    assert player.is_alive is False

    enemy = Character("Goblin", health=5)
    enemy.take_damage(10) # Overkill damage
    assert enemy.health == 0
    assert enemy.is_alive is False

# Test 4: Verify an attacking character deals 1 damage to target
def test_character_attacks_and_deals_damage():
    """
    Test that an attacking character successfully reduces the target's health by 1.
    """
    attacker = Character("Knight", health=10)
    defender = Character("Dragon", health=10)
    attacker.attack(defender)
    assert defender.health == 9
    assert attacker.health == 10 # The attacker should not lose health

# Test 5: Verify a dead character cannot attack
def test_dead_character_cannot_attack():
    """
    Test that a character who is already dead cannot perform an attack.
    """
    dead_char = Character("Zombie", health=0)
    target = Character("Victim", health=10)
    dead_char.attack(target)
    assert target.health == 10 # The target's health should remain unchanged
    # You might also check for specific console output here if desired

# Test 6: Verify a character cannot attack a dead target
def test_cannot_attack_dead_character():
    """
    Test that a character cannot attack another character who is already dead.
    """
    attacker = Character("Hero", health=10)
    dead_enemy = Character("Undead", health=0)
    attacker.attack(dead_enemy)
    assert dead_enemy.health == 0 # The dead enemy's HP should remain 0
    # You might also check for specific console output here if desired

# Test 7: Verify a dead character does not take further damage
def test_dead_character_does_not_take_further_damage():
    """
    Test that a character marked as dead does not take additional damage.
    """
    dead_char = Character("Ghost", health=0)
    dead_char.take_damage(5) # Attempt to deal more damage
    assert dead_char.health == 0
    assert dead_char.is_alive is False
    # You might also check for specific console output here if desired

# Test 8: Test character's health cannot go below zero even with excessive damage
def test_character_health_does_not_go_below_zero():
    """
    Test that a character's health cannot go below zero.
    """
    player = Character("Warrior", health=5)
    player.take_damage(10) # More damage than health
    assert player.health == 0
    assert player.is_alive is False

# Test 9: Verify a character starts alive by default
def test_character_starts_alive_by_default():
    """
    Test that a new character is alive by default if health is positive.
    """
    player = Character("Newbie", health=1)
    assert player.is_alive is True

# Test 10: Verify the __str__ representation of a character
def test_character_str_representation():
    """
    Test the string representation of the Character object.
    """
    player = Character("DisplayChar", health=7)
    assert str(player) == "DisplayChar (HP: 7, Vivant: True)"
    player.take_damage(7)
    assert str(player) == "DisplayChar (HP: 0, Vivant: False)"

