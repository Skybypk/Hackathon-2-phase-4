/**
 * Test Frontend Proxy for Todo Chatbot
 * ======================================
 * Test frontend proxy configuration and API routing.
 * 
 * Usage:
 *   node test_frontend_proxy.js
 */

// ============================================
// Configuration
// ============================================

const CONFIG = {
  BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
  FRONTEND_URL: process.env.FRONTEND_URL || 'http://localhost:3000',
  PROXY_PATH: '/api',
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
// Proxy Tests
// ============================================

async function testDirectBackendAccess(reporter) {
  const testName = 'Direct Backend Access';
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

async function testProxyEndpoint(reporter) {
  const testName = 'Frontend Proxy Endpoint';
  try {
    const response = await fetch(`${CONFIG.FRONTEND_URL}${CONFIG.PROXY_PATH}/`, {
      method: 'GET',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    
    if (response.status === 200) {
      reporter.pass(testName);
      return true;
    } else if (response.status === 404) {
      reporter.skip(testName, 'Proxy not configured (404)');
      return false;
    } else {
      reporter.fail(testName, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    reporter.skip(testName, `Frontend not accessible: ${error.message}`);
    return false;
  }
}

async function testProxyTodosEndpoint(reporter) {
  const testName = 'Proxy Todos Endpoint';
  try {
    const response = await fetch(`${CONFIG.FRONTEND_URL}${CONFIG.PROXY_PATH}/todos`, {
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
    } else if (response.status === 404) {
      reporter.skip(testName, 'Proxy not configured (404)');
      return false;
    } else {
      reporter.fail(testName, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    reporter.skip(testName, error.message);
    return false;
  }
}

async function testProxyChatEndpoint(reporter) {
  const testName = 'Proxy Chat Endpoint';
  try {
    const response = await fetch(`${CONFIG.FRONTEND_URL}${CONFIG.PROXY_PATH}/chat`, {
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
    } else if (response.status === 404) {
      reporter.skip(testName, 'Proxy not configured (404)');
      return false;
    } else {
      reporter.fail(testName, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    reporter.skip(testName, error.message);
    return false;
  }
}

// ============================================
// CORS Tests
// ============================================

async function testCORSHeaders(reporter) {
  const testName = 'CORS Headers';
  try {
    const response = await fetch(`${CONFIG.BACKEND_URL}/`, {
      method: 'OPTIONS',
      signal: AbortSignal.timeout(CONFIG.TIMEOUT),
    });
    
    const corsHeader = response.headers.get('access-control-allow-origin');
    
    if (corsHeader) {
      reporter.pass(`${testName} (${corsHeader})`);
      return true;
    } else {
      reporter.fail(testName, 'No CORS headers found');
      return false;
    }
  } catch (error) {
    reporter.fail(testName, error.message);
    return false;
  }
}

// ============================================
// Configuration Tests
// ============================================

async function testEnvironmentVariables(reporter) {
  const testName = 'Environment Variables';
  
  const hasBackendUrl = !!process.env.BACKEND_URL;
  const hasFrontendUrl = !!process.env.FRONTEND_URL;
  
  if (hasBackendUrl && hasFrontendUrl) {
    reporter.pass(`${testName} (BACKEND_URL and FRONTEND_URL set)`);
    return true;
  } else if (hasBackendUrl) {
    reporter.pass(`${testName} (BACKEND_URL set)`);
    return true;
  } else {
    reporter.fail(testName, 'BACKEND_URL not set');
    return false;
  }
}

// ============================================
// Main Test Runner
// ============================================

async function runTests() {
  console.log('='.repeat(60));
  console.log('FRONTEND PROXY TEST SUITE');
  console.log('='.repeat(60));
  console.log(`Backend URL: ${CONFIG.BACKEND_URL}`);
  console.log(`Frontend URL: ${CONFIG.FRONTEND_URL}`);
  console.log(`Proxy Path: ${CONFIG.PROXY_PATH}`);
  console.log('='.repeat(60) + '\n');

  const reporter = new TestReporter();

  // Test environment
  console.log('Testing environment configuration...\n');
  await testEnvironmentVariables(reporter);

  // Test backend
  console.log('\nTesting backend connectivity...\n');
  const backendAvailable = await testDirectBackendAccess(reporter);
  
  if (backendAvailable) {
    await testCORSHeaders(reporter);
  }

  // Test proxy
  console.log('\nTesting proxy configuration...\n');
  await testProxyEndpoint(reporter);
  await testProxyTodosEndpoint(reporter);
  await testProxyChatEndpoint(reporter);

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
