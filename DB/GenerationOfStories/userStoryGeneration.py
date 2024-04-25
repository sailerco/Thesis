import random
import pandas as pd
from transformers import pipeline
import torch

# Load the dataset
data = pd.read_csv('../datasets/Roles_small.csv')

# Initialize the GPT-2 model and tokenizer
model = pipeline("text-generation", model="meta-llama/Meta-Llama-3-70B", model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto", token="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")

# Function to select a random role, then choose a few skills
def select_role_and_skills():
    row = random.choice(data.index)
    selected_role = data.loc[row, 'Job Role']
    selected_skills = data.loc[row, 'skill']
    # Convert the string of skills to a list
    selected_skills = selected_skills.split(', ')
    random_number = random.uniform(0, 0.5)
    sample_size = int(len(selected_skills) * random_number)
    random_skills = random.sample(selected_skills, sample_size)
    return selected_role, random_skills

# Function to generate user story using GPT-2 model
def generate_user_story(role, skills):
    #prompt = "User Story for a Software Project: As a " + role + ", with the skills in " + ', '.join(skills) + " so that"
    #prompt = f"As a {role}, I want to use my skills in {', '.join(skills)} so that"
    #prompt = f"User Story in the form of: (As a [role] i want to [action] so i can [goal]) As a {role} with my skills in {', '.join(skills)} i want to"
    #prompt = f"The following is a user story (in this format: As a [role] i want to [action] so i can [goal]) based on the skills {', '.join(skills)}: "
    prompt = f"Based on the following skills {', '.join(skills)} generate a user story, in the following format 'As a role, I want to action, so I can goal' that would be solvable by the assignee who works in a software company."

    user_story = model(prompt, max_length=100, truncation=True)[0]['generated_text']
    #input_ids = tokenizer.encode(prompt, return_tensors="pt", max_length=100, truncation=True)
    #output = model.generate(input_ids, do_sample=True, max_length=150, pad_token_id=tokenizer.eos_token_id, num_return_sequences=1)
    #user_story = tokenizer.decode(output[0], skip_special_tokens=True)
    return user_story

# Main function to run the script
def main():
    role, skills = select_role_and_skills()
    user_story = generate_user_story(role, skills)
    print("Randomly Selected Role:", role)
    print("Selected Skills:", skills)
    print("Generated User Story:", user_story)

# Execute the script
if __name__ == "__main__":
    main()
