import streamlit as st
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

def main():
    st.title("Resume Generator")

    # Fields for input
    job_desc_url = st.text_input("Job Description URL:")
    github_url = st.text_input("GitHub Profile URL:")
    linkedin_url = st.text_input("LinkedIn Profile URL:")
    qualifications_file = st.file_uploader("Upload Additional Qualifications:")
    resume_file = st.file_uploader("Upload Current Resume:")

    # Button to start the process
    if st.button("Generate Resume"):
        # Process to generate the resume
        generated_resume = generate_resume(job_desc_url, github_url, linkedin_url, qualifications_file, resume_file)

        # Display the generated resume
        st.write("Generated Resume:")
        st.write(generated_resume)

    # Configuration options
    api_key = st.text_input("Enter API Key for LLM:")

    # Field for human feedback
    human_feedback = st.text_area("Human Feedback:")

    # Field to point to local documents
    local_documents = st.file_uploader("Upload Local Documents for Additional Input:")

    # Toggle to enable/disable internet search
    internet_search = st.checkbox("Enable Internet Search")

def generate_resume(job_desc_url, github_url, linkedin_url, qualifications_file, resume_file):
    # Placeholder for resume generation process
    # This function will be implemented based on your requirements
    # For now, it just returns a sample resume
    return """
    Name: John Doe
    Education: Bachelor's in Computer Science
    Experience: Software Engineer with 5 years of experience
    Skills: Python, JavaScript, React, Django
    """

# Função para obter a descrição da vaga
def get_job_description(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_description = soup.find('div', class_='show-more-less-html__markup relative overflow-hidden').text
    return job_description

# Função para gerar conteúdo do currículo

# def generate_resume_content(job_description, current_resume=None):
#     prompt = f"Baseado na seguinte descrição de vaga: {job_description}, gere um currículo otimizado."
#     if current_resume:
#         prompt += f" Aqui está o currículo atual: {current_resume}"
    
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=1500
#     )
#     return response.choices[0].text


# Exemplo de uso
url = 'https://www.linkedin.com/jobs/view/3948356909'
job_description = get_job_description(url)
# resume_content = generate_resume_content(job_description)
# print(resume_content)
# print(job_description)

if __name__ == "__main__":
    main()
