import { z } from 'zod';

export const CandidateLoading = z
	.object({
		state: z.enum(['done']).default('done'),
		candidateId: z.string().default(''),
		selected: z.boolean().default(false),
		finalSelected: z.boolean().default(false)
	})
	.strict();

export const VisualAssetLoading = z
	.object({
		type: z.literal('visual').default('visual'),
		state: z.enum(['not_started', 'generating', 'selecting', 'done']).default('not_started'),
		assetId: z.string().default(''),
		assetShortDesc: z.string().default(''),
		assetLongDesc: z.string().default(''),
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
		version_number: z.number().default(0),
		retry_number: z.number().default(0),
		success: z.boolean().nullish().default(null),
		aborted: z.boolean().default(false),
		selected: z.boolean().default(false)
	})
	.strict();

export const SceneLoading = z
	.object({
		scene_number: z.number().default(0),
		narration: NarrationLoading.default(NarrationLoading.parse({})),
		assets: z.array(AssetLoading).default([]),
		code: z.array(CodeGenLoading).default([]),
		render: z.array(CodeRenderLoading).default([]),

		duration_seconds: z.number().default(0),
		visuals_description: z.string().default(''),
		narration_script: z.string().default(''),
		sound_description: z.string().default(''),
		edit_notes: z.string().default(''),
		scene_structure: z.string().default('')
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
		url: z.string().default(''),
		mp4Url: z.string().default(''),
		desc: z.string().default(''),
		liked: z.boolean().default(false)
	})
	.strict();

export const SfxAssetGenObj = z
	.object({
		desc: z.string().default(''),
		done: z.boolean().default(false)
	})
	.strict();

export const VideoLoading = z
  .object({
    session_id: z.string().default(''),
		scenes: z.array(SceneLoading).default([]),
		topic: z.string().default(''),
		main_font: z.string().default(''),
		secondary_font: z.string().default(''),
		full_script: z.string().default(''),
		narration_gen: z.array(NarrationGenObj).default([]),
		visual_asset_gen: z.array(VisualAssetGenObj).default([]),
		sfx_asset_gen: z.array(SfxAssetGenObj).default([]),
		generationStep: z.enum(["INPUT", "WRITING SCRIPT", "DOING TASKS", "COMPLETED"]).default("INPUT"),
		generationStepView: z.enum(["INPUT", "WRITING SCRIPT", "DOING TASKS", "COMPLETED"]).default("INPUT")
	})
	.strict();

export type VideoLoadingType = z.infer<typeof VideoLoading>;

export type SceneLoadingType = z.infer<typeof SceneLoading>;
export type AssetLoadingType = z.infer<typeof AssetLoading>;
