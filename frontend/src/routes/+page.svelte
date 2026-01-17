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
	let character : "trump" | "obama" | undefined = $state("trump");
	let loading = $state(true);
	let isUnityLoaded = $state(false);
	$inspect(loading)
	$effect(() => {
		setTimeout(() => {
			unityPlayer?.changeBackgroundColor("#FFFFFF");
			loading = false;
		}, 4000)

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
			// unityPlayer.stopEverything
		}
	});

	$effect(() => {
		if (character && isUnityLoaded) {
			unityPlayer?.changeCharacter(character);
		}
	})
</script>
<div class="flex h-screen w-full flex-col items-center ">
	<div class="flex h-screen w-full max-w-8xl flex-col items-center gap-4">
		<ProgressFlow bind:generationStep={videoState.generationStepView} />
		<div class={["aspect-video w-4/5 rounded-3xl", unityPlayerHidden ? "hidden" : ""]}>
			<UnityPlayer bind:this={unityPlayer} bind:isUnityLoaded={isUnityLoaded}/>
		</div>
			{#if videoState.generationStepView === 'INPUT'}
			<PromptInput class={loading ? "cursor-wait" : ""} bind:voice={character} />
			{:else if videoState.generationStepView === 'WRITING SCRIPT'}
			<ScriptWritingData />
			{:else if videoState.generationStepView === 'DOING TASKS'}
			<DoingTasksDisplay />
			{:else if videoState.generationStepView === 'COMPLETED'}
			<FinalVideo />
		{/if}
	</div>
</div>
