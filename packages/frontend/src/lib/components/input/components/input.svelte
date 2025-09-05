<script lang="ts">
	import { cn } from '@lib/utils';
	import type { Props } from '..';
	import Eye from '~icons/heroicons/eye';
	import EyeSlash from '~icons/heroicons/eye-slash';

	let {
		type = '',
		children,
		class: className,
		inputClass = $bindable(
			'dark:bg-[#3E3E55] bg-[#F0F0F2] truncate dark:text-white dark:outline-0 outline box-border outline-[#e0e0e2] rounded-3 px-3 py-4 w-full text-[14px] rounded-[12px] px-4 py-3'
		),
		labelClass = $bindable('text-[#858597] text-[14px]'),
		classLabel = $bindable(''),
		label = $bindable(undefined),
		...rest
	}: Props = $props();

	const inputId = rest.id ?? 'hs-input-' + crypto.randomUUID();

	// --- reactive classes
	let inputCls = $state(cn(inputClass, className));
	let labelCls = $state(cn(labelClass, classLabel));
	$effect(() => {
		inputCls = cn(inputClass, className);
		labelCls = cn(labelClass, classLabel);
	});

	// --- password toggling
	let showPassword = $state(false);
	function togglePassword() {
		showPassword = !showPassword;
	}
</script>

{#if label !== undefined}
	<label class={labelCls} for={inputId}>{label}</label>
{/if}

{#if type === 'password'}
	<div class={cn("relative", inputCls)}>
		<input id={inputId} type={showPassword ? 'text' : 'password'} {...rest} />

		<button
			type="button"
			onclick={togglePassword}
			class="absolute inset-y-0 end-0 z-20 flex cursor-pointer items-center rounded-e-md px-3 text-gray-400 dark:text-white focus:text-blue-600 focus:outline-none dark:focus:text-blue-500"
			aria-label="Toggle password visibility"
		>
			<!-- eye / eye‑off icon -->
			{#if showPassword}
				<!-- eye‑off -->
				<EyeSlash/>
			{:else}
				<!-- eye -->
				<Eye/>
			{/if}
		</button>
	</div>
{:else}
	<!-- Plain input -->
	<input class={inputCls} id={inputId} {type} {...rest} />
{/if}
