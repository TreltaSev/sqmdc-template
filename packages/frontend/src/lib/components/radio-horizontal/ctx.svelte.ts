import { getContext, setContext } from "svelte";
import type { ClassValue } from "svelte/elements";

class StyleContext {
    public buttonClass: ClassValue = $state<ClassValue>('')
    public classButton: ClassValue = $state<ClassValue>('')
}

export function createRadioHorizontal() {

    const _class = new StyleContext();


    return { _class }
}

export function getRadioHorizontalData() {
    const NAME = "radiohorizontal-ctx" as const;
    return {
        NAME
    }
}

export function setRadioHorizontalCtx() {
    const { NAME } = getRadioHorizontalData();

    const radiohorizontal = {
        ...createRadioHorizontal()
    }

    setContext(NAME, radiohorizontal)

    return {
        ...radiohorizontal
    }
}

type RadioHorizontalGetReturn = ReturnType<typeof setRadioHorizontalCtx>;
export function getRadioHorizontalCtx() {
    const { NAME } = getRadioHorizontalData();
    return getContext<RadioHorizontalGetReturn>(NAME)
}