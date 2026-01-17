<script lang="ts">
    import {onMount, onDestroy} from 'svelte';

    let canvas: HTMLCanvasElement | undefined = $state();
    let container: HTMLDivElement | undefined = $state();

    let unityInstance: any = null;
    let script: HTMLScriptElement | undefined = $state();
    let profilerScript: HTMLScriptElement | undefined = $state();

    export function changeBackgroundColor(color: string) {
        if (unityInstance) {
            unityInstance.SendMessage('SceneManager', 'ChangeBackgroundColor', color);
        }
    }

    export function startTyping(script: string) {
        if (unityInstance) {
            unityInstance.SendMessage('SceneManager', 'StartTyping', script);
        }
    }

    export function changeCharacter(character: 'trump' | 'obama') {
        if (unityInstance) {
            unityInstance.SendMessage('SceneManager', 'ChangeCharacter', character);
        }
    }

    onMount(() => {
        // Load Profiler
        if (!profilerScript) {
            console.log("Loading Profiler");
            profilerScript = document.createElement("script");
            profilerScript.src = "/animation/TemplateData/profiler.js";
            document.body.appendChild(profilerScript);
            console.log("Profiler Loaded");
        }

        // Main logic
        var buildUrl = "/animation/Build";
        var loaderUrl = buildUrl + "/animation.loader.js";
        var config = {
            arguments: [],
            dataUrl: buildUrl + "/animation.data",
            frameworkUrl: buildUrl + "/animation.framework.js",
            codeUrl: buildUrl + "/animation.wasm",
            streamingAssetsUrl: "animation/StreamingAssets",
            companyName: "DefaultCompany",
            productName: "animations",
            productVersion: "1.0",
        };

        script = document.createElement("script");
        script.src = loaderUrl;
        script.onload = () => {
            // @ts-ignore
            createUnityInstance(canvas, config, (progress: number) => {
                // if (progressBarFull) progressBarFull.style.width = 100 * progress + "%"; TODO: Listen to progress
            }).then((instance: any) => {
                unityInstance = instance;

                // @ts-ignore
                // if (typeof unityProfiler !== 'undefined' && buildTitle) {
                //      // @ts-ignore
                //     var profile = unityProfiler.createButton(unityInstance);
                //     profile.style.marginLeft = '5px';
                // }

                var quit = document.createElement("button");
                quit.style.cssText = "margin-left: 5px; background-color: lightgray; border: none; padding: 5px; cursor: pointer";
                quit.innerHTML = "Unload";
                quit.onclick = () => {
                    unityInstance.Quit().then(() => {
                        // @ts-ignore
                        if (typeof unityProfiler !== 'undefined') unityProfiler.shutDown();
                        if (container) container.remove();
                        // @ts-ignore
                        canvas = null;
                        script?.remove();
                        // @ts-ignore
                        script = null;
                    });
                };
            }).catch((message: any) => {
                alert(message);
            });
        };
        document.body.appendChild(script);
    });

    onDestroy(() => {
        // Basic cleanup to prevent memory leaks if component is unmounted
        if (unityInstance) {
            // Note: Unity Quit is async, and might not be safe to call during component destruction if not carefully handled.
            // But usually it's better to try to quit.
            // unityInstance.Quit().catch(() => {});
        }
        if (script && script.parentNode) script.parentNode.removeChild(script);
        if (profilerScript && profilerScript.parentNode) profilerScript.parentNode.removeChild(profilerScript);
    });
</script>

<svelte:head>
    <link rel="stylesheet" href="/animation/TemplateData/style.css">
</svelte:head>

<div id="unity-container" class="unity-desktop" bind:this={container}>
    <canvas id="unity-canvas" tabindex="-1" bind:this={canvas}></canvas>
</div>

<style>
    #unity-container {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #231F20;
    }

    #unity-canvas {
        width: -webkit-fill-available;
        height: -webkit-fill-available;
        outline: none;
    }

    .unity-mobile {
        width: 100% !important;
        height: 100% !important;
        touch-action: none;
    }
</style>