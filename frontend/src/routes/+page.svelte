<script lang="ts">
	import { onMount } from 'svelte';
	import { type UserRequestType, StreamResponse } from '$lib/types/apiTypes';
	import PromptInput from '$lib/components/prompt-input.svelte';
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
	let allGenerationSteps = ["INPUT", "WRITING SCRIPT", "DOING TASKS", "COMPLETED"]
	let generationStep = $state("INPUT" as "INPUT" | "WRITING SCRIPT" | "DOING TASKS" | "COMPLETED");

	let plan = $state<VideoPlan>({});
	let scenesObj = $state<{ data: SceneLoadingType[] }>({ data: [] });
	let sessionId = $state<string>('');

	let isLoadingPlan = $state<boolean>(false);
	let isStitching = $state<boolean>(false);

</script>

<div class="flex h-screen w-full flex-col items-center gap-4">
	<div class="flex gap-2">
        <Breadcrumb.Root>
            <Breadcrumb.List>
                {#each allGenerationSteps as step}
                    <Breadcrumb.Item class={generationStep === step ? 'text-primary' : 'brightness-80'}>
                        <label>
                            <input
                                class="sr-only"
                                type="radio"
                                name="scoops"
                                value={step}
                                bind:group={generationStep}
                            />
                            {step.charAt(0) + step.slice(1).toLowerCase()}
                        </label>
                    </Breadcrumb.Item>
                    {#if step !== "COMPLETED"}
                    <Breadcrumb.Separator />
                    {/if}
                {/each}
            </Breadcrumb.List>
        </Breadcrumb.Root>
	</div>

	{#if generationStep === 'INPUT'}
		<PromptInput />
	{:else if generationStep === 'WRITING SCRIPT'}
		<PlanDisplay {plan} {isLoadingPlan} />
	{:else if generationStep === 'DOING TASKS'}
		<ScenesDisplay scenes={scenesObj.data} {sessionId} {isStitching} />
	{:else if generationStep === "COMPLETED"}
		<FinalVideo {sessionId} />
	{/if}
</div>
