import { z } from 'zod';

export const CandidateLoading = z
  .object({
    state: z.enum(['done']).catch('done'),
    candidateId: z.string().catch(''),
    selected: z.boolean().catch(false),
    finalSelected: z.boolean().catch(false)
  });

export const VisualAssetLoading = z
  .object({
    type: z.literal('visual').catch('visual'),
    state: z.enum(['not_started', 'generating', 'selecting', 'done']).catch('not_started'),
    assetId: z.string().catch(''),
    assetShortDesc: z.string().catch(''),
    assetLongDesc: z.string().catch(''),
    candidates: z.array(CandidateLoading).catch([])
  });

export const SfxAssetLoading = z
  .object({
    type: z.literal('sound_effect').catch('sound_effect'),
    state: z.enum(['not_started', 'generating', 'done']).catch('not_started'),
    assetId: z.string(),
    assetShortDesc: z.string().catch(''),
    assetLongDesc: z.string().catch(''),
  });

export const AssetLoading = z.union([VisualAssetLoading, SfxAssetLoading]);

export const NarrationLoading = z
  .object({
    type: z.literal('narration').catch('narration'),
    state: z.enum(['not_started', 'generating', 'done']).catch('not_started')
  });

export const CodeGenLoading = z
	.object({
		type: z.literal('code_gen').catch('code_gen'),
		state: z.enum(['not_started', 'generating', 'done']).catch('not_started'),
		version_number: z.number(),
		retry_number: z.number().catch(0)
	})
	;

export const CodeRenderLoading = z
	.object({
		type: z.literal('code_render').catch('code_render'),
		state: z.enum(['not_started', 'rendering', 'done']).catch('not_started'),
		version_number: z.number().catch(0),
		retry_number: z.number().catch(0),
		success: z.boolean().nullish().catch(null),
		aborted: z.boolean().catch(false),
		selected: z.boolean().catch(false)
	})
	;

export const SceneLoading = z
	.object({
		scene_number: z.number().catch(0),
		narration: NarrationLoading.catch(NarrationLoading.parse({})),
		assets: z.array(AssetLoading).catch([]),
		code: z.array(CodeGenLoading).catch([]),
		render: z.array(CodeRenderLoading).catch([]),

		duration_seconds: z.number().catch(0),
		visuals_description: z.string().catch(''),
		narration_script: z.string().catch(''),
		sound_description: z.string().catch(''),
		edit_notes: z.string().catch(''),
		scene_structure: z.string().catch('')
	})
	;

export const NarrationGenObj = z
	.object({
		scene_number: z.number(),
		done: z.boolean().catch(false)
	})
	;

export const VisualAssetGenObj = z
	.object({
		url: z.string().catch(''),
		mp4Url: z.string().catch(''),
		desc: z.string().catch(''),
		liked: z.boolean().catch(false)
	})
	;

export const SfxAssetGenObj = z
	.object({
		desc: z.string().catch(''),
		done: z.boolean().catch(false)
	})
	;

export const VideoLoading = z
	.object({
		session_id: z.string().catch(''),
		scenes: z.array(SceneLoading).catch([]),
		topic: z.string().catch(''),
		main_font: z.string().catch(''),
		secondary_font: z.string().catch(''),
		full_script: z.string().catch(''),
		narration_gen: z.array(NarrationGenObj).catch([]),
		visual_asset_gen: z.array(VisualAssetGenObj).catch([]),
		sfx_asset_gen: z.array(SfxAssetGenObj).catch([]),
		generationStep: z
			.enum(['INPUT', 'WRITING SCRIPT', 'DOING TASKS', 'COMPLETED'])
			.catch('INPUT'),
		generationStepView: z
			.enum(['INPUT', 'WRITING SCRIPT', 'DOING TASKS', 'COMPLETED'])
			.catch('INPUT'),
		completed: z.boolean().catch(false),
		sceneDurations: z.array(z.number()).catch([])
	})
	;

export type VideoLoadingType = z.infer<typeof VideoLoading>;

export type SceneLoadingType = z.infer<typeof SceneLoading>;
export type AssetLoadingType = z.infer<typeof AssetLoading>;
