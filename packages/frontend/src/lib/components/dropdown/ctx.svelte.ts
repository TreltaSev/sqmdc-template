import { getContext, setContext } from "svelte";
import type { ClassValue } from "svelte/elements";

class DropdownContext {
    public active: boolean = $state<boolean>(false)
    public content_reference: HTMLDivElement | undefined = $state<HTMLDivElement | undefined>(undefined)
}

class StyleContext {
    public buttonClass: ClassValue = $state<ClassValue>('')
    public contentClass: ClassValue = $state<ClassValue>('')
    public dividerClass: ClassValue = $state<ClassValue>('')

    public classButton: ClassValue = $state<ClassValue>('')
    public classContent: ClassValue = $state<ClassValue>('')
    public classDivider: ClassValue = $state<ClassValue>('')
}

export type tDropdownData = {
    active?: boolean,
    content_reference?: HTMLDivElement
}

export function createDropdown() {

    const _state = new DropdownContext();
    const _class = new StyleContext();


    function toggle() {
        _state.active = !_state.active;
    }

    function set(value: boolean) {
        _state.active = value
    }

    return {_state, _class, toggle, set}
}

export function getDropdownData() {
    const NAME = "dropdown-ctx" as const;
    return {
        NAME
    }
}

export function setDropdownCtx() {
    const { NAME } = getDropdownData();

    const dropdown = {
        ...createDropdown()
    }

    setContext(NAME, dropdown)

    return {
        ...dropdown
    }
}

type DropdownGetReturn = ReturnType<typeof setDropdownCtx>;
export function getDropdownCtx() {
    const { NAME } = getDropdownData();
    return getContext<DropdownGetReturn>(NAME)
}