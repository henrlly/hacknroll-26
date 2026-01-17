import { z } from 'zod';

export const voices = ['trump', 'peter', 'obama'] as const;

export const VoiceSchema = z.enum(voices);
export const PromptSchema = z.string().min(1);

export type VoiceType = z.infer<typeof VoiceSchema>;
export type PromptType = z.infer<typeof PromptSchema>;

export const UserRequest = z.object({
	prompt: PromptSchema,
	voice: VoiceSchema
});

export type UserRequestType = z.infer<typeof UserRequest>;

export const StartPipelineResponse = z.object({
	type: z.literal('start'),
	session_id: z.string(),
	success: z.boolean()
});

export const PlanStreamedResponse = z.object({
	type: z.literal('plan'),
	event_type: z.enum(['plan_start', 'plan_stream', 'plan_end']),
	delta: z.string().nullish()
});

export const AssetResponse = z.object({
	type: z.literal('asset'),
	event_type: z.enum(['generation_start', 'generation_end']),
	asset_id: z.string(),
	asset_type: z.enum(['visual', 'sound_effect']),
	candidate_id: z.string().nullish()
});

export const AssetSelectionResponse = z.object({
	type: z.literal('asset_selection'),
	event_type: z.enum(['selection_start', 'selection_end']),
	asset_id: z.string(),
	asset_type: z.literal('visual'),
	selected_candidate_ids: z.array(z.string()).nullish(),
	selected_candidate_id: z.string().nullish()
});

export const NarrationResponse = z.object({
	type: z.literal('narration'),
	event_type: z.enum(['narration_generation_start', 'narration_generation_end']),
	scene_number: z.number()
});

export const ManimCodeGenerationResponse = z.object({
	type: z.literal('code_generation'),
	event_type: z.enum(['code_generation_start', 'code_generation_end']),
	scene_number: z.number(),
	version_number: z.number(),
	retry_number: z.number().default(0),
	success: z.boolean().nullish()
});

export const ManimCodeRendingResponse = z.object({
	type: z.literal('code_rendering'),
	event_type: z.enum(['rendering_start', 'rendering_end']),
	scene_number: z.number(),
	version_number: z.number(),
	retry_number: z.number().default(0),
	success: z.boolean(),
	error_message: z.literal('cancelled').nullish()
});

export const ManimCodeRendingSelectionResponse = z.object({
	type: z.literal('code_rendering_selection'),
	scene_number: z.number(),
	version_number: z.number()
});

export const FinalVideoResponse = z.object({
	type: z.literal('final_video'),
	event_type: z.enum(['stitching_start', 'stitching_end']),
	success: z.boolean().nullish(),
	error_message: z.string().nullish()
});

export const SceneStreamedResponse = z.object({
  type: z.literal('scene'),
  event_type: z.enum(["scene_start", "scene_stream", "scene_end"]),
  delta: z.string()
})

export const SelectImageResponse = z.object({
  type: z.literal('select_image'),
  success: z.boolean(),
})

export const StreamResponse = z.union([
	StartPipelineResponse,
	PlanStreamedResponse,
	AssetResponse,
	AssetSelectionResponse,
	NarrationResponse,
	ManimCodeGenerationResponse,
	ManimCodeRendingResponse,
	ManimCodeRendingSelectionResponse,
  FinalVideoResponse,
  SceneStreamedResponse,
  SelectImageResponse
]);

export const SceneResponse = z.union([
	AssetResponse,
	AssetSelectionResponse,
	NarrationResponse,
	ManimCodeGenerationResponse,
	ManimCodeRendingResponse,
	ManimCodeRendingSelectionResponse
]);

export type SceneResponseType = z.infer<typeof SceneResponse>;

export type PlanStreamedResponseType = z.infer<typeof PlanStreamedResponse>;

export type StreamResponseType = z.infer<typeof StreamResponse>;

export const EditSceneRequest = z.object({
	type: z.literal('edit_scene_request').default('edit_scene_request'),
	edit_prompt_type: z.enum(['funny', 'detailed', 'pictures']).optional(),
	custom_edit_prompt: z.string().optional(),
	scene_number: z.number()
});

export const SelectImageRequest = z.object({
	type: z.literal('select_image_request').default('select_image_request'),
	asset_id: z.string(),
	selected_candidate_id: z.string()
});
