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

## Feature Implementation

### Brainstorming System
- Extend `Commands` class with:
  - `/brainstorm` command
  - History viewing commands
- Use existing:
  - Chat history system
  - Markdown formatting
  - File operations

### Planning System
- Leverage:
  - `RepoMap` for code context
  - `diffs.py` for versioning
  - `history.py` for tracking
- Features:
  - Hierarchical task lists
  - Progress visualization
  - Plan versioning

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
