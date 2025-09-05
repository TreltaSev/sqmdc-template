/* eslint-disable @typescript-eslint/no-explicit-any */
import { getContext, setContext } from 'svelte';
import { type Steps } from './types';

export class StepsHelpers {
	public ctx: StepsContext;

	constructor(ctx: StepsContext) {
		this.ctx = ctx;

		for (const key of Object.getOwnPropertyNames(Object.getPrototypeOf(this))) {
			const value = this[key as keyof this];
			if (typeof value === 'function' && key !== 'constructor') {
				this[key as keyof this] = value.bind(this);
			}
		}
	}

	/**
	 * Switches to the previous step if there is one
	 */
	public previous() {
		if (this.ctx.step - 1 < 0) {
			return;
		}
		this.ctx.step++;
	}

	/**
	 * Gets the recorded step value via a given step number
	 * @param step - Step number
	 * @returns
	 */
	public get_step(step: number) {
		return this.ctx.steps[step];
	}

	/**
	 * Gets the index of a step by its name.
	 * Throws an error if the step name is not found.
	 *
	 * @param name - The name of the step to find
	 * @returns The index of the step
	 * @throws Error if the step name is not found in the steps array
	 */
	public get_step_idx(name: string): number {
		const index = this.ctx.steps.findIndex((step) => step.name === name);
		if (index === -1) {
			throw new Error(`Step with name "${name}" not found`);
		}
		return index;
	}

	/**
	 * Switches the current step to the next step if there is one
	 */
	public next(event: Event) {
		event.preventDefault(); // Stop Default Behavior
		this.captureForm(event);

		if (this.ctx.steps.length <= this.ctx.step + 1) {
			return;
		}

		this.ctx.step++;
	}

	/**
	 * Saves a single key–value pair into the global data store.
	 * This is not scoped to any step.
	 *
	 * @param key - Key under which to store the data
	 * @param data - The actual value to store
	 */
	public inject(key: string, data: any) {
		this.ctx.data = {
			...this.ctx.data,
			[key]: data
		};
	}
	/**
	 * Extracts form data from the current step’s HTMLFormElement
	 * and stores it under that step’s name in the context data.
	 *
	 * @param event - The submit event containing the target form
	 */
	public captureForm(event: Event) {
		const target = event.target as HTMLFormElement | null;
		if (!target) return;
		const data = Object.fromEntries(new FormData(target));
		const _step = this.get_step(this.ctx.step);
		this.ctx.data = {
			...this.ctx.data,
			[_step.name]: data
		};
	}

	/**
	 * Collects and merges data from a specified set of step names.
	 * Useful for getting partial form state or validating certain steps.
	 *
	 * @param from - A list of step names to pull data from
	 * @returns Combined data from the selected steps
	 */
	public mergeSteps(...from: string[]): Record<string, any> {
		const compiled: Record<string, any> = {};
		for (const stepName of from) {
			if (stepName in this.ctx.data) {
				Object.assign(compiled, this.ctx.data[stepName]);
			}
		}
		return compiled;
	}

	/**
	 * Merges data from all steps into a single object.
	 *
	 * @returns Fully compiled step data
	 */
	public mergeAllSteps(): Record<string, any> {
		return Object.assign({}, ...Object.values(this.ctx.data));
	}
}

class StepsContext {
	public helpers = new StepsHelpers(this);
	public steps = $state<Steps>([]);
	public data = $state<Record<string, any>>({});
	public step = $state<number>(0);
}

export function createSteps() {
	const _ctx = new StepsContext();
	const _helpers = _ctx.helpers;
	return { _ctx, _helpers };
}

export function getStepsData() {
	const NAME = 'steps-ctx' as const;
	return {
		NAME
	};
}

export function setStepsCtx() {
	const { NAME } = getStepsData();

	const register = {
		...createSteps()
	};

	setContext(NAME, register);

	return {
		...register
	};
}

type RegisterGetReturn = ReturnType<typeof setStepsCtx>;
export function getStepsCtx() {
	const { NAME } = getStepsData();
	return getContext<RegisterGetReturn>(NAME);
}
