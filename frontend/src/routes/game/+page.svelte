<script lang="ts">
    import UnityPlayer from "$lib/components/UnityPlayer.svelte";

    let unityPlayer: UnityPlayer | undefined = $state();

    $effect(() => {
        setTimeout(() => {
            unityPlayer?.changeBackgroundColor("#4f00aa");
            unityPlayer?.changeCharacter('obama');
            setTimeout(() => {
                unityPlayer?.startTyping("Hello, this is a test of the Unity Svelte integration!");
                setTimeout(() => {
                    unityPlayer?.startNarration("Hello, this is a test of the Unity Svelte integration!");
                    setTimeout(() => {
                        unityPlayer?.startSfx("dog bark")
                    }, 1000)
                }, 3000);
            }, 1000);

        }, 4000)
    });
</script>

<!-- Put whatever height and width you want, the UnityPlayer will fill it -->
<div style="height: 50vh;">
    <UnityPlayer bind:this={unityPlayer}/>
</div>