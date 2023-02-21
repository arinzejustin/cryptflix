<script lang="ts">
	export let width: string,
		height: string,
		auto: string = 'auto',
  class: string = '';
</script>

<span
	style="--height: {height}; --width: {width}; --auto: {auto}"
	class="loader border-[black_black_transparent] dark:border-[white_white_transparent] h-[var(--height)] mx-[var(--auto)] w-[var(--width)]"
/>

<style>
	.loader {
		@apply rounded-full border-solid border-2 text-center block bg-transparent;
		border-image: initial;
		animation: 0.8s linear 0s infinite normal both running animation;
	}
	@keyframes animation {
		0% {
			transform: rotate(0deg) scale(1);
		}
		50% {
			transform: rotate(180deg) scale(0.8);
		}
		100% {
			transform: rotate(360deg) scale(1);
		}
	}

	@-webkit-keyframes checkmark {
		0% {
			stroke-dashoffset: 50px;
		}

		100% {
			stroke-dashoffset: 0;
		}
	}
</style>
