import { browser } from '$app/environment';

// Global access to websocket 
export const socketState = $state({
    socket: null as WebSocket | null,
    status: 'disconnected' as 'connected' | 'disconnected' | 'connecting',
});

export function connectWebSocket() {
    console.log("websocket connecting")
    if (!browser || socketState.socket) return;

    const socket = new WebSocket('ws://localhost:8000/api/ws');
    socketState.status = 'connecting';

    socket.onopen = () => {
        socketState.status = 'connected';
        socketState.socket = socket;
    };

    socket.onmessage = (event) => {
        // You can handle global events here 
    };

    socket.onclose = () => {
        socketState.status = 'disconnected';
        socketState.socket = null;
    };
}