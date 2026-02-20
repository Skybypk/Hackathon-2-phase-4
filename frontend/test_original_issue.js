/**
 * Test Original Issue for Todo Chatbot
 * ======================================
 * Test to reproduce and verify the original issue is fixed.
 * 
 * Original Issue:
 * - Chatbot not responding to commands
 * - Inconsistent response formats
 * - Frontend unable to connect to backend
 * 
 * Usage:
 *   node test_original_issue.js
 */

// ============================================
// Configuration
// ============================================

const CONFIG = {
  BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
  TIMEOUT: 10000,
};

// ============================================
// Test Reporter
// ============================================

class TestReporter {
  constructor() {
    this.total = 0;
    this.passed = 0;
    this.failed = 0;
    this.skipped = 0;
  }

  pass(testName) {
    this.total++;
    this.passed++;
    console.log(`✓ ${testName}`);
  }

  fail(testName, error) {
    this.total++;
    this.failed++;
    console.error(`✗ ${testName}`);
    console.error(`  Error: ${error.message || error}`);
  }

  skip(testName, reason) {
    this.total++;
    this.skipped++;
    console.warn(`⊘ ${testName}`);
    console.warn(`  Reason: ${reason}`);
  }

  summary() {
    console.log('\n' + '='.repeat(60));
    console.log('TEST SUMMARY');
    console.log('='.repeat(60));
    console.log(`Total:  ${this.total}`);
    console.log(`Passed: ${this.passed} (${(this.passed / this.total * 100).toFixed(1)}%)`);
    console.log(`Failed: ${this.failed} (${(this.failed / this.total * 100).toFixed(1)}%)`);
    console.log(`Skipped: ${this.skipped}`);
    console.log('='.repeat(60));
  }
}

// ============================================
// Original Issue Tests
// ============================================

/**
 * Issue #1: Chatbot not responding to commands
 * 
 * Root Cause: Pattern matching was too strict
 * Fix: Updated regex patterns to be more flexible
 */
async function testChatbotRespondsToCommands(reporter) {
  console.log('\n--- Issue #1: Chatbot Response ---\n');

  const commands = [
    { message: 'Add todo: buy milk', expectedAction: 'add' },
    { message: 'add todo: finish report', expectedAction: 'add' },
    { message: 'ADD TODO: urgent task', expectedAction: 'add' },
    { message: 'Show todos', expectedAction: 'show' },
    { message: 'Delete todo 1', expectedAction: 'delete' },
  ];

  for (const { message, expectedAction } of commands) {
    const testName = `Command: "${message}"`;
    try {
      const response = await fetch(`${CONFIG.BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
        signal: AbortSignal.timeout(CONFIG.TIMEOUT),
      });

      if (response.status === 200) {
        const data = await response.json();
        if (data.action === expectedAction && data.response) {
          reporter.pass(testName);
        } else {
          reporter.fail(testName, `Unexpected response format`);
        }
      } else {
        reporter.fail(testName, `HTTP ${response.status}`);
      }
    } catch (error) {
      reporter.fail(testName, error.message);
    }
  }
}

/**
 * Issue #2: Inconsistent response formats
 * 
 * Root Cause: Multiple response formats from different code paths
 * Fix: Standardized all responses to use ChatResponse model
 */
async function testConsistentResponseFormat(reporter) {
  console.log('\n--- Issue #2: Response Format Consistency ---\n');

  const commands = [
    'Hi',
    'Add todo: test',
    'Show todos',
    'Delete todo 1',
    'Help',
    'Random text',
  ];

  for (const command of commands) {
    const testName = `Response Format: "${command}"`;
    try {
      const response = await fetch(`${CONFIG.BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: command }),
        signal: AbortSignal.timeout(CONFIG.TIMEOUT),
      });

      if (response.status === 200) {
        const data = await response.json();
        
        // Check required fields
        const hasResponse = typeof data.response === 'string';
        const hasAction = typeof data.action === 'string';
        
        if (hasResponse && hasAction) {
          reporter.pass(testName);
        } else {
          reporter.fail(testName, `Missing fields (response: ${hasResponse}, action: ${hasAction})`);
        }
      } else {
        reporter.fail(testName, `HTTP ${response.status}`);
      }
    } catch (error) {
      reporter.fail(testName, error.message);
    }
  }
}

/**
 * Issue #3: Frontend unable to connect to backend
 * 
 * Root Cause: CORS not enabled
 * Fix: Added CORS middleware to FastAPI
 */
async function testFrontendBackendConnection(reporter) {
  console.log('\n--- Issue #3: Frontend-Backend Connection ---\n');

  // Test 1: Backend is accessible
  const testName1 = 'Backend Accessibility';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });

    if (response.status === 200) {
      reporter.pass(testName1);
    } else {
      reporter.fail(testName1, `HTTP ${response.status}`);
    }
  } catch (error) {
    reporter.fail(testName1, error.message);
  }

  // Test 2: CORS headers are present
  const testName2 = 'CORS Headers';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/`, {
      method: 'OPTIONS',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });

    const corsHeader = response.headers.get('access-control-allow-origin');
    
    if (corsHeader) {
      reporter.pass(`${testName2} (${corsHeader})`);
    } else {
      reporter.fail(testName2, 'No CORS headers found');
    }
  } catch (error) {
    reporter.fail(testName2, error.message);
  }

  // Test 3: POST request from different origin (simulated)
  const testName3 = 'Cross-Origin POST';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'Hi' }),
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });

    if (response.status === 200) {
      reporter.pass(testName3);
    } else {
      reporter.fail(testName3, `HTTP ${response.status}`);
    }
  } catch (error) {
    reporter.fail(testName3, error.message);
  }
}

/**
 * Issue #4: Error handling
 * 
 * Root Cause: Server crashes on invalid input
 * Fix: Added try-except blocks and input validation
 */
async function testErrorHandling(reporter) {
  console.log('\n--- Issue #4: Error Handling ---\n');

  const errorCases = [
    { message: '', description: 'Empty message' },
    { message: '   ', description: 'Whitespace only' },
    { message: 'Delete todo 9999', description: 'Non-existent ID' },
    { message: '<script>alert("xss")</script>', description: 'XSS attempt' },
    { message: 'A'.repeat(10000), description: 'Very long message' },
  ];

  for (const { message, description } of errorCases) {
    const testName = `Error Case: ${description}`;
    try {
      const response = await fetch(`${CONFIG.BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
        signal: AbortSignal.timeout(CONFIG.TIMEOUT),
      });

      // Should always return 200 with error message in response
      if (response.status === 200) {
        const data = await response.json();
        if (data.response) {
          reporter.pass(testName);
        } else {
          reporter.fail(testName, 'No response in error case');
        }
      } else {
        reporter.fail(testName, `HTTP ${response.status}`);
      }
    } catch (error) {
      reporter.fail(testName, error.message);
    }
  }
}

// ============================================
// Main Test Runner
// ============================================

async function runTests() {
  console.log('='.repeat(60));
  console.log('ORIGINAL ISSUE TEST SUITE');
  console.log('='.repeat(60));
  console.log(`Backend URL: ${CONFIG.BACKEND_URL}`);
  console.log(`Timeout: ${CONFIG.TIMEOUT}ms`);
  console.log('='.repeat(60));

  const reporter = new TestReporter();

  // Check backend availability first
  console.log('\nChecking backend availability...\n');
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    
    if (response.status !== 200) {
      console.error('Backend not available. Please start the backend server:');
      console.error('  cd backend');
      console.error('  python main.py');
      process.exit(1);
    }
  } catch (error) {
    console.error('Backend not available. Please start the backend server:');
    console.error('  cd backend');
    console.error('  python main.py');
    process.exit(1);
  }

  // Run all issue tests
  await testChatbotRespondsToCommands(reporter);
  await testConsistentResponseFormat(reporter);
  await testFrontendBackendConnection(reporter);
  await testErrorHandling(reporter);

  // Print summary
  reporter.summary();

  // Return exit code
  return reporter.failed === 0 ? 0 : 1;
}

// ============================================
// Export for testing frameworks
// ============================================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { runTests, CONFIG };
}

// Run if executed directly
if (typeof require !== 'undefined' && require.main === module) {
  runTests()
    .then(exitCode => process.exit(exitCode))
    .catch(error => {
      console.error('Test runner error:', error);
      process.exit(1);
    });
}
