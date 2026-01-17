<script lang="ts">
	import { videoState } from "$lib/stores/generation-data.svelte";

	let voiceoverDone = $derived(false);
	let gifsDone = $derived(false);
	let sfxDone = $derived(false);
</script>

<div class="w-full grid grid-cols-3 text-center gap-4 p-4">
	<div class="flex flex-col justify-between">
		<!-- <p>{JSON.stringify(videoState.narration_gen)}</p> -->
		<p>Recording Voiceover...</p>
	</div>
	<div class="flex flex-col justify-between">
		<!-- <p class="overflow-auto">{JSON.stringify(videoState.visual_asset_gen)}</p> -->
		<p>Picking GIFs...</p>
	</div>
	<div class="flex flex-col justify-between">
		<!-- <p>{JSON.stringify(videoState.sfx_asset_gen)}</p> -->
		<p>Recording SFXs...</p>
	</div>
</div>