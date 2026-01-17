<script lang="ts">
    import { onMount } from 'svelte'

    let { originalText, scrambledText = $bindable(""), speed = 1 } = $props();

    onMount(() => {
        let currentIndex = 0;
        scrambledText = ""; // Start empty

        const interval = setInterval(() => {
            if (currentIndex < originalText.length) {
                currentIndex++;
                scrambledText = originalText.slice(0, currentIndex);
            } else {
                clearInterval(interval);
            }
        }, speed);

        return () => clearInterval(interval); // Cleanup if component unmounts
    })
</script>

<div class="sr-only">
    {scrambledText}
</div>