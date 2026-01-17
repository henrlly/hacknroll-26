<script lang="ts">
	import type { VideoPlan } from '$lib/types/planTypes';

	let { plan, isLoadingPlan } = $props<{ plan: VideoPlan; isLoadingPlan: boolean }>();
</script>

<div class="mx-auto max-w-4xl space-y-6 p-6">
	{#if isLoadingPlan}
		<div
			class="mt-4 flex items-start gap-3 rounded border border-yellow-100 bg-yellow-50 p-3 text-sm text-gray-700"
		>
			<svg
				class="h-5 w-5 animate-spin text-yellow-500"
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
			>
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"
				></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
			</svg>
			<div>
				<div class="font-medium text-gray-900">Generating plan — streaming</div>
				<div class="text-xs text-gray-600">
					The plan is being generated and will appear here as scenes stream in. This may take a
					minute.
				</div>
			</div>
		</div>
	{:else}
		<!-- Plan Header -->
		<div class="border-b pb-4">
			<h1 class="text-2xl font-bold text-gray-900">{plan.topic || 'Video Plan'}</h1>
			{#if plan.main_font || plan.secondary_font}
				<div class="mt-2 space-x-4 text-sm text-gray-600">
					{#if plan.main_font}
						<span>Main Font: <span class="font-medium">{plan.main_font}</span></span>
					{/if}
					{#if plan.secondary_font}
						<span>Secondary Font: <span class="font-medium">{plan.secondary_font}</span></span>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Scenes -->
		{#if plan.scenes && plan.scenes.length > 0}
			<div class="space-y-4">
				<h2 class="text-xl font-semibold text-gray-900">Scenes ({plan.scenes.length})</h2>
				<div class="grid gap-4">
					{#each plan.scenes as scene}
						<div class="rounded-lg border bg-gray-50 p-4">
							<div class="mb-3 flex items-center justify-between">
								<h3 class="text-lg font-medium text-gray-900">
									Scene {scene.scene_number + 1}
								</h3>
								{#if scene.duration_seconds}
									<span class="rounded bg-white px-2 py-1 text-sm text-gray-600">
										{scene.duration_seconds}s
									</span>
								{/if}
							</div>

							{#if scene.visuals_description}
								<div class="mb-3">
									<h4 class="mb-1 text-sm font-medium text-gray-700">Visuals</h4>
									<p class="text-sm text-gray-600">{scene.visuals_description}</p>
								</div>
							{/if}

							{#if scene.narration_script}
								<div class="mb-3">
									<h4 class="mb-1 text-sm font-medium text-gray-700">Narration</h4>
									<p class="text-sm text-gray-600">{scene.narration_script}</p>
								</div>
							{/if}

							{#if scene.sound_description}
								<div class="mb-3">
									<h4 class="mb-1 text-sm font-medium text-gray-700">Sound</h4>
									<p class="text-sm text-gray-600">{scene.sound_description}</p>
								</div>
							{/if}

							{#if scene.edit_notes}
								<div class="mb-3">
									<h4 class="mb-1 text-sm font-medium text-gray-700">Edit Notes</h4>
									<p class="text-sm text-gray-600">{scene.edit_notes}</p>
								</div>
							{/if}

							{#if scene.assets_needed && scene.assets_needed.length > 0}
								<div>
									<h4 class="mb-2 text-sm font-medium text-gray-700">Assets Needed</h4>
									<div class="flex flex-wrap gap-2">
										{#each scene.assets_needed as asset}
											<span class="rounded bg-blue-100 px-2 py-1 text-xs text-blue-800">
												{asset.asset_type}: {asset.asset_short_desc}
											</span>
										{/each}
									</div>
								</div>
							{/if}
						</div>
					{/each}
				</div>
			</div>
		{:else}
			<div class="py-8 text-center text-gray-500">
				{#if isLoadingPlan}
					Waiting for the first scene to stream...
				{:else}
					Generating scenes...
				{/if}
			</div>
		{/if}
	{/if}
</div>
