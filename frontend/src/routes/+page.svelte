<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import { Textarea } from "$lib/components/ui/textarea/index.js";
	import { buttonVariants } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge/index.js";
	import { onMount } from "svelte";

    let submitted = $state(false);
    let socket: WebSocket;

    let sessionID: string = $state("");
    let generatedScript: string = $state("");
    let displayedScript: string = $state("");

    onMount(() => {
        socket = new WebSocket("ws://localhost:8000/api/ws");
    })

    let voice = $state("trump");
    let prompt = $state("");

    function selectVoice(selectedVoice: string) {
        return () => { voice = selectedVoice; };
    }

    async function handleSubmit() {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const payload = { prompt, voice };
            socket.send(JSON.stringify(payload));
            submitted = true;
        } else {
            console.error("WebSocket is not connected.");
        }
    }
</script>

<div class="w-full h-screen flex flex-col gap-4 items-center">
    <Card.Root class="w-2/3">
        {#if submitted}
        <Card.Header>
          <Card.Title>Generated Script</Card.Title>
          <Card.Description>We're cooking...</Card.Description>
        </Card.Header>
        {:else}
        <Card.Header>
          <Card.Title>Enter Prompt</Card.Title>
          <Card.Description>Describe what the video should explain</Card.Description>
        </Card.Header>
        {/if}
      <Card.Content>
          <form class="flex flex-col items-start" onsubmit={handleSubmit}>
            {#if submitted}
            <Textarea class="mb-4" name="prompt" placeholder="Enter video idea" bind:value={displayedScript}/>
            {:else}
            <Textarea class="mb-4 hover:shadow-primary hover:shadow-md focus:shadow-primary focus:shadow-md" name="prompt" placeholder="Enter video idea" bind:value={prompt}/>
            {/if}

              <input type="hidden" name="voice" bind:value={voice}>

              <div class="w-full flex justify-between">
                  <div class="flex gap-2">
                    <Badge class="h-6" variant={voice === "trump" ? "default" : "outline"} onclick={selectVoice("trump")}>Trump</Badge>
                    <Badge class="h-6" variant={voice === "peter" ? "default" : "outline"} onclick={selectVoice("peter")}>Peter</Badge>
                    <Badge class="h-6" variant={voice === "obama" ? "default" : "outline"} onclick={selectVoice("obama")}>Obama</Badge>
                  </div>
                  <button class="w-20 {buttonVariants({ variant: "default" })}">Submit</button>
              </div>
          </form>
      </Card.Content>
    </Card.Root>
</div>