import { z } from 'zod';

// Asset schema
export const AssetSchema = z.object({
  asset_id: z.string().catch(''),
  asset_type: z.enum(['visual', 'sound_effect']).catch('visual'),
  asset_short_desc: z.string().catch(''),
  asset_long_desc: z.string().catch(''),
}).partial();
export type Asset = z.infer<typeof AssetSchema>;

// Scene schema
export const SceneSchema = z.object({
  scene_number: z.number().catch(0),
  duration_seconds: z.number().catch(0),
  visuals_description: z.string().catch(''),
  narration_script: z.string().catch(''),
  sound_description: z.string().catch(''),
  edit_notes: z.string().catch(''),
  scene_structure: z.string().catch(''),
  assets_needed: z.array(AssetSchema).catch([]),
}).partial();
export type Scene = z.infer<typeof SceneSchema>;

// VideoPlan schema
export const VideoPlanSchema = z.object({
  topic: z.string().catch(''),
  main_font: z.string().catch(''),
  secondary_font: z.string().catch(''),
  scenes: z.array(SceneSchema).catch([]),
}).partial();
export type VideoPlan = z.infer<typeof VideoPlanSchema>;
