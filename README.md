# Multi-Agent Team Orchestration

A side-by-side comparison of multi-agent orchestration frameworks. This repository implements the same collaborative task across AutoGen and CrewAI to help you understand their different approaches to agent coordination.

## Frameworks Compared

- **AutoGen** (Microsoft) - Conversation-centric multi-agent framework
- **CrewAI** - Role-based agent collaboration with task delegation

## The Task

Each implementation creates a **Research and Writing Team** with three collaborating agents:

1. **Researcher** - Gathers information on a given topic
2. **Writer** - Transforms research into polished content
3. **Editor** - Reviews and improves the final output

This pattern demonstrates genuine multi-agent value: the output is better than any single agent would produce, and you can observe agents passing work between each other.

## Related Repository

For lightweight RAG implementations (using LlamaIndex, LangChain, and SmolAgents), see our companion repository:
**[agentic-rag](https://github.com/roguetrainer/agentic-rag)**

## Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key (or other LLM provider)

### Installation

```bash
# Clone the repository
git clone https://github.com/roguetrainer/multi-agent-team.git
cd multi-agent-team

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="your-key-here"
```

### Running the Examples

Each framework has its own implementation:

```bash
# AutoGen - Conversation-based agents
python examples/autogen/research_team.py

# CrewAI - Role-based crew
python examples/crewai/research_team.py
```

### Running the Comparison

To run both frameworks on the same topic and compare their approaches:

```bash
python compare_frameworks.py
```

You can customize the research topic:

```bash
python compare_frameworks.py --topic "The impact of quantum computing on cryptography"
```

## Project Structure

```
multi-agent-team/
├── README.md
├── requirements.txt
├── compare_frameworks.py          # Runs both frameworks and compares
├── examples/
│   ├── autogen/
│   │   └── research_team.py
│   └── crewai/
│       └── research_team.py
└── docs/
    ├── COMPARISON.md              # Detailed comparison analysis
    └── PATTERNS.md                # Common multi-agent patterns
```

## Sample Output

When you run the research team on a topic like "Sustainable urban farming technologies", you'll see:

**AutoGen**: Agents engage in a conversation, with the researcher sharing findings, the writer drafting content, and the editor providing feedback in a chat-like flow.

**CrewAI**: Tasks are delegated sequentially, with each agent completing their role before passing to the next, producing structured deliverables.

## Key Differences

| Aspect | AutoGen | CrewAI |
|--------|---------|--------|
| **Paradigm** | Conversation-centric | Task/Role-centric |
| **Agent Interaction** | Chat-based dialogue | Sequential task handoff |
| **Control Flow** | Emergent from conversation | Explicit task delegation |
| **Best For** | Debate, brainstorming, iterative refinement | Structured workflows, clear deliverables |
| **Learning Curve** | Moderate | Lower |
| **Flexibility** | High (custom conversation patterns) | Moderate (predefined roles) |

*See [docs/COMPARISON.md](docs/COMPARISON.md) for detailed analysis.*

## Customization

### Changing the Research Topic

Edit the topic in the example files or pass it as an argument:

```python
# In any example file
topic = "Your research topic here"
```

### Adding More Agents

Both frameworks support adding additional agents:

**AutoGen**: Add new `AssistantAgent` instances to the group chat
**CrewAI**: Define new `Agent` objects and corresponding `Task` entries

### Using Different LLM Providers

See [docs/PATTERNS.md](docs/PATTERNS.md) for configuration options with Anthropic, local models, and other providers.

## Common Multi-Agent Patterns

This repository focuses on the Research and Writing pattern, but both frameworks support many others:

- **Debate**: Agents argue opposing viewpoints
- **Hierarchical**: Manager agent delegates to specialists
- **Peer Review**: Agents critique each other's work
- **Tool Specialists**: Each agent has unique capabilities

See [docs/PATTERNS.md](docs/PATTERNS.md) for implementation examples of these patterns.

## When to Use Multi-Agent Orchestration

Multi-agent systems shine when:

- Tasks benefit from multiple perspectives or expertise areas
- You need iterative refinement through feedback loops
- Work can be decomposed into distinct roles
- Quality improves with review and critique cycles

They're overkill when:

- A single prompt can accomplish the task
- You need simple, deterministic outputs
- Latency and cost are primary concerns
- The task doesn't benefit from collaboration

## Contributing

Contributions welcome! Areas of interest:

- Additional multi-agent patterns
- Performance benchmarking
- Alternative framework comparisons
- Documentation improvements

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [AutoGen](https://microsoft.github.io/autogen/)
- [CrewAI](https://www.crewai.com/)
- [Agentic RAG Repository](https://github.com/roguetrainer/agentic-rag)
