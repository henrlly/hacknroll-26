<script lang="ts">
    import InstagramPost from '$lib/components/instagram-post.svelte';
    
    let { data } = $props();
</script>

<div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-6xl mx-auto">
        <header class="mb-12 text-center">
            <h1 class="text-4xl font-bold text-gray-900 mb-4">Example Generations</h1>
            <p class="text-lg text-gray-600">Browse through the library of AI-generated short-form content.</p>
        </header>

        {#if data.videos.length === 0}
            <div class="text-center p-20 bg-white rounded-xl border-2 border-dashed border-gray-200">
                <p class="text-gray-500 text-lg">No example videos found in static/examples/</p>
            </div>
        {:else}
            <div class="flex flex-col gap-12 items-center">
                {#each data.videos as video}
                    <div class="w-full max-w-sm bg-black rounded-xl overflow-hidden shadow-lg">
                        <video src="/examples/{video}" autoplay controls loop muted class="w-full"></video>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>
