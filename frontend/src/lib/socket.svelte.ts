import { browser } from '$app/environment';
import { StreamResponse } from './types/apiTypes';
import { videoState } from './stores/generation-data.svelte';
import { processSceneEvent, sceneFromPlan, sceneFromScenePlan } from './utils/process-scene';
import { ALL, parse } from 'partial-json';
import { SceneSchema, VideoPlanSchema } from './types/planTypes';
import {
	processFullScript,
	processNarrationGen,
	processSfxAssetGen,
	processVisualAssetGen
} from './utils/scenes';

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
	let scene_string = '';

	socket.onmessage = async (event) => {
		// console.log(event);
		const result = StreamResponse.safeParse(JSON.parse(event.data));
		if (result.error) {
			console.log(JSON.parse(event.data));
			return;
		}
		if (result.data.type === 'start') {
			videoState.session_id = result.data.session_id;
		} else if (result.data.type === 'plan') {
			// TODO: add plan loading before stream
			if (result.data.event_type === 'plan_start') {
				// isLoadingPlan = true;
			} else if (result.data.event_type === 'plan_stream') {
				plan_string += result.data.delta;
				const plan = VideoPlanSchema.parse(parse(plan_string, ALL));
				// console.log("PLANSTRING", plan_string)
				videoState.generationStep = 'WRITING SCRIPT';
				videoState.generationStepView = 'WRITING SCRIPT';
				sceneFromPlan(plan, videoState);
				processFullScript(videoState);
			} else if (result.data.event_type === 'plan_end') {
				plan_string = '';
				processNarrationGen(videoState);
				processVisualAssetGen(videoState);
				processSfxAssetGen(videoState);
				videoState.generationStep = 'DOING TASKS';
				videoState.generationStepView = 'DOING TASKS';
			}
		} else if (
			result.data.type !== 'final_video' &&
			result.data.type !== 'scene' &&
			result.data.type !== 'select_image'
		) {
			await processSceneEvent(result.data, videoState);
		} else if (result.data.type === 'final_video') {
			if (result.data.event_type === 'stitching_end') {
				videoState.generationStep = 'COMPLETED';
				videoState.generationStepView = 'COMPLETED';
				videoState.completed = true;
			}
		} else if (result.data.type === 'scene') {
			// TODO: add plan loading before stream
			if (result.data.event_type === 'scene_start') {
				// isLoadingPlan = true;
			} else if (result.data.event_type === 'scene_stream') {
				scene_string += result.data.delta;
				const scene = SceneSchema.parse(parse(scene_string, ALL));
				// console.log("PLANSTRING", plan_string)
				sceneFromScenePlan(scene, videoState);
				processFullScript(videoState);
			} else if (result.data.event_type === 'scene_end') {
				scene_string = '';
				processNarrationGen(videoState);
				processVisualAssetGen(videoState);
				processSfxAssetGen(videoState);
				videoState.generationStep = 'DOING TASKS';
				videoState.generationStepView = 'DOING TASKS';
			}
		} else if (result.data.type === 'select_image') {
			// well image is selected
			// export const SelectImageResponse = z.object({
			//      type: z.literal('select_image'),
			//      success: z.boolean(),
			//    })
			//
		}
		console.log(videoState);
	};

	socket.onclose = () => {
		socketState.status = 'disconnected';
		socketState.socket = null;
	};
}
