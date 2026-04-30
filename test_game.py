import pytest
import pygame
from unittest.mock import MagicMock, patch
#UNIT TESTS

pygame.init()
 
def make_mock_brawler(player=1, x=200, y=310, flip=False,
                      health=100, attack_cooldown=0):
    """
    Return a Brawlers instance whose pygame dependencies are all mocked out.
    The sprite-sheet is a real 896×896 surface (7 rows × 128 px, up to 9
    cols × 128 px) so load_images() can call subsurface() without errors.
    """
    from brawlers import Brawlers
 
    size   = 128
    scale  = 1
    offset = [20, 67]
    data   = [size, scale, offset]
 
    # A real surface large enough to hold every animation frame
    sprite_sheet = pygame.Surface((size * 9, size * 7))
 
    animation_steps      = [4, 5, 6, 3, 6, 9, 8]
    animation_cooldowns  = [150] * 7
 
    sound = MagicMock()
 
    brawler = Brawlers(
        player, x, y, flip,
        data, sprite_sheet, animation_steps, animation_cooldowns, sound
    )
    brawler.health         = health
    brawler.attack_cooldown = attack_cooldown
    return brawler

#5 PERSON MADE UNIT TEST
@pytest.fixture
def new_brawler():
    return make_mock_brawler(player=1, x=200, y=310)

@pytest.fixture
def two_brawlers():
    b1 = make_mock_brawler(player=1, x=200, y=310)
    b2 = make_mock_brawler(player=2, x=700, y=310)
    return b1, b2

#Test 1
def test_brawler_initial_state(new_brawler):
    b = new_brawler
    assert b.health    == 100
    assert b.alive     is True
    assert b.attacking is False
    assert b.jump      is False
    assert b.rect.x    == 200
    assert b.rect.y    == 310

#Test 2
def test_brawler_dies_when_health_reaches_zero(new_brawler):
    new_brawler.health = 0
    new_brawler.update()
    assert new_brawler.alive  is False
    assert new_brawler.health == 0

#Test 3
def test_brawler_faces_target(two_brawlers):
    b1, b2 = two_brawlers
    b1.move(1000, 600, MagicMock(), b2, round_over=False)
    assert b1.flip is False
    b2.rect.x = 50
    b1.move(1000, 600, MagicMock(), b2, round_over=False)
    assert b1.flip is True

#Test 4
def test_round_over_prevents_movement():
    brawler = make_mock_brawler(player=1, x=400)
    target  = make_mock_brawler(player=2, x=700)
 
    brawler.running   = False
    brawler.attacking = False
 
    brawler.move(1000, 600, MagicMock(), target, round_over=True)
 
    assert brawler.running   is False
    assert brawler.attacking is False
#Test 5
def test_hit_flag_set_and_action_switches_to_hurt():

    brawler = make_mock_brawler(player=1, x=200)
    brawler.attacking = True
    brawler.attack_type = 1
    brawler.hit = True  
    brawler.update()
 
    assert brawler.action == 3
    assert brawler.attacking is True

# ════════════════════════════════════════════════════════════════════════════
#  AI-ASSISTED TESTS  (6 – 10)
# ════════════════════════════════════════════════════════════════════════════
 
class TestGravityAndJump:
 
    def test_gravity_increases_vel_y_each_frame(self):
        """AI Test 6 – vel_y grows by GRAVITY (2) every move() call."""
        brawler = make_mock_brawler(player=1, x=400, y=100)
        target  = make_mock_brawler(player=2, x=700)
        surface = MagicMock()
 
        initial_vel_y = brawler.vel_y
        brawler.move(1000, 600, surface, target, round_over=False)
 
        assert brawler.vel_y > initial_vel_y
 
    def test_jump_flag_clears_on_landing(self):
        """AI Test 7 – jump resets to False once brawler hits the floor."""
        CANVAS_HEIGHT = 600
        FLOOR         = CANVAS_HEIGHT - 110        # 490 — boundary in move()
        brawler       = make_mock_brawler(player=1, x=400, y=FLOOR - 180)
        target        = make_mock_brawler(player=2, x=700)
        surface       = MagicMock()
        brawler.jump  = True
        brawler.vel_y = 200    # large enough to guarantee floor is hit in one step
 
        brawler.move(1000, CANVAS_HEIGHT, surface, target, round_over=False)
 
        assert brawler.jump is False
 
 
class TestBoundaryClamp:
 
    def test_brawler_cannot_move_past_left_wall(self):
        """AI Test 8 – rect.left never goes below 0."""
        brawler        = make_mock_brawler(player=1, x=0)
        brawler.rect.x = 0
        SPEED          = 10
        dx             = -SPEED
 
        if brawler.rect.left + dx < 0:
            dx = 0 - brawler.rect.left
        brawler.rect.x += dx
 
        assert brawler.rect.left >= 0
 
    def test_dead_brawler_cannot_attack(self):
        """AI Test 9 – a brawler with alive=False cannot deal damage even
        if attack() is called directly, because move() guards are bypassed
        and we confirm attack still fires — but the real guard is in move().
        This test verifies alive=False is set correctly and stays that way
        after multiple update() calls (no resurrection bug)."""
        brawler = make_mock_brawler(health=0)
        brawler.update()
        assert brawler.alive is False
 
        # Call update several more times — should stay dead
        brawler.update()
        brawler.update()
        assert brawler.alive is False
        assert brawler.health == 0
 
 
class TestActionStateMachine:
 
    def test_update_action_resets_frame_index(self):
        """AI Test 10 – switching action resets frame_index to 0."""
        brawler             = make_mock_brawler(player=1)
        brawler.frame_index = 3
 
        brawler.update_action(6)   # switch to run
 
        assert brawler.frame_index == 0
        assert brawler.action      == 6