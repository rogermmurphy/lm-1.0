## Brief overview
Zero tolerance for the eternal DevOps cycle. We deploy → test → remediate → deploy → test → remediate. We do not tolerate errors. We always test end-to-end before considering any feature complete.

## Zero Tolerance Philosophy
- No feature is "done" until it passes end-to-end testing
- Every deployment must be tested immediately
- Errors are not acceptable - they must be fixed before proceeding
- Manual testing counts as testing - automated tests are bonus
- The cycle continues until zero errors remain

## Testing Requirements
- After deploying database changes: Test with actual queries
- After deploying API endpoints: Test with actual HTTP requests
- After deploying UI changes: Test in browser with real interactions
- After deploying integrations: Test the full data flow

## The Cycle
```
Deploy → Test → (Errors?) → Remediate → Deploy → Test → (Success!)
```

Never skip the test phase. Never accept "it should work" without verification.

## Examples

**Database Migration:**
1. Deploy migration (CREATE TABLE users)
2. Test: INSERT a user, SELECT it back
3. Error found? Fix the schema
4. Deploy again
5. Test again
6. Success? Move to next step

**API Endpoint:**
1. Deploy endpoint (POST /classes)
2. Test: Make actual HTTP request with curl/Postman
3. Error? Fix the code
4. Deploy again
5. Test with real request
6. Success? Move to next endpoint

**UI Feature:**
1. Deploy component
2. Test: Open browser, click through the feature
3. Error? Fix the code
4. Deploy (hot reload)
5. Test again in browser
6. Success? Move to next feature

## Enforcement
- Do not proceed to the next task until current task passes testing
- Do not mark items as complete without verification
- Do not assume "it works" - prove it works
- Always show test results before moving forward

## Benefits
- Catch issues immediately when context is fresh
- Avoid compounding errors
- Build confidence in the system
- Reduce debugging time later
- Ensure production-ready code

## Anti-Patterns to Avoid
- ❌ "Let's build everything then test at the end"
- ❌ "It compiled so it probably works"
- ❌ "I'll test it later"
- ❌ "The tests will catch it"
- ❌ Skipping testing because "it's a small change"

## Correct Pattern
- ✅ Build one feature
- ✅ Deploy it
- ✅ Test it end-to-end
- ✅ Fix any issues found
- ✅ Test again
- ✅ Only then move to next feature
