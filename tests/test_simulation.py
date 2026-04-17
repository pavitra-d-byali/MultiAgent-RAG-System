import pytest
from core.environment import Environment
from core.agent import BaseAgent

def test_environment_initialization():
    env = Environment()
    assert env.time_step == 0
    assert len(env.agents) == 0

def test_collision_detection():
    env = Environment()
    a1 = BaseAgent((0,0), (10,10), "A1")
    a2 = BaseAgent((0.5,0), (10,10), "A2")
    
    env.add_agent(a1)
    env.add_agent(a2)
    
    # Radii are 0.5 each, distance is 0.5 < 1.0, so should collide immediately
    env.check_collisions()
    
    assert env.collisions > 0
    assert a1.state == "collision"
    assert a2.state == "collision"
