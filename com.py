
#!/usr/bin/env python3.10

from dotenv import load_dotenv

import os

from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent
from crewai import Task, Crew
# search_tool = SerperDevTool()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash",verbose = True,temperature = 0.1,google_api_key="AIzaSyCUjNpDbC2ZtnErTqgdkMH09WH2SjkgLdw")

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='',
  goal='Uncover groundbreaking technologies in {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "Driven by curiosity, you're at the forefront of"
    "innovation, eager to explore and share knowledge that could change"
    "the world."
  ),
  llm=model,
  allow_delegation=True
)

# # Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Narrate compelling tech stories about {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "With a flair for simplifying complex topics, you craft"
    "engaging narratives that captivate and educate, bringing new"
    "discoveries to light in an accessible manner."
  ),
  llm=model,
  allow_delegation=False
)

# Research task
research_task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points,"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  agent=writer,
  async_execution=False,
  output_file='new-blog-post.md'  # Example of output customization
)


crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, write_task],
            verbose=2
        )

result = crew.kickoff(inputs={'topic': 'AI in healthcare'})