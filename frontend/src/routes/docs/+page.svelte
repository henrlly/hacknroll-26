<script lang="ts">
    import * as Alert from "$lib/components/ui/alert";
    import * as Card from "$lib/components/ui/card";
    import { Separator } from "$lib/components/ui/separator";
    import { Badge } from "$lib/components/ui/badge";
    import { Terminal, Cpu, Zap, Rocket, ChevronRight } from "@lucide/svelte";
</script>

<div class="container max-w-4xl px-4 py-10">
    <div class="space-y-4 mb-10">
        <div class="flex items-center gap-2 text-primary">
            <Rocket class="size-5" />
            <span class="text-sm font-bold uppercase tracking-widest">Developer Documentation</span>
        </div>
        <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
            The AI Video Engine
        </h1>
        <p class="text-xl text-muted-foreground">
            A high-concurrency pipeline marrying LLMs with Manim for deterministic, educational video generation.
        </p>
    </div>

    <Separator class="my-8" />

    <section class="space-y-6">
        <div class="flex items-center gap-2">
            <Badge variant="outline">Architecture</Badge>
            <h2 class="text-2xl font-semibold tracking-tight">The Parallel Pipeline</h2>
        </div>
        
        <p class="leading-7 text-muted-foreground">
            Traditional video editors are linear. Our engine is <strong>asynchronous</strong>. We utilize 
            FastAPI WebSockets to stream state updates, allowing the frontend to render the UI 
            while the backend orchestrates heavy computation in parallel.
        </p>

        

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card.Root class="p-6 bg-muted/20">
                <Cpu class="size-6 mb-2 text-primary" />
                <h3 class="font-bold">Distributed Workers</h3>
                <p class="text-sm text-muted-foreground">Script generation, asset fetching, and Manim rendering occur in isolated threads, preventing bottlenecking.</p>
            </Card.Root>
            <Card.Root class="p-6 bg-muted/20">
                <Zap class="size-6 mb-2 text-primary" />
                <h3 class="font-bold">Real-time Sync</h3>
                <p class="text-sm text-muted-foreground">Using Svelte 5 Runes, the global <code>videoState</code> reacts instantly to WebSocket packets, ensuring 0ms UI lag.</p>
            </Card.Root>
        </div>
    </section>

    <section class="space-y-6 mt-16">
        <div class="flex items-center gap-2">
            <Badge variant="outline">Rendering</Badge>
            <h2 class="text-2xl font-semibold tracking-tight">Why Code (Manim) Beats Pixels</h2>
        </div>

        <Alert.Root>
            <Terminal class="size-4" />
            <Alert.Title>Deterministic Rendering</Alert.Title>
            <Alert.Description>
                By generating Python code (Manim) instead of raw video, we eliminate AI "hallucinations" in text and geometry.
            </Alert.Description>
        </Alert.Root>

        <p class="leading-7 text-muted-foreground">
            For educational content, accuracy is non-negotiable. Manim allows our AI to describe 
            mathematical relationships as code. The result is perfectly anti-aliased vectors, 
            precise timing, and the ability to re-render segments instantly without data loss.
        </p>
        
        
    </section>

    <section class="space-y-6 mt-16">
        <h2 class="text-2xl font-semibold tracking-tight">Pro-Grade Shortcuts</h2>
        <div class="rounded-lg border">
            <div class="grid grid-cols-3 bg-muted/50 p-3 text-sm font-bold">
                <div>Key</div>
                <div>Action</div>
                <div>Purpose</div>
            </div>
            <div class="divide-y">
                <div class="grid grid-cols-3 p-3 text-sm">
                    <div><kbd class="border px-1 rounded bg-muted">J / L</kbd></div>
                    <div>Seek 4s</div>
                    <div class="text-muted-foreground">Rapid scrubbing</div>
                </div>
                <div class="grid grid-cols-3 p-3 text-sm">
                    <div><kbd class="border px-1 rounded bg-muted">, / .</kbd></div>
                    <div>Frame Step</div>
                    <div class="text-muted-foreground">Precision alignment</div>
                </div>
                <div class="grid grid-cols-3 p-3 text-sm">
                    <div><kbd class="border px-1 rounded bg-muted">F</kbd></div>
                    <div>Fullscreen</div>
                    <div class="text-muted-foreground">Review mode</div>
                </div>
            </div>
        </div>
    </section>

    <section class="space-y-6 mt-16 p-8 bg-primary/5 rounded-3xl border border-primary/20 relative overflow-hidden">
        <div class="relative z-10">
            <h2 class="text-3xl font-bold tracking-tight mb-4">Pure Creative Play</h2>
            <p class="text-muted-foreground max-w-2xl">
                We believe video editing should feel like <strong>directing</strong>, not data entry. 
                The integration of a Unity-based 3D preview environment creates a "spatial" 
                editing experience, making the AI feedback loop tactile, fun, and incredibly fast.
            </p>
        </div>
        <div class="absolute -right-10 -bottom-10 opacity-10">
            <Rocket class="size-64" />
        </div>
    </section>
</div>