<script lang="ts">
    import { onMount } from 'svelte';

    let { 
        like = false, 
        desc = "", 
        url = "" 
    } = $props<{
        like?: boolean;
        desc?: string;
        url?: string;
    }>();

    let isLiked = $state(like);
    let overlayHeart = $state<SVGElement>();
    let likesCount = $state(isLiked ? 101 : 100);

    function toggleLike(triggerAnimation = false) {
        isLiked = !isLiked;
        
        // Update likes count based on state
        if (isLiked) {
            likesCount = 101;
            if (triggerAnimation) {
                playOverlayAnimation();
            }
        } else {
            likesCount = 100;
        }
    }

    function playOverlayAnimation() {
        if (!overlayHeart) return;
        
        // Reset animation
        overlayHeart.classList.remove('animate');
        void overlayHeart.getBoundingClientRect(); // Trigger reflow
        overlayHeart.classList.add('animate');
    }

    function handleImageDoubleClick() {
        if (!isLiked) {
            toggleLike(true);
        } else {
            playOverlayAnimation();
        }
    }

    // Dummy variable to prevent CSS purging of .animate class
    let animateClassPlaceholder = false;

    onMount(() => {
        if (like) {
            setTimeout(() => {
                playOverlayAnimation();
            }, 500);
        }
    });
</script>

<div class="post-card">
    <div class="post-header">
        <div class="user-avatar"></div>
        <span class="username">minimal_user</span>
    </div>
    
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div 
        class="post-image-container" 
        on:dblclick={handleImageDoubleClick}
    >
        <img src={url} alt="Post Image" class="post-image">
        <svg 
            bind:this={overlayHeart}
            class="like-heart-overlay" 
            class:animate={animateClassPlaceholder}
            width="120" 
            height="120" 
            viewBox="0 0 24 24"
        >
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
    </div>

    <div class="post-actions">
        <button 
            class="action-btn" 
            class:liked={isLiked} 
            on:click={() => toggleLike(false)}
            aria-label="Like"
        >
            <svg viewBox="0 0 24 24">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
        </button>
        <button class="action-btn" aria-label="Comment">
            <svg viewBox="0 0 24 24">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
            </svg>
        </button>
        <button class="action-btn" aria-label="Share">
            <svg viewBox="0 0 24 24">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
        </button>
    </div>

    <div class="post-content">
        <span class="likes-count">{likesCount} likes</span>
        <div class="description">
            <span class="username-text">minimal_user</span>
            {desc}
        </div>
    </div>
</div>

<style>
    .post-card {
        background-color: white;
        border: 1px solid #dbdbdb;
        border-radius: 3px;
        width: 100%;
        max-width: 160px; /* Scaled down ~3x from 470px */
        display: flex;
        flex-direction: column;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        overflow: hidden;
    }

    /* Header */
    .post-header {
        padding: 6px 8px;
        display: flex;
        align-items: center;
        flex-shrink: 0;
    }
    
    .user-avatar {
        width: 18px; /* Scaled down */
        height: 18px;
        border-radius: 50%;
        background-color: #eee;
        margin-right: 6px;
    }

    .username {
        font-weight: 600;
        font-size: 10px; /* Scaled down */
        color: #262626;
    }

    /* Image Container */
    .post-image-container {
        position: relative;
        width: 100%;
        aspect-ratio: 1 / 1; /* Keep square aspect ratio */
        background-color: #f0f0f0;
        overflow: hidden;
        cursor: pointer;
    }

    .post-image {
        width: 100%;
        height: 100%;
        object-fit: cover; /* Fill the square */
    }

    /* Big Heart Animation (Overlay) */
    .like-heart-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        z-index: 10;
        transform: translate(-50%, -50%) scale(0);
        pointer-events: none;
        opacity: 0;
        transition: transform 300ms ease-in-out;
    }

    .like-heart-overlay path {
        fill: white;
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.4));
    }

    /* Big heart size scaled down */
    .like-heart-overlay {
        width: 60px;
        height: 60px;
    }

    /* Using global to ensure animation class works if scoped styles cause issues, 
       but standard class selector should work fine in Svelte. 
       However, keyframes are scoped. */
    .like-heart-overlay.animate {
        animation: like-bounce 1500ms ease-in-out forwards;
    }

    @keyframes like-bounce {
        0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
        15% { transform: translate(-50%, -50%) scale(1.5); opacity: 0.9; }
        30% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
        80% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
    }

    /* Actions Bar */
    .post-actions {
        padding: 6px 8px;
        display: flex;
        gap: 10px;
        flex-shrink: 0;
    }

    .action-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        transition: transform 0.1s ease-in-out;
    }
    
    .action-btn:active {
        transform: scale(0.9);
    }

    .action-btn svg {
        width: 16px; /* Scaled down */
        height: 16px;
        fill: none;
        stroke: #262626;
        stroke-width: 2;
    }

    /* Liked State for Button */
    .action-btn.liked svg {
        fill: #ed4956;
        stroke: #ed4956;
        animation: heart-pop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    @keyframes heart-pop {
        0% { transform: scale(1); }
        50% { transform: scale(1.3); }
        100% { transform: scale(1); }
    }

    /* Description */
    .post-content {
        padding: 0 8px 8px;
        flex-shrink: 0;
    }

    .likes-count {
        font-weight: 600;
        font-size: 10px;
        margin-bottom: 4px;
        display: block;
    }

    .description {
        font-size: 10px;
        line-height: 1.2;
    }

    .username-text {
        font-weight: 600;
        margin-right: 3px;
    }
</style>
