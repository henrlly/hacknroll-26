<script lang="ts">
	import { type SceneLoadingType } from '$lib/types/sceneTypes';
	import { STATIC_API_BASE } from '$lib/utils/constants';
	import { onMount } from 'svelte';

	let { scenes, sessionId, isStitching } = $props<{
		scenes: SceneLoadingType[];
		sessionId: string;
		isStitching: boolean;
	}>();

	// TODO: change to version a version b instead of v0 v1

	// TODO: colors for python code

	// Store fetched Python code
	let pythonCode: Record<string, string> = {};
	// map a state to a small color class (using utility classes, but keep generic fallbacks)
	function stateClass(state: string) {
		switch (state) {
			case 'not_started':
				return 'bg-gray-200 text-gray-800';
			case 'generating':
			case 'rendering':
			case 'selecting':
				return 'bg-yellow-100 text-yellow-800';
			case 'done':
				return 'bg-green-100 text-green-800';
			default:
				return 'bg-gray-100 text-gray-800';
		}
	}

	function assetTypeLabel(a: any) {
		return a.type === 'visual' ? 'Visual' : a.type === 'sound_effect' ? 'SFX' : String(a.type);
	}

	// small helper to show a short id
	function shortId(id?: string) {
		if (!id) return '';
		return id.length > 8 ? id.slice(0, 8) + '…' : id;
	}

	// Fetch Python code for a specific scene and version
	async function fetchPythonCode(sceneIndex: number, versionIndex: number): Promise<string> {
		const cacheKey = `${sceneIndex}_${versionIndex}`;
		if (pythonCode[cacheKey]) {
			return pythonCode[cacheKey];
		}

		try {
			const url = `${STATIC_API_BASE}/${sessionId}/scene_${sceneIndex}_${versionIndex}.py`;
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error(`Failed to fetch: ${response.status}`);
			}
			const code = await response.text();
			pythonCode[cacheKey] = code;
			return code;
		} catch (error) {
			console.error('Error fetching Python code:', error);
			return `# Error loading code: ${error}`;
		}
	}

	// ensure component updates when underlying arrays are mutated by parent
	// (no-op, but keeps a dev hook if needed)
	onMount(() => {
		// placeholder for potential debugging
	});
</script>

<div class="mx-auto flex w-full max-w-4xl flex-col gap-4 p-4">
	{#if isStitching}
		<div class="flex items-center gap-3 rounded-lg border border-blue-300 bg-blue-100 p-4">
			<div class="text-2xl">🔗</div>
			<div>
				<div class="font-semibold text-blue-900">Video Stitching in Progress</div>
				<div class="text-sm text-blue-700">Combining scenes into final video...</div>
			</div>
		</div>
	{/if}

	{#if !scenes || scenes.length === 0}
		<div class="meta text-center">No scenes to display</div>
	{:else}
		{#each scenes as scene}
			<div class="scene-card">
				<div class="flex items-start justify-between gap-4">
					<div>
						<div class="flex items-baseline gap-3">
							<h3 class="text-lg font-semibold">Scene {scene.scene_number + 1}</h3>
							<!-- <div class="meta">index: {idx}</div> -->
						</div>
						<div class="meta mt-1">
							Assets: {scene.assets.length} · Code versions: {scene.code.length}
						</div>
					</div>

					<div class="flex items-center gap-2">
						<div class="badge {stateClass(scene.narration?.state ?? 'not_started')}">
							<span>🎤</span>
							<span>{scene.narration?.state ?? 'not_started'}</span>
						</div>
					</div>
				</div>

				<div class="mt-3 grid gap-3">
					<!-- Assets -->
					<div>
						<div class="mb-2 text-sm font-medium">Assets</div>
						{#if scene.assets.length === 0}
							<div class="meta">No assets</div>
						{:else}
							<div class="flex flex-col gap-2">
								{#each scene.assets as asset}
									<div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
										<div class="flex items-center gap-3">
											<div class="text-sm font-medium">{assetTypeLabel(asset)}</div>
											<div class="meta">id: {shortId(asset.assetId)}</div>
											<div class="badge {stateClass(asset.state)}">{asset.state}</div>
										</div>

										<!-- Short and long descriptions (show common fallback property names) -->
										<div class="mt-2">
											<div class="meta text-xs font-medium">Short description</div>
											<div class="meta">
												{asset.assetShortDesc ?? asset.shortDescription ?? 'No short description'}
											</div>

											<div class="meta mt-1 text-xs font-medium">Long description</div>
											<div class="meta">
												{asset.assetLongDesc ?? asset.longDescription ?? 'No long description'}
											</div>
										</div>

										{#if asset.type === 'visual'}
											<div
												class="mt-2 flex flex-col gap-2 sm:mt-0 sm:flex-row sm:items-center sm:gap-3"
											>
												<div class="meta">Candidates:</div>
												<div class="flex flex-wrap gap-2">
													{#if asset.candidates.length === 0}
														<div class="meta">No candidates</div>
													{:else}
														{#each asset.candidates as c}
															<div class="candidate flex flex-col gap-2">
																<div class="flex items-center gap-2">
																	<div class="text-xs font-medium">{shortId(c.candidateId)}</div>
																	<div class="meta text-xs">({c.state})</div>
																	{#if c.selected}
																		<div class="text-xs font-semibold text-yellow-700">
																			Selected
																		</div>
																	{/if}
																	{#if c.finalSelected}
																		<div class="text-xs font-bold text-green-700">Final</div>
																	{/if}
																</div>
																{#if c.state === 'done'}
																	<video class="video-preview" loop autoplay muted playsinline>
																		<source
																			src={`${STATIC_API_BASE}/${sessionId}/${asset.assetId}/${c.candidateId}.mp4`}
																			type="video/mp4"
																		/>
																		Your browser does not support the video tag.
																		<track kind="captions" />
																	</video>
																{/if}
															</div>
														{/each}
													{/if}
												</div>
											</div>
										{/if}
									</div>
								{/each}
							</div>
						{/if}
					</div>

					<!-- Code generation statuses -->
					<div>
						<div class="mb-2 text-sm font-medium">Code generation</div>
						{#if scene.code.length === 0}
							<div class="meta">No code versions</div>
						{:else}
							<div class="flex flex-wrap gap-2">
								{#each scene.code as c, i}
									<div class="badge {stateClass(c.state)}">
										<div class="flex flex-col items-start">
											<div class="text-xs font-semibold">v{i}</div>
											<div class="meta text-xs">retries: {c.retry_number}</div>
											<div class="text-xs">{c.state}</div>
										</div>
									</div>
								{/each}
							</div>

							<!-- Python Code Display -->
							<div class="mt-3">
								{#each scene.code as c, i}
									{#if c.state === 'done'}
										<div class="python-code-section">
											<div class="mb-1 text-xs font-medium">Python Code (v{i}):</div>
											{#await fetchPythonCode(scene.scene_number, i)}
												<div class="python-code">Loading...</div>
											{:then code}
												<pre class="python-code">{code}</pre>
											{:catch error}
												<div class="python-code"># Error loading code: {error}</div>
											{/await}
										</div>
									{/if}
								{/each}
							</div>
						{/if}
					</div>

					<!-- Render statuses -->
					<div>
						<div class="mb-2 text-sm font-medium">Render</div>
						{#if scene.render.length === 0}
							<div class="meta">No renders</div>
						{:else}
							<div class="flex flex-wrap gap-2">
								{#each scene.render as r, i}
									<div class="badge {stateClass(r.state)}">
										<div class="flex flex-col items-start">
											<div class="text-xs font-semibold">v{i}</div>
											<div class="meta text-xs">retries: {r.retry_number}</div>
											<div class="text-xs">{r.state}</div>
											{#if r.aborted === true}
												<div class="text-xs font-semibold text-orange-700">⚠ Aborted</div>
											{:else if r.state === 'done' && r.success !== null}
												<div
													class="text-xs font-semibold {r.success
														? 'text-green-700'
														: 'text-red-700'}"
												>
													{r.success ? '✓ Success' : '✗ Failed'}
												</div>
											{/if}
										</div>
									</div>
								{/each}
							</div>
						{/if}
					</div>

					<!-- Rendered Scene Video -->
					<div>
						<div class="mb-2 text-sm font-medium">Rendered Scene</div>
						{#if scene.render.some((r) => r.state === 'done')}
							{@const doneRenders = scene.render.filter((r) => r.state === 'done' && r.success)}
							{#each doneRenders as render}
								<div class="rendered-scene-container mb-4" class:selected={render.selected}>
									<div class="mb-1 text-xs text-gray-600">Version {render.version_number}</div>
									<video class="rendered-scene-video" controls autoplay loop preload="metadata">
										<source
											src="{STATIC_API_BASE}/{sessionId}/scene_{scene.scene_number}_{render.version_number}.mp4"
											type="video/mp4"
										/>
										Your browser does not support the video tag.
										<track kind="captions" />
									</video>
								</div>
							{/each}
						{:else}
							<div class="meta">Scene not yet rendered</div>
						{/if}
					</div>
				</div>
			</div>
		{/each}
	{/if}
</div>

<style>
	/* Minimal scoped styles to complement utility classes */
	.scene-card {
		border-radius: 8px;
		padding: 12px;
		border: 1px solid var(--border, #e5e7eb);
		background: var(--card-bg, #ffffff);
	}
	.badge {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 4px 8px;
		border-radius: 9999px;
		font-size: 0.75rem;
		font-weight: 600;
	}
	.candidate {
		border-radius: 6px;
		padding: 6px 8px;
		border: 1px solid var(--border, #e5e7eb);
		background: var(--candidate-bg, #fafafa);
	}
	.meta {
		font-size: 0.85rem;
		color: #6b7280;
	}
	.video-preview {
		max-width: 200px;
		max-height: 120px;
		border-radius: 4px;
		border: 1px solid var(--border, #e5e7eb);
	}
	.python-code-section {
		margin-top: 8px;
		padding: 8px;
		background: var(--code-bg, #f8f9fa);
		border-radius: 4px;
		border: 1px solid var(--border, #e5e7eb);
	}
	.python-code {
		font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
		font-size: 0.5rem;
		line-height: 1.2;
		color: #374151;
		background: transparent;
		margin: 0;
		padding: 0;
		white-space: pre-wrap;
		word-wrap: break-word;
		overflow-x: auto;
		max-height: 200px;
		overflow-y: auto;
	}
	.rendered-scene-container {
		display: flex;
		justify-content: center;
		padding: 8px;
		background: var(--code-bg, #f8f9fa);
		border-radius: 4px;
		border: 1px solid var(--border, #e5e7eb);
	}
	.rendered-scene-container.selected {
		border: 2px solid #3b82f6;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
		background-color: rgba(59, 130, 246, 0.05);
	}

	.rendered-scene-video {
		max-width: 100%;
		max-height: 400px;
		border-radius: 4px;
		border: 1px solid var(--border, #e5e7eb);
	}
</style>
