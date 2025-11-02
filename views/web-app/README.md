# Little Monster Web Application

Next.js frontend for the Little Monster AI educational platform.

## Setup

```bash
cd views/web-app
npm install
npm run dev
```

Application will run on http://localhost:3000

## Structure

- `src/app/` - Next.js app router pages
- `src/lib/api.ts` - API client for backend services
- `src/components/` - React components (to be added)

## API Integration

Connects to API Gateway at http://localhost which routes to:
- Auth Service (8001)
- LLM Agent (8005)
- Speech-to-Text (8002)
- Text-to-Speech (8003)
- Audio Recording (8004)

## Next Steps

1. Run `npm install` to install dependencies
2. Add authentication pages (login/register)
3. Add chat interface
4. Add transcription UI
5. Extract components from old/Ella-Ai/web-app

## Status

🟡 **IN PROGRESS** - Basic structure created, full UI to be implemented
