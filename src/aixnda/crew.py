from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Aixnda():
    """Aixnda crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
 
    @agent
    def legal_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['legal_reviewer'],
            verbose=True,
        )

    @agent
    def recommendation_maker(self) -> Agent:
        return Agent(
            config=self.agents_config['recommendation_maker'],
            verbose=True
        )
    
    @task
    def analyze_nda_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_nda_task'],
        )

    @task
    def recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['recommendation_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Aixnda crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
