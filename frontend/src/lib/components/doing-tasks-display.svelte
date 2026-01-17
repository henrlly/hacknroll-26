<script lang="ts">
	import { videoState } from "$lib/stores/generation-data.svelte";

	let voiceoverDone = $derived(!videoState.narration_gen.some(narration => !narration.done));
	let gifsDone = $derived(videoState.generationStep === "COMPLETED");
	let sfxDone = $derived(videoState.generationStep === "COMPLETED");
</script>

<div class="w-full grid grid-cols-3 text-center gap-4 p-4">
	<div class="flex flex-col justify-between">
		<!-- <p>{JSON.stringify(videoState.narration_gen)}</p> -->
		{#if voiceoverDone}
		<p>Voiceover recorded!</p>
		{:else}
		<p>Recording Voiceover...</p>
		{/if}
	</div>
	<div class="flex flex-col justify-between">
		<!-- <p class="overflow-auto">{JSON.stringify(videoState.visual_asset_gen)}</p> -->
		{#if gifsDone}
		<p>GIFs picked!</p>
		{:else}
		<p>Picking GIFs...</p>
		{/if}
	</div>
	<div class="flex flex-col justify-between">
		<!-- <p>{JSON.stringify(videoState.sfx_asset_gen)}</p> -->
		{#if sfxDone}
		<p>Sax performance ended</p>
		{:else}
		<p>Recording SFXs...</p>
		{/if}
	</div>
</div>