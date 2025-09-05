import type { Component } from "svelte";
import type { ClassValue, HTMLAttributes } from "svelte/elements";
import type { StepsHelpers } from "./ctx.svelte";


export type Step = {name: string, component: Component}
export type Steps = Step[]

export type tStepsProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    stepsClass?: ClassValue,
    
    // Extra Props Here:
    steps?: Steps,
    step?: number,
    helper?: StepsHelpers 
};