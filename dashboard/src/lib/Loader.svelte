<script lang="ts">
	export let width: string, height: string;
</script>

<span
	style="--height: {height}; --width: {width}"
	class="loader border-[black_black_transparent] dark:border-[white_white_transparent]"
/>

<style>
	.loader {
		@apply mx-auto rounded-full border-solid border-2 text-center block bg-transparent;
		border-image: initial;
		animation: 0.8s linear 0s infinite normal both running animation;
		width: var(--width);
		height: var(--height);
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
	/* animations */

	@-webkit-keyframes checkmark {
		0% {
			stroke-dashoffset: 50px;
		}

		100% {
			stroke-dashoffset: 0;
		}
	}
</style>
