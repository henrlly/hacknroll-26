<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import { Textarea } from "$lib/components/ui/textarea/index.js";
	import { buttonVariants } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { socketState } from "$lib/socket.svelte";

    let { character=$bindable() } = $props();
    let voice = $state("trump");
    let prompt = $state("");

    async function handleSubmit() {
        if (socketState.status === "connected" && socketState.socket) {
            const payload = { prompt, voice };
            socketState.socket.send(JSON.stringify(payload));
        } else {
            console.error("WebSocket is not connected.");
        }
    }
</script>

<div class="flex w-full justify-center items-center">
    <Card.Root class="w-2/3">
        <Card.Header>
            <Card.Title>Enter Prompt</Card.Title>
            <Card.Description>Describe what the video should explain</Card.Description>
        </Card.Header>
        <Card.Content>
            <form class="flex flex-col items-start" onsubmit={handleSubmit}>
            <Textarea class="mb-4 hover:shadow-primary hover:shadow-md focus:shadow-primary focus:shadow-md" name="prompt" placeholder="Enter video idea" bind:value={prompt}/>
    
                <input type="hidden" name="voice" bind:value={voice}>
    
                <div class="w-full flex justify-between">
                    <div class="flex gap-2">
                    <Badge class="h-6" variant={voice === "trump" ? "default" : "outline"} onclick={() => { voice = "trump"; character = "trump" }}>Trump</Badge>
                    <Badge class="h-6" variant={voice === "obama" ? "default" : "outline"} onclick={() => { voice = "obama"; character = "obama" }}>Obama</Badge>
                    <!-- <Badge class="h-6" variant={voice === "peter" ? "default" : "outline"} onclick={() => { voice = "peter" }}>Peter</Badge> -->
                    </div>
                    <button class="w-20 {buttonVariants({ variant: "default" })}">Submit</button>
                </div>
            </form>
        </Card.Content>
    </Card.Root>
</div>