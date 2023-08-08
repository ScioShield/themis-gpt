import re
import os
import openai  # ensure you have imported the openai package
from dotenv import load_dotenv

def setup_api_credentials():
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_key

def call_openai_api(prompt, content, model="gpt-4"):
    input_string = f"{prompt}\n{content}"
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": input_string}]
    )

    summary = completion['choices'][0]['message']["content"]
    return summary

def remove_text_from_file_regex(file_path, new_file_path):
    patterns_to_remove = [
        r'\[\[rule\.threat\]\]',
        r'framework = ".*"',
        r'\[\[rule\.threat\.technique\]\]',
        r'\[\[rule.threat.technique.subtechnique\]\]',
        r'id = ".*"',
        r'name = ".*"',
        r'reference = ".*"',
        r'\[rule\.threat\.tactic\]'
    ]
    
    technique_pattern = r'\[\[rule\.threat\.technique\]\]'
    subtechnique_pattern = r'\[\[rule.threat.technique.subtechnique\]\]'
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Count the number of techniques and subtechniques
    technique_count = sum(1 for line in lines if re.match(technique_pattern, line))
    subtechnique_count = sum(1 for line in lines if re.match(subtechnique_pattern, line))
    
    parsed_lines = [line for line in lines if not any(re.match(pattern, line.strip()) for pattern in patterns_to_remove)]

    with open(new_file_path, 'w') as new_file:
        for line in parsed_lines:
            new_file.write(line)
        
        # Dynamically format your question prompt based on the count
        question = f"""Give me {technique_count} techniques and {subtechnique_count} subtechniques that this rule would fit? JUST GIVE THE IDs, no explanation. In the format for each technique or subtechnique:
        Technique = ID or None
        Subtechnique = ID or None"""

        # Call the OpenAI API using the question and the processed text, and append the output to the new file
        api_output = call_openai_api(question, ''.join(parsed_lines))
        new_file.write("\n" + api_output)

def main():
    directory_path = input("Enter the path of the directory: ")

    for filename in os.listdir(directory_path):
        if filename.endswith('.toml'):
            old_file = os.path.join(directory_path, filename)
            new_file = os.path.join(directory_path, filename.rsplit('.', 1)[0] + ".parsed.toml")
            remove_text_from_file_regex(old_file, new_file)

if __name__ == "__main__":
    main()
