export const generationData = $state({
    generationStep: "INPUT" as "INPUT" | "WRITING SCRIPT" | "DOING TASKS" | "COMPLETED",
    finalScript: "",
    narrations: [],
    assets: [],
    sfx: [],
})