<script lang="ts">
	import { videoState } from "$lib/stores/generation-data.svelte";
	import UnityPlayer from "$lib/components/UnityPlayer.svelte";

    let unityPlayer: UnityPlayer | undefined = $state();
	let displayedScript = $state("");

	function startTypewriter(text: string, speed = 1) {
        displayedScript = "";
        let i = 0;
    
        const timer = setInterval(() => {
            if (i < text.length) {
                displayedScript += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    }

    $effect(() => {
        if (videoState) {
            startTypewriter(videoState.full_script);
        }
    });
	
	$effect(() => {
		setTimeout(() => {
			unityPlayer?.changeBackgroundColor("#09090b");
			unityPlayer?.startTyping(videoState.full_script);
		}, 5000)
	})
</script>

<div class="flex flex-col justify-center items-center w-full h-[90vh] gap-6">
	<div class="h-full w-[90%] rounded-3xl">
		 <UnityPlayer bind:this={unityPlayer}/>
	</div>
</div>
