<script lang="ts">
    import UnityPlayer from "$lib/components/UnityPlayer.svelte";

    let unityPlayer: UnityPlayer | undefined = $state();

    $effect(() => {
        setTimeout(() => {
            unityPlayer?.changeBackgroundColor("#4f00aa");
            unityPlayer?.startTyping("Hello, this is a test of the Unity Svelte integration!");
        }, 5000)
    });
</script>

<!-- Put whatever height and width you want, the UnityPlayer will fill it -->
<div style="height: 50vh;">
    <UnityPlayer bind:this={unityPlayer}/>
</div>