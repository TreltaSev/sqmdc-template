import type { ClassValue, HTMLAttributes } from "svelte/elements";
import type { tTextProps as skTextProps } from "sk-clib";


export type tTextProps = HTMLAttributes<HTMLSpanElement> & skTextProps & {
    textClass?: ClassValue,
};