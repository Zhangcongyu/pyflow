---
name: pyflow-brainstorming
description: |
  MUST use before any creative work - creating features, building components,
  adding functionality, or modifying behavior. Explores user intent, requirements
  and design before implementation. Receives --version-dir <VERSION_DIR> parameter
  for versioned requirements output.
---

# Brainstorming Ideas Into Designs

Turn ideas into fully formed designs and specs through natural collaborative dialogue.

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

## The Process

### Understanding the Idea

Check out the current project state first (files, docs, recent commits).

Then ask questions one at a time:
- Prefer multiple choice questions when possible
- Only one question per message
- Focus on: purpose, constraints, success criteria

### Exploring Approaches

Propose 2-3 different approaches with trade-offs:
- Present options conversationally with your recommendation
- Lead with your recommended option and explain why

### Presenting the Design

Once you understand what to build, present the design:
- Break into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify

### Key Principles

- **One question at a time** - Don't overwhelm
- **Multiple choice preferred** - Easier to answer
- **YAGNI ruthlessly** - Remove unnecessary features
- **Explore alternatives** - Propose 2-3 approaches
- **Incremental validation** - Present in sections, validate each
- **Be flexible** - Go back and clarify when needed

## After the Design

**Documentation**:
- Write the validated design to the output path
- Use elements-of-style:writing-clearly-and-concisely skill if available
- Commit the design document to git

**Implementation (if continuing)**:
- Ask: "Ready to set up for implementation?"
- Use superpowers:using-git-worktrees to create isolated workspace
- Use superpowers:writing-plans to create detailed implementation plan
