## Brief overview
All project documentation files are living documents that must be kept synchronized and updated whenever changes are made to any related specifications, requirements, or implementations. This rule establishes the principle that documentation is never "complete" and must evolve with the project.

## Living document philosophy
- Every document in the project is a living document that can and should be updated as requirements, implementations, or understanding evolves
- No document is ever considered "final" or "frozen" - all are subject to revision and improvement
- Changes to one document often necessitate updates to related documents to maintain consistency
- Documentation updates are part of the development process, not an afterthought

## Specification synchronization requirements
- Changes to functional specifications must trigger review and potential updates to technical specifications
- Updates to technical specifications must be reflected in functional specifications where applicable
- Platform-specific specifications (web, mobile, desktop) must remain consistent with overall functional and technical specs
- Any deviation between platform specifications must be explicitly documented with clear rationale

## Phased documentation updates
- When implementation reveals issues or improvements for a phase, update that phase's documentation immediately
- Completed phases may require documentation updates based on learnings from subsequent phases
- Phase 0 (environment setup), Phase 1 (implementation), and all future phases are living documents
- Changes in one phase that affect another phase must trigger updates to both phase documents

## Cross-document consistency
- Implementation plans must align with functional and technical specifications
- Business process flows must match functional requirements
- API documentation must reflect actual implementation details
- Database schemas in documentation must match deployed schemas

## Update triggers
- When code implementation differs from specification, update the specification to match reality or update code to match spec
- When business requirements change, cascade updates through functional specs, technical specs, and implementation plans
- When new tools or technologies are adopted, update environment setup and technical specifications
- When architectural decisions change, update all affected specification documents

## Documentation review requirements
- When updating any specification, review all related documents for necessary updates
- Maintain a "Last Updated" date on all living documents
- Include version numbers on major specification documents
- Document the reason for significant changes in commit messages

## File organization rules
- Phase-specific documents belong in phase-specific folders (e.g., docs/phase-0/, docs/phase-1/)
- All specifications belong in docs/specifications/ folder
- Keep related documents together to facilitate synchronized updates
- Use clear, descriptive file names that indicate document purpose and platform if applicable

## Examples of cascading updates
- User adds new feature to functional spec → Update technical spec with implementation details → Update implementation plan with new tasks → Update API documentation
- Database schema changes → Update technical specifications → Update implementation plan → Update business process flows if affected
- Environment requirements change → Update Phase 0 setup guide → Update technical specifications → Update implementation plan dependencies
- Platform-specific feature added → Update platform functional spec → Verify consistency with overall functional spec → Update technical spec if needed
