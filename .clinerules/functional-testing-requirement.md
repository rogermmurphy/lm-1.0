## Brief overview
Testing must verify actual functionality and user workflows, not just technical health checks. A feature is not "tested" until it works end-to-end from the user perspective.

## Functional testing requirement
Testing must verify:
1. User can complete the actual workflow
2. Feature produces expected results
3. UI responds as designed
4. Data persists correctly
5. Error cases handled gracefully

NOT sufficient:
- Just checking if service is running
- Just checking if endpoint returns 200
- Just checking if component renders
- Technical health without user workflow verification

## Examples of proper functional testing

**Audio Recording Feature:**
- ✅ User clicks "Record Audio", microphone activates, waveform displays, recording uploads, appears in list
- ❌ Just checking if AudioRecorder component exists

**PowerPoint Generation:**
- ✅ User clicks "Generate PowerPoint" on note, modal opens, user selects options, PowerPoint generates and downloads
- ❌ Just checking if Presenton container is running

**Camera Capture:**
- ✅ User clicks "Capture Photo", camera activates, preview displays, photo captures, uploads, appears in gallery
- ❌ Just checking if getUserMedia API is available

## Testing workflow requirement
For each feature:
1. Start as if you're the user (no technical knowledge)
2. Click through the UI
3. Verify expected outcome happens
4. Check data was saved
5. Test error scenarios

## Zero-tolerance testing applies to functionality
- Feature is NOT done until it works from user perspective
- "Services running" ≠ "Feature working"
- Must test the complete user journey
- Fix any functional issues before marking complete

## Documentation of testing
When documenting testing:
- Describe what user action was taken
- Describe what happened as a result
- Include screenshots/evidence when possible
- Don't just say "tested" - say what was tested and what the result was
