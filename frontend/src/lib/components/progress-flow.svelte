<script lang="ts">
    import * as Breadcrumb from "$lib/components/ui/breadcrumb/index.js";
    import { videoState } from "$lib/stores/generation-data.svelte";

    let { generationStep = $bindable() } = $props();
    let allGenerationSteps = ["INPUT", "WRITING SCRIPT", "DOING TASKS", "COMPLETED"]
    let maxStepIndex = $derived(allGenerationSteps.indexOf(videoState.generationStep));
</script>

<Breadcrumb.Root>
    <Breadcrumb.List>
        {#each allGenerationSteps as step, i}
            {@const isDisabled = i > maxStepIndex}
            <Breadcrumb.Item class={
                generationStep === step ? 'text-primary' : 'brightness-80'}>
                <label class="text-lg {isDisabled ? "cursor-not-allowed" : ""}">
                    <input
                        disabled={isDisabled}
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
