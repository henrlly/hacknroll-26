<script lang="ts">
	import SceneDisplay from './SceneDisplay.svelte';
	import type { SceneLoadingType } from '$lib/types/sceneTypes';

	export let scene: SceneLoadingType;
</script>

<SceneDisplay {scene} />