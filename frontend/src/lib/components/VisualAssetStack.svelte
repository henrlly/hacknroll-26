<script lang="ts">
	import type { SceneLoadingType, AssetLoadingType } from '$lib/types/sceneTypes';
	import { STATIC_API_BASE } from '$lib/utils/constants';
	import { videoState } from '$lib/stores/generation-data.svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { Badge } from '$lib/components/ui/badge';
	import { Play, Pause, Check } from '@lucide/svelte';
	import { selectVisual } from '$lib/utils/editing';

	interface Props {
		scene: SceneLoadingType;
		setTouched: () => void;
	}

	let { scene, setTouched }: Props = $props();

	let dialogOpen = $state(false);
	let playingVideos = $state(new Set<string>());
	let loadingVideos = $state(new Set<string>());
	let errorVideos = $state(new Set<string>());

	// Filter visual assets only
	const visualAssets = $derived(
		scene.assets.filter(
			(asset): asset is Extract<AssetLoadingType, { type: 'visual' }> => asset.type === 'visual'
		)
	);

	// Get video URL for an asset candidate
	function getVideoUrl(assetId: string, candidateId: string): string {
		return `${STATIC_API_BASE}/${videoState.session_id}/${assetId}/${candidateId}.mp4`;
	}

	// Handle video play/pause
	function toggleVideo(videoId: string) {
		const video = document.getElementById(videoId) as HTMLVideoElement;
		if (video) {
			if (video.paused) {
				video.play();
				playingVideos.add(videoId);
			} else {
				video.pause();
				playingVideos.delete(videoId);
			}
			playingVideos = new Set(playingVideos);
		}
	}

	// Handle video loading states
	function handleVideoLoadStart(videoId: string) {
		loadingVideos.add(videoId);
		loadingVideos = new Set(loadingVideos);
		errorVideos.delete(videoId);
		errorVideos = new Set(errorVideos);
	}

	function handleVideoCanPlay(videoId: string) {
		loadingVideos.delete(videoId);
		loadingVideos = new Set(loadingVideos);
	}

	function handleVideoError(videoId: string) {
		loadingVideos.delete(videoId);
		errorVideos.add(videoId);
		loadingVideos = new Set(loadingVideos);
		errorVideos = new Set(errorVideos);
	}

	// Handle asset selection in dialog
	function handleAssetSelection(assetId: string, candidateId: string) {
		selectVisual({ assetId, selectedCandidateId: candidateId });
		dialogOpen = false;
		setTouched();
	}

	// Open dialog with selected asset
	function openAssetDialog(assetId: string) {
		dialogOpen = true;
	}

	// Get the final selected candidate for an asset
	function getFinalSelectedCandidate(asset: Extract<AssetLoadingType, { type: 'visual' }>) {
		return asset.candidates.find((c) => c.finalSelected) || asset.candidates[0];
	}

	// Get stack offset based on index
	function getStackOffset(index: number, total: number) {
		const maxOffset = Math.min(total - 1, 3) * 4; // Max 3 visible cards with 4px offset each
		return Math.min(index, 3) * 4;
	}
</script>

<!-- Main Stack Display -->
<div class="relative">
	{#if visualAssets.length > 0}
		<!-- Container with proper padding to accommodate stack offset -->
		<div
			class="relative cursor-pointer"
			onclick={() => openAssetDialog(visualAssets[0].assetId)}
			style="padding-right: {Math.min(visualAssets.length - 1, 3) * 4}px; padding-bottom: {Math.min(
				visualAssets.length - 1,
				3
			) * 4}px;"
		>
			<!-- Base container to establish proper height -->
			<div class="aspect-video w-full">
				{#each visualAssets.slice(0, 4) as asset, index}
					{@const finalCandidate = getFinalSelectedCandidate(asset)}
					{#if finalCandidate}
						<div
							class="rounded-lg border-2 border-gray-200 bg-white shadow-md transition-transform hover:scale-105 {index ===
							0
								? 'relative'
								: 'absolute top-0 left-0'}"
							style="transform: translate({getStackOffset(
								index,
								visualAssets.length
							)}px, -{getStackOffset(
								index,
								visualAssets.length
							)}px); z-index: {visualAssets.length - index}; width: calc(100% - {Math.min(
								visualAssets.length - 1,
								3
							) * 4}px);"
						>
							<div class="aspect-video w-full overflow-hidden rounded-lg">
								<video
									class="h-full w-full object-cover"
									src={getVideoUrl(asset.assetId, finalCandidate.candidateId)}
									muted
									loop
									autoplay
									onerror={() => {
										console.warn(
											`Failed to load video: ${asset.assetId}/${finalCandidate.candidateId}`
										);
									}}
								>
									<track kind="captions" />
								</video>
							</div>
						</div>
					{/if}
				{/each}

				{#if visualAssets.length > 4}
					<div
						class="absolute right-2 bottom-2 rounded-full bg-black/70 px-2 py-1 text-xs text-white"
						style="z-index: {visualAssets.length + 1};"
					>
						+{visualAssets.length - 4}
					</div>
				{/if}
			</div>
		</div>
	{:else}
		<div
			class="flex aspect-video w-full items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50"
		>
			<p class="text-gray-500">No visual assets available</p>
		</div>
	{/if}
</div>

<!-- Selection Dialog -->
<Dialog.Root bind:open={dialogOpen}>
	<Dialog.Content class="max-w-6xl">
		<Dialog.Header>
			<Dialog.Title>Select Visual Asset</Dialog.Title>
			<Dialog.Description>
				Choose from the available candidates for each visual asset in this scene.
			</Dialog.Description>
		</Dialog.Header>

		<ScrollArea class="max-h-[80vh]">
			<div class="space-y-6 p-4">
				{#each visualAssets as asset}
					<Card>
						<CardContent class="p-6">
							<div class="mb-4">
								<h3 class="text-lg font-semibold">{asset.assetShortDesc}</h3>
								<p class="text-sm text-gray-600">{asset.assetLongDesc}</p>
								<Badge variant="secondary" class="mt-2">{asset.state}</Badge>
							</div>

							<ScrollArea class="w-full whitespace-nowrap">
								<div class="flex gap-4 pb-4">
									{#each asset.candidates as candidate}
										{@const videoId = `video-${asset.assetId}-${candidate.candidateId}`}
										{@const isPlaying = playingVideos.has(videoId)}
										{@const isLoading = loadingVideos.has(videoId)}
										{@const hasError = errorVideos.has(videoId)}

										<div class="relative min-w-50">
											<Card
												class="cursor-pointer transition-all hover:ring-2 hover:ring-primary {candidate.finalSelected
													? 'ring-2 ring-green-500'
													: ''}"
												onclick={() => handleAssetSelection(asset.assetId, candidate.candidateId)}
											>
												<CardContent class="p-0">
													<div class="relative aspect-video">
														<video
															id={videoId}
															class="h-full w-full rounded-t-lg object-cover"
															src={getVideoUrl(asset.assetId, candidate.candidateId)}
															muted
															loop
															onloadstart={() => handleVideoLoadStart(videoId)}
															oncanplay={() => handleVideoCanPlay(videoId)}
															onerror={() => handleVideoError(videoId)}
														>
															<track kind="captions" />
														</video>

														<!-- Loading State -->
														{#if isLoading}
															<div
																class="absolute inset-0 flex items-center justify-center bg-black/50"
															>
																<div
																	class="h-6 w-6 animate-spin rounded-full border-2 border-white border-t-transparent"
																></div>
															</div>
														{/if}

														<!-- Error State -->
														{#if hasError}
															<div
																class="absolute inset-0 flex items-center justify-center bg-red-500/20"
															>
																<p class="text-xs text-red-600">Failed to load</p>
															</div>
														{/if}

														<!-- Play/Pause Overlay -->
														{#if !isLoading && !hasError}
															<div
																class="absolute inset-0 flex items-center justify-center bg-black/20 opacity-0 transition-opacity hover:opacity-100"
																onclick={(e) => {
																	e.stopPropagation();
																	toggleVideo(videoId);
																}}
															>
																<Button size="icon" variant="secondary" class="rounded-full">
																	{#if isPlaying}
																		<Pause class="h-4 w-4" />
																	{:else}
																		<Play class="h-4 w-4" />
																	{/if}
																</Button>
															</div>
														{/if}

														<!-- Selection Indicator -->
														{#if candidate.finalSelected}
															<div class="absolute right-2 bottom-2">
																<Badge variant="default" class="bg-green-500">
																	<Check class="mr-1 h-3 w-3" />
																	Selected
																</Badge>
															</div>
														{/if}
													</div>
												</CardContent>
											</Card>
										</div>
									{/each}
								</div>
							</ScrollArea>
						</CardContent>
					</Card>
				{/each}
			</div>
		</ScrollArea>

		<Dialog.Footer>
			<Button variant="outline" onclick={() => (dialogOpen = false)}>Close</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>

<style>
	/* Ensure videos don't interfere with click events when stacked */
	video {
		pointer-events: none;
	}

	.cursor-pointer video {
		pointer-events: auto;
	}
</style>
