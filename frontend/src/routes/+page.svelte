<script lang="ts">
	import ProgressFlow from '$lib/components/progress-flow.svelte';
	import PromptInput from '$lib/components/prompt-input.svelte';
	import PlanDisplay from '$lib/components/plan/plan-display.svelte';
	import ScenesDisplay from '$lib/components/scenes/ScenesDisplay.svelte';
	import FinalVideo from '$lib/components/pages/final-video.svelte';

	let generationStep = $state("INPUT" as "INPUT" | "WRITING SCRIPT" | "DOING TASKS" | "COMPLETED");
</script>

<div class="flex h-screen w-full flex-col items-center gap-4">
	<ProgressFlow {generationStep}/>

	{#if generationStep === 'INPUT'}
		<PromptInput />
	{:else if generationStep === 'WRITING SCRIPT'}
		<!-- <PlanDisplay {plan} {isLoadingPlan} /> -->
	{:else if generationStep === 'DOING TASKS'}
		<!-- <ScenesDisplay scenes={scenesObj.data} {sessionId} {isStitching} /> -->
	{:else if generationStep === "COMPLETED"}
		<!-- <FinalVideo {sessionId} /> -->
	{/if}
</div>
