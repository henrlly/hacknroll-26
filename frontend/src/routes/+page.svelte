<script lang="ts">
	import ProgressFlow from '$lib/components/progress-flow.svelte';
	import PromptInput from '$lib/components/prompt-input.svelte';
	import ScriptWritingData from '$lib/components/script-writing-display.svelte';
	import DoingTasksDisplay from '$lib/components/doing-tasks-display.svelte';
	import FinalVideo from '$lib/components/final-video.svelte';

	let generationStepView = $state("INPUT")
</script>

<div class="flex h-screen w-full flex-col items-center gap-4">
	<ProgressFlow bind:generationStep={generationStepView}/>

	{#if generationStepView === 'INPUT'}
		<PromptInput />
	{:else if generationStepView === 'WRITING SCRIPT'}
		<ScriptWritingData />
	{:else if generationStepView === 'DOING TASKS'}
		<DoingTasksDisplay />
	{:else if generationStepView === "COMPLETED"}
		<FinalVideo />
	{/if}
</div>
