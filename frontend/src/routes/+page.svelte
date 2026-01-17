<script lang="ts">
	import ProgressFlow from '$lib/components/progress-flow.svelte';
	import PromptInput from '$lib/components/prompt-input.svelte';
	import ScriptWritingData from '$lib/components/script-writing-display.svelte';
	import DoingTasksDisplay from '$lib/components/doing-tasks-display.svelte';
	import FinalVideo from '$lib/components/final-video.svelte';
	import { generationData } from '$lib/stores/generation-data.svelte';

</script>

<div class="flex h-screen w-full flex-col items-center gap-4">
	<ProgressFlow bind:generationStep={generationData.generationStep}/>

	{#if generationData.generationStep === 'INPUT'}
		<PromptInput />
	{:else if generationData.generationStep === 'WRITING SCRIPT'}
		<ScriptWritingData />
	{:else if generationData.generationStep === 'DOING TASKS'}
		<DoingTasksDisplay />
	{:else if generationData.generationStep === "COMPLETED"}
		<FinalVideo />
	{/if}
</div>
