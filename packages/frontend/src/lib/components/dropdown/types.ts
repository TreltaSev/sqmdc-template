import type { ClassValue, HTMLAttributes, HTMLButtonAttributes } from "svelte/elements";

export type tDropdownProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    dropdownClass?: ClassValue,
    buttonClass?: ClassValue
    contentClass?: ClassValue,
    dividerClass?: ClassValue

    // --- User Defined Classes:
    classButton?: ClassValue,
    classContent?: ClassValue,
    classDivider?: ClassValue
    
    // Extra Props Here:
    name?: string

};

export type tDropdownButtonProps = HTMLButtonAttributes & {
    // Classes:

    // --- Default Classes:
    buttonClass?: ClassValue,
    
    // Extra Props Here:
    href?: string
};
export type tDropdownDividerProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    dividerClass?: ClassValue,
    
    // Extra Props Here:
};
export type tDropdownContentProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    contentClass?: ClassValue,
    
    // Extra Props Here:
};
export type tDropdownTriggerProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    triggerClass?: ClassValue,
    
    // Extra Props Here:
};