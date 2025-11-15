"""
AutoGen Research Team Example
==============================
Demonstrates multi-agent collaboration using AutoGen's conversation-centric approach.
Agents communicate through a group chat, naturally passing information and feedback.
"""

import os
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager


def create_research_team(topic: str) -> dict:
    """
    Create a research team with Researcher, Writer, and Editor agents.
    
    AutoGen uses conversation-based coordination where agents
    communicate through natural dialogue in a group chat.
    """
    
    # Configure the LLM
    llm_config = {
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "api_key": os.getenv("OPENAI_API_KEY")
    }
    
    # Create the Researcher agent
    researcher = AssistantAgent(
        name="Researcher",
        system_message="""You are a thorough research specialist. Your role is to:
- Gather comprehensive information on the given topic
- Identify key facts, trends, and insights
- Organize findings in a clear, structured format
- Cite important points and provide context

When you've completed your research, summarize your findings clearly for the Writer.
Focus on accuracy and depth of information.""",
        llm_config=llm_config
    )
    
    # Create the Writer agent
    writer = AssistantAgent(
        name="Writer",
        system_message="""You are a skilled content writer. Your role is to:
- Transform research findings into engaging, well-structured content
- Create clear narratives that are informative and readable
- Ensure logical flow and coherent organization
- Use appropriate tone for the subject matter

Take the Researcher's findings and craft them into polished prose.
When done, present your draft to the Editor for review.""",
        llm_config=llm_config
    )
    
    # Create the Editor agent
    editor = AssistantAgent(
        name="Editor",
        system_message="""You are a meticulous editor. Your role is to:
- Review content for clarity, accuracy, and engagement
- Suggest improvements to structure and flow
- Check for consistency and completeness
- Provide constructive feedback

Review the Writer's draft and provide specific, actionable feedback.
If the content meets high standards, approve it. Otherwise, suggest improvements.
When satisfied, provide the final polished version.""",
        llm_config=llm_config
    )
    
    # Create a user proxy to initiate the conversation
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",  # Fully automated
        max_consecutive_auto_reply=0,
        code_execution_config=False
    )
    
    # Create the group chat
    groupchat = GroupChat(
        agents=[user_proxy, researcher, writer, editor],
        messages=[],
        max_round=10,  # Maximum conversation rounds
        speaker_selection_method="auto"  # Let the system decide who speaks next
    )
    
    # Create the manager to orchestrate the conversation
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )
    
    return {
        "user_proxy": user_proxy,
        "manager": manager,
        "agents": {
            "researcher": researcher,
            "writer": writer,
            "editor": editor
        }
    }


def run_research_task(topic: str) -> str:
    """
    Execute the research team workflow on a given topic.
    
    Returns the conversation history and final output.
    """
    print(f"\nAutoGen Research Team")
    print("=" * 60)
    print(f"Topic: {topic}")
    print("=" * 60)
    
    # Create the team
    team = create_research_team(topic)
    
    # Initiate the conversation
    initial_message = f"""Team, we need to create comprehensive content about: {topic}

Researcher: Please begin by gathering key information and insights on this topic.
Writer: Once research is complete, craft the findings into engaging content.
Editor: Review the draft and provide feedback or approval.

Let's collaborate to produce high-quality content. Researcher, please start."""

    print("\nStarting multi-agent conversation...\n")
    print("-" * 60)
    
    # Start the chat
    team["user_proxy"].initiate_chat(
        team["manager"],
        message=initial_message
    )
    
    # Extract the conversation history
    chat_history = team["manager"].groupchat.messages
    
    # Format the output
    output = "\n".join([
        f"\n[{msg.get('name', 'System')}]:\n{msg.get('content', '')}"
        for msg in chat_history
    ])
    
    print("-" * 60)
    print("\nConversation complete!")
    
    return output


def main():
    # Default research topic
    topic = "The future of sustainable urban farming technologies"
    
    print("\n" + "=" * 60)
    print("AUTOGEN MULTI-AGENT RESEARCH TEAM")
    print("=" * 60)
    
    # Run the research task
    result = run_research_task(topic)
    
    # Save the output
    output_file = "autogen_output.txt"
    with open(output_file, "w") as f:
        f.write(f"Topic: {topic}\n")
        f.write("=" * 60 + "\n")
        f.write(result)
    
    print(f"\nFull conversation saved to: {output_file}")
    print("\n" + "=" * 60)
    print("AutoGen Research Team Example Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
