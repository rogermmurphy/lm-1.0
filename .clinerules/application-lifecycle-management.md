## Brief overview
Project-specific rule for managing application start, stop, and restart operations. All lifecycle operations must be executed via the batch scripts in the scripts/ directory.

## Never use manual process management
- Do not use `taskkill` or `kill` commands to stop services
- Do not use `ps` or `tasklist` to check running processes
- Do not manually restart Node.js processes
- Do not run `npm start` or `npm run dev` directly in subdirectories

## Always use scripts/ directory batch files
- Use `.\scripts\start-all.bat` to start all services
- Use `.\scripts\stop-all.bat` to stop all services
- Use `.\scripts\restart-all.bat` to restart all services
- These scripts handle proper startup/shutdown and build processes
- Scripts are managed centrally and ensure consistent behavior

## Do not block on start/stop/restart
- Starting services is a background operation
- Do not wait for "server ready" messages
- Do not confirm services are running after starting
- Move forward with the task immediately after executing start command
- If services fail to start, user will report it

## Example of correct behavior
```bash
# Correct: Use npm scripts
cd backend && npm start
cd web-app && npm run dev

# Wrong: Manual process management
taskkill /F /IM node.exe
kill -9 $(pgrep node)
```

## When services need restart
- Assume npm start will restart automatically if already running
- If restart truly needed, use npm scripts (not manual kill)
- Better: implement hot-reload in development
- Production: use process managers (PM2, Docker) not manual commands

## Why this matters
- npm scripts handle cleanup, environment setup, and proper shutdown
- Manual process killing can leave orphaned processes or corrupt state
- Scripts are cross-platform compatible
- Reduces errors and inconsistencies
