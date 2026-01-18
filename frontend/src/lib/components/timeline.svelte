<script lang="ts">
	import { videoState } from '$lib/stores/generation-data.svelte';

	// Types
	interface SegmentWithPosition {
		name: string;
		duration: number;
		startTime: number;
		endTime: number;
		startPercent: number;
		widthPercent: number;
	}

	// Props
	let {
		currentTime = $bindable(0),
		currentScene = $bindable(0),
		paused = $bindable(false)
	}: { currentTime: number; currentScene: number; paused: boolean } = $props();
	let sceneDurations: number[] = $derived(videoState.sceneDurations);

	let timelineElement: HTMLDivElement;
	let isDragging: boolean = $state(false);

	// Calculate total duration
	let totalDuration: number = $derived(
		sceneDurations.length > 0
			? sceneDurations.reduce((sum: number, duration: number) => sum + duration, 0)
			: 0
	);

	// Calculate segment positions
	let segments: SegmentWithPosition[] = $derived(
		sceneDurations.map((duration: number, index: number): SegmentWithPosition => {
			const startTime: number = sceneDurations
				.slice(0, index)
				.reduce((sum: number, d: number) => sum + d, 0);
			const endTime: number = startTime + duration;
			const startPercent: number = totalDuration > 0 ? (startTime / totalDuration) * 100 : 0;
			const widthPercent: number = totalDuration > 0 ? (duration / totalDuration) * 100 : 0;

			return {
				name: `Scene ${index + 1}`,
				duration,
				startTime,
				endTime,
				startPercent,
				widthPercent
			};
		})
	);

	// Calculate current time position as percentage
	let currentTimePercent: number = $derived(
		totalDuration > 0 ? (currentTime / totalDuration) * 100 : 0
	);

	// Calculate current scene based on current time
	$effect(() => {
		if (segments.length > 0) {
			const newCurrentScene = segments.findIndex(
				(segment) => currentTime >= segment.startTime && currentTime < segment.endTime
			);
			// If we're at or beyond the last segment, set to last scene
			if (newCurrentScene === -1 && currentTime >= segments[segments.length - 1].startTime) {
				currentScene = segments.length - 1;
			} else if (newCurrentScene !== -1) {
				currentScene = newCurrentScene;
			}
		}
	});

	// Update currentTime based on mouse position
	function updateTimeFromPosition(clientX: number): void {
		if (!timelineElement) return;

		const rect: DOMRect = timelineElement.getBoundingClientRect();
		const clickX: number = clientX - rect.left;
		const clickPercent: number = (clickX / rect.width) * 100;
		const newTime: number = (clickPercent / 100) * totalDuration;

		// Clamp to valid range and update bindable prop
		currentTime = Math.max(0, Math.min(newTime, totalDuration));
	}

	// Handle timeline click
	function handleTimelineClick(event: MouseEvent): void {
		if (isDragging) return;
		updateTimeFromPosition(event.clientX);
	}

	// Handle drag start
	function handleMouseDown(event: MouseEvent): void {
		event.preventDefault();
		isDragging = true;
		updateTimeFromPosition(event.clientX);

		// Add global event listeners
		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);
		document.body.style.userSelect = 'none'; // Prevent text selection
		document.body.style.cursor = 'grabbing';
	}

	// Handle drag move
	function handleMouseMove(event: MouseEvent): void {
		if (!isDragging) return;
		event.preventDefault();
		updateTimeFromPosition(event.clientX);
	}

	// Handle drag end
	function handleMouseUp(): void {
		isDragging = false;

		// Remove global event listeners
		document.removeEventListener('mousemove', handleMouseMove);
		document.removeEventListener('mouseup', handleMouseUp);
		document.body.style.userSelect = '';
		document.body.style.cursor = '';
	}

	// Format time for display (mm:ss)
	function formatTime(seconds: number): string {
		const minutes: number = Math.floor(seconds / 60);
		const remainingSeconds: number = Math.floor(seconds % 60);
		return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
	}

	// Toggle pause state
	function togglePause(): void {
		paused = !paused;
	}
</script>

<div class="timeline-container">
	<!-- Controls -->
	<div class="timeline-controls">
		<button class="pause-button" on:click={togglePause} aria-label={paused ? 'Play' : 'Pause'}>
			{#if paused}
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
					<path d="M8 5v14l11-7z" />
				</svg>
			{:else}
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
					<path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
				</svg>
			{/if}
		</button>

		<!-- Time labels -->
		<div class="time-labels">
			<span class="time-start">0:00</span>
			<span class="time-current">{formatTime(currentTime)}</span>
			<span class="time-end">{formatTime(totalDuration)}</span>
		</div>
	</div>

	<!-- Timeline track -->
	<div
		class="timeline-track"
		bind:this={timelineElement}
		on:click={handleTimelineClick}
		on:mousedown={handleMouseDown}
		role="slider"
		tabindex="0"
		aria-label="Timeline scrubber"
		aria-valuemin="0"
		aria-valuemax={totalDuration}
		aria-valuenow={currentTime}
		class:dragging={isDragging}
	>
		<!-- Duration segments -->
		{#each segments as segment, index}
			<div
				class="timeline-segment"
				class:active={index === currentScene}
				style="left: {segment.startPercent}%; width: {segment.widthPercent}%"
				title="{segment.name}: {formatTime(segment.duration)}"
			>
				<div class="segment-label">{segment.name}</div>
			</div>
		{/each}

		<!-- Current time indicator -->
		<div
			class="timeline-cursor"
			class:dragging={isDragging}
			style="left: {currentTimePercent}%"
			on:mousedown={handleMouseDown}
		></div>
	</div>
</div>

<style>
	.timeline-container {
		width: 100%;
		max-width: 800px;
		margin: 0 auto;
		padding: 20px;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
	}

	.timeline-controls {
		display: flex;
		align-items: center;
		gap: 16px;
		margin-bottom: 8px;
	}

	.pause-button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		border: none;
		border-radius: 50%;
		background: #2563eb;
		color: white;
		cursor: pointer;
		transition: all 0.2s;
		box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
	}

	.pause-button:hover {
		background: #1d4ed8;
		transform: scale(1.05);
		box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
	}

	.pause-button:active {
		transform: scale(0.95);
	}

	.time-labels {
		display: flex;
		justify-content: space-between;
		flex: 1;
		font-size: 12px;
		color: #666;
	}

	.time-current {
		font-weight: bold;
		color: #2563eb;
	}

	.timeline-track {
		position: relative;
		width: 100%;
		height: 60px;
		background: #f3f4f6;
		border-radius: 8px;
		cursor: pointer;
		border: 2px solid #e5e7eb;
		transition: border-color 0.2s;
	}

	.timeline-track.dragging {
		cursor: grabbing;
	}

	.timeline-track:hover {
		border-color: #d1d5db;
	}

	.timeline-track:focus {
		outline: none;
		border-color: #2563eb;
		box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
	}

	.timeline-segment {
		position: absolute;
		top: 4px;
		bottom: 4px;
		background: linear-gradient(135deg, #3b82f6, #1e40af);
		border-radius: 4px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		font-size: 11px;
		font-weight: 500;
		transition: transform 0.2s;
		overflow: hidden;
	}

	.timeline-segment:hover {
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
	}

	.timeline-segment.active {
		background: linear-gradient(135deg, #f59e0b, #d97706);
		box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
		transform: translateY(-1px);
	}

	.segment-label {
		text-overflow: ellipsis;
		overflow: hidden;
		white-space: nowrap;
		padding: 0 8px;
	}

	.timeline-cursor {
		position: absolute;
		top: -2px;
		bottom: -2px;
		width: 3px;
		background: #dc2626;
		border-radius: 2px;
		transform: translateX(-50%);
		box-shadow: 0 2px 8px rgba(220, 38, 38, 0.4);
		z-index: 10;
		cursor: grab;
		transition: transform 0.1s ease;
	}

	.timeline-cursor:hover {
		transform: translateX(-50%) scale(1.2);
	}

	.timeline-cursor.dragging {
		cursor: grabbing;
		transform: translateX(-50%) scale(1.3);
		box-shadow: 0 4px 16px rgba(220, 38, 38, 0.6);
	}

	.timeline-cursor::before {
		content: '';
		position: absolute;
		top: -6px;
		left: 50%;
		transform: translateX(-50%);
		width: 0;
		height: 0;
		border-left: 6px solid transparent;
		border-right: 6px solid transparent;
		border-top: 6px solid #dc2626;
	}

	.segment-list {
		margin-top: 16px;
		padding: 12px;
		background: #f9fafb;
		border-radius: 6px;
		border: 1px solid #e5e7eb;
	}

	.segment-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 6px 0;
		border-bottom: 1px solid #e5e7eb;
	}

	.segment-item:last-child {
		border-bottom: none;
	}

	.segment-item.active {
		background-color: #fef3c7;
		border-radius: 4px;
		padding: 8px 6px;
		margin: 2px 0;
	}

	.segment-item.active .segment-name {
		color: #d97706;
		font-weight: 600;
	}

	.segment-name {
		font-weight: 500;
		color: #374151;
	}

	.segment-time {
		font-size: 12px;
		color: #6b7280;
		font-family: 'Monaco', 'Menlo', monospace;
	}

	@media (max-width: 640px) {
		.timeline-container {
			padding: 16px;
		}

		.timeline-controls {
			gap: 12px;
		}

		.pause-button {
			width: 36px;
			height: 36px;
		}

		.timeline-track {
			height: 50px;
		}

		.segment-label {
			font-size: 10px;
		}

		.segment-item {
			flex-direction: column;
			align-items: flex-start;
			gap: 2px;
		}
	}
</style>
