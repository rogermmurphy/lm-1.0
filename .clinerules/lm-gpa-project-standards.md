## Brief overview
Project-specific guidelines for developing the Little Monster (LM) GPA study platform, a multi-platform educational application with AI video generation, audio transcription, and social learning features.

## Documentation standards
- Create separate functional and technical specification documents for each platform component
- Use clear, unambiguous file naming: one file serves one specific purpose
- Organize specifications by platform: web-functional-spec.md, web-technical-spec.md, mobile-functional-spec.md, mobile-technical-spec.md
- Maintain consistency across all documentation following established templates
- Place all project documentation in dedicated docs/ folder with clear hierarchy

## Multi-platform architecture requirements
- Design for three deployment targets: web application, mobile app, and desktop application
- Ensure code reusability across platforms using React Native or similar cross-platform framework
- Plan for responsive design that works seamlessly across different screen sizes
- Maintain feature parity across all platforms while optimizing for each platform's strengths

## Scalability and performance targets
- Design system to support minimum 100 concurrent users for initial rollout
- Implement cloud-based data storage and processing
- Plan for horizontal scaling capabilities from day one
- Target performance metrics: TTI < 1.5s desktop, < 2.5s mobile, API response < 200ms P95

## AI and audio integration preferences
- Integrate self-hosted LLM solution to minimize external API costs
- Implement audio transcription capabilities for user input
- Add audio listening/playback features for generated content
- Design modular AI service architecture for easy model swapping

## Development workflow
- Break large projects into clearly defined components with separate documentation
- Maintain clear separation between functional requirements and technical implementation
- Create comprehensive task progress tracking with markdown checklists
- Follow iterative development approach with regular progress confirmation

## Technology stack preferences
- Frontend: React with TypeScript for web, React Native for mobile
- Backend: Firebase or Supabase for cloud services and real-time data
- State Management: Zustand for lightweight app state, React Query for server state
- Styling: TailwindCSS for consistent design system
- Build Tools: Vite for fast development and optimized bundling

## Project organization principles
- Organize code by feature/component rather than by file type
- Maintain consistent naming conventions using kebab-case for files
- Create clear component hierarchies with proper abstraction levels
- Keep business logic separate from UI components

## Quality assurance standards
- Implement comprehensive testing strategy: unit, integration, and E2E tests
- Use TypeScript for type safety across the entire codebase
- Apply consistent linting and formatting rules
- Plan for cross-platform compatibility testing
