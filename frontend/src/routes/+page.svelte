<script lang="ts">
	import { onMount } from 'svelte';
	import { type UserRequestType, StreamResponse } from '$lib/types/apiTypes';
	import InitialInput from '$lib/components/pages/initial-input.svelte';
	import { VideoPlanSchema, type VideoPlan } from '$lib/types/planTypes';
	import { ALL, parse } from 'partial-json';
	import PlanDisplay from '$lib/components/plan/plan-display.svelte';
	import type { SceneLoadingType } from '$lib/types/sceneTypes';
	import { processSceneEvent, sceneFromPlan } from '$lib/utils/process-scene';
	import ScenesDisplay from '$lib/components/scenes/ScenesDisplay.svelte';
	import FinalVideo from '$lib/components/pages/final-video.svelte';
	import { WS_API } from '$lib/utils/constants';
	import { Badge } from '$lib/components/ui/badge';
    import * as Breadcrumb from "$lib/components/ui/breadcrumb/index.js";

	let socket: WebSocket;

	// TODO: enable or disable based on page state
	type PageStateType = 'initialInput' | 'plan' | 'scenes' | 'final';
	let pageState: PageStateType = $state('initialInput');
	const pageStates: Record<PageStateType, string> = {
		initialInput: 'Initial Input',
		plan: 'Plan',
		scenes: 'Scenes',
		final: 'Final Video'
	};

	let plan_string = '';
	// TODO: persist across refreshes with sessionStorage?
	let plan = $state<VideoPlan>({});
	let scenesObj = $state<{ data: SceneLoadingType[] }>({ data: [] });
	let sessionId = $state<string>('');

	let isLoadingPlan = $state<boolean>(false);
	let isStitching = $state<boolean>(false);

	onMount(() => {
		socket = new WebSocket(WS_API);
		socket.onmessage = async (event) => {
			// console.log(event);
			const result = StreamResponse.safeParse(JSON.parse(event.data));
			if (result.error) {
				console.log(JSON.parse(event.data));
				return;
			}
			if (result.data.type === 'start') {
				sessionId = result.data.session_id;
			} else if (result.data.type === 'plan') {
				// TODO: add plan loading before stream
				if (result.data.event_type === 'plan_start') {
					isLoadingPlan = true;
				} else if (result.data.event_type === 'plan_stream') {
					isLoadingPlan = false;
					plan_string += result.data.delta;
					plan = VideoPlanSchema.parse(parse(plan_string, ALL));
				} else {
					sceneFromPlan(plan, scenesObj);
					pageState = 'scenes';
				}
			} else if (result.data.type !== 'final_video') {
				processSceneEvent(result.data, scenesObj);
			} else {
				if (result.data.event_type === 'stitching_start') {
					isStitching = true;
				} else {
					isStitching = false;
					pageState = 'final';
				}
			}
		};

		socket.onclose = () => console.log('WebSocket connection closed');

		return () => socket.close(); // Clean up on destroy
	});

	function handleSubmit({ prompt, voice }: UserRequestType) {
		if (socket && socket.readyState === WebSocket.OPEN) {
			const payload = { prompt, voice };
			console.log(payload);
			socket.send(JSON.stringify(payload));
			pageState = 'plan';
		} else {
			console.error('WebSocket is not connected.');
		}
	}
</script>

<div class="flex h-screen w-full flex-col items-center gap-4">
	<div class="flex gap-2">
        <Breadcrumb.Root>
            <Breadcrumb.List>
                {#each Object.entries(pageStates) as [pageStateOption, pageStateLabel]}
                    <Breadcrumb.Item class={pageState === pageStateOption ? 'text-primary font-bold' : 'brightness-80'}>
                        <label>
                            <input
                                class="sr-only"
                                type="radio"
                                name="scoops"
                                value={pageStateOption}
                                bind:group={pageState}
                            />
                            {pageStateLabel}
                        </label>
                    </Breadcrumb.Item>
                    {#if pageStateOption !== "final"}
                    <Breadcrumb.Separator />
                    {/if}
                {/each}
            </Breadcrumb.List>
        </Breadcrumb.Root>
	</div>

	{#if pageState === 'initialInput'}
		<InitialInput {handleSubmit} />
	{:else if pageState === 'plan'}
		<PlanDisplay {plan} {isLoadingPlan} />
	{:else if pageState === 'scenes'}
	    <!-- <div>{JSON.stringify(scenesObj.data)}</div> -->
		<ScenesDisplay scenes={scenesObj.data} {sessionId} {isStitching} />
	{:else}
		<FinalVideo {sessionId} />
	{/if}
</div>
