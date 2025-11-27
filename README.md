# Catherine's Claude Code Skills

Custom skills for Claude Code to improve code quality, architecture enforcement, and context recovery across projects.

## Available Skills

### 1. anchor-based-context-recovery
**Use when:** Starting work after context compaction, switching features, or gathering context without re-reading entire files.

Searches HTML comment anchors (`<!-- anchor: name -->`) in project documentation to quickly recover relevant context instead of re-reading full files.

**Benefits:**
- 95% reduction in context usage (940-line file → 50 lines of anchor context)
- Survives refactoring (anchors update when files split)
- Searchable by concept, not file path
- Works across sessions and compaction

### 2. react-architecture-enforcer
**Use when:** Fixing bugs, adding features, or modifying React components - especially when request says "quick fix", "keep it simple", or "follow existing pattern".

Enforces five architecture laws:
- No logic in UI components
- No mutating singletons
- No file >300 lines
- No duplicated logic
- No unexamined useEffect hooks

### 3. multi-ai-orchestration
**Use when:** Complex problems requiring multiple perspectives, architecture validation, or debugging hits a wall.

Guides leveraging multiple AI models in parallel for better results on complex tasks.

### 4. us_tax_code_skill
**Use when:** Working with US tax code questions or compliance issues.

Complete US Internal Revenue Code (Title 26) with 2,160 sections covering individual income tax, business deductions, corporate tax, partnerships, international tax, capital gains, and all federal tax provisions.

## Installation

**One-time setup:**

```bash
# Clone this repo
cd ~/repos
git clone https://github.com/yourusername/catherine-claude-skills.git

# Create symlinks to make skills available globally
cd ~/.claude/skills
ln -s ~/repos/catherine-claude-skills/anchor-based-context-recovery .
ln -s ~/repos/catherine-claude-skills/react-architecture-enforcer .
ln -s ~/repos/catherine-claude-skills/multi-ai-orchestration .
ln -s ~/repos/catherine-claude-skills/us_tax_code_skill .
```

**Update all skills:**
```bash
cd ~/repos/catherine-claude-skills
git pull
```

## Usage

Skills are invoked using the Skill tool in Claude Code:

```
Use the anchor-based-context-recovery skill to find context for this feature
```

Or configure auto-triggering in your project's CLAUDE.md:

```markdown
## Mandatory Rules
- BEFORE starting ANY task → MUST invoke `anchor-based-context-recovery` skill
```

## Creating Anchor Documentation

For the `anchor-based-context-recovery` skill to work, projects need anchor documentation:

**1. Create `docs/architecture/anchors.md` in your project:**

```markdown
<!-- anchor: validation-rules -->
## Validation Architecture
- Rule 1: Description
- Rule 2: Description
- Located: src/App.jsx:229-474
- Related: state-management anchor

<!-- anchor: state-management -->
## Core State Structure
- State variables and their purpose
- Located: src/App.jsx:285-290
```

**2. Add to project CLAUDE.md:**

```markdown
## Context Recovery Protocol

**BEFORE starting ANY task:**
1. Invoke `anchor-based-context-recovery` skill
2. Search for relevant anchors in `docs/architecture/anchors.md`
3. Read ONLY anchor sections (not full files)
```

**3. Update anchors when refactoring:**

When you split files or refactor, update the anchor documentation to reference new locations.

## How Symlinks Work

Symlinks (symbolic links) make files appear in multiple places without duplicating them:

- **Real files:** `/Users/you/repos/catherine-claude-skills/anchor-recovery/SKILL.md`
- **Symlink:** `~/.claude/skills/anchor-recovery/SKILL.md` → points to real file
- **Result:** Edit either location, changes appear in both (they're the same file)

**Benefits for skills:**
- Skills live in ONE git repo
- Multiple projects use the SAME skill files via symlinks
- Update skill once → all projects get the update immediately
- Version control for all skills

## Contributing

To add a new skill:

1. Create directory: `mkdir new-skill-name`
2. Create skill file: `new-skill-name/SKILL.md`
3. Add skill description to this README
4. Create symlink: `ln -s ~/repos/catherine-claude-skills/new-skill-name ~/.claude/skills/`
5. Commit and push

## License

MIT
