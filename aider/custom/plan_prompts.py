class PlanPrompts:
    @staticmethod
    def get_plan_prompt(prompt, existing_content, files_context):
        return f"""Let's create a project plan for: {prompt}

Current project files:
{files_context}

Here are the existing plan items:
{existing_content}

Please suggest 3-5 new tasks or milestones, formatted as markdown bullet points:
- [ ] Task:"""
