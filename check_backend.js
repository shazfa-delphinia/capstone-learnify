// Script untuk check apakah backend server running
// Jalankan dengan: node check_backend.js

const http = require('http');

const checkBackend = () => {
  return new Promise((resolve, reject) => {
    const req = http.get('http://localhost:5000/', (res) => {
      if (res.statusCode === 200) {
        resolve(true);
      } else {
        reject(new Error(`Backend returned status ${res.statusCode}`));
      }
    });

    req.on('error', (err) => {
      reject(err);
    });

    req.setTimeout(3000, () => {
      req.destroy();
      reject(new Error('Connection timeout'));
    });
  });
};

checkBackend()
  .then(() => {
    console.log('✅ Backend server is running on port 5000');
    process.exit(0);
  })
  .catch((err) => {
    console.error('❌ Backend server is NOT running');
    console.error('Error:', err.message);
    console.log('\n📝 Cara menjalankan backend:');
    console.log('1. Buka terminal/PowerShell');
    console.log('2. cd learnify-backend');
    console.log('3. npm start');
    process.exit(1);
  });

