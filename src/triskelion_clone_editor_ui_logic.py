"""
TRISKELION Clone Editor Interface
=================================

This module provides a command-line interface (CLI) for users to create and interact
with personalized Codex-based clone agents. Users select traits such as tone, formality,
task bias, and memory depth to define their CloneAgent's behavior.

Usage:
- Select traits via text input
- Interact with your clone by submitting prompts
- View responses based on the customized trait pipeline

Dependencies:
- triskelion_codex_clone_agent.py (must be in same directory or in PYTHONPATH)
"""

from triskelion_codex_clone_agent import CloneAgent

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.clones = []

    def create_clone(self, clone_name, traits):
        clone = CloneAgent(clone_name, self, traits)
        self.clones.append(clone)
        return clone

def prompt_trait_selection():
    print("\nWelcome to the TRISKELION Clone Editor")
    print("Please select your clone's traits:")

    tone = input("Choose tone (poetic / formal / casual): ").strip().lower()
    formality = input("Formality level (low / medium / high): ").strip().lower()
    memory_depth = input("Memory depth (session-only / short-term / long): ").strip().lower()
    task_bias = input("Primary task bias (code / summarization / creative writing / Q&A / general): ").strip().lower()

    return {
        "tone": tone,
        "formality": formality,
        "memory_depth": memory_depth,
        "task_bias": task_bias
    }

def interaction_loop(clone):
    print(f"\nYour clone '{clone.name}' is ready. Begin interaction:")
    print("Type 'exit' to end the session.\n")

    while True:
        prompt = input("You: ")
        if prompt.lower() in ['exit', 'quit']:
            print("Session ended.")
            break
        response = clone.respond(prompt)
        print(response)

def main():
    print("=== TRISKELION CLONE CREATION ===\n")
    name = input("Enter your name: ").strip()
    user_id = input("Assign a user ID: ").strip()
    user = User(user_id, name)

    clone_name = input("Name your clone agent: ").strip()
    traits = prompt_trait_selection()

    clone = user.create_clone(clone_name, traits)
    interaction_loop(clone)

if __name__ == "__main__":
    main()
