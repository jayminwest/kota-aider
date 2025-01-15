# Kaider Upgrade Plan

## Overview
This document outlines the plan to enhance Aider with new features while maximizing reuse of existing systems.

## Core Infrastructure Integration

### Key Existing Systems to Leverage
- `Coder` class as base
- `Commands` system for new commands
- `IO` class for user interaction
- `RepoMap` for code context
- `history.py` for version tracking

### New Directory Structure
```
.aider/
  brainstorm/      # Brainstorming history
  plans/           # Planning documents
  memory/          # Memory storage
  active_memory.md # Shared memory file
```

## Feature Implementation - Updated Storage Approach

### Brainstorming System
- Storage Implementation:
  - Create `.aider.brainstorm.history.md` file
  - Use same format as chat history
  - Add metadata headers for sessions
  - Include timestamped entries
  - Support markdown formatting

- Example File Structure:
```markdown
# Brainstorm Session History

## Session 1 - 2023-10-15 14:30:00
- [x] Idea: Implement memory system
- [ ] Idea: Add planning interface
- [ ] Idea: Create brainstorming templates

## Session 2 - 2023-10-16 09:15:00
- [x] Idea: Use existing history format
- [ ] Idea: Add session management
```

### Planning System
- Storage Implementation:
  - Create `.aider.plan.history.md` file
  - Use hierarchical markdown lists
  - Include task status indicators
  - Add progress tracking
  - Support version history

- Example File Structure:
```markdown
# Project Plan History

## Version 1 - 2023-10-15
- [x] Phase 1: Core Extensions
  - [x] Add new directories
  - [x] Extend Commands class
- [ ] Phase 2: Brainstorming
  - [x] Add brainstorming commands
  - [ ] Implement session tracking

## Version 2 - 2023-10-16
- [x] Phase 1: Core Extensions
  - [x] Add new directories
  - [x] Extend Commands class
  - [x] Add configuration system
- [ ] Phase 2: Brainstorming
  - [x] Add brainstorming commands
  - [x] Implement session tracking
  - [ ] Create history system
```

### Integration with Existing Systems
- Leverage:
  - History file parsing from `history.py`
  - Markdown rendering from `mdstream.py`
  - File watching from `watch.py`
  - Version control from `repo.py`

### Benefits of This Approach
- Consistent with existing patterns
- Easy to version control
- Human-readable format
- Compatible with existing tools
- Simple to parse and process

### Memory System
- Build on:
  - Chat history storage
  - `RepoMap` tagging
  - File watching
- Features:
  - Plugin architecture
  - Vector store integration
  - Knowledge graph support

### Active Memory
- Integrate with:
  - File watching
  - Git conflict resolution
  - Markdown rendering
- Features:
  - Real-time collaboration
  - Change tracking
  - Conflict resolution

## Implementation Roadmap

### Phase 1: Core Extensions
- Add new directories to `.aider`
- Extend `Commands` class
- Create base memory handlers

### Phase 2: Brainstorming
- Add brainstorming commands
- Implement session tracking
- Create history system

### Phase 3: Planning
- Add planning commands
- Implement hierarchical planning
- Create progress tracking

### Phase 4: Memory
- Implement memory interface
- Add memory commands
- Create query system

### Phase 5: Active Memory
- Implement markdown handler
- Add conflict resolution
- Create sync system

### Phase 6: Integration
- Add unified interface
- Implement error handling
- Create documentation
