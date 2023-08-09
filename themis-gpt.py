import re
import os
import openai  # ensure you have imported the openai package
from dotenv import load_dotenv
from tqdm import tqdm
import time

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
        r'\[rule\.threat\.tactic\]',
        r'mitre = ".*"',
        r'mitre_attack_tactic = ".*"',
        r'mitre_attack_technique = ".*"',
        r'mitre_attack_url = ".*"',
        r'tactics = ".*"',
        r'/\*.*?\*/'
    ]

    technique_pattern = r'\[\[rule\.threat\.technique\]\]'
    subtechnique_pattern = r'\[\[rule.threat.technique.subtechnique\]\]'

    with open(file_path, 'r') as file:
        content = file.read()

    # Count the number of techniques and subtechniques
    technique_count = sum(1 for match in re.finditer(technique_pattern, content))
    subtechnique_count = sum(1 for match in re.finditer(subtechnique_pattern, content))
    
    # Process content by removing patterns and modifying rule name
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    content = re.sub(r"rule mitre_attack_(T\d{4})_(\d{3})_", 'rule ', content)

    with open(new_file_path, 'w') as new_file:
        new_file.write(content)

        # Dynamically format your question prompt based on the count
        question = f"""Give me {technique_count} techniques and {subtechnique_count} subtechniques that this rule would fit? JUST GIVE THE IDs, no explanation. In the format for each technique or subtechnique:
        Technique = ID or None
        Subtechnique = ID or None"""

        # If you're calling an OpenAI API or another service, add the call here.
        api_output = call_openai_api(question, content)
        new_file.write("\n" + api_output)
        time.sleep(0.5)

def main():
    directory_path = input("Enter the path of the directory: ")

    # Get all the .toml and .yaral files
    all_files_toml = [f for f in os.listdir(directory_path) if f.endswith('.toml')]
    all_files_yaral = [f for f in os.listdir(directory_path) if f.endswith('.yaral')]

    # Filter out the .toml files which have a corresponding .parsed.toml
    to_process_toml = [f for f in all_files_toml if not os.path.exists(os.path.join(directory_path, f.rsplit('.', 1)[0] + ".parsed.toml")) and not f.endswith(".parsed.toml")]

    # Filter out the .yaral files which have a corresponding .parsed.yaral
    to_process_yaral = [f for f in all_files_yaral if not os.path.exists(os.path.join(directory_path, f.rsplit('.', 1)[0] + ".parsed.yaral")) and not f.endswith(".parsed.yaral")]

    # Combine both lists
    to_process = to_process_toml + to_process_yaral

    for filename in tqdm(to_process, desc="Processing files", unit="file"):
        old_file = os.path.join(directory_path, filename)
        
        # Decide on the new file extension based on the current file's extension
        if filename.endswith(".toml"):
            new_file_name = filename.rsplit('.', 1)[0] + ".parsed.toml"
        elif filename.endswith(".yaral"):
            new_file_name = filename.rsplit('.', 1)[0] + ".parsed.yaral"

        new_file = os.path.join(directory_path, new_file_name)

        # Process the file
        remove_text_from_file_regex(old_file, new_file)

if __name__ == "__main__":
    main()
