<script lang="ts">
	import ProgressFlow from '$lib/components/progress-flow.svelte';
	import PromptInput from '$lib/components/prompt-input.svelte';
	import ScriptWritingData from '$lib/components/script-writing-display.svelte';
	import DoingTasksDisplay from '$lib/components/doing-tasks-display.svelte';
	import FinalVideo from '$lib/components/completed-stage.svelte';
	import { videoState } from '$lib/stores/generation-data.svelte';
	import UnityPlayer from "$lib/components/UnityPlayer.svelte";
	
	let unityPlayer: UnityPlayer | undefined = $state();
	let unityPlayerHidden = $state(true);
	let character = $state("trump" as "trump" | "obama");
	$effect(() => {
		setTimeout(() => {
			unityPlayer?.changeBackgroundColor("#FFFFFF");
		}, 5000)
	})

	$effect(() => {
		if (videoState.generationStepView === "COMPLETED") {
			unityPlayerHidden = true;
		} else if (videoState.generationStepView === "WRITING SCRIPT") {
			unityPlayerHidden = false;
			unityPlayer?.startTyping(videoState.full_script);
		} else if (videoState.generationStepView === "DOING TASKS") {
			unityPlayerHidden = false;
			unityPlayer?.startNarration(videoState.full_script);
		} else {
			unityPlayerHidden = false;
		}
		
		if (character) {
			unityPlayer?.changeCharacter(character);
		}
	})
</script>

<div class="flex h-screen w-full flex-col items-center gap-4">
	<ProgressFlow bind:generationStep={videoState.generationStepView} />
	<div class="h-[50vh] w-[90%] rounded-3xl {unityPlayerHidden ? "hidden" : "" }">
		<UnityPlayer bind:this={unityPlayer}/>
	</div>
		{#if videoState.generationStepView === 'INPUT'}
		<PromptInput bind:character={character} />
		{:else if videoState.generationStepView === 'WRITING SCRIPT'}
		<ScriptWritingData />
		{:else if videoState.generationStepView === 'DOING TASKS'}
		<DoingTasksDisplay />
		{:else if videoState.generationStepView === 'COMPLETED'}
		<FinalVideo />
	{/if}
</div>
