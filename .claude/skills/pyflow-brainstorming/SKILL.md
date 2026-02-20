---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. Receives --version-dir <VERSION_DIR> parameter for versioned requirements output."
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project state, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## Parameters

**Receives**: `--version-dir <VERSION_DIR>` + user request

**Example**:
```
--version-dir v0_initial 创建一个待办事项应用
--version-dir v1_auth_api 添加用户认证功能
```

**Output path**: Determined by `--version-dir` parameter:
- With `--version-dir`: `pjflow/{VERSION_DIR}/requirements.md`
- Without `--version-dir`: `./pjflow/requirements.md.tmp` (temporary file for executor to move)

## Parameter Parsing

**Step 1**: Parse args to extract `--version-dir` and user request
```python
# Parse --version-dir if present
if "--version-dir" in args:
    parts = args.split("--version-dir", 1)[1].strip().split(None, 1)
    version_dir = parts[0]
    user_request = parts[1] if len(parts) > 1 else ""
else:
    version_dir = None
    user_request = args
```

**Step 2**: Determine output path
```python
if version_dir:
    output_path = f"pjflow/{version_dir}/requirements.md"
else:
    output_path = "./pjflow/requirements.md.tmp"
```

## The Process

**Understanding the idea:**
- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Documentation:**
- Write the validated design to the output path determined by `--version-dir` parameter
- Use elements-of-style:writing-clearly-and-concisely skill if available
- Commit the design document to git

**Implementation (if continuing):**
- Ask: "Ready to set up for implementation?"
- Use superpowers:using-git-worktrees to create isolated workspace
- Use superpowers:writing-plans to create detailed implementation plan

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
