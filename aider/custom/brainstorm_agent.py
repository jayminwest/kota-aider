from pathlib import Path
from datetime import datetime

class BrainstormAgent:
    def __init__(self, io, coder=None):
        self.io = io
        self.coder = coder
        self.session_file = Path(".aider/brainstorm/history.md")
        if coder is None:
            from aider.coders.base_coder import Coder
            self.coder = Coder.create(io=io)
        
    def start_session(self):
        """Initialize a new brainstorming session"""
        try:
            brainstorm_dir = self.session_file.parent
            brainstorm_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if not self.session_file.exists():
                with open(self.session_file, "w", encoding="utf-8") as f:
                    f.write(f"# Brainstorm Session History\n\n")
                    f.write(f"## Session 1 - {timestamp}\n")
            
            self.io.tool_output(f"Brainstorm session started at {timestamp}")
            return True
        except Exception as e:
            self.io.tool_error(f"Error starting brainstorm session: {e}")
            return False

    def add_idea(self, idea):
        """Add an idea to the current brainstorming session"""
        try:
            if not self.session_file.exists():
                if not self.start_session():
                    return False
            
            with open(self.session_file, "a", encoding="utf-8") as f:
                f.write(f"- [ ] Idea: {idea}\n")
            return True
        except Exception as e:
            self.io.tool_error(f"Error adding brainstorm idea: {e}")
            return False

    def get_session_content(self):
        """Get the content of the current brainstorming session"""
        try:
            if not self.session_file.exists():
                return None
                
            with open(self.session_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Extract just the ideas, skipping headers
                ideas = []
                for line in content.splitlines():
                    if line.startswith("- [ ] Idea:"):
                        ideas.append(line)
                return "\n".join(ideas) if ideas else None
        except Exception as e:
            self.io.tool_error(f"Error reading brainstorm session: {e}")
            return None

    def brainstorm_with_ai(self, prompt):
        """Use AI to help brainstorm ideas about the given prompt"""
        if not prompt.strip():
            self.io.tool_error("Please provide a brainstorming prompt")
            return

        # Get existing ideas
        existing_content = self.get_session_content() or ""
        
        # Get current chat files context if coder is available
        file_context = ""
        if self.coder and hasattr(self.coder, 'abs_fnames') and self.coder.abs_fnames:
            file_context = "\n\nCurrent files in chat session:\n"
            for fname in self.coder.abs_fnames:
                try:
                    with open(fname, "r", encoding="utf-8") as f:
                        content = f.read()
                        file_context += f"\nFile: {fname}\n```\n{content}\n```\n"
                except Exception as e:
                    self.io.tool_error(f"Error reading {fname}: {e}")
        
        # Create a more structured brainstorming prompt
        brainstorm_prompt = f"""Let's brainstorm some ideas about: {prompt}

Here's the context:
1. Previous ideas from our session:
{existing_content or 'No previous ideas yet.'}
2. Relevant files:
{file_context}

Please suggest 3-5 specific, actionable ideas that:
- Are relevant to the prompt and context
- Build on or complement existing ideas
- Are technically feasible
- Are clearly explained

Format requirements:
- Each idea must start with "- [ ] Idea: "
- Include a brief explanation after each idea
- Keep each idea concise (1-2 sentences)

Example format:
- [ ] Idea: Implement feature X using approach Y
  This would solve problem Z by doing A, B, and C

Please only respond with properly formatted ideas, no extra commentary.
"""

        # Use the coder to generate ideas
        from aider.coders.base_coder import Coder
        brainstorm_coder = Coder.create(
            io=self.io,
            from_coder=self.coder,
            edit_format="ask",
            summarize_from_coder=False
        )
        
        # Run the brainstorm and capture response
        brainstorm_coder.run(brainstorm_prompt)
        
        # Get the last assistant message
        all_messages = brainstorm_coder.done_messages + brainstorm_coder.cur_messages
        assistant_messages = [msg for msg in reversed(all_messages) if msg["role"] == "assistant"]
        
        if assistant_messages:
            response = assistant_messages[0]["content"]
            
            # Validate and extract ideas
            ideas = []
            for line in response.splitlines():
                line = line.strip()
                if line.startswith("- [ ] Idea:"):
                    idea = line[11:].strip()  # Remove "- [ ] Idea:" prefix
                    if idea:  # Only add non-empty ideas
                        ideas.append(idea)
            
            if not ideas:
                self.io.tool_warning("No valid ideas found in the AI response")
                return
                
            # Add each idea with confirmation
            for idea in ideas:
                if self.io.confirm_ask(f"Add this idea? '{idea}'"):
                    self.add_idea(idea)
                    self.io.tool_output(f"Added idea: {idea}")
                else:
                    self.io.tool_output(f"Skipped idea: {idea}")
