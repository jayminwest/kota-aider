from pathlib import Path
from datetime import datetime

class BrainstormAgent:
    def __init__(self, io, coder):
        self.io = io
        self.coder = coder
        self.session_file = Path(".aider/brainstorm/history.md")
        
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
        
        # Create a brainstorming prompt
        brainstorm_prompt = f"""Let's brainstorm some ideas about: {prompt}

Previous ideas from our brainstorming session:
{existing_content or 'No previous ideas yet.'}

Please suggest 3-5 new creative and specific ideas that build on or complement the existing ones.
Format each idea as a markdown checkbox item starting with "- [ ] Idea: "

For example:
- [ ] Idea: Implement feature X using approach Y to solve problem Z
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
            # Extract ideas from the response and add them to history
            response = assistant_messages[0]["content"]
            for line in response.splitlines():
                if line.startswith("- [ ] Idea:"):
                    self.add_idea(line[13:].strip())  # Remove "- [ ] Idea: " prefix
