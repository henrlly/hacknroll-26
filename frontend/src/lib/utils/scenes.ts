import {
	NarrationGenObj,
	SfxAssetGenObj,
	VisualAssetGenObj,
	type VideoLoadingType
} from '$lib/types/sceneTypes';
import { STATIC_API_BASE } from './constants';

export function processFullScript(video: VideoLoadingType) {
	let full_script = '';
	for (let scene of video.scenes!) {
		full_script += scene.narration_script + ' ';
	}
	video.full_script = full_script.trim();
}

export function processNarrationGen(video: VideoLoadingType) {
	let narration_gen = [];
	for (let scene of video.scenes!) {
		narration_gen.push(
			NarrationGenObj.parse({
				scene_number: scene.scene_number,
				done: scene.narration.state === 'done'
			})
		);
	}
	video.narration_gen = narration_gen;
}

export function processVisualAssetGen(video: VideoLoadingType) {
	let visual_asset_gen = [];
	for (let scene of video.scenes!) {
		for (let asset of scene.assets) {
			if (asset.type === 'sound_effect') continue;
			for (let c of asset.candidates) {
				visual_asset_gen.push(
					VisualAssetGenObj.parse({
						url: `${STATIC_API_BASE}/${video.session_id}/${asset.assetId}/${c.candidateId}.jpg`,
						mp4Url: `${STATIC_API_BASE}/${video.session_id}/${asset.assetId}/${c.candidateId}.mp4`,
						desc: asset.assetShortDesc,
						liked: c.selected
					})
				);
			}
		}
	}
	video.visual_asset_gen = visual_asset_gen;
}

export function processSfxAssetGen(video: VideoLoadingType) {
	let sfx_asset_gen = [];
	for (let scene of video.scenes!) {
		for (let asset of scene.assets) {
			if (asset.type === 'visual') continue;
			sfx_asset_gen.push(
				SfxAssetGenObj.parse({
					url: `${STATIC_API_BASE}/${video.session_id}/${asset.assetId}.mp3`,
					desc: asset.assetShortDesc
				})
			);
		}
	}
	video.sfx_asset_gen = sfx_asset_gen;
}
