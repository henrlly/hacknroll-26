<script lang="ts">
	import { videoState } from "$lib/stores/generation-data.svelte";

	let taskDone = $derived(videoState.generationStep === "COMPLETED" || videoState.generationStep === "DOING TASKS");

</script>

<div class="flex flex-col justify-center items-center w-full gap-6">
	{#if taskDone}
	<p>Script done!</p>
	{:else}
	<p>Writing script...</p>
	{/if}
</div>
