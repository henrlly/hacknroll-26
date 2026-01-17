<script lang="ts">
	import * as Card from "$lib/components/ui/card";
	import { Separator } from "$lib/components/ui/separator";
	import { Badge } from "$lib/components/ui/badge";

	let teamName = "[Team Name]";
</script>

<div class="min-h-screen bg-[#fdfdfc] text-[#1a1a1a] selection:bg-[#fff2cc]">
	<div class="h-1.5 w-full bg-[#1a1a1a]"></div>

	<article class="mx-auto max-w-4xl px-6 py-12 lg:py-24">
		<header class="mb-16 text-center">
			<div class="mb-4 flex items-center justify-center gap-4">
				<span class="font-mono text-[10px] uppercase tracking-[0.3em] text-neutral-500">Vol. MMXXVI — No. 01</span>
			</div>
			
			<h1 class="mb-8 font-serif text-6xl font-black leading-tight tracking-tighter md:text-8xl">
				The Narrative Engine.
			</h1>

			<div class="flex flex-col items-center justify-center gap-4 border-y border-neutral-200 py-4 md:flex-row md:gap-8">
				<p class="font-mono text-[11px] uppercase tracking-widest underline decoration-1 underline-offset-4">
					Dispatch from {teamName}
				</p>
				<p class="font-mono text-[11px] uppercase tracking-widest text-neutral-400">
					Jan 13, 2026
				</p>
				<p class="font-mono text-[11px] uppercase tracking-widest text-neutral-400">
					NUS Hackathon '26
				</p>
			</div>
		</header>

		<section class="mb-20 grid grid-cols-1 gap-8 md:grid-cols-12">
			<div class="md:col-span-4">
				<h2 class="font-mono text-[11px] font-bold uppercase tracking-[0.2em] text-neutral-400">
					The Crisis of Attention
				</h2>
			</div>
			<div class="md:col-span-8">
				<p class="font-serif text-2xl leading-relaxed first-letter:float-left first-letter:mr-3 first-letter:text-8xl first-letter:font-black first-letter:leading-[0.7]">
					Modern learning is failing the "fried brain." In an era of infinite scroll and algorithmic dopamine, the standard academic explainer has become a relic. We are too distracted to read, but too curious to ignore the truth. 
				</p>
				<p class="mt-6 font-serif text-xl leading-relaxed text-neutral-700 italic">
					Our tool bridges this gap. We take the "boring" out of education by using high-octane personas—Donald Trump, Peter Griffin, or your own voice—to teach complex concepts via programmatic motion graphics and agentic transparency.
				</p>
			</div>
		</section>

		<section class="mb-24">
			<div class="mb-8 border-l-4 border-black pl-4">
				<h3 class="font-serif text-3xl font-bold italic">The Transparent Pipeline</h3>
				<p class="font-mono text-xs uppercase tracking-widest text-neutral-400 mt-1">From Prompt to Render</p>
			</div>

			<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
				{#each [
					{ title: "I. Semantic Analysis", desc: "Agent parses prompt using TipTap, identifying verbs for Manim animations and nouns for asset fetching." },
					{ title: "II. Synthesis", desc: "Parallel generation of ElevenLabs narration, Suno Bark backgrounds, and Python-based Manim code blocks." },
					{ title: "III. Composition", desc: "User-steered editor allows for one-click swaps of candidate clips while the agent 'thinks' out loud." }
				] as stage}
					<Card.Root class="rounded-none border-neutral-200 bg-transparent shadow-none">
						<Card.Header class="pb-2">
							<Card.Title class="font-serif text-lg italic">{stage.title}</Card.Title>
						</Card.Header>
						<Card.Content>
							<p class="font-serif text-sm leading-relaxed text-neutral-600">{stage.desc}</p>
						</Card.Content>
					</Card.Root>
				{/each}
			</div>
		</section>

		<section class="mb-20 space-y-16">
			<Separator class="bg-neutral-200" />
			
			<div class="flex flex-col gap-12 md:flex-row">
				<div class="flex-1 space-y-4">
					<Badge variant="outline" class="rounded-none font-mono text-[10px]">VISUALS</Badge>
					<h4 class="font-serif text-3xl font-bold">The Manim Bridge</h4>
					<p class="font-serif text-lg leading-relaxed text-neutral-700">
						Most AI video is a hallucination. {teamName} uses **Manim** to write and execute programmatic Python scripts, ensuring that graphs and technical concepts are mathematically perfect every time.
					</p>
				</div>
				<div class="flex-1 space-y-4">
					<Badge variant="outline" class="rounded-none font-mono text-[10px]">AGENCY</Badge>
					<h4 class="font-serif text-3xl font-bold">User Steering</h4>
					<p class="font-serif text-lg leading-relaxed text-neutral-700">
						We prioritize the "Quality of Result." At any point, users can pause the generation, steer the agent's "Thought Process," and select alternative visual candidates from the right-hand editor.
					</p>
				</div>
			</div>
		</section>

		<footer class="mt-32 border-t-2 border-black pt-12">
			<div class="flex flex-wrap gap-x-12 gap-y-8">
				<div class="space-y-1">
					<p class="font-mono text-[10px] uppercase text-neutral-400">Frontend</p>
					<p class="font-serif font-bold italic">Svelte 5 + Shadcn</p>
				</div>
				<div class="space-y-1">
					<p class="font-mono text-[10px] uppercase text-neutral-400">Backend</p>
					<p class="font-serif font-bold italic">FastAPI + WebSockets</p>
				</div>
				<div class="space-y-1">
					<p class="font-mono text-[10px] uppercase text-neutral-400">Audio</p>
					<p class="font-serif font-bold italic">ElevenLabs / Suno</p>
				</div>
				<div class="space-y-1">
					<p class="font-mono text-[10px] uppercase text-neutral-400">Intelligence</p>
					<p class="font-serif font-bold italic">GPT-4o Agentic Model</p>
				</div>
			</div>
			
			<div class="mt-20 text-center">
				<span class="font-serif text-sm italic text-neutral-400">
					© 2026 {teamName} — Built for the NUS Hackathon
				</span>
			</div>
		</footer>
	</article>
</div>

<style>
	/* Standard New York Times style typography targets */
	:global(body) {
		-webkit-font-smoothing: antialiased;
		text-rendering: optimizeLegibility;
	}
</style>