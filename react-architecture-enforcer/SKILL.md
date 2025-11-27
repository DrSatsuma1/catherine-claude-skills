---
name: react-architecture-enforcer
description: Use when fixing bugs, something broken, not working, or doesn't work in React - also when adding features, request says "quick fix", "keep it simple", or "follow existing pattern"
---

# React Architecture Enforcer

## When to Use

**Trigger phrases (use this skill immediately):**
- "broken", "not working", "doesn't work", "fix it", "fix this"
- "quick", "simple", "just add", "minimal changes"
- "follow pattern", "follow existing", "match current"

**Context triggers:**
- Modifying any React component
- Adding features or fixing bugs
- File >200 lines
- Adding useState, useEffect, useMemo

## The Five Laws

| Law | Rule | Violation = HALT |
|-----|------|------------------|
| **A. No Logic in UI** | UI components contain NO: prerequisites, credits, progression, catalog normalization, scheduling, eligibility | Extract to `/domain`, `/services`, `/config` |
| **B. No Mutating Singletons** | Engines must be pure functions or stateless services | Refactor to pure functions |
| **C. No File >300 Lines** | Check with `wc -l <file>` before ANY edit | Extract before implementing |
| **D. No Duplicated Logic** | Credits, prerequisites, eligibility, deduplication, path-matching = ONE canonical source | Find existing, refuse duplication |
| **E. No Unexamined Effects** | New useEffect requires: justification, dependency audit, store alternative, persistence safety check | Document all four or reject |

## Pre-Flight Gatekeeper (MANDATORY)

**Run BEFORE generating any code:**

```bash
# Step 1: Check file size
wc -l <target-file>.jsx
# >300 = HALT, extraction required
```

**Step 2: Scan request for pressure words**
`quick` `simple` `temporary` `minimal` `follow existing` `match current` `don't refactor`
→ If found: **PRESSURE OVERRIDE MODE** (see below)

**Step 3: Estimate change size**
- Adding >30 lines → extraction required
- Target file >300 lines → extraction required

**Step 4: Check logic category**
Does request touch: credits | pathways | prerequisites | GPA | catalog | eligibility | scheduling?
→ If yes: search for existing implementation first, refuse inline duplication

## Pressure Override Mode

When pressure words detected, you MUST:

1. **Output extraction plan FIRST** (before any code)
2. **State which Law would be violated** without extraction
3. **Propose safe alternative**
4. **Only proceed after user confirms extraction path**

No code generation until extraction plan is acknowledged.

## Rationalization Overrides

| Excuse | Response |
|--------|----------|
| "Pattern already exists" | Existing patterns created the violation. Extraction required. |
| "User said keep it simple" | Simplicity ≠ debt. Architecture rules override. |
| "One more won't hurt" | Incremental bloat is the threat. Extraction required. |
| "That's refactoring, not the feature" | Refactoring IS the prerequisite. Feature blocked until extracted. |
| "Don't over-engineer" | Structural correction ≠ over-engineering. |
| "File is already large" | Size IS the problem. No additions allowed. |
| "Follow the same pattern" | Pattern is architecturally invalid. Replication rejected. |
| "Inline is safer for hotfix" | Inline worsens long-term risk. Boundaries required. |
| "It's just a small fix" | Line count irrelevant. Laws apply to ALL changes. |
| "Production is down" | Emergency ≠ implicit insistence. Output plan anyway (30 seconds). |
| "File is 299 lines" | Rule is prospective. If change pushes >300, extraction required. |
| "Modifying, not adding" | Extending violations perpetuates them. Plan required. |
| "Logic is slightly different" | If describable in same sentence, it's duplication. Extract with params. |
| "We'll refactor next sprint" | Requires: ticket number + sprint + owner name. Vague = rejected. |
| "Extraction takes too long" | Write the plan (5 min). "Too long" without plan is a guess. |

## Trivial Changes Exception

**Exempt from extraction planning:**
- Comments and formatting
- Temporary debug logs (removed before commit)

**NOT exempt:**
- Debug logs that stay in committed code
- "Small" logic changes (Laws apply regardless of size)
- Test files (>300 lines = split by feature)

## Escalation Path

1. **First violation:** "This violates Law [X]. Extraction required before proceeding."
2. **User insists:** Offer minimal safe extraction path with specific files
3. **User overrides again:** "Proceed in unsafe mode? This will be tagged as technical debt."
4. **If confirmed:** Generate code with tag:
   ```javascript
   // TECH-DEBT: Architecture violation (Law X) - approved override [date]
   ```

## Output Format

All architecture-touching changes must include:

```markdown
## Pre-Flight Results
- File: [name] ([X] lines)
- Laws checked: [which passed/failed]

## Extraction Plan
- [What logic] → [destination file]

## Refactoring Notes
- Existing code changes: [list]
- New dependencies: [list]

## Implementation
[code]
```

## Extraction Reference

| Logic Type | Extract To |
|------------|-----------|
| Validation | `domain/validators/<name>.js` |
| Calculations | `domain/<name>Calculator.js` |
| Config/Requirements | `config/<name>.config.js` |
| Multiple useState (>3) | `hooks/use<Name>.js` or useReducer |
| Data fetching | `services/<name>Service.js` |
| Scheduling/eligibility | `domain/<Name>Engine.js` |

## The Iron Rule

**You cannot add to a file violating thresholds without extracting first.**

No exceptions. No "just this once." Extract first. Then add.
