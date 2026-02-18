const http = require('http');

const testFrontendRoute = (path, method = 'GET', data = null) => {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8000,
      path: path,
      method: method,
      headers: data ? {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      } : {}
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        console.log(`\n=== ${method} ${path} ===`);
        console.log(`Status: ${res.statusCode}`);
        console.log(`Response: ${body}`);
        console.log('==================\n');
        resolve({ statusCode: res.statusCode, body });
      });
    });

    req.on('error', (error) => {
      console.error(`Request failed: ${error.message}`);
      reject(error);
    });

    if (data) {
      req.write(data);
    }
    req.end();
  });
};

async function testFrontendAuth() {
  console.log('🧪 Testing Frontend Authentication Routes...\n');

  try {
    // Test all the routes that frontend should be calling
    console.log('✅ Testing CORRECT routes (with /api prefix):');

    // Test 1: GET /api/auth/me
    await testFrontendRoute('/api/auth/me');

    // Test 2: POST /api/auth/login
    const loginData = JSON.stringify({
      email: 'test@test.com',
      password: 'Test1234!'
    });
    await testFrontendRoute('/api/auth/login', 'POST', loginData);

    // Test 3: POST /api/auth/register
    const registerData = JSON.stringify({
      email: 'newuser@test.com',
      password: 'Test1234!',
      name: 'New User'
    });
    await testFrontendRoute('/api/auth/register', 'POST', registerData);

    console.log('\n❌ Testing WRONG routes (without /api prefix) for comparison:');

    // Test 4: GET /auth/me (should fail)
    await testFrontendRoute('/auth/me');

    // Test 5: POST /auth/login (should fail)
    await testFrontendRoute('/auth/login', 'POST', loginData);

  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

testFrontendAuth();
