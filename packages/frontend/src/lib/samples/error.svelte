<script lang="ts">
	let error =	'No error detection system set up yet. Sample error. Other things to note: it works perfectly on a mobile device but but need work on computer. Make sure to check components and edit any code as needed. Need to make deafult font Poppins.';
</script>

<div class="mt-10 flex flex-col items-center justify-center text-center">
	<!-- Optional messages -->
	{#if error}
		<div
			id="toast-danger"
			class="mb-4 flex w-full max-w-xs items-center rounded-lg bg-[#F0F0F2] p-4 text-gray-500 shadow-sm dark:bg-gray-800 dark:text-gray-400"
			role="alert"
		>
			<div
				class="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-red-100 text-red-500 dark:bg-red-800 dark:text-red-200"
			>
				<svg
					class="h-5 w-5"
					aria-hidden="true"
					xmlns="http://www.w3.org/2000/svg"
					fill="currentColor"
					viewBox="0 0 20 20"
				>
					<path
						d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"
					/>
				</svg>
				<span class="sr-only">Error icon</span>
			</div>
			<div class="ms-3 text-sm">{error}</div>
		</div>
	{/if}
</div>
