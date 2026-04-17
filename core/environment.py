from typing import List, Dict, Any
from core.agent import BaseAgent
import math

class Environment:
    """
    Manages the 2D spatial world where agents interact.
    """
    def __init__(self, bounds: tuple = (100.0, 100.0)):
        self.bounds = bounds # (width, height)
        self.agents: List[BaseAgent] = []
        self.time_step = 0
        self.collisions = 0
        
    def add_agent(self, agent: BaseAgent):
        self.agents.append(agent)
        
    def get_global_state(self) -> Dict[str, Any]:
        """Returns the current state of all agents."""
        return {
            "time_step": self.time_step,
            "agents": {a.id: a.get_state_dict() for a in self.agents}
        }
        
    def check_collisions(self):
        """Checks for intersections between any two agents."""
        for i in range(len(self.agents)):
            for j in range(i + 1, len(self.agents)):
                a1 = self.agents[i]
                a2 = self.agents[j]
                dist = math.hypot(a1.position[0] - a2.position[0], a1.position[1] - a2.position[1])
                if dist < (a1.radius + a2.radius):
                    self.collisions += 1
                    # Basic collision response: halt them
                    a1.state = "collision"
                    a2.state = "collision"
                    a1.velocity = [0.0, 0.0]
                    a2.velocity = [0.0, 0.0]

    def step(self):
        """Advances the simulation by one tick."""
        global_state = self.get_global_state()
        
        # 1. Ask every agent to plan and move
        for agent in self.agents:
            if agent.state != "collision":
                agent.step(global_state)
                
        # 2. Check for collisions
        self.check_collisions()
        
        self.time_step += 1
