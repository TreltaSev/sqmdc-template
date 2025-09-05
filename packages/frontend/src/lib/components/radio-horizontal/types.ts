import type { ClassValue, HTMLAttributes, HTMLButtonAttributes } from "svelte/elements";

export type tRadioHorizontalProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    radiohorizontalClass?: ClassValue,
    buttonClass?: ClassValue

    // --- User Defined Classes:
    classButton?: ClassValue,
    
    // Extra Props Here:
    name?: string

};

export type tRadioHorizontalButtonProps = HTMLButtonAttributes & {
    // Classes:

    // --- Default Classes:
    buttonClass?: ClassValue,
    
    // Extra Props Here:
    href?: string
};