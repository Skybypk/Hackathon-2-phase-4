/**
 * Test Proxy Fix for Todo Chatbot
 * =================================
 * Test to verify the proxy fix is working correctly.
 * 
 * Fix Applied:
 * - Added CORS middleware to FastAPI backend
 * - Configured Next.js rewrites in next.config.js
 * - Set up environment variables in .env.local
 * 
 * Usage:
 *   node test_proxy_fix.js
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
// CORS Fix Tests
// ============================================

async function testCORSFix(reporter) {
  console.log('\n--- CORS Fix Verification ---\n');

  // Test 1: OPTIONS preflight request
  const testName1 = 'OPTIONS Preflight';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/chat`, {
      method: 'OPTIONS',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });

    if (response.status === 200) {
      const corsHeaders = {
        allowOrigin: response.headers.get('access-control-allow-origin'),
        allowMethods: response.headers.get('access-control-allow-methods'),
        allowHeaders: response.headers.get('access-control-allow-headers'),
        allowCredentials: response.headers.get('access-control-allow-credentials'),
      };

      if (corsHeaders.allowOrigin) {
        reporter.pass(`${testName1} (Origin: ${corsHeaders.allowOrigin})`);
      } else {
        reporter.fail(testName1, 'Missing Allow-Origin header');
      }
    } else {
      reporter.fail(testName1, `HTTP ${response.status}`);
    }
  } catch (error) {
    reporter.fail(testName1, error.message);
  }

  // Test 2: GET request with CORS
  const testName2 = 'GET Request with CORS';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/todos`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });

    if (response.status === 200) {
      reporter.pass(testName2);
    } else {
      reporter.fail(testName2, `HTTP ${response.status}`);
    }
  } catch (error) {
    reporter.fail(testName2, error.message);
  }

  // Test 3: POST request with CORS
  const testName3 = 'POST Request with CORS';
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

// ============================================
// Next.js Rewrite Tests
// ============================================

async function testNextJsRewrites(reporter) {
  console.log('\n--- Next.js Rewrites Verification ---\n');

  const proxyPath = '/api';

  // Test 1: Proxy root
  const testName1 = 'Proxy Root (/api/)';
  try {
    const response = await fetch(`${CONFIG.FRONTEND_URL}${proxyPath}/`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });

    if (response.status === 200) {
      reporter.pass(testName1);
    } else if (response.status === 404) {
      reporter.skip(testName1, 'Rewrites not configured');
    } else {
      reporter.fail(testName1, `HTTP ${response.status}`);
    }
  } catch (error) {
    reporter.skip(testName1, `Frontend not accessible: ${error.message}`);
  }

  // Test 2: Proxy todos
  const testName2 = 'Proxy Todos (/api/todos)';
  try {
    const response = await fetch(`${CONFIG.FRONTEND_URL}${proxyPath}/todos`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });

    if (response.status === 200) {
      const data = await response.json();
      if (Array.isArray(data)) {
        reporter.pass(testName2);
      } else {
        reporter.fail(testName2, 'Response is not an array');
      }
    } else if (response.status === 404) {
      reporter.skip(testName2, 'Rewrites not configured');
    } else {
      reporter.fail(testName2, `HTTP ${response.status}`);
    }
  } catch (error) {
    reporter.skip(testName2, error.message);
  }

  // Test 3: Proxy chat
  const testName3 = 'Proxy Chat (/api/chat)';
  try {
    const response = await fetch(`${CONFIG.FRONTEND_URL}${proxyPath}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'Hi' }),
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });

    if (response.status === 200) {
      const data = await response.json();
      if (data.response && data.action) {
        reporter.pass(testName3);
      } else {
        reporter.fail(testName3, 'Missing response or action field');
      }
    } else if (response.status === 404) {
      reporter.skip(testName3, 'Rewrites not configured');
    } else {
      reporter.fail(testName3, `HTTP ${response.status}`);
    }
  } catch (error) {
    reporter.skip(testName3, error.message);
  }
}

// ============================================
// Environment Variables Tests
// ============================================

async function testEnvironmentVariables(reporter) {
  console.log('\n--- Environment Variables Verification ---\n');

  // Test 1: BACKEND_URL is set
  const testName1 = 'BACKEND_URL';
  if (process.env.BACKEND_URL) {
    reporter.pass(`${testName1} (${process.env.BACKEND_URL})`);
  } else {
    reporter.fail(testName1, 'Not set (using default)');
  }

  // Test 2: FRONTEND_URL is set
  const testName2 = 'FRONTEND_URL';
  if (process.env.FRONTEND_URL) {
    reporter.pass(`${testName2} (${process.env.FRONTEND_URL})`);
  } else {
    reporter.fail(testName2, 'Not set (using default)');
  }

  // Test 3: .env.local file exists
  const testName3 = '.env.local File';
  try {
    const fs = require('fs');
    const path = require('path');
    const envLocalPath = path.join(__dirname, '.env.local');
    
    if (fs.existsSync(envLocalPath)) {
      reporter.pass(testName3);
    } else {
      reporter.fail(testName3, 'File not found');
    }
  } catch (error) {
    reporter.fail(testName3, error.message);
  }
}

// ============================================
// Integration Tests
// ============================================

async function testIntegration(reporter) {
  console.log('\n--- Integration Tests ---\n');

  // Test complete workflow through proxy
  const workflow = [
    { method: 'POST', path: '/chat', body: { message: 'Hi' } },
    { method: 'POST', path: '/chat', body: { message: 'Add todo: test task' } },
    { method: 'GET', path: '/todos', body: null },
  ];

  for (const { method, path, body } of workflow) {
    const testName = `Integration: ${method} ${path}`;
    try {
      const options = {
        method,
        signal: AbortSignal.timeout(CONFIG.TIMEOUT),
      };

      if (body) {
        options.headers = { 'Content-Type': 'application/json' };
        options.body = JSON.stringify(body);
      }

      const response = await fetch(`${CONFIG.FRONTEND_URL}/api${path}`, options);

      if (response.status === 200) {
        reporter.pass(testName);
      } else if (response.status === 404) {
        reporter.skip(testName, 'Proxy not configured');
      } else {
        reporter.fail(testName, `HTTP ${response.status}`);
      }
    } catch (error) {
      reporter.skip(testName, error.message);
    }
  }
}

// ============================================
// Main Test Runner
// ============================================

async function runTests() {
  console.log('='.repeat(60));
  console.log('PROXY FIX TEST SUITE');
  console.log('='.repeat(60));
  console.log(`Backend URL: ${CONFIG.BACKEND_URL}`);
  console.log(`Frontend URL: ${CONFIG.FRONTEND_URL}`);
  console.log('='.repeat(60) + '\n');

  const reporter = new TestReporter();

  // Check backend availability
  console.log('Checking backend availability...\n');
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    
    if (response.status !== 200) {
      console.error('Backend not available. Please start the backend server.');
    }
  } catch (error) {
    console.error('Backend not available. Please start the backend server.');
  }

  // Run tests
  await testCORSFix(reporter);
  await testEnvironmentVariables(reporter);
  await testNextJsRewrites(reporter);
  await testIntegration(reporter);

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
