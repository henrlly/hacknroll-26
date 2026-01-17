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
		render: z.array(CodeRenderLoading)
	})
	.strict();

export type SceneLoadingType = z.infer<typeof SceneLoading>;
export type AssetLoadingType = z.infer<typeof AssetLoading>;
