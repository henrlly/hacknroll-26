<script lang="ts">
    import { quintOut } from 'svelte/easing';
    import InstagramPost from './instagram-post.svelte';

    type Post = {
        liked: boolean;
        desc: string;
        url: string;
    };

    let { 
        posts = [], 
        displayDuration = 1000, 
        pauseDuration = 500, 
        animDuration = 500
    } = $props<{
        posts?: Post[];
        displayDuration?: number;
        pauseDuration?: number;
        animDuration?: number;
    }>();

    let currentIndex = $state(0);
    let visible = $state(true);

    $effect(() => {
        if (posts.length === 0) return;

        let timeout: ReturnType<typeof setTimeout>;

        if (visible) {
            timeout = setTimeout(() => {
                visible = false;
            }, displayDuration);
        } else {
            timeout = setTimeout(() => {
                currentIndex = (currentIndex + 1) % posts.length;
                visible = true;
            }, animDuration + pauseDuration);
        }

        return () => clearTimeout(timeout);
    });

    // Custom transition: Fly + Scale
    function flyAndScale(node: Element, { 
        y = 0, 
        start = 0.5, 
        duration = 400, 
        easing = quintOut 
    }: { y?: number, start?: number, duration?: number, easing?: any } = {}) {
        const style = getComputedStyle(node);
        const transform = style.transform === 'none' ? '' : style.transform;
        
        return {
            duration,
            easing,
            css: (t: number) => `
                transform: ${transform} translate3d(0, ${(1 - t) * y}px, 0) scale(${start + (1 - start) * t});
                opacity: ${t};
            `
        };
    }
</script>

<div 
    class="relative flex items-center justify-center h-full w-full overflow-hidden"
    style="mask-image: linear-gradient(to bottom, transparent, black 20%, black 80%, transparent); -webkit-mask-image: linear-gradient(to bottom, transparent, black 20%, black 80%, transparent);"
>
    {#if visible && posts.length > 0}
        <div 
            in:flyAndScale={{ y: 50, start: 0.8, duration: animDuration }}
            out:flyAndScale={{ y: -50, start: 0.8, duration: animDuration }}
            class="absolute inset-0 flex items-center justify-center p-2"
        >
            <InstagramPost
                like={posts[currentIndex].liked}
                desc={posts[currentIndex].desc}
                url={posts[currentIndex].url}
            />
        </div>
    {/if}
</div>
