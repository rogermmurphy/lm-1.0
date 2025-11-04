## Brief overview
Global debugging methodology emphasizing zero tolerance for errors, continuous iteration until completion (YOLO mode), and systematic analysis through Sequential Thinking. Use when encountering errors or implementing fixes.

## Zero Tolerance principle
- No errors are acceptable at any stage
- Every error must be fixed before moving to next step
- Build → Test → Remediate → Build → Test → Remediate cycle continues until zero errors
- Never mark tasks as complete with known errors remaining
- "It should work" without verification is unacceptable

## YOLO Mode (You Only Live Once) execution
- Answer own questions instead of asking user for clarification
- Continue working until task 100% complete - don't stop mid-way
- Do whatever is needed to complete task, including:
  - Rebooting MCP servers when needed
  - Restarting containers
  - Searching entire codebase
  - Testing multiple approaches
- Persistence until zero errors achieved

## Required methodology sequence
**Always follow in order:**
1. **Sequential Thinking** - Use MCP tool to break down problems systematically
2. **Task List** - Create comprehensive checklist with all steps
3. **Deep Research** - Read relevant files, understand working patterns
4. **Full Thinking** - Analyze thoroughly before implementing
5. **Remediate** - Apply fixes based on analysis
6. **Test** - Verify fixes work
7. **Repeat** - If errors remain, restart from step 1

## Pattern analysis strategy
When encountering errors:
- Identify working services (no 404/401 errors)
- Compare working vs broken implementations
- Find the successful pattern
- Apply that pattern to broken services
- Example: If Flashcards works and Classes doesn't, study what Flashcards does differently

## Sequential Thinking tool usage
- Launch for every complex problem
- Break problems into 10-20 systematic thoughts
- Question assumptions at each step
- Form hypothesis
- Verify hypothesis through code inspection
- Document findings clearly
- Continue until confident solution found

## Build-test-remediate cycle
After EVERY code change:
1. Build/restart affected containers
2. Test the specific functionality changed
3. Check for errors (use Playwright, curl, or browser console)
4. If ANY errors found:
   - Stop immediately
   - Use Sequential Thinking to analyze error
   - Fix the root cause
   - Restart from step 1
5. Only proceed to next feature when current has ZERO errors

## Environment variable consistency
- Check ALL services for matching variable names
- Example: `JWT_SECRET_KEY` not `JWT_SECRET`
- Search codebase when fixing one service to find all instances
- Restart containers after .env changes

## Legacy code identification
- Old/archived code may contain outdated patterns (e.g., Supabase references)
- Active codebase is in services/, views/, database/, shared/ folders
- Don't fix issues in old/ or poc/ directories unless they affect active code
- Verify paths before applying fixes

## MCP server management
- If MCP tools not responding, user may need to reboot
- In YOLO mode, request MCP reboot when needed
- Don't give up due to MCP connection issues
