/* eslint-disable @typescript-eslint/no-explicit-any */
import { cubicOut } from 'svelte/easing';

export function expand(node: HTMLElement, params: any, { duration = 300 }) {
	const height = node.scrollHeight;

	return {
		duration,
		easing: params.easing || cubicOut,
		css: (t: number) =>
			`height: ${t * height}px; opacity: ${t}; margin-top: ${t * (params.offset !== undefined ? params.offset : 8)}px;`
	};
}
