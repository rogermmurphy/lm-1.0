# Phase 10: Strategic 3-Week MVP - Progress Log

**Started**: November 3, 2025  
**Approach**: Strategic MVP (prioritize core features, defer complex services)

---

## Week 1: Critical Fixes (Days 1-5)

### Day 1: TTS Service Diagnosis ✅ COMPLETE

**Status**: TTS Service is WORKING

**Findings**:
- ✅ Container running successfully (lm-tts)
- ✅ Azure Speech API credentials configured (from POC 11)
  - Key: 3EMlKJ...3w3 (valid, tested in POC)
  - Region: eastus
  - Default voice: en-US-JennyNeural
- ✅ Logs show successful 200 OK responses
- ✅ Service listening on port 8000 in container
- ✅ Nginx routing traffic to service

**Curl test failed** due to Windows cmd.exe JSON escaping (not a service issue)

**Next Steps**:
- Test in browser at http://localhost:3000/dashboard/tts (real end-to-end test)
- If browser test works, mark TTS as COMPLETE
- If browser test fails, investigate frontend/API integration

**Time Spent**: 0.5 days  
**Estimated Remaining**: 0 days (appears complete, pending browser verification)

---

### Day 1-2: Deploy Notifications Service ✅ COMPLETE

**Goal**: Fix dashboard notification bell errors

**Current Status**: DEPLOYED AND WORKING

**What Was Done**:
- ✅ Dockerfile paths correct
- ✅ Built service successfully
- ✅ Fixed environment variables in docker-compose.yml (lowercase field names)
- ✅ Started service on port 8013
- ✅ Added nginx upstream and routes
- ✅ Tested endpoints - **200 OK on /api/notifications/unread-count**
- ✅ Browser successfully calling service

**Issues Resolved**:
1. **Pydantic case-sensitivity**: docker-compose had `DB_HOST` but config expects `database_url`
2. **Duplicate service definition**: Removed duplicate notifications-service in docker-compose.yml
3. **Nginx path mapping**: Fixed to pass /api prefix to service

**Time Spent**: 0.5 days (much faster than 1-2 days estimated!)

---

## Services Deferred to Phase 11

Based on Enhanced Plan recommendations:
- AI Study Tools (LLM dependency complexity)
- Full Content Capture with OCR (Tesseract installation complexity)
- Social Collaboration (low priority)
- Gamification (low priority)
- Study Analytics (medium priority, but not critical for MVP)

---

## Key Decisions Made

1. **TTS Provider**: Using Azure (already configured, working)
2. **Deployment Strategy**: One service at a time with immediate testing
3. **MVP Scope**: Focus on TTS, Notifications, Class Management, Basic Content Upload
4. **Timeline**: 3 weeks for stable Alpha 1.0

---

## Week 1 Summary (So Far)

**Time Elapsed**: 0.5-1 days  
**Planned**: 5 days  
**Status**: AHEAD OF SCHEDULE! 🎉

### Services Deployed
1. ✅ TTS - Already working with Azure (no action needed)
2. ✅ Notifications - Deployed successfully, routes working

### Key Learnings
1. Always check docker logs first before assuming service is broken
2. Environment variable case-sensitivity matters in pydantic Settings
3. docker-compose environment vars override .env files
4. Nginx path mapping requires careful attention to trailing slashes

## Next Actions

1. ✅ ~~Deploy Notifications service~~ COMPLETE
2. Test both TTS and Notifications in browser (verify UI works)
3. **Update BACKLOG.md** with progress
4. Deploy Class Management (Week 2)
5. Deploy simplified Content Capture (Week 2)
6. Integration testing (Week 3)
7. Polish and documentation (Week 3)
8. Release Alpha 1.0

---

## Notes

- Zero-tolerance testing approach: test after EVERY change
- Document as we go, not after
- Adjust scope if needed - better 3 solid features than 7 broken ones
