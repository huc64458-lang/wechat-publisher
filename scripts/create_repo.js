const https = require('https');

const token = process.argv[2];

const data = JSON.stringify({
  name: 'wechat-publisher',
  description: '公众号AI写作工作流插件 — 写作·配图·封面·检测·发布一条龙',
  private: false
});

const req = https.request({
  hostname: 'api.github.com',
  path: '/user/repos',
  method: 'POST',
  headers: {
    'Authorization': `token ${token}`,
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'wechat-publisher'
  }
}, (res) => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    const result = JSON.parse(body);
    if (res.statusCode === 201) {
      console.log('OK ' + result.html_url);
    } else {
      console.log('ERR ' + res.statusCode + ' ' + (result.message || body.slice(0, 300)));
    }
  });
});

req.write(data);
req.end();
