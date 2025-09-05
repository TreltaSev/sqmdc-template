import type { ClassValue, HTMLAttributes } from "svelte/elements";
import type { tHeaderProps as skHeaderProps } from "sk-clib/ui";


export type tHeaderProps = HTMLAttributes<HTMLHeadingElement> & skHeaderProps & {
    headerClass?: ClassValue,
};