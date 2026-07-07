from tools import web_search_tool
from models import ChosenJob
from models import RankedJobList
from models import JobList
import dotenv
import os
dotenv.load_dotenv()

from crewai import Crew,Task,Agent
from crewai.project import CrewBase,agent,task,crew
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource


os.getenv("COHERE_API_KEY")

resume_knowledge = TextFileKnowledgeSource(
    file_path=[
        "resume.txt"
    ]
)


@CrewBase
class JobHunterCrew:
    @agent
    def job_search_agent(self):
        return Agent(config=self.agents_config['job_search_agent'],tools=[web_search_tool])

    @agent
    def job_matching_agent(self):
        return Agent(config=self.agents_config['job_matching_agent'], knowledge_sources=[resume_knowledge])
    
    @agent
    def resume_optimization_agent(self):
        return Agent(config=self.agents_config['resume_optimization_agent'], knowledge_sources=[resume_knowledge])
    
    @agent
    def company_research_agent(self):
        return Agent(config=self.agents_config['company_research_agent'], tools=[web_search_tool], knowledge_sources=[resume_knowledge])
    
    @agent
    def interview_prep_agent(self):
        return Agent(config=self.agents_config['interview_prep_agent'], knowledge_sources=[resume_knowledge])
    
    @task
    def job_extraction_task(self):
        return Task(config=self.tasks_config['job_extraction_task'],output_pydantic=JobList)
    
    @task
    def job_matching_task(self):
        return Task(config=self.tasks_config['job_matching_task'], output_pydantic=RankedJobList)
    
    @task
    def job_selection_task(self):
        return Task(config=self.tasks_config['job_selection_task'], output_pydantic=ChosenJob)
    
    @task
    def resume_rewriting_task(self):
        return Task(config=self.tasks_config['resume_rewriting_task'])
    
    @task
    def company_research_task(self):
        return Task(config=self.tasks_config['company_research_task'], context=[self.job_selection_task()])
    
    @task
    def interview_prep_task(self):
        return Task(config=self.tasks_config['interview_prep_task'],context=[self.job_selection_task(), self.resume_rewriting_task(), self.company_research_task()])
    
    @crew
    def assemble_crew(self):
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            verbose=True
        )

JobHunterCrew().assemble_crew().kickoff(inputs={"level":"Junior","position":"Full stack developer","location":"Remote"})
    
        