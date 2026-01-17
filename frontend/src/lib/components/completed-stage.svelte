<script lang="ts">
	import { STATIC_API_BASE } from '$lib/utils/constants';
    import { videoState } from '$lib/stores/generation-data.svelte';
	import ScriptDisplay from './script-display.svelte';
	import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import { Label } from "$lib/components/ui/label";
    import { Badge } from "$lib/components/ui/badge";
	import { Input } from "$lib/components/ui/input/index.js";
	import { ChevronDown, ChevronUp, Sparkles, Wand2, Edit2, Check } from '@lucide/svelte';
	import { sendEditPrompt, selectVisual } from '$lib/utils/editing';

	let editingMode = $state(false);
	let currentIndex = $state(0);
	$effect(() => {
		if (editingMode && videoState.visual_asset_gen.length > 1) {
            const interval = setInterval(() => {
                currentIndex = (currentIndex + 1) % videoState.visual_asset_gen.length;
            }, 2000);

            return () => clearInterval(interval);
        }
	})

	let editPrompt = $state("");
	let openEditPhotos = $state(false);
	let activeAsset: string = $derived(videoState.visual_asset_gen[currentIndex].mp4Url)

	function handleSubmitPrompt(e: SubmitEvent) {
		e.preventDefault();
		if (!editPrompt.trim()) return;

		try {
			// Ensure sendEditPrompt is awaited if it's an async function
			sendEditPrompt(editPrompt);
			editPrompt = ''; // Clear input after success
		} catch (err) {
			console.error('Failed to send edit:', err);
		}
	}
</script>

<div class="flex flex-col items-center gap-6 w-full max-w-5xl mx-auto py-4">
	<div class="aspect-video w-4/5 rounded-xl border-1 border-dashed border-primary relative">
		<video
			class="h-full w-full rounded-xl"
			src={`${STATIC_API_BASE}/${videoState.session_id}/final_video.mp4`}
			controls
			autoplay
		>
			<track kind="captions" />
		</video>
		<Badge variant="secondary" class="absolute top-4 left-4 gap-1 opacity-80">
			<Sparkles class="size-3" /> Final Render
		</Badge>
	</div>
	<div class="flex w-4/5 items-center justify-between px-2">
        <div class="flex flex-col">
            <h3 class="text-sm font-medium text-muted-foreground uppercase tracking-wider">Project Workspace</h3>
            <p class="text-xs text-muted-foreground/60">Session: {videoState.session_id}</p>
        </div>
        
        <Button 
            variant="outline" 
            size="sm" 
            class={"gap-2 transition-all"}
            onclick={() => editingMode = !editingMode}
        >	
			{#if !editingMode}
            <Wand2 class="size-4" />
			{/if}
            {editingMode ? "Close Editor" : "Refine Script"}
            {#if editingMode}
                <ChevronUp class="size-4" />
            {:else}
                <ChevronDown class="size-4" />
            {/if}
        </Button>
    </div>

    {#if editingMode}
        <div class="w-full backdrop-blur-sm">
            <div class="flex w-full h-full gap-6 p-6">
                
                <div class="flex flex-col w-[60%] gap-4 shrink-0">
                    <div class="flex flex-col gap-1.5">
                        <Label class="text-xs uppercase text-muted-foreground">Video Script</Label>
                        <div class="rounded-md ">
                            <ScriptDisplay />
                        </div>
                    </div>
                    
                    <div class="flex flex-col gap-1.5 h-1/2">
                        <Label class="text-xs uppercase text-muted-foreground">Adjust Prompt</Label>
						<form onsubmit={handleSubmitPrompt} class="relative z-10">
							<Input 
								type="text" 
								placeholder="e.g. Make the tone more exciting..." 
								bind:value={editPrompt}
							/>
						</form>
                    </div>
                </div>

                <div class="flex-grow flex flex-col gap-1.5">
                    <Label class="text-xs uppercase text-muted-foreground">Active Clip</Label>
                    <div class="relative flex-grow overflow-hidden rounded-xl border bg-black shadow-inner">
						{#key activeAsset}
                        <video 
                            class="w-full h-full object-cover opacity-80" 
                            src={activeAsset}
                            autoplay
                            loop
                            muted
                        >
							<track kind="captions"> 
                        </video>
						{/key}
                        <div class="absolute top-3 right-3">
        <Dialog.Root bind:open={openEditPhotos}>
            <Dialog.Trigger>
                    <Button 
                        variant="secondary" 
                        size="icon" 
                        class="h-8 w-8 rounded-full shadow-lg opacity-50 hover:opacity-100"
                    >
                        <Edit2 class="size-4" />
                    </Button>
            </Dialog.Trigger>
            
            <Dialog.Content class="sm:max-w-[600px]">
                <Dialog.Header>
                    <Dialog.Title>Select Visual Asset</Dialog.Title>
                    <Dialog.Description>
                        Choose which image or clip to use for this segment of the video.
                    </Dialog.Description>
                </Dialog.Header>

                <div class="grid grid-cols-3 gap-4 py-4">
                    {#each videoState.visual_asset_gen as asset}
                        <button 
                            onclick={() => { selectVisual({ assetId: "idk", selectedCandidateId: "idk"})}}
                            class="relative aspect-video rounded-md overflow-hidden border-2 transition-all hover:ring-2 hover:ring-primary"
                        >
                            <video src={asset.mp4Url} class="object-cover w-full h-full">
								<track kind="captions" />
							</video>
                            
                            {#if activeAsset === asset.mp4Url}
                                <div class="absolute inset-0 bg-primary/20 flex items-center justify-center">
                                    <Badge class="rounded-full p-1">
                                        <Check class="size-3" />
                                    </Badge>
                                </div>
                            {/if}
                        </button>
                    {/each}
                </div>

                <Dialog.Footer>
                    <Button onclick={() => openEditPhotos = false} type="submit">Confirm Selection</Button>
                </Dialog.Footer>
            </Dialog.Content>
        </Dialog.Root>
                    </div>
                </div>
            </div>
        </div>
	</div>
	{/if}
</div>