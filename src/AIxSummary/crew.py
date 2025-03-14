from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class AIxSummary():
    """AIxSummary crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
 
    @agent
    def document_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['document_summarizer'],
            verbose=True,
        )

    @agent
    def summary_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_reviewer'],
            verbose=True
        )
    
    @task
    def summarize_document_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_document_task'],
        )

    @task
    def review_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_summary_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AIxSummary crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
