#scoring a job's compatibility
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
api_key=os.environ['OPENAI_API_KEY'], )

def scoring(user_profile, job_description):

    prompt = f"""
    Evaluate the compatibility between the following user profile of a Northwestern University student and job description. Provide a score from 0 to 100 based on the compatibility of their skills, GPA, and major.

    User Profile:
    - Skills: {', '.join(user_profile['skills'])}
    - GPA: {user_profile['gpa']}
    - Major: {user_profile['major']}
    - Year: {user_profile['year']}

    Job Description:
    {job_description}

    Please provide only the compatibility score (0-100) as a plain number with no additional text.
    """
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "You are an expert evaluator."},
              {"role": "user", "content": prompt}]
    )

    # Parse and print the response
    result = response.choices[0].message.content
    return result

# user_profile = {
#     'skills': ["python", "HTML"],
#     'gpa': "3.2", 
#     'major': ["computer science"],
#     'year': 2,
# }

# job_description = "We dont expect you to have a background in finance or any other specific field—we’re looking for smart people who enjoy solving interesting problems. We’re more interested in how you think and learn than what you currently know. You should be:A strong quantitative thinker who enjoys working collaboratively on a team Eager to ask questions, admit mistakes, and learn new things There is a strong technology component to our trading strategy. Knowing a particular programming language is not required, but general programming experience is a plus. If you’d like to learn more, you can read about all the internships we offer, our interview process, and meet some of our newest hires.If you're a recruiting agency and want to partner with us, please reach out to agency-partnerships@janestreet.com."

# print(scoring(user_profile, job_description))

