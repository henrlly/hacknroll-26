import {
	CodeGenLoading,
	CodeRenderLoading,
	SceneLoading,
	SfxAssetLoading,
	VisualAssetLoading,
	type SceneLoadingType
} from '$lib/types/sceneTypes';
import type { Scene } from '$lib/types/planTypes';
import { NUM_CODE_VERSIONS_PER_SCENE } from './constants';

export function convertSceneToLoading(scene: Scene): SceneLoadingType {
	const assets = [];
	for (const asset of scene.assets_needed || []) {
		if (asset.asset_id === undefined) continue;
		if (asset.asset_type === 'sound_effect') {
			assets.push(
				SfxAssetLoading.parse({
					assetId: asset.asset_id,
					assetShortDesc: asset.asset_short_desc,
					assetLongDesc: asset.asset_long_desc
				})
			);
		} else if (asset.asset_type === 'visual') {
			assets.push(
				VisualAssetLoading.parse({
					assetId: asset.asset_id,
					assetShortDesc: asset.asset_short_desc,
					assetLongDesc: asset.asset_long_desc
				})
			);
		}
	}

	const code = Array.from({ length: NUM_CODE_VERSIONS_PER_SCENE }, (_, version_number) =>
		CodeGenLoading.parse({ version_number })
	);
	const render = Array.from({ length: NUM_CODE_VERSIONS_PER_SCENE }, (_, version_number) =>
		CodeRenderLoading.parse({ version_number })
	);
	return SceneLoading.parse({
		scene_number: scene.scene_number,
		assets,
		code,
		render,
		duration_seconds: scene.duration_seconds,
		visuals_description: scene.visuals_description,
		narration_script: scene.narration_script,
		sound_description: scene.sound_description,
		edit_notes: scene.edit_notes,
		scene_structure: scene.scene_structure
	});
}
