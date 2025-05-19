# === TRISKELION Codex Clone Agent with OpenAI API Integration ===

import openai

# Set your OpenAI API key
openai.api_key = "sk-...REPLACE_WITH_YOUR_KEY..."

# -----------------------------
# CloneAgent class with Codex API
# -----------------------------
class CloneAgent:
    def __init__(self, name, parent_user, traits):
        self.name = name
        self.parent_user = parent_user
        self.traits = traits
        self.memory_log = []
        self.clone_id = f"{parent_user.user_id}_{name}"

    def respond(self, prompt):
        styled_prompt = self.process_prompt(prompt, self.traits)

        # --- OpenAI Codex API call ---
        try:
            response = openai.Completion.create(
                engine="code-davinci-002",  # Codex model
                prompt=styled_prompt,
                max_tokens=300,
                temperature=0.5,
                n=1,
                stop=None
            )
            output = response.choices[0].text.strip()
        except Exception as e:
            output = f"[Error]: {str(e)}"

        self.memory_log.append({"prompt": prompt, "response": output})
        return output

    def process_prompt(self, prompt, traits):
        style_prefix = self.apply_tone_style(traits['tone'], traits.get('formality', 'medium'))
        task_prefix = self.apply_task_bias(traits.get('task_bias', 'general'))
        memory_context = self.get_context(traits.get('memory_depth', 'session-only'))

        full_prompt = f"{memory_context}\n{style_prefix}\n{task_prefix}\nUser: {prompt}"
        return full_prompt

    def apply_tone_style(self, tone, formality):
        if tone == "poetic":
            return "Respond in a lyrical, metaphoric style."
        elif tone == "formal":
            return "Use academic, precise language."
        elif tone == "casual":
            return "Use a relaxed, conversational tone."
        else:
            return f"Use a general {formality} tone."

    def apply_task_bias(self, task_bias):
        task_map = {
            "code": "This is a Python code generation task.",
            "summarization": "Summarize the following information.",
            "creative writing": "Write a creative, narrative response.",
            "Q&A": "Answer the question clearly and concisely.",
            "general": ""
        }
        return task_map.get(task_bias, "")

    def get_context(self, memory_depth):
        if memory_depth == "long":
            return "[Recall past related user queries and coding examples.]"
        elif memory_depth == "short-term":
            return "[Use only the last few interactions.]"
        else:
            return "[No previous context. Begin fresh.]"

# -----------------------------
# Example User and Clone
# -----------------------------
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.clones = []

    def create_clone(self, clone_name, traits):
        clone = CloneAgent(clone_name, self, traits)
        self.clones.append(clone)
        return clone

# Create example user + clone
user = User(user_id="U001", name="Ori’el")
traits = {
    "tone": "formal",
    "formality": "high",
    "memory_depth": "short-term",
    "task_bias": "code"
}
codex_clone = user.create_clone("DevHelper", traits)

# Run prompt
response = codex_clone.respond("Write a Python function that reverses a string.")
print(response)
