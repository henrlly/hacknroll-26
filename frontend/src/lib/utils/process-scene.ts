import type { SceneResponseType } from '$lib/types/apiTypes';
import type { VideoPlan } from '$lib/types/planTypes';
import {
	CandidateLoading,
	type SceneLoadingType,
	type VideoLoadingType
} from '$lib/types/sceneTypes';
import { convertSceneToLoading } from './convert-scene-to-loading';
import { processNarrationGen, processSfxAssetGen, processVisualAssetGen } from './scenes';

export function sceneFromPlan(plan: VideoPlan, videoObj: VideoLoadingType) {
	console.log('processing plan');
	console.log(plan);
	if (plan?.scenes === undefined) return;
	for (let scene of plan.scenes) {
		videoObj.scenes.push(convertSceneToLoading(scene));
		// assetIdToSceneNumber = updateAssetIdToSceneNumber(scene, assetIdToSceneNumber);
	}
	console.log(videoObj.scenes);
}

function assetIdToSceneNumber(assetId: string, scenes: SceneLoadingType[]) {
	return scenes.findIndex((scene) => scene.assets.map((a) => a.assetId).includes(assetId));
}

export function processSceneEvent(event: SceneResponseType, videoObj: VideoLoadingType) {
	console.log(event);
	// type safety doesnt work with switch statement
	if (event.type === 'narration') {
		videoObj.scenes[event.scene_number].narration.state =
			event.event_type === 'narration_generation_start' ? 'generating' : 'done';
    processNarrationGen(videoObj);
  } else if (event.type === 'asset') {
		const scene_number = assetIdToSceneNumber(event.asset_id, videoObj.scenes);
		const assetIdx = videoObj.scenes[scene_number].assets.findIndex(
			(a) => a.assetId === event.asset_id
		);

		if (event.asset_type === 'sound_effect') {
			videoObj.scenes[scene_number].assets[assetIdx].state =
				event.event_type === 'generation_start' ? 'generating' : 'done';
			processSfxAssetGen(videoObj);
		} else {
			if (videoObj.scenes[scene_number].assets[assetIdx].type !== 'visual') {
				throw 'Asset type mismatch: expected visual';
			}
			if (event.event_type === 'generation_start') {
				videoObj.scenes[scene_number].assets[assetIdx].state = 'generating';
			} else {
				videoObj.scenes[scene_number].assets[assetIdx].candidates.push(
					CandidateLoading.parse({ candidateId: event.candidate_id, state: 'done' })
				);
			}
			processVisualAssetGen(videoObj);
		}
	} else if (event.type === 'asset_selection') {
		const scene_number = assetIdToSceneNumber(event.asset_id, videoObj.scenes);
		const assetIdx = videoObj.scenes[scene_number].assets.findIndex(
			(a) => a.assetId === event.asset_id
		);
		if (videoObj.scenes[scene_number].assets[assetIdx].type !== 'visual') {
			throw 'Asset type mismatch: expected visual';
		}
		if (event.event_type === 'selection_start') {
			videoObj.scenes[scene_number].assets[assetIdx].state = 'selecting';
		} else {
			const candidates = videoObj.scenes[scene_number].assets[assetIdx].candidates;
			// find candidate idx that matches event.selected_candidate_ids
			const candidateIdxs = candidates
				.map((e, i) => (event.selected_candidate_ids?.includes(e.candidateId) ? i : ''))
				.filter((idx) => typeof idx === 'number');
			// find candidate idx that matches event.selected_candidate_id
			const candidateIdx = candidates.findIndex(
				(c) => c.candidateId === event.selected_candidate_id
			);
			for (const idx of candidateIdxs)
				videoObj.scenes[scene_number].assets[assetIdx].candidates[idx].selected = true;
			videoObj.scenes[scene_number].assets[assetIdx].candidates[candidateIdx].finalSelected = true;
			videoObj.scenes[scene_number].assets[assetIdx].state = 'done';
		}
	} else if (event.type === 'code_generation') {
		videoObj.scenes[event.scene_number].code[event.version_number].retry_number =
			event.retry_number;
		videoObj.scenes[event.scene_number].code[event.version_number].state =
			event.event_type === 'code_generation_start' ? 'generating' : 'done';
	} else if (event.type === 'code_rendering') {
		videoObj.scenes[event.scene_number].render[event.version_number].retry_number =
			event.retry_number;
		videoObj.scenes[event.scene_number].render[event.version_number].state =
			event.event_type === 'rendering_start' ? 'rendering' : 'done';
		videoObj.scenes[event.scene_number].render[event.version_number].success = event.success;
		videoObj.scenes[event.scene_number].render[event.version_number].aborted =
			event.error_message === 'cancelled';
	} else if (event.type === 'code_rendering_selection') {
		videoObj.scenes[event.scene_number].render[event.version_number].selected = true;
	}
	console.log(videoObj.scenes);
}
