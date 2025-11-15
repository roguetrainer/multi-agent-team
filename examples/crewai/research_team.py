"""
CrewAI Research Team Example
=============================
Demonstrates multi-agent collaboration using CrewAI's role-based approach.
Agents have defined roles, goals, and backstories, with explicit task delegation.
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI


def create_research_team(topic: str) -> Crew:
    """
    Create a research team with Researcher, Writer, and Editor agents.
    
    CrewAI uses role-based coordination where each agent has a clear
    role, goal, and backstory, and tasks are delegated explicitly.
    """
    
    # Configure the LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )
    
    # Create the Researcher agent
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Conduct thorough research and gather comprehensive information on assigned topics",
        backstory="""You are an experienced research analyst with a keen eye for detail 
and a passion for uncovering insights. You have years of experience synthesizing 
complex information from multiple sources into clear, actionable findings. 
You pride yourself on accuracy and thoroughness.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Create the Writer agent
    writer = Agent(
        role="Content Writer",
        goal="Transform research findings into engaging, well-structured content",
        backstory="""You are a skilled writer who excels at taking complex information 
and making it accessible and engaging. You have a talent for narrative flow 
and know how to structure content for maximum impact. You always ensure your 
writing is clear, informative, and tailored to the audience.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Create the Editor agent
    editor = Agent(
        role="Senior Editor",
        goal="Review and refine content to ensure quality, clarity, and accuracy",
        backstory="""You are a meticulous editor with decades of experience in 
publishing. You have an eye for detail and a commitment to excellence. 
You provide constructive feedback that improves content while maintaining 
the author's voice. You ensure every piece meets the highest standards.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Define the research task
    research_task = Task(
        description=f"""Conduct comprehensive research on: {topic}
        
Your research should include:
1. Key concepts and definitions
2. Current trends and developments
3. Important statistics or data points
4. Expert opinions and perspectives
5. Challenges and opportunities
6. Future outlook

Compile your findings in a structured format that will be useful for content creation.""",
        expected_output="A comprehensive research report with organized findings, key insights, and supporting data",
        agent=researcher
    )
    
    # Define the writing task
    writing_task = Task(
        description=f"""Using the research findings provided, create an engaging article about: {topic}
        
Your article should:
1. Have a compelling introduction that hooks the reader
2. Present information in a logical, flowing structure
3. Include relevant examples and insights from the research
4. Use clear, accessible language
5. Have a strong conclusion with key takeaways

The article should be informative, engaging, and approximately 500-800 words.""",
        expected_output="A well-written, engaging article that effectively communicates the research findings",
        agent=writer,
        context=[research_task]  # This task depends on research
    )
    
    # Define the editing task
    editing_task = Task(
        description="""Review and refine the article draft.
        
Your review should:
1. Check for clarity and readability
2. Ensure accuracy of information
3. Improve flow and structure where needed
4. Fix any grammatical or stylistic issues
5. Enhance engagement and impact

Provide the final polished version of the article.""",
        expected_output="A polished, publication-ready article with all improvements incorporated",
        agent=editor,
        context=[writing_task]  # This task depends on writing
    )
    
    # Create the crew
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,  # Tasks execute in order
        verbose=True
    )
    
    return crew


def run_research_task(topic: str) -> str:
    """
    Execute the research team workflow on a given topic.
    
    Returns the final output from the crew.
    """
    print(f"\nCrewAI Research Team")
    print("=" * 60)
    print(f"Topic: {topic}")
    print("=" * 60)
    
    # Create the crew
    crew = create_research_team(topic)
    
    print("\nStarting crew execution...\n")
    print("-" * 60)
    
    # Execute the crew's tasks
    result = crew.kickoff()
    
    print("-" * 60)
    print("\nCrew execution complete!")
    
    return str(result)


def main():
    # Default research topic
    topic = "The future of sustainable urban farming technologies"
    
    print("\n" + "=" * 60)
    print("CREWAI MULTI-AGENT RESEARCH TEAM")
    print("=" * 60)
    
    # Run the research task
    result = run_research_task(topic)
    
    # Display the final result
    print("\n" + "=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print(result)
    
    # Save the output
    output_file = "crewai_output.txt"
    with open(output_file, "w") as f:
        f.write(f"Topic: {topic}\n")
        f.write("=" * 60 + "\n")
        f.write(result)
    
    print(f"\nFinal output saved to: {output_file}")
    print("\n" + "=" * 60)
    print("CrewAI Research Team Example Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
