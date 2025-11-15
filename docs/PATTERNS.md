# Multi-Agent Patterns

This document covers common multi-agent patterns and their implementation in AutoGen and CrewAI.

## Overview of Patterns

Multi-agent systems can be organized in various ways depending on the task. Here are the most common patterns:

1. **Sequential Pipeline** - Agents work in a defined order
2. **Hierarchical** - Manager agent delegates to specialists
3. **Debate/Adversarial** - Agents argue opposing positions
4. **Collaborative** - Agents work together as peers
5. **Tool Specialists** - Each agent has unique capabilities

## Pattern 1: Sequential Pipeline (Research Team)

This is the pattern implemented in our main examples. Work flows through agents in sequence.

```
Researcher → Writer → Editor → Final Output
```

### When to Use
- Clear workflow stages
- Each stage builds on previous
- Well-defined handoffs

### AutoGen Implementation
```python
# Agents communicate sequentially through conversation
groupchat = GroupChat(
    agents=[researcher, writer, editor],
    max_round=6,
    speaker_selection_method="round_robin"  # Force sequential
)
```

### CrewAI Implementation
```python
# Tasks execute in order
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential
)
```

---

## Pattern 2: Hierarchical Delegation

A manager agent coordinates work among specialists.

```
       Manager
      /   |   \
   Agent1 Agent2 Agent3
```

### When to Use
- Complex tasks needing decomposition
- Dynamic task allocation
- Quality control at top level

### AutoGen Implementation
```python
manager = AssistantAgent(
    name="Manager",
    system_message="""You are a project manager. Analyze tasks and delegate 
to specialists. Coordinate their work and synthesize results.""",
    llm_config=llm_config
)

# Use nested chats or custom speaker selection
def custom_speaker_selection(last_speaker, groupchat):
    if last_speaker.name == "Manager":
        # Manager decides who to delegate to
        return select_best_agent(groupchat.messages[-1])
    else:
        # Specialists report back to manager
        return manager
```

### CrewAI Implementation
```python
crew = Crew(
    agents=[manager, specialist1, specialist2, specialist3],
    tasks=[main_task],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o-mini")
)
```

---

## Pattern 3: Debate/Adversarial

Agents argue opposing positions to explore a topic thoroughly.

```
Pro Agent ←→ Con Agent
      ↓
   Moderator
```

### When to Use
- Exploring complex decisions
- Need multiple perspectives
- Risk assessment
- Policy analysis

### AutoGen Implementation
```python
pro_agent = AssistantAgent(
    name="Advocate",
    system_message="""You argue IN FAVOR of the proposition. 
Present strong arguments, evidence, and rebuttals.""",
    llm_config=llm_config
)

con_agent = AssistantAgent(
    name="Critic",
    system_message="""You argue AGAINST the proposition. 
Present counterarguments, risks, and challenges.""",
    llm_config=llm_config
)

moderator = AssistantAgent(
    name="Moderator",
    system_message="""You moderate the debate. After hearing both sides,
summarize key points and provide a balanced conclusion.""",
    llm_config=llm_config
)

# Let them debate naturally
groupchat = GroupChat(
    agents=[user_proxy, pro_agent, con_agent, moderator],
    max_round=8,
    speaker_selection_method="auto"
)
```

### CrewAI Implementation
```python
# Define tasks for each perspective
pro_task = Task(
    description="Argue in favor of: {topic}. Present 3-5 strong arguments.",
    agent=advocate,
    expected_output="Compelling arguments supporting the proposition"
)

con_task = Task(
    description="Argue against: {topic}. Present 3-5 counterarguments.",
    agent=critic,
    expected_output="Strong counterarguments challenging the proposition"
)

synthesis_task = Task(
    description="Synthesize both perspectives into a balanced analysis.",
    agent=moderator,
    context=[pro_task, con_task],
    expected_output="Balanced analysis with recommendation"
)

crew = Crew(
    agents=[advocate, critic, moderator],
    tasks=[pro_task, con_task, synthesis_task],
    process=Process.sequential
)
```

---

## Pattern 4: Peer Review

Agents review and improve each other's work iteratively.

```
Creator → Reviewer1 → Creator (revise) → Reviewer2 → Final
```

### When to Use
- Quality-critical outputs
- Need multiple review passes
- Academic or technical writing
- Code review processes

### AutoGen Implementation
```python
# Natural fit - conversation enables back-and-forth
creator = AssistantAgent(
    name="Creator",
    system_message="You create content. Incorporate feedback from reviewers.",
    llm_config=llm_config
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="""You review content critically. Provide specific, 
actionable feedback. Approve only when quality is excellent.""",
    llm_config=llm_config
)

# Allow multiple rounds
groupchat = GroupChat(
    agents=[user_proxy, creator, reviewer],
    max_round=10,  # Allow several revision cycles
    speaker_selection_method="auto"
)
```

### CrewAI Implementation
```python
# Less natural fit - need to structure iterations explicitly
# Could use multiple task cycles or custom process

# Option 1: Multiple review tasks
draft_task = Task(description="Create initial draft", agent=creator)
review1_task = Task(description="First review", agent=reviewer1, context=[draft_task])
revise_task = Task(description="Revise based on feedback", agent=creator, context=[review1_task])
review2_task = Task(description="Final review", agent=reviewer2, context=[revise_task])
```

---

## Pattern 5: Tool Specialists

Each agent has unique tools or capabilities.

```
Coordinator
    ↓
[Web Search Agent] [Database Agent] [Calculator Agent]
```

### When to Use
- Need different data sources
- Specialized computations
- Integration with external services
- Complex multi-step reasoning

### AutoGen Implementation
```python
# AutoGen has built-in code execution
search_agent = AssistantAgent(
    name="WebSearcher",
    system_message="You search the web for information.",
    llm_config=llm_config
)

# Can execute code
calculator_agent = AssistantAgent(
    name="Calculator",
    system_message="You perform calculations. Write and execute Python code.",
    llm_config=llm_config,
    code_execution_config={"work_dir": "coding"}
)
```

### CrewAI Implementation
```python
from crewai_tools import SerperDevTool, FileReadTool

# Define tools
search_tool = SerperDevTool()
file_tool = FileReadTool()

# Assign tools to agents
researcher = Agent(
    role="Web Researcher",
    goal="Find information online",
    backstory="Expert at finding information",
    tools=[search_tool],
    llm=llm
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze data from files",
    backstory="Expert at data analysis",
    tools=[file_tool],
    llm=llm
)
```

---

## Advanced Patterns

### Consensus Building
Multiple agents must agree on a decision.

```python
# AutoGen: Natural through conversation
# Set termination condition when all agents agree

# CrewAI: Use voting task
voting_task = Task(
    description="Review proposals and vote. Require unanimous agreement.",
    agent=coordinator,
    context=[proposal1_task, proposal2_task, proposal3_task]
)
```

### Swarm Intelligence
Many simple agents solve complex problems collectively.

```python
# Better suited for custom implementations
# Both frameworks can support with custom orchestration
```

### Human-in-the-Loop
Human feedback integrated into agent workflow.

```python
# AutoGen
user_proxy = UserProxyAgent(
    name="Human",
    human_input_mode="ALWAYS"  # or "TERMINATE"
)

# CrewAI
# Use input() in tasks or custom tools
```

---

## Choosing a Pattern

| Pattern | AutoGen Fit | CrewAI Fit | Best For |
|---------|-------------|------------|----------|
| Sequential Pipeline | Good | Excellent | Structured workflows |
| Hierarchical | Good | Excellent | Complex decomposition |
| Debate/Adversarial | Excellent | Good | Multi-perspective analysis |
| Peer Review | Excellent | Moderate | Quality improvement |
| Tool Specialists | Excellent | Excellent | Diverse capabilities |

## LLM Configuration

### OpenAI (Default)

Both frameworks work seamlessly with OpenAI:

```python
# AutoGen
llm_config = {
    "model": "gpt-4o-mini",
    "api_key": os.getenv("OPENAI_API_KEY")
}

# CrewAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")
```

### Anthropic Claude

```python
# AutoGen (via config)
llm_config = {
    "model": "claude-3-sonnet-20240229",
    "api_type": "anthropic",
    "api_key": os.getenv("ANTHROPIC_API_KEY")
}

# CrewAI
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
```

### Local Models (Ollama)

```python
# AutoGen
llm_config = {
    "model": "llama3",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama"  # Placeholder
}

# CrewAI
from langchain_community.llms import Ollama
llm = Ollama(model="llama3")
```

## Best Practices

1. **Start Simple**: Begin with sequential patterns before adding complexity.

2. **Clear Roles**: Well-defined agent personalities lead to better outputs.

3. **Limit Rounds**: Set reasonable conversation/task limits to avoid infinite loops.

4. **Test Thoroughly**: Multi-agent systems can have emergent behaviors.

5. **Monitor Costs**: More agents = more API calls = higher costs.

6. **Log Everything**: Capture full execution traces for debugging.

7. **Graceful Degradation**: Handle agent failures without complete system failure.

## Next Steps

- Try implementing the patterns above
- Experiment with hybrid approaches
- Consider production deployment requirements
- Explore framework-specific advanced features

For RAG-specific comparisons, see: [agentic-rag](https://github.com/roguetrainer/agentic-rag)
