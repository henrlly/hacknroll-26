import { z } from 'zod';

// Asset schema
export const AssetSchema = z.object({
  asset_id: z.string(),
  asset_type: z.enum(['visual', 'sound_effect']),
  asset_short_desc: z.string(),
  asset_long_desc: z.string(),
}).partial();
export type Asset = z.infer<typeof AssetSchema>;

// Scene schema
export const SceneSchema = z.object({
  scene_number: z.number(),
  duration_seconds: z.number(),
  visuals_description: z.string(),
  narration_script: z.string(),
  sound_description: z.string(),
  edit_notes: z.string(),
  assets_needed: z.array(AssetSchema),
  scene_structure: z.string(),
}).partial();
export type Scene = z.infer<typeof SceneSchema>;

// VideoPlan schema
export const VideoPlanSchema = z.object({
  topic: z.string(),
  main_font: z.string(),
  secondary_font: z.string(),
  scenes: z.array(SceneSchema),
}).partial();
export type VideoPlan = z.infer<typeof VideoPlanSchema>;

// ManimCodeResponse schema
export const ManimCodeResponseSchema = z.object({
  code: z.string(),
});
export type ManimCodeResponse = z.infer<typeof ManimCodeResponseSchema>;

// VisualChoiceResponse schema
export const VisualChoiceResponseSchema = z.object({
  selected_image_indexes: z.array(z.number()),
});
export type VisualChoiceResponse = z.infer<typeof VisualChoiceResponseSchema>;
