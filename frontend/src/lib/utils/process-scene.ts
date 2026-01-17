import type { SceneResponseType } from '$lib/types/apiTypes';
import type { VideoPlan } from '$lib/types/planTypes';
import { CandidateLoading, type SceneLoadingType } from '$lib/types/sceneTypes';
import { convertSceneToLoading } from './convert-scene-to-loading';

export function sceneFromPlan(plan: VideoPlan, scenesObj: { data: SceneLoadingType[] }) {
	console.log('processing plan');
	console.log(plan);
	if (plan?.scenes === undefined) return;
	for (let scene of plan.scenes) {
		scenesObj.data.push(convertSceneToLoading(scene));
		// assetIdToSceneNumber = updateAssetIdToSceneNumber(scene, assetIdToSceneNumber);
	}
	console.log(scenesObj.data);
}

function assetIdToSceneNumber(assetId: string, scenes: SceneLoadingType[]) {
	return scenes.findIndex((scene) => scene.assets.map((a) => a.assetId).includes(assetId));
}

export function processSceneEvent(
	event: SceneResponseType,
	scenesObj: { data: SceneLoadingType[] }
) {
	console.log(event);
	// type safety doesnt work with switch statement
	if (event.type === 'narration') {
		scenesObj.data[event.scene_number].narration.state =
			event.event_type === 'narration_generation_start' ? 'generating' : 'done';
	} else if (event.type === 'asset') {
		const scene_number = assetIdToSceneNumber(event.asset_id, scenesObj.data);
		const assetIdx = scenesObj.data[scene_number].assets.findIndex(
			(a) => a.assetId === event.asset_id
		);

		if (event.asset_type === 'sound_effect') {
			scenesObj.data[scene_number].assets[assetIdx].state =
				event.event_type === 'generation_start' ? 'generating' : 'done';
		} else {
			if (scenesObj.data[scene_number].assets[assetIdx].type !== 'visual') {
				throw 'Asset type mismatch: expected visual';
			}
			if (event.event_type === 'generation_start') {
				scenesObj.data[scene_number].assets[assetIdx].state = 'generating';
			} else {
				scenesObj.data[scene_number].assets[assetIdx].candidates.push(
					CandidateLoading.parse({ candidateId: event.candidate_id, state: 'done' })
				);
			}
		}
	} else if (event.type === 'asset_selection') {
		const scene_number = assetIdToSceneNumber(event.asset_id, scenesObj.data);
		const assetIdx = scenesObj.data[scene_number].assets.findIndex(
			(a) => a.assetId === event.asset_id
		);
		if (scenesObj.data[scene_number].assets[assetIdx].type !== 'visual') {
			throw 'Asset type mismatch: expected visual';
		}
		if (event.event_type === 'selection_start') {
			scenesObj.data[scene_number].assets[assetIdx].state = 'selecting';
		} else {
			const candidates = scenesObj.data[scene_number].assets[assetIdx].candidates;
			// find candidate idx that matches event.selected_candidate_ids
			const candidateIdxs = candidates
				.map((e, i) => (event.selected_candidate_ids?.includes(e.candidateId) ? i : ''))
				.filter((idx) => typeof idx === 'number');
			// find candidate idx that matches event.selected_candidate_id
			const candidateIdx = candidates.findIndex(
				(c) => c.candidateId === event.selected_candidate_id
			);
			for (const idx of candidateIdxs)
				scenesObj.data[scene_number].assets[assetIdx].candidates[idx].selected = true;
			scenesObj.data[scene_number].assets[assetIdx].candidates[candidateIdx].finalSelected = true;
			scenesObj.data[scene_number].assets[assetIdx].state = 'done';
		}
	} else if (event.type === 'code_generation') {
		scenesObj.data[event.scene_number].code[event.version_number].retry_number = event.retry_number;
		scenesObj.data[event.scene_number].code[event.version_number].state =
			event.event_type === 'code_generation_start' ? 'generating' : 'done';
	} else if (event.type === 'code_rendering') {
		scenesObj.data[event.scene_number].render[event.version_number].retry_number =
			event.retry_number;
		scenesObj.data[event.scene_number].render[event.version_number].state =
			event.event_type === 'rendering_start' ? 'rendering' : 'done';
		scenesObj.data[event.scene_number].render[event.version_number].success = event.success;
		scenesObj.data[event.scene_number].render[event.version_number].aborted =
			event.error_message === 'cancelled';
  } else if (event.type === 'code_rendering_selection') {
    scenesObj.data[event.scene_number].render[event.version_number].selected = true;
  }
	console.log(scenesObj.data);
}
