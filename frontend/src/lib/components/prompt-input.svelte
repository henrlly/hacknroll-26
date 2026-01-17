<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import {Textarea} from "$lib/components/ui/textarea/index.js";
    import {buttonVariants} from "$lib/components/ui/button";
    import {Badge} from "$lib/components/ui/badge/index.js";
    import {socketState} from "$lib/socket.svelte";
    import type {HTMLAttributes} from "svelte/elements";
    import { ArrowUp } from "@lucide/svelte";

    let {voice = $bindable(), class: className}: {
        voice: "trump" | "obama" | undefined
    } & HTMLAttributes<HTMLDivElement> = $props();
    let prompt = $state("");

    async function handleSubmit() {
        if (socketState.status === "connected" && socketState.socket) {
            const payload = {prompt, voice};
            socketState.socket.send(JSON.stringify(payload));
        } else {
            console.error("WebSocket is not connected.");
        }
    }
</script>

<div class="flex w-full justify-center items-center">
    <div class="w-2/5">
            <h1 class="mb-4 text-2xl font-anthropic">What ponders the curious cat today?</h1>
            <form class="flex flex-col items-start" onsubmit={handleSubmit}>
                <Textarea
                        class="mb-4 hover:shadow-primary hover:shadow-md focus:shadow-primary focus:shadow-md + {className}"
                        name="prompt" placeholder="e.g. Make a video explaining how I can win Hack&Roll" bind:value={prompt}/>

                <input type="hidden" name="voice" bind:value={voice}>

                <div class="w-full flex justify-between">
                    <div class="flex gap-2">
                        <Badge class="h-8 cursor-pointer hover:shadow-yellow-500 hover:shadow-md" variant={voice === "trump" ? "default" : "outline"}
                               onclick={() => { voice = "trump" }}>Trump
                        </Badge>
                        <Badge class="h-8 cursor-pointer hover:shadow-amber-950 hover:shadow-lg" variant={voice === "obama" ? "default" : "outline"}
                               onclick={() => { voice = "obama" }}>Obama
                        </Badge>
                        <!-- <Badge class="h-6" variant={voice === "peter" ? "default" : "outline"} onclick={() => { voice = "peter" }}>Peter</Badge> -->
                    </div>
                    <button class=" {buttonVariants({ variant: "default" })}">
                        <ArrowUp />
                    </button>
                </div>
            </form>
    </div>
</div>