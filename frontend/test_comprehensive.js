/**
 * Test Comprehensive for Todo Chatbot Frontend
 * ==============================================
 * Comprehensive test suite for the frontend components.
 * 
 * Usage:
 *   npm test -- test_comprehensive.js
 *   or
 *   node test_comprehensive.js
 */

// ============================================
// Configuration
// ============================================

const CONFIG = {
  BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
  FRONTEND_URL: process.env.FRONTEND_URL || 'http://localhost:3000',
  TIMEOUT: 10000,
};

// ============================================
// Test Utilities
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
// API Tests
// ============================================

async function testBackendHealth(reporter) {
  const testName = 'Backend Health Check';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    
    if (response.status === 200) {
      reporter.pass(testName);
      return true;
    } else {
      reporter.fail(testName, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    reporter.fail(testName, error.message);
    return false;
  }
}

async function testTodosEndpoint(reporter) {
  const testName = 'Todos Endpoint';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/todos`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    
    if (response.status === 200) {
      const data = await response.json();
      if (Array.isArray(data)) {
        reporter.pass(testName);
        return true;
      } else {
        reporter.fail(testName, 'Response is not an array');
        return false;
      }
    } else {
      reporter.fail(testName, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    reporter.fail(testName, error.message);
    return false;
  }
}

async function testChatEndpoint(reporter) {
  const testName = 'Chat Endpoint';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'Hi' }),
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    
    if (response.status === 200) {
      const data = await response.json();
      if (data.response && data.action) {
        reporter.pass(testName);
        return true;
      } else {
        reporter.fail(testName, 'Missing response or action field');
        return false;
      }
    } else {
      reporter.fail(testName, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    reporter.fail(testName, error.message);
    return false;
  }
}

// ============================================
// Chatbot Command Tests
// ============================================

async function testChatbotCommands(reporter) {
  const commands = [
    { message: 'Add todo: test task', expectedAction: 'add' },
    { message: 'Show todos', expectedAction: 'show' },
    { message: 'Hi', expectedAction: 'greeting' },
    { message: 'Help', expectedAction: 'help' },
    { message: 'Random text', expectedAction: 'unknown' },
  ];

  for (const { message, expectedAction } of commands) {
    const testName = `Chatbot Command: "${message}"`;
    try {
      const response = await fetch(`${CONFIG.BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
        signal: AbortSignal.timeout(CONFIG.TIMEOUT),
      });
      
      if (response.status === 200) {
        const data = await response.json();
        if (data.action === expectedAction) {
          reporter.pass(testName);
        } else {
          reporter.fail(testName, `Expected action "${expectedAction}", got "${data.action}"`);
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
// Frontend Tests
// ============================================

async function testFrontendHealth(reporter) {
  const testName = 'Frontend Health Check';
  try {
    const response = await fetch(`${CONFIG.FRONTEND_URL}/`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    
    if (response.status === 200) {
      reporter.pass(testName);
      return true;
    } else {
      reporter.fail(testName, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    reporter.skip(testName, 'Frontend not running');
    return false;
  }
}

// ============================================
// Performance Tests
// ============================================

async function testResponseTime(reporter) {
  const testName = 'API Response Time';
  try {
    const startTime = Date.now();
    const response = await fetch(`${CONFIG.BACKEND_URL}/`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    const elapsed = Date.now() - startTime;
    
    if (response.status === 200) {
      if (elapsed < 1000) {
        reporter.pass(`${testName} (${elapsed}ms)`);
      } else {
        reporter.fail(testName, `Response time ${elapsed}ms exceeds 1000ms`);
      }
    } else {
      reporter.fail(testName, `HTTP ${response.status}`);
    }
  } catch (error) {
    reporter.fail(testName, error.message);
  }
}

// ============================================
// Main Test Runner
// ============================================

async function runTests() {
  console.log('='.repeat(60));
  console.log('COMPREHENSIVE TEST SUITE');
  console.log('='.repeat(60));
  console.log(`Backend URL: ${CONFIG.BACKEND_URL}`);
  console.log(`Frontend URL: ${CONFIG.FRONTEND_URL}`);
  console.log(`Timeout: ${CONFIG.TIMEOUT}ms`);
  console.log('='.repeat(60) + '\n');

  const reporter = new TestReporter();

  // Check backend first
  console.log('Checking backend availability...\n');
  const backendAvailable = await testBackendHealth(reporter);

  if (backendAvailable) {
    console.log('\nRunning API tests...\n');
    await testTodosEndpoint(reporter);
    await testChatEndpoint(reporter);
    await testChatbotCommands(reporter);
    await testResponseTime(reporter);
  } else {
    console.warn('\n⚠ Backend not available, skipping API tests\n');
  }

  // Check frontend
  console.log('\nChecking frontend availability...\n');
  await testFrontendHealth(reporter);

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
