## Brief overview
Project-specific rule for Little Monster GPA platform. Mandates that when operating in ZERO TOLERANCE + YOLO MODE, tasks can ONLY close by either completing full E2E testing OR creating a new task with comprehensive context using the new_task tool. Simple handover documents are NOT sufficient.

## ZERO TOLERANCE + YOLO MODE definition
When user specifies these modes:
- **Zero Tolerance**: No errors acceptable, build-test-remediate until zero errors
- **YOLO Mode**: Answer own questions, continue until 100% complete, do whatever needed (reboot servers, restart containers, etc.)
- **Mandate**: Task cannot close until EITHER full testing complete OR new task created

## Task closure requirements
In ZERO TOLERANCE + YOLO MODE, you can ONLY close a task by:

### Option 1: Full E2E Testing Complete
- ALL pages tested with Playwright MCP
- Console logs checked on every page
- ZERO errors verified (except acceptable ones like favicon 404)
- Functional workflows tested
- Results documented

### Option 2: Create New Task with Context (REQUIRED if testing incomplete)
You MUST use the new_task tool with comprehensive context including:
- All work completed in current session
- All bugs fixed with file paths
- Root cause analysis findings
- Remaining work to be done
- Sequential Thinking insights
- Pattern analysis results
- Exact testing methodology required
- References to relevant documentation

**DO NOT** simply write a handover document and close - this violates the rule

## Mandatory workflow sequence
Every task in this mode MUST follow:
1. **Sequential Thinking** - Load each objective as thoughts (10-15 thoughts)
2. **Task List** - Every thought becomes a task in the checklist
3. **Deep Research** - Read all relevant MD documents before starting
4. **Full LLM Thinking** - Analyze thoroughly, don't rush to code
5. **Execute** - Implement fixes systematically
6. **Test** - Verify each change
7. **Remediate** - Fix any errors found
8. **Repeat** - Until zero errors OR create new task

## Sequential Thinking integration
- EVERY item in a plan must be loaded as a Sequential Thinking thought first
- Each Sequential Thinking session adds to the task list
- Thoughts should break down complex problems into 10-20 steps
- Must form hypotheses and verify them
- Document findings before implementing

## Pattern analysis requirement
When debugging:
- Identify working services (e.g., services without 404/401 errors)
- Compare working implementation with broken one
- Find the successful pattern
- Apply that pattern to fix broken service
- Verify fix matches system design, don't assume

## New task context requirements
When creating new task due to incomplete work, include:
1. **Current Work Summary**: All fixes applied, files modified, containers restarted
2. **Root Cause Analysis**: What was wrong, how it was discovered (Sequential Thinking results)
3. **Pattern Findings**: What works, what doesn't, why
4. **Technical Details**: File paths, code changes, environment variables modified
5. **Testing Status**: What was tested, what remains
6. **Methodology**: Exact steps next developer must follow
7. **Documentation**: Links to relevant docs, handover files, architecture docs
8. **Verification**: How to verify fixes work (curl commands, Playwright steps)

## Pre-handover document updates
Before creating new task, update:
- `docs/implementation/DEVELOPER-HANDOVER.md` - Technical handover
- Add any discovered patterns or lessons learned
- Document all files modified
- Include verification steps

## Enforcement
Attempting to close task without either:
- Complete E2E testing with zero errors, OR
- Creating new task with comprehensive context via new_task tool

Will result in task rejection and requirement to continue work
