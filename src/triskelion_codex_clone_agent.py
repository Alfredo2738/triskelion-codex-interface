import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class CloneAgent:
    def __init__(self, name, parent_user, traits):
        self.name = name
        self.parent_user = parent_user
        self.traits = traits
        self.memory_log = []
        self.clone_id = f"{parent_user.user_id}_{name}"
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def respond(self, prompt):
        styled_prompt = self.process_prompt(prompt, self.traits)

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a personalized Codex clone. Respond according to your behavioral traits."},
                    {"role": "user", "content": styled_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            reply = response.choices[0].message.content
            self.memory_log.append({"prompt": prompt, "response": reply})
            return reply
        except Exception as e:
            return f"[Codex Error]: {str(e)}"

    def process_prompt(self, prompt, traits):
        style_prefix = self.apply_tone_style(traits['tone'], traits.get('formality', 'medium'))
        task_prefix = self.apply_task_bias(traits.get('task_bias', 'general'))
        memory_context = self.get_context(traits.get('memory_depth', 'session-only'))
        return f"{memory_context}\n{style_prefix}\n{task_prefix}\nUser: {prompt}"

    def apply_tone_style(self, tone, formality):
        if tone == "poetic":
            return "Respond in a lyrical, metaphor-rich manner."
        elif tone == "formal":
            return "Respond with high-register academic language."
        elif tone == "casual":
            return "Respond in a friendly, conversational tone."
        else:
            return f"Respond in a {formality} style."

    def apply_task_bias(self, task_bias):
        bias_map = {
            "code": "This is a code generation task.",
            "summarization": "Provide a clear and structured summary.",
            "creative writing": "Create a vivid and imaginative response.",
            "Q&A": "Answer the question precisely and informatively.",
            "general": ""
        }
        return bias_map.get(task_bias, "")

    def get_context(self, memory_depth):
        if memory_depth == "long":
            return "[Recall long-term user history and stylistic patterns.]"
        elif memory_depth == "short-term":
            return "[Refer to recent session data.]"
        else:
            return "[Fresh interaction; no prior context.]"

