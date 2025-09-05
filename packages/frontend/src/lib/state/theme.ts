import { get, writable, type Writable } from "svelte/store";

/**
 * Manages the application's theme state ("light" or "dark") using Svelte stores and localStorage.
 */
class ThemeManager {
    /**
     * Svelte writable store for the current theme.
     */
    theme$: Writable<string> = writable("light");

    constructor() {
        if (typeof window === 'undefined') return;
        const localTheme: string | null = localStorage.getItem("theme");
        this.theme$.set(localTheme || "dark");
    }

    /**
     * Sets the theme to "light" or "dark" and persists it in localStorage.
     * @param value - The theme value ("light" | "dark").
     */
    set(value: "light" | "dark") {
        this.theme$.set(value);
        localStorage.setItem("theme", this.theme);
    }

    /**
     * Gets the current theme value.
     */
    get theme() {
        return get(this.theme$);
    }

    /**
     * Toggles the theme between "light" and "dark", updating localStorage.
     */
    toggle() {
        const isDark = this.theme === "dark";
        this.theme$.set(isDark ? "light" : "dark");
        localStorage.setItem("theme", this.theme);
    }
}

/**
 * Global theme manager instance.
 */
export const global_theme$ = new ThemeManager();