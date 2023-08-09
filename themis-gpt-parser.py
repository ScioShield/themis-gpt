import os
import re

def extract_ids_from_raw(file_path):
    technique_pattern = r'\[\[rule\.threat\.technique\]\](?:.*\n)*?\s*id = "(T[0-9]+)"'
    subtechnique_pattern = r'\[\[rule\.threat\.technique\.subtechnique\]\](?:.*\n)*?\s*id = "(T[0-9]+\.[0-9]+)"'

    with open(file_path, 'r') as file:
        content = file.read()

    technique_matches = re.findall(technique_pattern, content)
    subtechnique_matches = re.findall(subtechnique_pattern, content)

    return technique_matches, subtechnique_matches

def extract_ids_from_parsed(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    technique_matches = re.findall(r'Technique = (T[0-9]+)', content)
    subtechnique_matches_raw = re.findall(r'Subtechnique = ([\w\.]+(?:, [\w\.]+)*)', content)
    
    # Flatten the list and extract individual subtechniques
    subtechnique_matches = [item.strip() for sublist in subtechnique_matches_raw for item in sublist.split(',')]
    
    # Remove any 'None' values from the list
    subtechnique_matches = [s for s in subtechnique_matches if s != 'None']

    return technique_matches, subtechnique_matches

def extract_ids_from_yar(file_path):
    url_pattern = r'(?:reference|mitre_attack_url) = "https://attack\.mitre\.org/techniques/(T\d{4})(?:/(\d{3}))?/?'

    with open(file_path, 'r') as file:
        content = file.read()

    matches = re.findall(url_pattern, content)

    technique_matches = [match[0] for match in matches]
    subtechnique_matches = [f"{match[0]}.{match[1]}" for match in matches if match[1]]

    return technique_matches, subtechnique_matches

def compare_ids_for_file(raw_file, parsed_file):
    if raw_file.endswith('.toml'):
        raw_techniques, raw_subtechniques = extract_ids_from_raw(raw_file)
        parsed_techniques, parsed_subtechniques = extract_ids_from_parsed(parsed_file)

        m_tech = len(set(raw_techniques).intersection(set(parsed_techniques)))
        t_tech = len(raw_techniques)
        m_subtech = len(set(raw_subtechniques).intersection(set(parsed_subtechniques)))
        t_subtech = len(raw_subtechniques)
        
        return m_tech, t_tech, m_subtech, t_subtech

    elif raw_file.endswith('.yaral'):
        raw_techniques, raw_subtechniques = extract_ids_from_yar(raw_file)
        parsed_techniques, parsed_subtechniques = extract_ids_from_parsed(parsed_file)

        m_tech = len(set(raw_techniques).intersection(set(parsed_techniques)))
        t_tech = len(raw_techniques)
        m_subtech = len(set(raw_subtechniques).intersection(set(parsed_subtechniques)))
        t_subtech = len(raw_subtechniques)

        return m_tech, t_tech, m_subtech, t_subtech

    else:
        return 0, 0, 0, 0  # Unsupported file type
    
def main():
    directory_path = input("Enter the path of the directory: ")

    total_techniques = 0
    matched_techniques = 0
    total_subtechniques = 0
    matched_subtechniques = 0

    for filename in os.listdir(directory_path):
        if filename.endswith('.toml') and not filename.endswith('.parsed.toml'):
            raw_file = os.path.join(directory_path, filename)
            parsed_file = os.path.join(directory_path, filename.rsplit('.', 1)[0] + ".parsed.toml")
            
            m_tech, t_tech, m_subtech, t_subtech = compare_ids_for_file(raw_file, parsed_file)
            matched_techniques += m_tech
            total_techniques += t_tech
            matched_subtechniques += m_subtech
            total_subtechniques += t_subtech

            print(f"For file {filename}:")
            print(f"Techniques matched: {m_tech}/{t_tech}")
            print(f"Subtechniques matched: {m_subtech}/{t_subtech}\n")

        elif filename.endswith('.yaral') and not filename.endswith('.parsed.yaral'):
            raw_file = os.path.join(directory_path, filename)
            parsed_file = os.path.join(directory_path, filename.rsplit('.', 1)[0] + ".parsed.yaral")
            
            # Using the function specific to yar files
            raw_techniques, raw_subtechniques = extract_ids_from_yar(raw_file)
            parsed_techniques, parsed_subtechniques = extract_ids_from_parsed(parsed_file)

            m_tech = len(set(raw_techniques).intersection(set(parsed_techniques)))
            t_tech = len(raw_techniques)
            m_subtech = len(set(raw_subtechniques).intersection(set(parsed_subtechniques)))
            t_subtech = len(raw_subtechniques)

            matched_techniques += m_tech
            total_techniques += t_tech
            matched_subtechniques += m_subtech
            total_subtechniques += t_subtech

            print(f"For file {filename}:")
            print(f"Techniques matched: {m_tech}/{t_tech}")
            print(f"Subtechniques matched: {m_subtech}/{t_subtech}\n")

    technique_match_percentage = (matched_techniques / total_techniques) * 100 if total_techniques else 0
    subtechnique_match_percentage = (matched_subtechniques / total_subtechniques) * 100 if total_subtechniques else 0

    print(f"Overall Technique matches: {matched_techniques} out of {total_techniques} ({technique_match_percentage:.2f}% matched)")
    print(f"Overall Subtechnique matches: {matched_subtechniques} out of {total_subtechniques} ({subtechnique_match_percentage:.2f}% matched)")

if __name__ == "__main__":
    main()
