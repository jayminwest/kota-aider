from pathlib import Path
from datetime import datetime

class PlanAgent:
    def __init__(self, io, coder):
        self.io = io
        self.coder = coder
        self.plan_file = Path(".aider/plans/history.md")
        self.plan_files = set()  # Track plan-related files
        
    def start_session(self):
        """Initialize a new planning session"""
        try:
            plan_dir = self.plan_file.parent
            plan_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if not self.plan_file.exists():
                with open(self.plan_file, "w", encoding="utf-8") as f:
                    f.write(f"# Project Plan History\n\n")
                    f.write(f"## Version 1 - {timestamp}\n")
            
            # Add plan file to chat session
            self.coder.add_rel_fname(str(self.plan_file))
            self.plan_files.add(str(self.plan_file))
            
            self.io.tool_output(f"Planning session started at {timestamp}")
            return True
        except Exception as e:
            self.io.tool_error(f"Error starting planning session: {e}")
            return False

    def add_item(self, item):
        """Add an item to the current plan"""
        try:
            if not self.plan_file.exists():
                if not self.start_session():
                    return False
            
            with open(self.plan_file, "a", encoding="utf-8") as f:
                f.write(f"- [ ] {item}\n")
            
            # Ensure plan file is in chat session
            if str(self.plan_file) not in self.plan_files:
                self.coder.add_rel_fname(str(self.plan_file))
                self.plan_files.add(str(self.plan_file))
                
            return True
        except Exception as e:
            self.io.tool_error(f"Error adding plan item: {e}")
            return False

    def get_plan_content(self):
        """Get the content of the current plan"""
        try:
            if not self.plan_file.exists():
                return None
                
            # Check if plan file is in chat files
            chat_files = self.coder.get_inchat_relative_files()
            if str(self.plan_file) not in chat_files:
                self.coder.add_rel_fname(str(self.plan_file))
                self.plan_files.add(str(self.plan_file))
                
            with open(self.plan_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            self.io.tool_error(f"Error reading plan: {e}")
            return None

    def plan_with_ai(self, prompt):
        """Use AI to help create a project plan"""
        if not prompt.strip():
            self.io.tool_error("Please provide a planning prompt")
            return

        # Get existing plan items
        existing_content = self.get_plan_content() or ""
        
        # Get current chat files for context
        chat_files = self.coder.get_inchat_relative_files()
        files_context = "\n".join(f"- {f}" for f in chat_files if f != str(self.plan_file))
        
        # Create a planning prompt
        plan_prompt = f"""Let's create a project plan for: {prompt}

Current project files:
{files_context}

Here are the existing plan items:
{existing_content}

Please suggest 3-5 new tasks or milestones, formatted as markdown bullet points:
- [ ] Task:"""

        # Use the coder to generate plan items
        from aider.coders.base_coder import Coder
        plan_coder = Coder.create(
            io=self.io,
            from_coder=self.coder,
            edit_format="ask",
            summarize_from_coder=False
        )
        
        plan_coder.run(plan_prompt)
