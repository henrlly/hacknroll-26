<script>
    import InstagramPostCycle from '$lib/components/instagram-post-cycle.svelte';

    const listOfPosts = [
        {
            like: true,
            desc: "Beautiful morning vibes ☀️ #goodmorning #sunrise",
            url: "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        },
        {
            like: false,
            desc: "Coffee time ☕ #coffeelover #morningcoffee",
            url: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        },
        {
            like: true,
            desc: "Weekend adventures 🏔️ #hiking #nature #adventure",
            url: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        },
        {
            like: true,
            desc: "Homemade pizza night 🍕 #foodie #homemade",
            url: "https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        },
        {
            like: false,
            desc: "City lights at night 🌃 #cityscape #urban #photography",
            url: "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        }
    ];
</script>

<div class="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
    <InstagramPostCycle posts={listOfPosts} />
</div>
