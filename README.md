# Overview
This application simulates agents operating in an environment.

# History
I origanally developed this application as an assignment for the AI and Games module which was part of the BSc in Computer Science I was studying.

# Agents
There are two types of agent:

1. Workers dipicted as blue squares.
2. Grazers dipicted as yellow squares.

## Worker agents
The worker agents have the following behaviour:

1. Search the environment.
2. Avoid obsticals.
3. Gather resources.
4. Return resources to their home (a white square).
5. Remove grazer agents from the environment.

## Grazer agents
The grazer agents have the following behaviour:

1. Search the environment.
2. Avoid obsticals.
2. Gather resources.
3. Evade worker agents.

## Vector lines
In order to get a better idea of how the agents are moving I included vector lines.  Each agent has two vector lines:
1. The green vector line shows the current direction that the agent is moving.
2. The red vector line shows the desired direction that the agent wants to move to.

# The running simulation
![The running agent simulation](/images/agent-simulation.png "The running agent simulation")