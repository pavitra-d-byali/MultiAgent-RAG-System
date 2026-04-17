from typing import Dict, Any, List

class Network:
    """
    Simulates a V2V (Vehicle-to-Vehicle) or Agent-to-Agent communication network.
    Agents can broadcast messages to be received by others within a certain radius.
    """
    def __init__(self, range_limit: float = 20.0):
        self.range_limit = range_limit
        self.mailboxes: Dict[str, List[Dict[str, Any]]] = {}
        
    def register_agent(self, agent_id: str):
        if agent_id not in self.mailboxes:
            self.mailboxes[agent_id] = []
            
    def broadcast(self, sender_id: str, sender_pos: List[float], message: Dict[str, Any], environment_state: Dict[str, Any]):
        """
        Broadcasts a message from an agent. Received by all agents within range_limit.
        """
        import math
        msg_payload = {
            "sender_id": sender_id,
            "sender_pos": sender_pos,
            "content": message
        }
        
        for tgt_id, state in environment_state["agents"].items():
            if tgt_id == sender_id:
                continue
                
            tgt_pos = state["position"]
            dist = math.hypot(sender_pos[0] - tgt_pos[0], sender_pos[1] - tgt_pos[1])
            
            if dist <= self.range_limit and tgt_id in self.mailboxes:
                self.mailboxes[tgt_id].append(msg_payload)
                
    def receive(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Fetches all unread messages for an agent and clears the mailbox.
        """
        if agent_id in self.mailboxes:
            messages = self.mailboxes[agent_id]
            self.mailboxes[agent_id] = []
            return messages
        return []
