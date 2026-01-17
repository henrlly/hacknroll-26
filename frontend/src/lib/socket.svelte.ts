import { browser } from "$app/environment";

export const socketState = $state({
    socket: null as WebSocket | null,
    status: "disconnected" as "connected" | "disconnected",
})

export function connectWebSocket() {
    if (!browser || socketState.socket) return;

    const socket = new WebSocket("ws://localhost:8000/api/ws");
    socket.onopen = () => {
        socketState.status = "connected";
        socketState.socket = socket;
    }

    socket.onmessage = (event) => {
        // Handle Messages from server here
    }

    socket.onclose = () => {
        socketState.status = "disconnected";
        socketState.socket = null;
    }
}