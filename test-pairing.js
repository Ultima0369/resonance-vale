const WebSocket = require('ws');

// Gateway WebSocket URL
const wsUrl = 'ws://127.0.0.1:18789/ws';

// 创建WebSocket连接
const ws = new WebSocket(wsUrl);

ws.on('open', function open() {
  console.log('Connected to Gateway');
  
  // 发送配对请求
  const pairingRequest = {
    jsonrpc: '2.0',
    method: 'pairing.request',
    params: {
      deviceName: 'test-user-2',
      roles: ['operator'],
      scopes: ['operator.read', 'operator.write']
    },
    id: 1
  };
  
  ws.send(JSON.stringify(pairingRequest));
});

ws.on('message', function incoming(data) {
  console.log('Received:', data.toString());
});

ws.on('error', function error(err) {
  console.error('WebSocket error:', err);
});

ws.on('close', function close() {
  console.log('Disconnected from Gateway');
});