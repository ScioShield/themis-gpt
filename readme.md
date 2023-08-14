## Introduction
This project aims to determine the viability of OpenAI's ChatGPT (GPT-4) at determining a SIEM rule Mitre ATT&CK technique and subtechnique IDs. The corpus of rules tested were from Elastic Security and Google's Chronicle Security products. All the Elastic rules are tagged with at least one Mitre ATT&CK ID, Chronicle Security on the other hand is more of a amalgamation of different methodologies and doesn't have a uniform meta data structure.  

## Conclusion 
Based on the results of testing ~600 Elastic and ~100 Chronicle SIEM rules it is clear that ChatGPT (GPT-4) isn't able to effectively evaluate rules and determine their Mitre ATT&CK ID. With a demonstrated maximum accuracy for Elastic (44%) and Chronicle (30%). Accuracy underperforming a coin flip. Alternative prompt engineering avenues were validated. Generic prompt alterations, changing the boilerplate question, proved ineffective (41%) on a subset of Elastic detection rules. Multiple attempts only slightly more effective at (46%). Cost for ~800 API calls was ~$30. In sum ChatGPT (GPT-4) is a invaluable assistant to the skilled analyst/engineer, not a market replacement.  

### One Shot Neutral Prompt Method
Chronicle Security detection rules  
129 rules tested  
Overall Technique matches: 10 out of 33 (30.30% matched)  
Overall Subtechnique matches: 3 out of 18 (16.67% matched)  

Elastic detection rules  
612 rules tested  
Overall Technique matches: 354 out of 800 (44.25% matched)  
Overall Subtechnique matches: 128 out of 421 (30.40% matched)  

## Methodology

`themis-gpt.py` script is the core processing component. The script is able to accept either `.toml` Elastic rules or `.yaral` Chronicle rules. The processing involves identifying and scrubbing any reference to Mitre ATT&CK within the raw rule using a selection of regex patterns. Once the references are scrubbed the rule is submitted to the API and a rule ID is returned. Upon completion a copy of the rule is saved with an extension `parsed.toml` or `parsed.yaral`. The parsed file is used by the `themis-gpt-parser.py` script. The script also features a progress bar and completion awareness to prevent resubmission.  

`themis-gpt-roulette.py` was used to identify a subset of rules for testing in a "random" manner.  

The scripts were used to exclude excessively long rules to not impinge the 2,000 token limit.  

`themis-gpt-parser.py` this is responsible for comparison of the `.parsed.*` files to the raw files. If a valid Mitre ATT&CK ID can be gathered it will then be compared with the ID output from GPT-4, if the rule matches it will count towards the total, if not then it won't. All rules are kept track of by name.  

The `*_rule_list.txt` files contain all rules tested and what rules were excluded for reasons.  

The `*_output_themis-gpt-parser.py.txt` files are the terminal output of all full runs.  

The `elastic_prompt_engineering.txt` was a validation of different prompt engineering approaches on a representative subset of 40 rules.  

## References
https://github.com/chronicle/detection-rules.git  
https://github.com/elastic/detection-rules.git  
https://invertedstone.com/tools/openai-pricing/  
https://platform.openai.com/tokenizer  