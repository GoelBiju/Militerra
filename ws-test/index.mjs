import WebSocket from 'ws';
import fetch from 'node-fetch';

const WS_CONNECTION = 'wss://ws.tryterra.co/connect';

async function getToken() {
    const url = 'https://ws.tryterra.co/auth/developer';
    const options = {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'dev-id': 'militerra-testing-Zbf5Rx4BcZ',
            'x-api-key': 'roLM-wTfZOpwjaa8hlsWPcr-W4cB0X24',
        },
    };

    try {
        const tokenResp = await fetch(url, options);
        return (await tokenResp.json())['token'];
    } catch (e) {
        console.error(e);
    }
    return '';
}

function initWS(token) {
    const socket = new WebSocket(WS_CONNECTION);

    socket.addEventListener('open', () =>
        console.log('Connection Established')
    );

    socket.addEventListener('close', (event) => {
        console.log('close');
        console.log(event.reason);
    });

    socket.addEventListener('error', (event) => {
        console.log('error');
        console.log(event);
    });

    let expectingHeartBeatAck = false;

    function heartBeat() {
        if (expectingHeartBeatAck) socket.close();
        const heartBeatPayload = JSON.stringify({ op: 0 });
        socket.send(heartBeatPayload);
        console.log('↑  ' + heartBeatPayload);
        expectingHeartBeatAck = true;
    }

    socket.addEventListener('message', function (event) {
        console.log('↓  ' + event.data);
        const msg = JSON.parse(event.data);
        if (msg.op == 2) {
            heartBeat();
            const interval = msg.d.heartbeat_interval;
            setInterval(heartBeat, interval);
            const payload = JSON.stringify({
                op: 3,
                d: {
                    token: token,
                    type: 1, // 0 for user, 1 for developer
                },
            });
            socket.send(payload);
        }
        if (msg.op == 1) {
            expectingHeartBeatAck = false;
        }
    });
}

getToken().then((token) => initWS(token));
