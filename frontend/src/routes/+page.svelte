<script lang="ts">
	import ProgressFlow from '$lib/components/progress-flow.svelte';
	import PromptInput from '$lib/components/prompt-input.svelte';
	import ScriptWritingData from '$lib/components/script-writing-display.svelte';
	import DoingTasksDisplay from '$lib/components/doing-tasks-display.svelte';
	import FinalVideo from '$lib/components/completed-stage.svelte';
	import { videoState } from '$lib/stores/generation-data.svelte';
</script>

<div class="flex h-screen w-full flex-col items-center gap-4">
	{#if videoState.completed}{:else}
		<ProgressFlow bind:generationStep={videoState.generationStepView} />

		{#if videoState.generationStepView === 'INPUT'}
			<PromptInput />
		{:else if videoState.generationStepView === 'WRITING SCRIPT'}
			<ScriptWritingData />
		{:else if videoState.generationStepView === 'DOING TASKS'}
			<DoingTasksDisplay />
		{:else if videoState.generationStepView === 'COMPLETED'}
			<FinalVideo />
		{/if}
	{/if}
</div>
