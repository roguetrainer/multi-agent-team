"""
Multi-Agent Framework Comparison Script
========================================
Runs the same research task on both AutoGen and CrewAI to compare approaches.
"""

import argparse
import time
import sys
from pathlib import Path

# Add examples to path
sys.path.insert(0, str(Path(__file__).parent))

from examples.autogen.research_team import run_research_task as run_autogen
from examples.crewai.research_team import run_research_task as run_crewai


def run_comparison(topic: str):
    """Run both frameworks on the same topic and compare results."""
    
    print("=" * 70)
    print("MULTI-AGENT FRAMEWORK COMPARISON")
    print("=" * 70)
    print(f"\nResearch Topic: {topic}")
    print("\nThis comparison will run the same research task on both frameworks")
    print("to demonstrate their different approaches to multi-agent orchestration.")
    print("\n" + "-" * 70)
    
    results = {}
    
    # Test AutoGen
    print("\n[1/2] AUTOGEN")
    print("-" * 70)
    print("Approach: Conversation-centric multi-agent dialogue")
    print("Agents communicate through natural chat-based interaction\n")
    
    try:
        start = time.time()
        autogen_result = run_autogen(topic)
        autogen_time = time.time() - start
        
        results["autogen"] = {
            "output": autogen_result,
            "time": autogen_time,
            "success": True
        }
        
        print(f"\nExecution time: {autogen_time:.2f}s")
        
        # Save AutoGen output
        with open("comparison_autogen_output.txt", "w") as f:
            f.write(f"Topic: {topic}\n")
            f.write(f"Framework: AutoGen\n")
            f.write(f"Execution Time: {autogen_time:.2f}s\n")
            f.write("=" * 70 + "\n")
            f.write(autogen_result)
        
    except Exception as e:
        print(f"Error: {e}")
        results["autogen"] = {"error": str(e), "success": False}
    
    # Test CrewAI
    print("\n\n[2/2] CREWAI")
    print("-" * 70)
    print("Approach: Role-based task delegation")
    print("Agents have defined roles and tasks execute sequentially\n")
    
    try:
        start = time.time()
        crewai_result = run_crewai(topic)
        crewai_time = time.time() - start
        
        results["crewai"] = {
            "output": crewai_result,
            "time": crewai_time,
            "success": True
        }
        
        print(f"\nExecution time: {crewai_time:.2f}s")
        
        # Save CrewAI output
        with open("comparison_crewai_output.txt", "w") as f:
            f.write(f"Topic: {topic}\n")
            f.write(f"Framework: CrewAI\n")
            f.write(f"Execution Time: {crewai_time:.2f}s\n")
            f.write("=" * 70 + "\n")
            f.write(crewai_result)
        
    except Exception as e:
        print(f"Error: {e}")
        results["crewai"] = {"error": str(e), "success": False}
    
    # Summary
    print("\n\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    
    print("\n1. EXECUTION TIMES")
    print("-" * 40)
    if results.get("autogen", {}).get("success"):
        print(f"   AutoGen: {results['autogen']['time']:.2f}s")
    else:
        print(f"   AutoGen: FAILED - {results.get('autogen', {}).get('error', 'Unknown error')}")
    
    if results.get("crewai", {}).get("success"):
        print(f"   CrewAI:  {results['crewai']['time']:.2f}s")
    else:
        print(f"   CrewAI:  FAILED - {results.get('crewai', {}).get('error', 'Unknown error')}")
    
    print("\n2. KEY DIFFERENCES")
    print("-" * 40)
    print("""
   AutoGen:
   - Conversation-based: Agents talk to each other
   - Emergent behavior: Flow determined by dialogue
   - Flexible: Can handle back-and-forth discussion
   - Output: Full conversation transcript
   
   CrewAI:
   - Task-based: Explicit task definitions
   - Sequential: Clear workflow order
   - Structured: Defined inputs/outputs per task
   - Output: Final deliverable from last task
""")
    
    print("3. WHEN TO USE EACH")
    print("-" * 40)
    print("""
   AutoGen is better for:
   - Brainstorming and ideation
   - Iterative refinement through dialogue
   - Complex reasoning requiring debate
   - Scenarios needing flexible agent interaction
   
   CrewAI is better for:
   - Structured workflows with clear stages
   - Production pipelines needing predictability
   - Clear role separation and task handoffs
   - Scenarios requiring defined deliverables
""")
    
    print("4. OUTPUT FILES")
    print("-" * 40)
    print("   comparison_autogen_output.txt - Full AutoGen conversation")
    print("   comparison_crewai_output.txt  - Final CrewAI deliverable")
    
    print("\n" + "=" * 70)
    print("For lightweight RAG comparisons, see:")
    print("https://github.com/roguetrainer/agentic-rag")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Compare AutoGen and CrewAI multi-agent frameworks"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="The future of sustainable urban farming technologies",
        help="Research topic for the agents to work on"
    )
    
    args = parser.parse_args()
    run_comparison(args.topic)


if __name__ == "__main__":
    main()
