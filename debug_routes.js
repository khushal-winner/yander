const http = require('http');

const testRoute = (path, method = 'GET', data = null) => {
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

async function debugRoutes() {
  console.log('🔍 Debugging Authentication Routes...\n');

  try {
    // Test 1: Health check
    await testRoute('/health');

    // Test 2: Root endpoint
    await testRoute('/');

    // Test 3: Auth register
    const registerData = JSON.stringify({
      email: 'test@test.com',
      password: 'Test1234!',
      name: 'Test User'
    });
    await testRoute('/api/auth/register', 'POST', registerData);

    // Test 4: Auth login
    const loginData = JSON.stringify({
      email: 'test@test.com',
      password: 'Test1234!'
    });
    await testRoute('/api/auth/login', 'POST', loginData);

    // Test 5: Test wrong route
    await testRoute('/auth/register', 'POST', registerData);

  } catch (error) {
    console.error('❌ Debug failed:', error.message);
  }
}

debugRoutes();
