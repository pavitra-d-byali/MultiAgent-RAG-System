import uuid
import math
from typing import Tuple, Dict, Any, List

class BaseAgent:
    """
    Represents a generic autonomous agent in the 2D MAS environment.
    """
    def __init__(self, start_pos: Tuple[float, float], goal_pos: Tuple[float, float], agent_id: str = None):
        self.id = agent_id or str(uuid.uuid4())[:8]
        self.position = list(start_pos) # [x, y]
        self.goal = list(goal_pos)      # [x, y]
        self.velocity = [0.0, 0.0]      # [vx, vy]
        self.max_speed = 1.0
        self.radius = 0.5               # Physical footprint size
        self.state = "idle"             # idle, moving, reached_goal, waiting
        
    def get_state_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "position": self.position.copy(),
            "velocity": self.velocity.copy(),
            "goal": self.goal.copy(),
            "state": self.state
        }
        
    def distance_to(self, point: Tuple[float, float]) -> float:
        return math.hypot(self.position[0] - point[0], self.position[1] - point[1])
        
    def step(self, environment_state: Dict[str, Any]) -> None:
        """
        Calculates next movement based on current state and environment observations.
        To be overridden or augmented by local_planner.
        """
        dist_to_goal = self.distance_to(self.goal)
        if dist_to_goal < 0.1:
            self.state = "reached_goal"
            self.velocity = [0.0, 0.0]
            return

        self.state = "moving"
        # Basic direct-to-goal vector (no coordination yet)
        dx = self.goal[0] - self.position[0]
        dy = self.goal[1] - self.position[1]
        magnitude = math.hypot(dx, dy)
        
        if magnitude > 0:
            self.velocity[0] = (dx / magnitude) * self.max_speed
            self.velocity[1] = (dy / magnitude) * self.max_speed
            
        # Apply velocity
        self.position[0] += self.velocity[0] * 0.1 # assuming dt=0.1
        self.position[1] += self.velocity[1] * 0.1
