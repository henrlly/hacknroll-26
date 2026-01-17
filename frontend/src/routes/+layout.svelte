<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { ModeWatcher } from 'mode-watcher';
	import { Film } from "@lucide/svelte";
	import GithubIcon from "$lib/components/github.svelte";
	import { Button } from '$lib/components/ui/button';
	import Separator from "$lib/components/ui/separator/separator.svelte";
	import ModeSwitcher from '$lib/components/mode-switcher.svelte';
	import { onMount } from 'svelte';
	import { connectWebSocket } from '$lib/socket.svelte';

	onMount(() => {
		connectWebSocket();
	})

	let { children } = $props();
</script>

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
<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}