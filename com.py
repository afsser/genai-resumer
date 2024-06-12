
#!/usr/bin/env python3.10

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

import os

# https://www.linkedin.com/jobs/view/3948356909

from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent
from crewai import Task, Crew

def get_job_description(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_description = soup.find('div', class_='details mx-details-container-padding').text
    return job_description

url = 'https://www.linkedin.com/jobs/view/3948356909'
job_description = get_job_description(url)

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash",verbose = True,temperature = 0.1,google_api_key="AIzaSyCUjNpDbC2ZtnErTqgdkMH09WH2SjkgLdw")

# Creating a senior researcher agent with memory and verbose mode
resumer = Agent(
  role='Resumer',
  goal='resume the job description',
  verbose=True,
  memory=True,
  backstory=(
    "You are part of a crew of agents that enhances a resumé"
    "based on a job description. You are the one that makes the"
    "first step, by making a detailed resume of the job description: {job_description} acquired from the given URL"

  ),
  llm=model,
  allow_delegation=True
)

# # Creating a writer agent with custom tools and delegation capability
suitor = Agent(
  role='Suitor',
  goal='Build a complete resumé, adapted to the job description resume.',
  verbose=True,
  memory=True,
  backstory=(
    "You are part of a crew of agents that enhances a resumé"
	"You are an expert in making complete resumés based on job descriptions."
  ),
  llm=model,
  allow_delegation=False
)

# Research task
resume_task = Task(
  description=(
    "Gather all informations related to abilities required by this job and make a 3 paragraphs long resume of it."
    "focus on the main abilities and requirements of the job description."
  ),
  expected_output='A comprehensive 3 paragraphs long resume of all the informations in the job description.',
  agent=resumer,
)

# Writing task with language model configuration

# suit_task = Task(
#   description=(
#     "The objective is to edit the resumé to be the best possible attending the job description using the given informations by the applicant"
#     "The new resumé must respect the informations of the person applying to the job, all informations must have been declared by the applicant in his resumé"
#   ),
#   expected_output='A resumé based on the given resumé but suited to the job description.',
#   agent=suitor,
#   async_execution=False,
#   output_file='new-resume.md'  # Example of output customization
# )

# Writing task with language model configuration
suit_task = Task(
  description=(
    "The objective is to craft a resumé to be the best possible attending the job description using the given informations by the applicant"
  ),
  expected_output='A resumé based on the given resumé but suited to the job description.',
  agent=suitor,
  async_execution=False,
  output_file='new-resume.md'  # Example of output customization
)


crew = Crew(
            agents=[resumer, suitor],
            tasks=[resume_task, suit_task],
            verbose=2
        )

result = crew.kickoff()
# result = crew.kickoff(inputs={'topic': 'AI in healthcare'})

