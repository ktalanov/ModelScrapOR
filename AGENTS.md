You are an AI agent that helps the user with various tasks, specifically coding and occasionally answering generaly questions. Be concise, precise, but offer the user suggestiosns if required. Update this file as necessary.

**IMPORTANT**

You are running on Fedora 43 KDE Plasma.

If you receive an insufficient privileges error, etc, re-run the command but instead of for example:

$ sudo dnf -y install nmap

replace 'sudo' with 'pkexec', for example:

$ pkexec dnf -y install nmap

This will show the user a GUI prompt that will give you elevated permissions if the user types in the correct password.

** PROJECT **

This is a single python script that:

1) Accesses an OpenAI account via its own OPENAI_SCRAPE_TOKEN located in .zshrc.
2) Gets a list of available models based on OpenRouter categories and runs queries to produces the following output, models-YYYY-MM-DD.html. For example, these are the current categories as of today, December 23 2025.

Programming
Roleplay
Marketing
SEO
Technology
Science
Translation
Legal
Finance
Health
Trivia
Academia

4) The scripts queries the OpenRouter API to produce the following file, with a separate table for each category. 

[example: models-YYYY-MM-DD.html]
# OpenRouter Models as of $current_date

## PROGRAMMING
### Daily Rankings

* 1) xAI: Grok Code Fast 1 ($0.20/$1.50)
* 2) Anthropic: Claude Sonnet 4.5 ($3/$15)
* 3) Anthropic: Claude Opus 4.5 ($5/$25)

### Rankings by Price (#1 is highest)

* 1) Anthropic: Claude Opus 4.5 ($5/$25)
* 2) Anthropic: Claude Sonnet 4.5 ($3/$15)
* 3) Google: Gemini 3 Pro Preview ($2/$12)

### Rankings by Price (#1 is lowest)

* 1) MiniMax: MiniMax M2 ($0.20/$1) (ranking: #7)
* 2) xAI: Grok Code Fast 1 ($0.20/$1.50) (ranking: #1)
* 3) Google: Gemini 3 Flash Preview ($0.50/$3) (ranking: #6)

### Best FREE modes (maximum three)

* [FREE] Kwaipilot: KAT-Coder-Pro V1 (Programming #5)
* [FREE] MiniMax: MiniMax M2 (Programming #7)
* [FREE] Mistral: Devstral 2 2512 (Programming #8)

## ROLEPLAY
### Daily Rankings

1) DeepSeek: DeepSeek V3.2 ($0.224/$0.32)
2) DeepSeek R1T2 Chimera ($0.30/$1.20)
3) DeepSeek V3 0324 ($0.20/$0.66)

### Rankings by Price (#1 is highest)
* 1) ...
[/example]

** SPECIFICS **

* COSTS

In a line such as:

Anthropic: Claude Opus 4.5 ($5/$25)

The ($5/$25) means "$5/M input tokens/$25 output tokens". Any other tokens, such as audio tokens or any other type of token is to be ignored.

* Rankings

In a line such as:

MiniMax: MiniMax M2 ($0.20/$1) (ranking: #7)

The ranking you should obtain is from the current category, in the example above it would be "Programming" so you should look for how that specific model is ranked in the programming category

** OUTCOME **

Generate an HTML file that is simple, respects dark/light mode (while also having a switch) and has a separate section for each category and separate table for each subsection.
This will not be an internet-facing website, it should be use HTML, plain JS and style.css for its needs. The python script should generated the file and the file should look the same every day, just with newly scraped information.
