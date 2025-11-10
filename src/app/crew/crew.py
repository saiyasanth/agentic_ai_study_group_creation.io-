# src/app/crew/crew.py
# Crew definition using CrewAI patterns from docs

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List
from .. import matching, database, crud
from sqlalchemy.orm import Session


@CrewBase
class StudyMatchingCrew:
    agents_config = {
        "profile_analyzer": {
            "role": "Profile Analyzer",
            "goal": "Analyze student academic profile"
        },
        "schedule_coordinator": {
            "role": "Schedule Coordinator",
            "goal": "Find optimal meeting times"
        },
        "performance_matcher": {
            "role": "Performance Matcher",
            "goal": "Find complementary peers"
        },
        "group_facilitator": {
            "role": "Group Facilitator",
            "goal": "Form and persist study groups"
        },
    }

    # ---------------------------
    # Agents
    # ---------------------------

    @agent
    def profile_analyzer(self) -> Agent:
        return Agent(config=self.agents_config["profile_analyzer"], verbose=True)

    @agent
    def schedule_coordinator(self) -> Agent:
        return Agent(config=self.agents_config["schedule_coordinator"], verbose=True)

    @agent
    def performance_matcher(self) -> Agent:
        return Agent(config=self.agents_config["performance_matcher"], verbose=True)

    @agent
    def group_facilitator(self) -> Agent:
        return Agent(config=self.agents_config["group_facilitator"], verbose=True)

    # ---------------------------
    # Tasks
    # ---------------------------

    @task
    def recommend_peers_task(self) -> Task:
        return Task(
            config={
                "description": "Run recommendation flow",
                "expected_output": "List of matched peers"
            }
        )

    # ---------------------------
    # Crew Orchestration
    # ---------------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # agents run one after another
            verbose=True
        )


# ---------------------------
# Helper function to kickoff matching
# ---------------------------

def kickoff_recommendations(student_id: int, top_k: int = 5):
    """
    Run the matching logic (currently local DB function).
    Later, agents can call this or extend it with more AI logic.
    """
    db: Session = database.SessionLocal()
    matches = matching.top_k_matches(db, student_id, top_k)
    db.close()
    return matches
