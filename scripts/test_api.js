const https = require('https');

const key = process.argv[2] || 'sk-72210b6d984612c8f2d4560ecd6bd1e09932f6a0fb05e6c503031766a3d37654';
const data = JSON.stringify({
  model: 'gpt-image-2',
  prompt: 'a red apple on white background',
  images: [],
  aspectRatio: '1024x1536',
  replyType: 'json'
});

const req = https.request({
  hostname: 'grsaiapi.com',
  path: '/v1/api/generate',
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${key}`,
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(data)
  },
  timeout: 30000
}, (res) => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    try {
      const j = JSON.parse(body);
      console.log('STATUS:', j.status);
      console.log('HAS_RESULTS:', !!j.results);
      if (j.results) console.log('URL:', j.results[0]?.url?.slice(0, 50));
      if (j.error) console.log('ERR:', j.error);
    } catch(e) {
      console.log('PARSE_ERR:', body.slice(0, 200));
    }
  });
});
req.on('error', e => console.log('REQ_ERR:', e.message));
req.write(data);
req.end();
