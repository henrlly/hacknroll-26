<script lang="ts">
    import * as Breadcrumb from "$lib/components/ui/breadcrumb/index.js";
    
    let { generationStep = $bindable() } = $props();
    let allGenerationSteps = ["INPUT", "WRITING SCRIPT", "DOING TASKS", "COMPLETED"]
</script>
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