import json
import ollama

with open("saas_ideas.json", "r") as f:
    saas_ideas = json.load(f)

def analyze_idea(idea):
    """Use Ollama to analyze an idea and rank it"""
    prompt = f"Rate this SaaS idea based on innovation and market fit:\n\nTitle: {idea['title']}\nComments: {idea['comments']}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    rating = response["message"]["content"].strip()
    return rating
for idea in saas_ideas:
    idea["llm_rating"] = analyze_idea(idea)
with open("ranked_saas_ideas.json", "w") as f:
    json.dump(saas_ideas, f, indent=4)

print(" Ranked ideas using Ollama!")
