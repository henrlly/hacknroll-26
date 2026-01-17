<script>
	import { STATIC_API_BASE } from '$lib/utils/constants';

	let { sessionId } = $props();
</script>

<div class="aspect-video w-4/5 rounded-xl border-1 border-dashed border-primary">
	<video
		class="h-full w-full rounded-xl"
		src={`${STATIC_API_BASE}/${sessionId}/final_video.mp4`}
		controls
		loop
		autoplay
	>
		<track kind="captions" />
	</video>
</div>
