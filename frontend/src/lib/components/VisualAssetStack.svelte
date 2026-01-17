<script lang="ts">
	import type { SceneLoadingType, AssetLoadingType } from '$lib/types/sceneTypes';
	import { STATIC_API_BASE } from '$lib/utils/constants';
	import { videoState } from '$lib/stores/generation-data.svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { Badge } from '$lib/components/ui/badge';
	import { Check } from '@lucide/svelte';
	import { selectVisual } from '$lib/utils/editing';

	interface Props {
		scene: SceneLoadingType;
		setTouched: () => void;
	}

	let { scene, setTouched }: Props = $props();

	let dialogOpen = $state(false);

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

	// Handle asset selection in dialog
	function handleAssetSelection(assetId: string, candidateId: string) {
		selectVisual({ assetId, selectedCandidateId: candidateId });
		dialogOpen = false;
		setTouched();
	}

	// Get the final selected candidate for an asset
	function getFinalSelectedCandidate(asset: Extract<AssetLoadingType, { type: 'visual' }>) {
		return asset.candidates.find((c) => c.finalSelected) || asset.candidates[0];
	}
</script>

<!-- Main Stack Display -->
<div class="relative w-full">
	{#if visualAssets.length > 0}
		<div class="group relative cursor-pointer" onclick={() => (dialogOpen = true)}>
			<!-- Stack container with fixed spacing -->
			<div class="relative aspect-video w-full pr-3 pb-3">
				{#each visualAssets.slice(0, 4) as asset, index}
					{@const finalCandidate = getFinalSelectedCandidate(asset)}
					{#if finalCandidate}
						<div
							class="absolute inset-0 rounded-lg border-2 border-gray-200 bg-white shadow-sm transition-all duration-200 group-hover:shadow-lg"
							style="
								transform: translate({index * 3}px, {index * -3}px);
								z-index: {10 - index};
								right: {index * 3}px;
								bottom: {index * 3}px;
							"
						>
							<div class="aspect-video w-full overflow-hidden rounded-lg">
								<video
									class="h-full w-full object-cover"
									src={getVideoUrl(asset.assetId, finalCandidate.candidateId)}
									muted
									loop
									autoplay
									playsinline
								>
									<track kind="captions" />
								</video>
							</div>
						</div>
					{/if}
				{/each}

				<!-- Count badge for additional assets -->
				{#if visualAssets.length > 4}
					<div
						class="absolute top-2 right-2 rounded-full bg-black/80 px-2 py-1 text-xs font-medium text-white"
						style="z-index: 15;"
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
			<p class="text-sm text-gray-500">No visual assets available</p>
		</div>
	{/if}
</div>

<!-- Selection Dialog -->
<Dialog.Root bind:open={dialogOpen}>
	<Dialog.Content class="max-h-[90vh] w-full max-w-full">
		<Dialog.Header>
			<Dialog.Title>Select Visual Asset</Dialog.Title>
			<Dialog.Description>
				Choose from the available candidates for each visual asset in this scene.
			</Dialog.Description>
		</Dialog.Header>

		<ScrollArea class="max-h-[70vh]">
			<div class="space-y-6 p-4">
				{#each visualAssets as asset}
					<Card>
						<CardContent class="p-4">
							<div class="mb-4 min-w-0">
								<h3 class="text-lg font-semibold break-words">{asset.assetShortDesc}</h3>
								<p class="overflow-wrap-anywhere mt-1 text-sm break-words text-gray-600">
									{asset.assetLongDesc}
								</p>
								<Badge variant="secondary" class="mt-2">{asset.state}</Badge>
							</div>

							<div class="w-full overflow-hidden">
								<ScrollArea class="max-w-full" orientation="horizontal">
									<div class="flex gap-3 pb-4">
										{#each asset.candidates as candidate}
											{@const videoId = `video-${asset.assetId}-${candidate.candidateId}`}

											<div class="w-40 flex-shrink-0">
												<Card
													class="cursor-pointer transition-all hover:ring-2 hover:ring-blue-500 {candidate.finalSelected
														? 'bg-green-50 ring-2 ring-green-500'
														: ''}"
													onclick={() => handleAssetSelection(asset.assetId, candidate.candidateId)}
												>
													<CardContent class="p-0">
														<div class="relative aspect-video">
															<video
																id={videoId}
																class="h-full w-full rounded-lg object-cover"
																src={getVideoUrl(asset.assetId, candidate.candidateId)}
																muted
																loop
																autoplay
																playsinline
															>
																<track kind="captions" />
															</video>

															<!-- Selection indicator -->
															{#if candidate.finalSelected}
																<div class="absolute top-2 right-2">
																	<Badge class="bg-green-500 text-white hover:bg-green-600">
																		<Check class="mr-1 h-3 w-3" />
																		Selected
																	</Badge>
																</div>
															{/if}
														</div>

														<!-- Candidate info -->
														<div class="min-w-0 p-3">
															<p class="truncate text-xs text-gray-600">
																Candidate {candidate.candidateId}
															</p>
														</div>
													</CardContent>
												</Card>
											</div>
										{/each}
									</div>
								</ScrollArea>
							</div>
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
	/* Prevent video controls from interfering with click events */
	video {
		pointer-events: none;
	}
</style>
