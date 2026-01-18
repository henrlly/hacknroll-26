<script lang="ts">
	import ProgressFlow from '$lib/components/progress-flow.svelte';
	import PromptInput from '$lib/components/prompt-input.svelte';
	import ScriptWritingData from '$lib/components/script-writing-display.svelte';
	import DoingTasksDisplay from '$lib/components/doing-tasks-display.svelte';
	import FinalVideo from '$lib/components/completed-stage.svelte';
	import { videoState } from '$lib/stores/generation-data.svelte';
	import UnityPlayer from '$lib/components/UnityPlayer.svelte';

	let unityPlayer: UnityPlayer | undefined = $state();
	let unityPlayerHidden = $state(true);
	let character: 'trump' | 'obama' | undefined = $state('trump');
	let loading = $state(true);
	let isUnityLoaded = $state(false);
	$inspect(loading);
	$effect(() => {
		setTimeout(() => {
			unityPlayer?.changeBackgroundColor('#FFFFFF');
			loading = false;
		}, 4000);
	});

	let completed_index = 0;

	$effect(() => {
		if (videoState.generationStepView === 'COMPLETED') {
			unityPlayerHidden = true;
		} else if (videoState.generationStepView === 'WRITING SCRIPT') {
			unityPlayerHidden = false;
			let nextPeriod = videoState.full_script.indexOf('.', completed_index);
			if (nextPeriod !== -1) {
				const slice = videoState.full_script.slice(completed_index, nextPeriod);
				unityPlayer?.startTyping(slice);
				completed_index = nextPeriod + 1;
			}
		} else if (videoState.generationStepView === 'DOING TASKS') {
			unityPlayerHidden = false;
			unityPlayer?.startNarration(videoState.full_script);
			if (videoState.sfx_asset_gen.length === 0) {
				unityPlayer?.startSfx("")
			} else {
				let i = 0;
				setInterval(() => {
					unityPlayer?.startSfx(videoState.sfx_asset_gen[i % videoState.sfx_asset_gen.length].desc);
					i++;
				}, 2000);
			}
			unityPlayer?.startScrolling(JSON.stringify(videoState.visual_asset_gen))
		} else {
			unityPlayerHidden = false;
			// unityPlayer.stopEverything
		}
	});

	$effect(() => {
		if (character && isUnityLoaded) {
			unityPlayer?.changeCharacter(character);
		}
	});
</script>

<div class="flex h-screen w-full flex-col items-center">
	<div class="max-w-8xl flex h-screen w-full flex-col items-center gap-4">
		<ProgressFlow bind:generationStep={videoState.generationStepView} />
		<div class="relative aspect-video w-3/5 overflow-hidden rounded-3xl">
			<div class="h-full w-full scale-125">
				<UnityPlayer bind:this={unityPlayer} bind:isUnityLoaded />
			</div>
		</div>
		{#if videoState.generationStepView === 'INPUT'}
			<PromptInput class={loading ? 'cursor-wait' : ''} bind:voice={character} />
		{:else if videoState.generationStepView === 'WRITING SCRIPT'}
			<ScriptWritingData />
		{:else if videoState.generationStepView === 'DOING TASKS'}
			<DoingTasksDisplay />
		{:else if videoState.generationStepView === 'COMPLETED'}
			<FinalVideo />
		{/if}
	</div>
</div>
