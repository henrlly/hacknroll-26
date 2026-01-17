<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { ModeWatcher } from 'mode-watcher';
	import { Film } from "@lucide/svelte";
	import GithubIcon from "$lib/components/github.svelte";
	import { Button } from '$lib/components/ui/button';
	import Separator from "$lib/components/ui/separator/separator.svelte";
	import ModeSwitcher from '$lib/components/mode-swticher.svelte';
	import { onMount } from 'svelte';
	import { connectWebSocket } from '$lib/socket.svelte';

	onMount(() => {
		connectWebSocket();
	})
	let { children } = $props();
</script>

<div class="flex h-screen w-full flex-col overflow-hidden">
	<ModeWatcher />
	<header class="flex w-full justify-between items-center p-2 pt-4 px-6 mb-4">
		<div class="flex gap-4 items-center text-sm">
			<a href="/">
				<Film />
			</a>
			<a href="/">Try</a>
			<a href="/examples">Examples</a>
			<a href="/docs">Docs</a>
		</div>
		<div class="flex gap-2 h-4 items-center">
			<Button target="_blank" href="https://github.com/henrlly/DO-NOT-SUBMIT-2026" variant="ghost">
				<GithubIcon class="size-5" />
			</Button>
			<Separator class="h-1/2" orientation="vertical" />
			<ModeSwitcher />
		</div>
	</header>
	
    <main class="flex-grow overflow-hidden">
		{@render children()}
    </main>
</div>
<svelte:head>
	<link rel="icon" href={favicon} />
	<style>
		/* Kill default browser margins that cause small scrolls */
		body { margin: 0; padding: 0; overflow: hidden; }
	</style>
</svelte:head>
