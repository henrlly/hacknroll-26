import { z } from 'zod';

export const CandidateLoading = z
	.object({
		state: z.enum(['done']).default('done'),
		candidateId: z.string(),
		selected: z.boolean().default(false),
		finalSelected: z.boolean().default(false)
	})
	.strict();

export const VisualAssetLoading = z
	.object({
		type: z.literal('visual').default('visual'),
		state: z.enum(['not_started', 'generating', 'selecting', 'done']).default('not_started'),
		assetId: z.string(),
		assetShortDesc: z.string(),
		assetLongDesc: z.string(),
		candidates: z.array(CandidateLoading).default([])
	})
	.strict();

export const SfxAssetLoading = z
	.object({
		type: z.literal('sound_effect').default('sound_effect'),
		state: z.enum(['not_started', 'generating', 'done']).default('not_started'),
		assetId: z.string(),
		assetShortDesc: z.string(),
		assetLongDesc: z.string()
	})
	.strict();

export const AssetLoading = z.union([VisualAssetLoading, SfxAssetLoading]);

export const NarrationLoading = z
	.object({
		type: z.literal('narration').default('narration'),
		state: z.enum(['not_started', 'generating', 'done']).default('not_started')
	})
	.strict();

export const CodeGenLoading = z
	.object({
		type: z.literal('code_gen').default('code_gen'),
		state: z.enum(['not_started', 'generating', 'done']).default('not_started'),
		version_number: z.number(),
		retry_number: z.number().default(0)
	})
	.strict();

export const CodeRenderLoading = z
	.object({
		type: z.literal('code_render').default('code_render'),
		state: z.enum(['not_started', 'rendering', 'done']).default('not_started'),
		version_number: z.number(),
		retry_number: z.number().default(0),
		success: z.boolean().nullish().default(null),
		aborted: z.boolean().default(false),
		selected: z.boolean().default(false)
	})
	.strict();

export const SceneLoading = z
	.object({
		scene_number: z.number(),
		narration: NarrationLoading.default(NarrationLoading.parse({})),
		assets: z.array(AssetLoading),
		code: z.array(CodeGenLoading),
		render: z.array(CodeRenderLoading),

		duration_seconds: z.number(),
		visuals_description: z.string(),
		narration_script: z.string(),
		sound_description: z.string(),
		edit_notes: z.string(),
		scene_structure: z.string()
	})
	.strict();

export const NarrationGenObj = z
	.object({
		scene_number: z.number(),
		done: z.boolean().default(false)
	})
	.strict();

export const VisualAssetGenObj = z
	.object({
		url: z.string(),
		desc: z.string(),
		liked: z.boolean().default(false)
	})
	.strict();

export const SfxAssetGenObj = z
	.object({
		desc: z.string(),
		done: z.boolean().default(false)
	})
	.strict();

export const VideoLoading = z
  .object({
    session_id: z.string().default(''),
		scenes: z.array(SceneLoading),
		topic: z.string().default(''),
		main_font: z.string().default(''),
		secondary_font: z.string().default(''),
		full_script: z.string().default(''),
		narration_gen: z.array(NarrationGenObj).default([]),
		visual_asset_gen: z.array(VisualAssetGenObj).default([]),
		sfx_asset_gen: z.array(SfxAssetGenObj).default([]),
		generation_step: z.enum(["initial_input", "pre_plan", "plan_generation", "scene_generation", "final_video"])
	})
	.strict();

export type VideoLoadingType = z.infer<typeof VideoLoading>;

export type SceneLoadingType = z.infer<typeof SceneLoading>;
export type AssetLoadingType = z.infer<typeof AssetLoading>;
