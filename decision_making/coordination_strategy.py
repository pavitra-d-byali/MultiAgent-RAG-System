from typing import Dict, Any, List

class CoordinationStrategy:
    """
    Decentralized conflict resolution logic.
    Agents use this to decide who yields when paths cross.
    """
    @staticmethod
    def negotiate_priority(my_id: str, my_dist_to_goal: float, other_id: str, other_dist_to_goal: float) -> bool:
        """
        Returns True if `my_id` has priority over `other_id`.
        Priority rule: Agent closer to its goal has priority. If equal, lower ID string wins.
        """
        # Small epsilon for float comparison
        if abs(my_dist_to_goal - other_dist_to_goal) > 0.5:
            return my_dist_to_goal < other_dist_to_goal
        
        return my_id < other_id

    @staticmethod
    def process_messages(my_agent: Any, messages: List[Dict[str, Any]]):
        """
        Processes incoming V2V messages.
        If another agent is nearby and on a conflicting trajectory, negotiate priority.
        """
        my_agent.state = "moving" # Default optimistic assumption
        
        for msg in messages:
            content = msg["content"]
            if "status" in content and content["status"] == "reached_goal":
                 continue
                 
            sender_id = msg["sender_id"]
            sender_pos = msg["sender_pos"]
            sender_dist_to_goal = content.get("dist_to_goal", float('inf'))
            
            # Simple collision anticipation (if very close)
            # A real MAS would calculate trajectory intersection.
            dist_to_other = my_agent.distance_to(sender_pos)
            
            if dist_to_other < (my_agent.radius * 4): # They are close!
                my_dist_to_goal = my_agent.distance_to(my_agent.goal)
                has_priority = CoordinationStrategy.negotiate_priority(
                    my_agent.id, my_dist_to_goal, sender_id, sender_dist_to_goal
                )
                
                if not has_priority:
                    # Yield to the other agent
                    my_agent.state = "yielding"
                    return # Stop moving
