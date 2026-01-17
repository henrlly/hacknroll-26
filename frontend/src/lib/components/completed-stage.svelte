<script>
	import { STATIC_API_BASE } from '$lib/utils/constants';
    import { videoState } from '$lib/stores/generation-data.svelte';
	import ScriptDisplay from './script-display.svelte';
	import * as Card from "$lib/components/ui/card";
    import { Button } from "$lib/components/ui/button";
    import { Label } from "$lib/components/ui/label";
    import { Badge } from "$lib/components/ui/badge";
	import { Input } from "$lib/components/ui/input/index.js";
	import { ChevronDown, ChevronUp, Sparkles, Wand2 } from '@lucide/svelte';

	let editingMode = $state(false);
	let currentIndex = $state(0);
	$effect(() => {
		if (editingMode && videoState.visual_asset_gen.length > 1) {
            const interval = setInterval(() => {
                currentIndex = (currentIndex + 1) % videoState.visual_asset_gen.length;
            }, 2000); // 2 seconds

            // Cleanup function: runs when editingMode is false or component is destroyed
            return () => clearInterval(interval);
        }
	})

	let activeAsset = $derived(videoState.visual_asset_gen[currentIndex].mp4Url)
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
            <Wand2 class="size-4" />
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
                        <Input type="text" placeholder="e.g. Make the tone more exciting..." class="bg-background" />
                    </div>
                </div>

                <div class="flex-grow flex flex-col gap-1.5">
                    <Label class="text-xs uppercase text-muted-foreground">Active Clip</Label>
                    <div class="relative flex-grow overflow-hidden rounded-xl border bg-black shadow-inner">
                        <video 
                            class="w-full h-full object-cover opacity-80" 
                            src={activeAsset}
                            autoplay
                            loop
                            muted
                        >
                            <track kind="captions"> 
                        </video>
                        <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent pointer-events-none"></div>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>