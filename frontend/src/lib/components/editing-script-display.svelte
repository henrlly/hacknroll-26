<script lang="ts">
    import { videoState } from "$lib/stores/generation-data.svelte";
    import * as Tabs from "$lib/components/ui/tabs/index.js";
    import { FileText, Image as ImageIcon } from "@lucide/svelte";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import * as Card from "$lib/components/ui/card";
</script>

<Tabs.Root value="script">
    <Tabs.List>
        <Tabs.Trigger value="script">Script</Tabs.Trigger>
        <Tabs.Trigger value="visual">Visuals</Tabs.Trigger>
    </Tabs.List>

    <Card.Root class="h-48 overflow-auto backdrop-blur-sm pt-0 shadow-sm">
        <ScrollArea>
            <div class="p-4">
                <Tabs.Content value="script" class="mt-0 outline-none">
                    <article class="text-sm leading-relaxed whitespace-pre-wrap font-medium">
                        {videoState.full_script}
                    </article>
                </Tabs.Content>

                <Tabs.Content value="visual" class="mt-0 outline-none">
                    <div class="grid gap-3">
                        {#each videoState.visual_asset_gen as asset, i}
                            <div class="group flex gap-3 p-3 rounded-lg border bg-background/50 transition-colors hover:border-primary/50">
                                <div class="flex flex-col items-center">
                                    <span class="text-[10px] font-bold text-muted-foreground mb-1">#{i + 1}</span>
                                    <div class="w-1 h-full bg-muted rounded-full group-hover:bg-primary/30 transition-colors"></div>
                                </div>
                                <p class="text-xs text-muted-foreground italic leading-snug pt-1">
                                    "{asset.desc}"
                                </p>
                            </div>
                        {/each}
                    </div>
                </Tabs.Content>
            </div>
        </ScrollArea>
    </Card.Root>
</Tabs.Root>