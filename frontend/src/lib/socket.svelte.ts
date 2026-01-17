import { browser } from '$app/environment';
import { StreamResponse } from './types/apiTypes';
import { videoState } from './stores/generation-data.svelte';
import { processSceneEvent, sceneFromPlan } from './utils/process-scene';
import { ALL, parse } from 'partial-json';
import { VideoPlanSchema } from './types/planTypes';
import { processFullScript, processNarrationGen, processSfxAssetGen, processVisualAssetGen } from './utils/scenes';

// Global access to websocket
export const socketState = $state({
	socket: null as WebSocket | null,
	status: 'disconnected' as 'connected' | 'disconnected' | 'connecting'
});

export function connectWebSocket() {
	if (!browser || socketState.socket) return;

	const socket = new WebSocket('ws://localhost:8000/api/ws');
	socketState.status = 'connecting';

	socket.onopen = () => {
		socketState.status = 'connected';
		socketState.socket = socket;
	};

	let plan_string = '';
	let plan = VideoPlanSchema.parse({});

	socket.onmessage = async (event) => {
		// console.log(event);
		const result = StreamResponse.safeParse(JSON.parse(event.data));
		if (result.error) {
			console.log(JSON.parse(event.data));
			return;
		}
		if (result.data.type === 'start') {
			videoState.session_id = result.data.session_id;
			videoState.generationStep = 'WRITING SCRIPT';
			videoState.generationStepView = 'WRITING SCRIPT';
		} else if (result.data.type === 'plan') {
			// TODO: add plan loading before stream
			if (result.data.event_type === 'plan_start') {
				// isLoadingPlan = true;
			} else if (result.data.event_type === 'plan_stream') {
				plan_string += result.data.delta;
				plan = VideoPlanSchema.parse(parse(plan_string, ALL));
				sceneFromPlan(plan, videoState);
        processFullScript(videoState);
			} else {
        sceneFromPlan(plan, videoState);
        processNarrationGen(videoState);
        processVisualAssetGen(videoState);
        processSfxAssetGen(videoState);
				videoState.generationStep = 'DOING TASKS';
				videoState.generationStepView = 'DOING TASKS';
			}
		} else if (result.data.type !== 'final_video') {
			processSceneEvent(result.data, videoState);
		} else {
			if (result.data.event_type === 'stitching_end') {
				videoState.generationStep = 'COMPLETED';
				videoState.generationStepView = 'COMPLETED';
			}
		}
	};

	socket.onclose = () => {
		socketState.status = 'disconnected';
		socketState.socket = null;
	};
}
