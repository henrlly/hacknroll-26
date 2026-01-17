import { socketState } from '$lib/socket.svelte';
import { EditSceneRequest, SelectImageRequest } from '$lib/types/apiTypes';

export function sendEditPrompt(prompt: string) {
	const request = EditSceneRequest.parse({
		custom_edit_prompt: prompt,
		scene_number: 1,
	});

	socketState.socket?.send(JSON.stringify(request));
}

export function selectVisual({
	assetId,
	selectedCandidateId
}: {
	assetId: string;
	selectedCandidateId: string;
}) {
	const request = SelectImageRequest.parse({
		asset_id: assetId,
		selected_candidate_id: selectedCandidateId
	});
	socketState.socket?.send(JSON.stringify(request));
}
