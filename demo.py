import sys
import os

# Add the project root to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.environment import Environment
from communication.network import Network
from decision_making.local_planner import SmartAgent
import time

def run_demo():
    print("Initializing Multi-Agent System (MAS) Demo...")
    # 1. Setup World
    env = Environment()
    net = Network(range_limit=50.0) # Network covers the whole intersection
    
    # 2. Setup Agents (Intersection Scenario)
    # Agent A moves East, Agent B moves North. They cross paths at (10, 10)
    agent_a = SmartAgent(start_pos=(0.0, 10.0), goal_pos=(20.0, 10.0), network=net, agent_id="Agent_A")
    agent_b = SmartAgent(start_pos=(10.0, 0.0), goal_pos=(10.0, 20.0), network=net, agent_id="Agent_B")
    
    env.add_agent(agent_a)
    env.add_agent(agent_b)
    
    # 3. Simulate Loop
    print("Starting simulation loop. Target interaction point: (10, 10)")
    print("-" * 50)
    
    all_reached = False
    
    while not all_reached and env.time_step < 400:
        env.step()
        
        # Logging
        all_reached = True
        print(f"Step {env.time_step:03d} | Collisions: {env.collisions}")
        for agent in env.agents:
            if agent.state != "reached_goal":
                all_reached = False
            print(f"  [{agent.id}] Pos: ({agent.position[0]:.1f}, {agent.position[1]:.1f}) | State: {agent.state:12s} | GoalDist: {agent.distance_to(agent.goal):.1f}")
            
    print("-" * 50)
    if all_reached:
        print("Demo Success: Both agents reached their goals safely without colliding!")
    else:
        print(f"Demo Ended: Max steps reached or collision occurred. Collisions: {env.collisions}")

if __name__ == "__main__":
    run_demo()
