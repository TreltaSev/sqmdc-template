import type { ClassValue, HTMLInputAttributes } from "svelte/elements";

export type tInputProps = HTMLInputAttributes & {
    // Classes:

    // --- Default Classes:
    inputClass?: ClassValue,
    labelClass?: ClassValue,

    classLabel?: ClassValue
    
    // Extra Props Here:
    label?: string,

};