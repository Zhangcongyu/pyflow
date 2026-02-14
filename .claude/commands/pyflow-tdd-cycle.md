---
description: Execute comprehensive Test-Driven Development (TDD) workflow with strict red-green-refactor discipline. Use for implementing features or bugfixes with test-first methodology, ensuring quality through coordinated agent orchestration with fail-first verification, incremental implementation, and continuous refactoring.
handoffs:
  - label: Code Review
    agent: comprehensive-review:code-reviewer
    prompt: Review the TDD implementation for code quality, test coverage, and adherence to TDD principles. Verify all tests pass and coverage meets requirements.
  - label: Security Audit
    agent: comprehensive-review:security-auditor
    prompt: Perform security analysis of the TDD implementation, checking for vulnerabilities, security best practices, and compliance with security standards.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Execute a comprehensive Test-Driven Development (TDD) workflow with strict red-green-refactor discipline for: `$ARGUMENTS`

This workflow enforces test-first development through coordinated agent orchestration. Each phase of the TDD cycle is strictly enforced with fail-first verification, incremental implementation, and continuous refactoring. The workflow supports both incremental (test-by-test) and test suite approaches with configurable coverage thresholds.

Follow this execution flow:

## Configuration

### Coverage Thresholds

Define and enforce minimum coverage standards:

- **Minimum line coverage**: 80%
- **Minimum branch coverage**: 75%
- **Critical path coverage**: 100%

### Refactoring Triggers

Automatically trigger refactoring when:

- Cyclomatic complexity > 10
- Method length > 20 lines
- Class length > 200 lines
- Duplicate code blocks > 3 lines

## Phase 1: Test Specification and Design

### 1. Requirements Analysis

**Agent**: `comprehensive-review:architect-review`

**Prompt Template**:
```
Analyze requirements for: $ARGUMENTS

Define:
- Acceptance criteria with measurable outcomes
- Edge cases and boundary conditions
- Test scenarios covering happy paths and error paths
- Integration points and dependencies

Output: Comprehensive test specification document.
```

**Validation**:
- [ ] All requirements have corresponding test scenarios
- [ ] Edge cases identified and documented
- [ ] Acceptance criteria are measurable and testable

**Output**: Test specification, acceptance criteria, edge case matrix

---

### 2. Test Architecture Design

**Agent**: `unit-testing:test-automator`

**Prompt Template**:
```
Design test architecture for: $ARGUMENTS based on test specification.

Define:
- Test structure and organization
- Fixture design for test data
- Mock strategy for external dependencies
- Test data management approach

Ensure:
- Tests are isolated and independent
- Test execution is fast
- Tests are maintainable and readable

Output: Test architecture document with fixture design and mock strategy.
```

**Validation**:
- [ ] Architecture supports isolated, fast, reliable tests
- [ ] Fixture strategy is clear and reusable
- [ ] Mock strategy covers all external dependencies

**Output**: Test architecture, fixture design, mock strategy

---

## Phase 2: RED - Write Failing Tests

### 3. Write Unit Tests (Failing)

**Agent**: `unit-testing:test-automator`

**Prompt Template**:
```
Write FAILING unit tests for: $ARGUMENTS

Requirements:
- Tests must fail initially (before implementation)
- Include edge cases, error scenarios, and happy paths
- DO NOT implement any production code
- Follow test architecture design from Phase 1

Test coverage:
- Unit tests for all public methods
- Boundary value tests
- Error handling tests
- State transition tests

Output: Complete test suite with all tests failing.
```

**CRITICAL Validation**:
- [ ] All tests fail with expected error messages
- [ ] Test failures are due to missing implementation
- [ ] No test passes accidentally
- [ ] Test code compiles and runs

**Output**: Failing unit tests, test documentation

---

### 4. Verify Test Failure

**Agent**: `tdd-workflows:code-reviewer`

**Prompt Template**:
```
Verify that all tests for: $ARGUMENTS are failing correctly.

Check:
- Tests fail for the right reasons (missing implementation, not test errors)
- No false positives (tests that should fail but pass)
- Error messages are meaningful and helpful
- No syntax errors in test code

Confirm:
- All failures are expected
- No tests pass accidentally

Output: Test failure verification report with pass/fail status for each test.
```

**GATE**: Do not proceed until all tests fail appropriately

**Output**: Test failure verification report

---

## Phase 3: GREEN - Make Tests Pass

### 5. Minimal Implementation

**Agent**: `python-development:python-pro` (for Python) or appropriate language agent

**Prompt Template**:
```
Implement MINIMAL code to make tests pass for: $ARGUMENTS

Constraints:
- Focus ONLY on making tests green
- DO NOT add extra features or optimizations
- Keep implementation simple and direct
- Follow test architecture design

Implementation approach:
- Write simplest code that passes tests
- No premature optimization
- No extra methods or functionality
- Strict adherence to YAGNI (You Aren't Gonna Need It)

Output: Minimal working implementation.
```

**Validation**:
- [ ] No code beyond what's needed to pass tests
- [ ] Implementation is straightforward and readable
- [ ] All design patterns are justified by tests

**Output**: Minimal working implementation

---

### 6. Verify Test Success

**Agent**: `unit-testing:test-automator`

**Prompt Template**:
```
Run all tests for: $ARGUMENTS and verify they pass.

Check:
- All tests pass (100% pass rate)
- Test coverage meets minimum thresholds:
  - Line coverage ≥ 80%
  - Branch coverage ≥ 75%
- No tests were accidentally broken
- No test modifications occurred

Generate:
- Test execution report with pass/fail counts
- Coverage metrics by module and overall
- List of any failing tests with error messages

Output: Test execution report, coverage metrics.
```

**GATE**: All tests must pass before proceeding

**Output**: Test execution report, coverage metrics

---

## Phase 4: REFACTOR - Improve Code Quality

### 7. Code Refactoring

**Agent**: `tdd-workflows:code-reviewer`

**Prompt Template**:
```
Refactor implementation for: $ARGUMENTS while keeping tests green.

Apply:
- SOLID principles (Single Responsibility, Open/Closed, etc.)
- DRY (Don't Repeat Yourself) - remove duplication
- Improve naming for clarity
- Optimize performance only if needed
- Reduce complexity to within thresholds

Constraints:
- Tests must remain green throughout refactoring
- Run tests after each significant refactoring
- Maintain same test coverage
- No behavior changes

Check after each refactoring:
- All tests still pass
- Cyclomatic complexity ≤ 10
- No code duplication > 3 lines

Output: Refactored code with refactoring report documenting changes.
```

**Validation**:
- [ ] All tests still pass after refactoring
- [ ] Code complexity reduced
- [ ] Duplication eliminated
- [ ] Performance improved or maintained

**Output**: Refactored code, refactoring report

---

### 8. Test Refactoring

**Agent**: `unit-testing:test-automator`

**Prompt Template**:
```
Refactor tests for: $ARGUMENTS

Improve:
- Remove test duplication
- Improve test names for clarity
- Extract common fixtures
- Enhance test readability
- Optimize test execution speed

Ensure:
- Tests still provide same coverage
- All tests still pass
- No test behavior changes

Output: Refactored tests with improved test structure.
```

**Validation**:
- [ ] Coverage metrics unchanged or improved
- [ ] Tests are more readable and maintainable
- [ ] Test execution time acceptable

**Output**: Refactored tests, improved test structure

---

## Phase 5: Integration and System Tests

### 9. Write Integration Tests (Failing First)

**Agent**: `unit-testing:test-automator`

**Prompt Template**:
```
Write FAILING integration tests for: $ARGUMENTS

Test:
- Component interactions
- API contracts
- Data flow between components
- Integration with external systems
- End-to-end scenarios

Requirements:
- Tests must fail initially
- Focus on integration points, not unit functionality
- Test realistic scenarios

Output: Failing integration tests.
```

**Validation**:
- [ ] Tests fail due to missing integration logic
- [ ] Integration scenarios are realistic
- [ ] Tests are independent of unit tests

**Output**: Failing integration tests

---

### 10. Implement Integration

**Agent**: `python-development:python-pro` (or appropriate language agent)

**Prompt Template**:
```
Implement integration code for: $ARGUMENTS to make integration tests pass.

Focus on:
- Component interaction and communication
- Data flow and transformation
- API contract compliance
- Error handling across boundaries

Output: Integration implementation.
```

**Validation**:
- [ ] All integration tests pass
- [ ] Unit tests still pass
- [ ] Integration points are clean and well-defined

**Output**: Integration implementation

---

## Phase 6: Continuous Improvement Cycle

### 11. Performance and Edge Case Tests

**Agent**: `unit-testing:test-automator`

**Prompt Template**:
```
Add performance tests and additional edge case tests for: $ARGUMENTS

Include:
- Stress tests (load, volume)
- Boundary tests (limits, thresholds)
- Error recovery tests
- Concurrency tests (if applicable)

Measure:
- Execution time
- Resource usage
- Throughput

Output: Extended test suite with performance metrics.
```

**Metric**: Increased test coverage and scenario coverage

**Output**: Extended test suite

---

### 12. Final Code Review

**Agent**: `comprehensive-review:architect-review`

**Prompt Template**:
```
Perform comprehensive review of: $ARGUMENTS

Verify:
- TDD process was followed correctly
- Code quality meets standards
- Test quality is high
- Coverage exceeds thresholds
- Design patterns are appropriate
- Documentation is complete

Suggest:
- Improvements for code quality
- Additional test scenarios
- Performance optimizations
- Security considerations

Output: Review report with improvement suggestions.
```

**Action**: Implement critical suggestions while maintaining green tests

**Output**: Review report, improvement suggestions

---

## Development Modes

### Incremental Development Mode

For test-by-test development (recommended for complex features):

1. Write ONE failing test
2. Make ONLY that test pass
3. Refactor if needed
4. Repeat for next test

**Usage**: Add `--incremental` flag to focus on one test at a time.

**Benefits**:
- Smaller, focused changes
- Faster feedback loop
- Easier debugging
- Natural refactoring opportunities

---

### Test Suite Mode

For comprehensive test suite development (recommended for well-understood features):

1. Write ALL tests for a feature/module (failing)
2. Implement code to pass ALL tests
3. Refactor entire module
4. Add integration tests

**Usage**: Add `--suite` flag for batch test development.

**Benefits**:
- Faster overall development
- Comprehensive test coverage upfront
- Clear feature scope
- Efficient for simple features

---

## Validation Checkpoints

### RED Phase Validation

- [ ] All tests written before implementation
- [ ] All tests fail with meaningful error messages
- [ ] Test failures are due to missing implementation
- [ ] No test passes accidentally
- [ ] Test code has no syntax errors

### GREEN Phase Validation

- [ ] All tests pass
- [ ] No extra code beyond test requirements
- [ ] Coverage meets minimum thresholds:
  - [ ] Line coverage ≥ 80%
  - [ ] Branch coverage ≥ 75%
- [ ] No test was modified to make it pass
- [ ] Implementation is minimal

### REFACTOR Phase Validation

- [ ] All tests still pass after refactoring
- [ ] Code complexity reduced:
  - [ ] Cyclomatic complexity ≤ 10
  - [ ] Method length ≤ 20 lines
  - [ ] Class length ≤ 200 lines
- [ ] Duplication eliminated (no blocks > 3 lines)
- [ ] Performance improved or maintained
- [ ] Test readability improved

---

## Coverage Reports

Generate coverage reports after each major phase:

### Metrics to Track

- **Line coverage**: Percentage of code lines executed
- **Branch coverage**: Percentage of decision branches tested
- **Function coverage**: Percentage of functions called
- **Statement coverage**: Percentage of statements executed

### Reporting

```bash
# Generate coverage report
pytest --cov=module --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Threshold Enforcement

- Fail if line coverage < 80%
- Fail if branch coverage < 75%
- Critical paths must have 100% coverage

---

## Failure Recovery

If TDD discipline is broken at any point:

### Recovery Process

1. **STOP** immediately
2. Identify which phase was violated
3. Rollback to last valid state
   - Use git to revert changes
   - Restore last known good state
4. Resume from correct phase
5. Document lesson learned
   - What went wrong?
   - How to prevent recurrence?

### Common Violations

- Writing implementation before tests
- Modifying tests to make them pass
- Skipping refactor phase
- Ignoring failing tests
- Writing multiple features without tests

---

## TDD Metrics Tracking

Track and report the following metrics:

### Development Metrics

- **Time in each phase**: RED / GREEN / REFACTOR duration
- **Number of test-implementation cycles**: How many iterations
- **Test count growth**: Total tests over time
- **Coverage progression**: Coverage improvement over time

### Quality Metrics

- **Refactoring frequency**: How often code is improved
- **Defect escape rate**: Bugs found after TDD completion
- **Test execution time**: Speed of test suite
- **Test reliability**: Flaky test frequency

### Reporting

Generate metrics report at completion:
```
TDD Cycle Summary for: $ARGUMENTS

Phase Durations:
- RED: X minutes
- GREEN: Y minutes
- REFACTOR: Z minutes
- Total: X+Y+Z minutes

Coverage:
- Line: XX%
- Branch: YY%
- Function: ZZ%

Quality Metrics:
- Total tests: N
- Refactoring cycles: M
- Test execution time: T seconds
```

---

## Anti-Patterns to Avoid

### Strictly Prohibited

- ❌ Writing implementation before tests
- ❌ Writing tests that already pass
- ❌ Skipping the refactor phase
- ❌ Writing multiple features without tests
- ❌ Modifying tests to make them pass
- ❌ Ignoring failing tests
- ❌ Writing tests after implementation
- ❌ Skipping verification gates

### Why These Are Problems

- **Implementation before tests**: Violates test-first principle, loses design benefits
- **Tests that pass**: Fails to verify test correctness
- **Skipping refactor**: Technical debt accumulates
- **Multiple features without tests**: High risk, hard to debug
- **Modifying tests**: Breaks test integrity, invalidates verification

---

## Success Criteria

Completion is successful when ALL criteria are met:

### Process Criteria

- [ ] 100% of code written test-first
- [ ] All tests pass continuously (no regressions)
- [ ] Strict RED-GREEN-REFACTOR discipline followed

### Quality Criteria

- [ ] Coverage exceeds thresholds:
  - [ ] Line coverage ≥ 80%
  - [ ] Branch coverage ≥ 75%
  - [ ] Critical path coverage = 100%
- [ ] Code complexity within limits:
  - [ ] Cyclomatic complexity ≤ 10
  - [ ] Method length ≤ 20 lines
  - [ ] Class length ≤ 200 lines
- [ ] Zero defects in covered code
- [ ] No code duplication > 3 lines

### Documentation Criteria

- [ ] Clear test documentation
- [ ] All tests are self-documenting (names describe behavior)
- [ ] Test architecture documented

### Performance Criteria

- [ ] Fast test execution (< 5 seconds for unit tests)
- [ ] Tests are independent and isolated
- [ ] No flaky tests

---

## Notes

### Key Principles

- **Enforce strict RED-GREEN-REFACTOR discipline**
- **Each phase must be completed before moving to next**
- **Tests are the specification**
- **If a test is hard to write, the design needs improvement**
- **Refactoring is NOT optional**
- **Keep test execution fast**
- **Tests should be independent and isolated**

### Best Practices

- Write descriptive test names that explain behavior
- One assertion per test when possible
- Use fixtures for common test data
- Mock external dependencies
- Keep tests simple and readable
- Run tests frequently during development
- Treat test code with same care as production code

### Troubleshooting

**Problem**: Tests are hard to write
**Solution**: Improve design, reduce complexity, extract dependencies

**Problem**: Tests are slow
**Solution**: Mock external dependencies, use in-memory resources, parallelize

**Problem**: Tests are flaky
**Solution**: Isolate tests, remove dependencies, fix race conditions

---

**TDD implementation for**: $ARGUMENTS

**Execution Mode**: [incremental | suite] (specify or default to recommended)

**Start Time**: [timestamp]

**Completion**: When all success criteria are met
