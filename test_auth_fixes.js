const http = require('http');

const makeRequest = (options, data) => {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: body
        });
      });
    });
    req.on('error', reject);
    if (data) {
      req.write(data);
    }
    req.end();
  });
};

async function testAuth() {
  console.log('🧪 Testing Authentication Fixes...\n');

  try {
    // Test 1: Register User
    console.log('1️⃣ Testing POST /api/auth/register');
    const registerData = JSON.stringify({
      email: 'test@test.com',
      password: 'Test1234!',
      name: 'Test User'
    });

    const registerRes = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/auth/register',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(registerData)
      }
    }, registerData);

    console.log(`Status: ${registerRes.statusCode}`);
    console.log(`Response: ${registerRes.body}\n`);

    if (registerRes.statusCode === 201) {
      const registerResult = JSON.parse(registerRes.body);
      const accessToken = registerResult.accessToken;

      // Test 2: Get Current User
      console.log('2️⃣ Testing GET /api/auth/me');
      const meRes = await makeRequest({
        hostname: 'localhost',
        port: 8000,
        path: '/api/auth/me',
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });

      console.log(`Status: ${meRes.statusCode}`);
      console.log(`Response: ${meRes.body}\n`);

      // Test 3: Login
      console.log('3️⃣ Testing POST /api/auth/login');
      const loginData = JSON.stringify({
        email: 'test@test.com',
        password: 'Test1234!'
      });

      const loginRes = await makeRequest({
        hostname: 'localhost',
        port: 8000,
        path: '/api/auth/login',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(loginData)
        }
      }, loginData);

      console.log(`Status: ${loginRes.statusCode}`);
      console.log(`Response: ${loginRes.body}\n`);

      // Test 4: Refresh Token
      if (loginRes.statusCode === 200) {
        const loginResult = JSON.parse(loginRes.body);
        console.log('4️⃣ Testing POST /api/auth/refresh');
        const refreshData = JSON.stringify({
          refreshToken: loginResult.refreshToken
        });

        const refreshRes = await makeRequest({
          hostname: 'localhost',
          port: 8000,
          path: '/api/auth/refresh',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(refreshData)
          }
        }, refreshData);

        console.log(`Status: ${refreshRes.statusCode}`);
        console.log(`Response: ${refreshRes.body}\n`);
      }
    }

    console.log('✅ Authentication tests completed!');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

testAuth();
