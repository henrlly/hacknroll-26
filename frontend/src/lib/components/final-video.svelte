<script>
	import { STATIC_API_BASE } from '$lib/utils/constants';
    import { videoState } from '$lib/stores/generation-data.svelte';
</script>

<div class="aspect-video w-4/5 rounded-xl border-1 border-dashed border-primary">
	<video
		class="h-full w-full rounded-xl"
		src={`${STATIC_API_BASE}/${videoState.session_id}/final_video.mp4`}
		controls
		autoplay
	>
		<track kind="captions" />
	</video>
</div>