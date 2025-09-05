import type { ClassValue, HTMLInputAttributes } from "svelte/elements";

export type tCodeInputProps = HTMLInputAttributes & {
    // Classes:
    classWrapper?: ClassValue,
    classContainer?: ClassValue,
    

    // --- Default Classes:
    wrapperClass?: ClassValue
    containerClass?: ClassValue,
    codeInputClass?: ClassValue,

    
    // Extra Props Here:
    length?: number


};