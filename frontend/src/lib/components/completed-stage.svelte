<script lang="ts">
	import { STATIC_API_BASE } from '$lib/utils/constants';
	import { videoState } from '$lib/stores/generation-data.svelte';
	import ScriptDisplay from './script-display.svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import { Label } from '$lib/components/ui/label';
	import { Badge } from '$lib/components/ui/badge';
	import { Input } from '$lib/components/ui/input/index.js';
	import { ChevronDown, ChevronUp, Sparkles, Wand2, Edit2, Check } from '@lucide/svelte';
	import { sendEditPrompt, selectVisual } from '$lib/utils/editing';
	import Timeline from './timeline.svelte';
	import SceneDisplay from './SceneDisplay.svelte';

	let editingMode = $state(false);
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
	let openEditPhotos = $state(false);
	let activeAsset: string = $derived(videoState.visual_asset_gen[currentIndex].mp4Url);
	let currentTime = $state(0);
	let currentScene = $state(0);
	let paused = $state(false);
</script>

<div class="mx-auto flex w-full max-w-5xl flex-col items-center gap-6 py-4">
	<div class="relative aspect-video w-4/5 rounded-xl border-1 border-dashed border-primary">
		<video
			bind:currentTime
			bind:paused
			onclick={() => paused = !paused}
			class="h-full w-full rounded-xl"
			src={`${STATIC_API_BASE}/${videoState.session_id}/final_video.mp4`}
			autoplay
		>
			<track kind="captions" />
		</video>
		<Badge variant="secondary" class="absolute top-4 left-4 gap-1 opacity-80">
			<Sparkles class="size-3" /> Final Render
		</Badge>
	</div>
	<Timeline bind:currentScene bind:currentTime bind:paused />
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
		<div class="w-full backdrop-blur-sm">
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
						<form
							onsubmit={(e) => {
								e.preventDefault();
								sendEditPrompt(editPrompt, currentScene);
							}}
							class="relative z-10"
						>
							<Input type="text" placeholder="e.g. Make the tone more exciting..." />
						</form>
					</div>
				</div>

				<div class="flex flex-grow flex-col gap-1.5">
					<Label class="text-xs text-muted-foreground uppercase">Active Clip</Label>
					<div class="relative flex-grow overflow-hidden rounded-xl border bg-black shadow-inner">
						{#key activeAsset}
							<video
								class="h-full w-full object-cover opacity-80"
								src={activeAsset}
								autoplay
								loop
								muted
							>
								<track kind="captions" />
							</video>
						{/key}
						<div class="absolute top-3 right-3">
							<Dialog.Root bind:open={openEditPhotos}>
								<Dialog.Trigger>
									<Button
										variant="secondary"
										size="icon"
										class="h-8 w-8 rounded-full opacity-50 shadow-lg hover:opacity-100"
									>
										<Edit2 class="size-4" />
									</Button>
								</Dialog.Trigger>

								<Dialog.Content class="sm:max-w-[600px]">
									<Dialog.Header>
										<Dialog.Title>Select Visual Asset</Dialog.Title>
										<Dialog.Description>
											Choose which image or clip to use for this segment of the video.
										</Dialog.Description>
									</Dialog.Header>

									<div class="grid grid-cols-3 gap-4 py-4">
										{#each videoState.visual_asset_gen as asset}
											<button
												onclick={() => {
													selectVisual({ assetId: 'idk', selectedCandidateId: 'idk' });
												}}
												class="relative aspect-video overflow-hidden rounded-md border-2 transition-all hover:ring-2 hover:ring-primary"
											>
												<video src={asset.mp4Url} class="h-full w-full object-cover">
													<track kind="captions" />
												</video>

												{#if activeAsset === asset.mp4Url}
													<div
														class="absolute inset-0 flex items-center justify-center bg-primary/20"
													>
														<Badge class="rounded-full p-1">
															<Check class="size-3" />
														</Badge>
													</div>
												{/if}
											</button>
										{/each}
									</div>

									<Dialog.Footer>
										<Button onclick={() => (openEditPhotos = false)} type="submit"
											>Confirm Selection</Button
										>
									</Dialog.Footer>
								</Dialog.Content>
							</Dialog.Root>
						</div>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
