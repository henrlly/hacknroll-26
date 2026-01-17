import { socketState } from '$lib/socket.svelte';
import { videoState } from '$lib/stores/generation-data.svelte';
import { EditSceneRequest, MakeSceneRequest, RenderRequest, SelectImageRequest, StitchRequest } from '$lib/types/apiTypes';

export function sendEditPrompt(prompt: string, scene_number: number) {
	const request = EditSceneRequest.parse({
		custom_edit_prompt: prompt,
		scene_number,
	});

	socketState.socket?.send(JSON.stringify(request));
}

export function sendMakeScene(scene_number: number) {
  const request = MakeSceneRequest.parse({
    scene_number
  });

  socketState.socket?.send(JSON.stringify(request));
}

export function sendRenderAndStitch(scene_number: number) {
  // find version number in videoState's scene where
  console.log("R", videoState.scenes[scene_number].render)
  const version_number = videoState.scenes[scene_number].render.findIndex(r => r.success)
	const request = RenderRequest.parse({
    scene_number,
    version_number
  });
	socketState.socket?.send(JSON.stringify(request));
  const stitchRequest = StitchRequest.parse({});
  socketState.socket?.send(JSON.stringify(stitchRequest));
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
