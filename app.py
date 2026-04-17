import sys
import os

# Ensure modules can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import plotly.graph_objects as go
import time
from core.environment import Environment
from communication.network import Network
from decision_making.local_planner import SmartAgent
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Simulation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 Autonomous Multi-Agent Decision System")
st.markdown("A FAANG-level simulation visualizing cooperative V2V path planning and conflict resolution.")

# Initialization logic using session_state
def init_simulation():
    env = Environment()
    net = Network(range_limit=50.0)
    
    agent_a = SmartAgent(start_pos=(0.0, 10.0), goal_pos=(20.0, 10.0), network=net, agent_id="Agent_A")
    agent_b = SmartAgent(start_pos=(10.0, 0.0), goal_pos=(10.0, 20.0), network=net, agent_id="Agent_B")
    
    env.add_agent(agent_a)
    env.add_agent(agent_b)
    
    st.session_state["env"] = env
    st.session_state["net"] = net
    st.session_state["history"] = []
    st.session_state["simulation_running"] = False
    logger.info("Simulation initialized.")

if "env" not in st.session_state:
    init_simulation()

# UI Layout
sidebar = st.sidebar
sidebar.header("Simulation Controls")

if sidebar.button("Reset Simulation"):
    init_simulation()
    st.rerun()

run_button = sidebar.button("Run Simulation Step")
auto_play = sidebar.checkbox("Auto-play")

# Plotting Function
def plot_environment(env: Environment):
    fig = go.Figure()
    
    # Draw Agents and Goals
    for agent in env.agents:
        # Goal Marker
        fig.add_trace(go.Scatter(
            x=[agent.goal[0]], y=[agent.goal[1]],
            mode='markers',
            marker=dict(size=12, symbol="star", color='rgba(255, 100, 100, 0.8)'),
            name=f"{agent.id} Goal"
        ))
        
        # Agent Position
        color = "green" if agent.state == "reached_goal" else ("red" if agent.state == "collision" else ("orange" if agent.state == "yielding" else "blue"))
        fig.add_trace(go.Scatter(
            x=[agent.position[0]], y=[agent.position[1]],
            mode='markers+text',
            text=[agent.id[:5]],
            textposition="top center",
            marker=dict(size=20, color=color, line=dict(width=2, color='DarkSlateGrey')),
            name=agent.id
        ))

    # Layout constraints
    fig.update_layout(
        xaxis=dict(range=[-5, 25], title="X Position", showgrid=True, zeroline=False),
        yaxis=dict(range=[-5, 25], title="Y Position", showgrid=True, zeroline=False),
        height=600,
        plot_bgcolor='rgba(10,10,10,0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title="Intersection Monitoring Dashboard",
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# Main Area
col1, col2 = st.columns([2, 1])

env: Environment = st.session_state["env"]

# Advance Step Logic
if run_button or auto_play:
    if env.time_step < 400:
        env.step()
        all_reached = all(a.state == "reached_goal" for a in env.agents)
        if all_reached:
            st.session_state["simulation_running"] = False
            st.success("All agents reached their goals!")
            auto_play = False
        if env.collisions > 0:
            st.error(f"Collision detected! Total: {env.collisions}")
            auto_play = False
    else:
        st.warning("Max simulation steps reached.")
        auto_play = False
    
    # Use sleep for visual playback speed in auto-play
    if auto_play:
        time.sleep(0.1)
        st.rerun()

with col1:
    fig = plot_environment(env)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("System Metrics")
    st.metric("Time Step", f"{env.time_step:03d}")
    st.metric("Collisions", env.collisions)
    
    st.subheader("Agent Status")
    for agent in env.agents:
        dist = agent.distance_to(agent.goal)
        state = agent.state.replace("_", " ").title()
        color = "🟢" if state == "Reached Goal" else ("🔴" if state == "Collision" else "🟡")
        st.markdown(f"**{agent.id}** {color}  \nState: `{state}`  \nDistance to Goal: `{dist:.1f}`")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>Powered by Streamlit & Plotly | Multi-Agent Decision System Ecosystem</div>", unsafe_allow_html=True)
