<script lang="ts">
	import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import type { SceneLoadingType } from '$lib/types/sceneTypes';

	export let scene: SceneLoadingType;

	// Parse the scene structure into an ordered list
	function parseSceneStructure(structureText: string): string[] {
		if (!structureText.trim()) return [];
		
		// Split by lines and filter out empty lines
		const lines = structureText.split('\n').filter(line => line.trim());
		
		// Remove existing numbering if present and clean up
		return lines.map(line => {
			// Remove patterns like "1. ", "2. ", etc.
			return line.replace(/^\d+\.\s*/, '').trim();
		}).filter(line => line.length > 0);
	}

	// Parse sound effects from sound_description
	function parseSoundEffects(soundText: string): Array<{name: string, description: string}> {
		if (!soundText.trim()) return [];
		
		// Try to split by common delimiters and extract sound effects
		const lines = soundText.split(/[,;\n]/).filter(line => line.trim());
		
		return lines.map((line, index) => {
			const trimmed = line.trim();
			// Try to split name and description by colon or dash
			const colonMatch = trimmed.match(/^([^:]+):\s*(.+)$/);
			const dashMatch = trimmed.match(/^([^-]+)-\s*(.+)$/);
			
			if (colonMatch) {
				return {
					name: colonMatch[1].trim(),
					description: colonMatch[2].trim()
				};
			} else if (dashMatch) {
				return {
					name: dashMatch[1].trim(),
					description: dashMatch[2].trim()
				};
			} else {
				// If no clear separator, treat the whole line as a name with empty description
				return {
					name: trimmed,
					description: ''
				};
			}
		});
	}

	$: sceneStructureList = parseSceneStructure(scene.scene_structure);
	$: soundEffects = parseSoundEffects(scene.sound_description);
</script>

<div class="w-full max-w-4xl mx-auto p-4">
	<div class="mb-4">
		<h2 class="text-2xl font-bold text-gray-800 dark:text-gray-200">
			Scene {scene.scene_number}
		</h2>
		{#if scene.duration_seconds > 0}
			<p class="text-sm text-gray-600 dark:text-gray-400">
				Duration: {scene.duration_seconds}s
			</p>
		{/if}
	</div>

	<Tabs value="structure" class="w-full">
		<TabsList class="grid w-full grid-cols-4">
			<TabsTrigger value="structure">Structure</TabsTrigger>
			<TabsTrigger value="visuals">Visuals</TabsTrigger>
			<TabsTrigger value="narration">Narration</TabsTrigger>
			<TabsTrigger value="sfx">SFX</TabsTrigger>
		</TabsList>
		
		<TabsContent value="structure" class="mt-4">
			<div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
				<h3 class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200">
					Scene Structure
				</h3>
				{#if sceneStructureList.length > 0}
					<ol class="list-decimal list-inside space-y-2 text-gray-700 dark:text-gray-300">
						{#each sceneStructureList as item, index}
							<li class="leading-relaxed">{item}</li>
						{/each}
					</ol>
				{:else}
					<p class="text-gray-500 dark:text-gray-400 italic">
						No scene structure available
					</p>
				{/if}
			</div>
		</TabsContent>

		<TabsContent value="visuals" class="mt-4">
			<div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
				<h3 class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200">
					Visuals Description
				</h3>
				{#if scene.visuals_description.trim()}
					<div class="prose prose-sm max-w-none dark:prose-invert">
						<p class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">
							{scene.visuals_description}
						</p>
					</div>
				{:else}
					<p class="text-gray-500 dark:text-gray-400 italic">
						No visual description available
					</p>
				{/if}
			</div>
		</TabsContent>

		<TabsContent value="narration" class="mt-4">
			<div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
				<h3 class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200">
					Narration Script
				</h3>
				{#if scene.narration_script.trim()}
					<div class="prose prose-sm max-w-none dark:prose-invert">
						<p class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">
							{scene.narration_script}
						</p>
					</div>
				{:else}
					<p class="text-gray-500 dark:text-gray-400 italic">
						No narration script available
					</p>
				{/if}
			</div>
		</TabsContent>

		<TabsContent value="sfx" class="mt-4">
			<div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
				<h3 class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200">
					Sound Effects
				</h3>
				{#if soundEffects.length > 0}
					<div class="space-y-3">
						{#each soundEffects as sfx, index}
							<div class="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
								<div class="flex-shrink-0">
									<span class="inline-flex items-center justify-center w-6 h-6 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm font-medium">
										{index + 1}
									</span>
								</div>
								<div class="flex-1 min-w-0">
									<h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">
										{sfx.name}
									</h4>
									{#if sfx.description}
										<p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
											{sfx.description}
										</p>
									{/if}
								</div>
							</div>
						{/each}
					</div>
				{:else if scene.sound_description.trim()}
					<div class="prose prose-sm max-w-none dark:prose-invert">
						<p class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">
							{scene.sound_description}
						</p>
					</div>
				{:else}
					<p class="text-gray-500 dark:text-gray-400 italic">
						No sound effects available
					</p>
				{/if}
			</div>
		</TabsContent>
	</Tabs>

	{#if scene.edit_notes.trim()}
		<div class="mt-6 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
			<h4 class="text-sm font-medium text-yellow-800 dark:text-yellow-200 mb-2">
				Edit Notes
			</h4>
			<p class="text-sm text-yellow-700 dark:text-yellow-300 whitespace-pre-line">
				{scene.edit_notes}
			</p>
		</div>
	{/if}
</div>