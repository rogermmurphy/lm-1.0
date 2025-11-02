## Brief overview
Establishes testing organization, structure, and standards for the Little Monster GPA platform. All tests must be organized in the qa/ folder with clear separation by component type and test scope.

## Testing folder structure
```
qa/
├── backend/
│   ├── api/          # API endpoint tests (one file per route)
│   ├── services/     # Service layer tests (one file per service)
│   └── e2e/          # End-to-end integration tests
├── frontend/
│   ├── components/   # React component tests
│   ├── pages/        # Page-level tests
│   └── e2e/          # Frontend E2E tests
└── shared/
    ├── types/        # Type validation tests
    └── utils/        # Utility function tests
```

## Test file naming
- One test file per service/route/component
- Format: `{component-name}.test.ts` or `{feature-name}.test.js`
- E2E tests: `{workflow-name}.e2e.test.js`

## Test organization rules
- **One test case per function** - Each function gets its own describe block
- **Separate happy path and error cases** - Clear test organization
- **E2E tests for complete workflows** - User registration, class creation, content upload
- **No redundant tests** - If functionality is covered in E2E, don't duplicate in unit tests

## Example test structure
```javascript
// qa/backend/services/auth.service.test.ts
describe('AuthService', () => {
  describe('register', () => {
    it('should create new user with valid data', async () => {
      // Test happy path
    });
    
    it('should reject duplicate email', async () => {
      // Test error case
    });
  });
  
  describe('login', () => {
    it('should return JWT tokens for valid credentials', async () => {
      // Test happy path
    });
    
    it('should reject invalid password', async () => {
      // Test error case
    });
  });
});
```

## Test coverage requirements
- **Services:** 80% minimum coverage
- **API Routes:** 90% minimum coverage  
- **Critical paths (auth, payments):** 100% coverage
- **E2E workflows:** Cover all major user journeys

## Testing tools
- **Unit/Integration:** Jest with TypeScript
- **E2E:** Playwright or native fetch API
- **Mocking:** Jest mocks for external services
- **Database:** Test database with rollback between tests

## Zero tolerance testing integration
All new features must pass tests before marking complete:
1. Build feature
2. Write test
3. Run test
4. Fix errors
5. Re-test
6. Mark complete only when passing

No feature is done until tests pass!
