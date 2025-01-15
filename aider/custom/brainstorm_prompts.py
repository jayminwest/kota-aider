class BrainstormPrompts:
    @staticmethod
    def get_brainstorm_prompt(prompt, existing_content, file_context):
        return f"""Let's brainstorm some ideas about: {prompt}

Here's the context:
1. Previous ideas from our session:
{existing_content or 'No previous ideas yet.'}
2. Relevant files in chat:
{file_context or 'No files currently in chat'}

Please suggest 3-5 specific, actionable ideas that:
- Directly address the prompt: {prompt}
- Are relevant to the files and context
- Are technically feasible given the current codebase
- Include clear explanations of how they would work

Format requirements:
- Each idea must start with "- [ ] Idea: "
- Include a brief explanation after each idea
- Keep each idea concise (1-2 sentences)
- Reference specific files or code when relevant

Example format:
- [ ] Idea: Implement feature X using approach Y
  This would solve problem Z by doing A, B, and C
  Relevant files: file1.py, file2.js

Please only respond with properly formatted ideas, no extra commentary.
"""
