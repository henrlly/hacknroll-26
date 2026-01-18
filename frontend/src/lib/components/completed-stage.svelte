<script lang="ts">
	import { STATIC_API_BASE } from '$lib/utils/constants';
	import { videoState } from '$lib/stores/generation-data.svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import { Label } from '$lib/components/ui/label';
	import { Badge } from '$lib/components/ui/badge';
	import { Input } from '$lib/components/ui/input/index.js';
	import { ChevronDown, ChevronUp, Sparkles, Wand2, Edit2, Check } from '@lucide/svelte';
	import {
		sendEditPrompt,
		selectVisual,
		sendRenderAndStitch,
		sendMakeScene
	} from '$lib/utils/editing';
	import Timeline from './timeline.svelte';
	import SceneDisplay from './SceneDisplay.svelte';
	import VisualAssetStack from './VisualAssetStack.svelte';

	let editingMode = $state(true);
	let currentIndex = $state(0);
	$effect(() => {
		if (editingMode && videoState.visual_asset_gen.length > 1) {
			const interval = setInterval(() => {
				currentIndex = (currentIndex + 1) % videoState.visual_asset_gen.length;
			}, 2000);

			return () => clearInterval(interval);
		}
	});

	let editPrompt = $state('');
	let currentScene = $state(0);
	let currentTime = $state(0);
	let paused = $state(false);
	let planRegened = $state(false);
	let src = $state(`${STATIC_API_BASE}/${videoState.session_id}/final_video.mp4`);

	let sceneEnableRending = $state<Record<number, boolean>>({});

	function handleSubmitPrompt(e: Event) {
		e.preventDefault();
		if (!editPrompt.trim()) return;

		try {
			sendEditPrompt(editPrompt, currentScene);
			editPrompt = ''; 
			planRegened = true;
			sceneEnableRending[currentScene] = true;
		} catch (err) {
			console.error('Failed to send edit:', err);
		}
	}
	function handleSubmitRender() {
		try {
			if (planRegened) {
				sendMakeScene(currentScene);
			}
			sendRenderAndStitch(currentScene);
			sceneEnableRending[currentScene] = false;
			// refresh video src
			src = '';
			src = `${STATIC_API_BASE}/${videoState.session_id}/final_video.mp4`;
		} catch (err) {
			console.error('Failed to send edit:', err);
		}
	}

	const setTouched = () => (sceneEnableRending[currentScene] = true);

	let videoElement: HTMLVideoElement | null = $state(null);
	function handleKeyDown(e: KeyboardEvent) {
		if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) {
			return;
		}

		if (!videoElement) return;

		const frameTime = 1 / 24;

		switch (e.code) {
			case 'KeyK':
			case 'Space':
				e.preventDefault(); // Stop page from scrolling down
				if (videoElement.paused) {
					videoElement.play();
				} else {
					videoElement.pause();
				}
				break;
			case 'KeyL':
			case 'ArrowRight':
				e.preventDefault();
				videoElement.currentTime += 4;
				break;
			case 'KeyJ':
			case 'ArrowLeft':
				e.preventDefault();
				videoElement.currentTime -= 4;
				break;
			case 'Period':
				e.preventDefault();
				videoElement.pause();
				videoElement.currentTime += frameTime;
				break;

			case 'Comma':
				e.preventDefault();
				videoElement.pause();
				videoElement.currentTime -= frameTime;
				break;
		}
	}
</script>

<svelte:window onkeydown={handleKeyDown} />

<div class="mx-auto flex w-full flex-col items-center gap-6 py-4">
	<div class="relative aspect-video w-3/5 rounded-xl border-1 border-dashed border-primary">
		<video
			bind:currentTime
			bind:paused
			bind:this={videoElement}
			onclick={() => (paused = !paused)}
			class="h-full w-full rounded-xl"
			{src}
			autoplay
			controls
		>
			<track kind="captions" />
		</video>
		<Badge variant="secondary" class="absolute top-4 left-4 gap-1 opacity-80">
			<Sparkles class="size-3" /> Final Render
		</Badge>
	</div>
	<!-- <Timeline bind:currentScene bind:currentTime bind:paused /> -->
	<div class="flex w-4/5 items-center justify-between px-2">
		<div class="flex flex-col">
			<h3 class="text-sm font-medium tracking-wider text-muted-foreground uppercase">
				Project Workspace
			</h3>
			<p class="text-xs text-muted-foreground/60">Session: {videoState.session_id}</p>
		</div>

		<Button
			variant="outline"
			size="sm"
			class={'gap-2 transition-all'}
			onclick={() => (editingMode = !editingMode)}
		>
			{#if !editingMode}
				<Wand2 class="size-4" />
			{/if}
			{editingMode ? 'Close Editor' : 'Refine Script'}
			{#if editingMode}
				<ChevronUp class="size-4" />
			{:else}
				<ChevronDown class="size-4" />
			{/if}
		</Button>
	</div>

	{#if editingMode}
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div class="w-full backdrop-blur-sm" onclick={() => (paused = true)}>
			<div class="flex h-full w-full gap-6 p-6">
				<div class="flex w-[60%] shrink-0 flex-col gap-4">
					<div class="flex flex-col gap-1.5">
						<Label class="text-xs text-muted-foreground uppercase">Video Script</Label>
						<div class="rounded-md">
							<SceneDisplay scene={videoState.scenes[currentScene]} />
						</div>
					</div>

					<div class="flex h-1/2 flex-col gap-1.5">
						<Label class="text-xs text-muted-foreground uppercase">Adjust Prompt</Label>
						<form onsubmit={handleSubmitPrompt} class="relative z-10">
							<Input
								type="text"
								placeholder="e.g. Make the tone more exciting..."
								bind:value={editPrompt}
							/>
						</form>
						<Button type="submit" class="mt-2" onclick={handleSubmitPrompt}>
							<Edit2 class="mr-2 size-4" />
							Regenerate Plan
						</Button>
					</div>
				</div>

				<div class="flex flex-grow flex-col gap-1.5">
					<div>
						<VisualAssetStack scene={videoState.scenes[currentScene]} {setTouched} />
					</div>

					<Button
						class="mt-2"
						onclick={handleSubmitRender}
						disabled={!sceneEnableRending[currentScene]}
					>
						<Edit2 class="mr-2 size-4" />
						Rerender Video
					</Button>
				</div>
			</div>
		</div>
	{/if}
</div>
