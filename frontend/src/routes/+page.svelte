<script lang="ts">
    import PromptInput from "$lib/components/prompt-input.svelte";
    import { socketState } from "$lib/socket.svelte";

    let sessionID: string = $state("");
    let generationStep = $state("idle" as "idle" | "writing_script" | "doing_tasks" | "complete");
</script>

<div class="w-full h-screen flex flex-col gap-4 items-center">
    {#if generationStep === "idle"}
        <PromptInput />
    {/if}
</div>