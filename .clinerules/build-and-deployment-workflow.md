## Brief overview
Project-specific rules for build and deployment workflow. Emphasizes the requirement to always build before running services and proper start/stop/restart procedures.

## Build-first requirement
- ALWAYS run the build script before starting any service
- Never skip the build step, even if it seems like code hasn't changed
- The build process catches compilation errors early and prevents runtime issues
- Example: For backend, run `npm run build` before `npm start`
- Example: For frontend, ensure Vite properly compiles before serving

## Required npm scripts
Every service (backend, frontend, etc.) must have these scripts in package.json:
- `build`: Compiles TypeScript/builds the project
- `start`: Starts the compiled/built version (not dev mode)
- `stop`: Gracefully stops the running service (if applicable)
- `restart`: Stops and starts the service (essentially `stop` + `build` + `start`)
- `dev`: Development mode with hot-reload (separate from production build/start)

## Deployment workflow sequence
1. Run `npm run build` to compile
2. Check for compilation errors
3. Fix any errors found
4. Re-run `npm run build`
5. Only after successful build, run `npm start`
6. Test the running service
7. If changes needed, make changes and repeat from step 1

## Development vs production
- Development: Use `npm run dev` for hot-reload during active development
- Production/Testing: Use `npm run build` then `npm start` for production-like testing
- Never assume dev mode will catch all issues - always test with build script

## Error handling
- If `npm start` fails, it's often because `npm run build` wasn't run first or failed
- Always check build output for errors before attempting to start
- TypeScript compilation errors must be fixed at build time, not ignored
