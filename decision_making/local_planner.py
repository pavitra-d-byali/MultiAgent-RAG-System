from typing import Dict, Any, Tuple
from core.agent import BaseAgent
from communication.network import Network
from decision_making.coordination_strategy import CoordinationStrategy
import math

class SmartAgent(BaseAgent):
    """
    An agent that uses V2V communication to negotiate pathing conflicts.
    """
    def __init__(self, start_pos: Tuple[float, float], goal_pos: Tuple[float, float], network: Network, agent_id: str = None):
        super().__init__(start_pos, goal_pos, agent_id)
        self.network = network
        self.network.register_agent(self.id)
        
    def step(self, environment_state: Dict[str, Any]) -> None:
        """
        Plans next step, broadcasts intentions, and yields if necessary.
        """
        dist_to_goal = self.distance_to(self.goal)
        
        if dist_to_goal < 0.1:
            self.state = "reached_goal"
            self.velocity = [0.0, 0.0]
            # Broadcast reached goal so others don't wait for us
            self.network.broadcast(self.id, self.position, {"status": "reached_goal"}, environment_state)
            return

        # 1. Read messages from network
        messages = self.network.receive(self.id)
        
        # 2. Coordinate / Negotiate with neighbors
        CoordinationStrategy.process_messages(self, messages)
        
        # 3. Broadcast my info for next step
        self.network.broadcast(self.id, self.position, {
            "status": self.state,
            "dist_to_goal": dist_to_goal
        }, environment_state)

        # 4. Execute movement if not yielding
        if self.state == "yielding":
            self.velocity = [0.0, 0.0] # Stop and wait
        else:
            self.state = "moving"
            # Move towards goal
            dx = self.goal[0] - self.position[0]
            dy = self.goal[1] - self.position[1]
            magnitude = math.hypot(dx, dy)
            
            if magnitude > 0:
                self.velocity[0] = (dx / magnitude) * self.max_speed
                self.velocity[1] = (dy / magnitude) * self.max_speed
                
            self.position[0] += self.velocity[0] * 0.1
            self.position[1] += self.velocity[1] * 0.1
