<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import Icon from './Icon.svelte';

	let navbar = [
			{
				url: '/app',
				class: '',
				name: 'Dashboard',
				svg: ''
			},
			{
				url: '/app/inbox',
				class: 'mb-4',
				name: 'Inbox',
				svg: ''
			},
			{
				url: '/app/transaction/withdraw',
				class: 'mt-4',
				name: 'Withdraw',
				svg: ''
			},
			{
				url: '/app/transaction/deposit',
				class: '',
				name: 'Invest',
				svg: ''
			},
			{
				url: '/app/transaction/market',
				class: 'mb-4',
				name: 'Market',
				svg: ''
			},
			{
				url: '/app/news',
				class: 'mt-3',
				name: 'News',
				svg: ''
			}
		],
		aside = () => {};

	onMount(() => {
		aside = () => {
			var side = document.querySelector('aside')!,
				slot = document.querySelector('#slot')!,
				header = document.querySelector('#header')!;
			setTimeout(() => {
				side.classList.remove('mdc-drawer--open');
				slot.classList.remove('hidden');
				header.classList.remove('hidden');
			}, 2500);
		};
	});
</script>

<div class="overflow-y-auto">
	<div class="mb-8 mt-6 pt-4 grid grid-row-2 gap-2">
		<img src="/logo.png" alt="" class="w-16 h-16 mx-auto" />
		<p class="text-xs uppercase font-mono text-center">Lifting souls through crypto</p>
	</div>
	<div class="mt-5 pt-4">
		{#each navbar as links}
			<div class="py-3 group/item px-3 font-open">
				<!-- svelte-ignore a11y-missing-content -->
				<a
					on:click={() => {
						aside();
					}}
					href={links.url}
					class="{$page.url.pathname === links.url
						? 'bg-yellow-100 theme-text-app dark:bg-yellow-100/20 transform group-hover/item:bg-bg-yellow-100 dark:group-hover/item:bg-yellow-100/20'
						: 'group-hover/item:bg-slate-500/10 group-hover/item:translate-x-2 dark:group-hover/item:bg-slate-500/30'} flex flex-auto px-2 items-center rounded-md transition-all duration-100 py-3.5 {links.class}"
				>
					<svg
						class="w-5 h-5 mx-2 text-slate-700 dark:text-slate-50"
						xmlns="http://www.w3.org/2000/svg"
						width="1.13em"
						height="1em"
						viewBox="0 0 36 32"
						><rect x="0" y="0" width="36" height="32" fill="none" stroke="none" /><path
							fill="currentColor"
							d="M.5 31.983a.503.503 0 0 0 .612-.354c1.03-3.843 5.216-4.839 7.718-5.435c.627-.149 1.122-.267 1.444-.406c2.85-1.237 3.779-3.227 4.057-4.679a.5.5 0 0 0-.165-.473c-1.484-1.281-2.736-3.204-3.526-5.416a.492.492 0 0 0-.103-.171c-1.045-1.136-1.645-2.337-1.645-3.294c0-.559.211-.934.686-1.217a.5.5 0 0 0 .243-.408C10.042 5.036 13.67 1.026 18.12 1l.107.007c4.472.062 8.077 4.158 8.206 9.324a.498.498 0 0 0 .178.369c.313.265.459.601.459 1.057c0 .801-.427 1.786-1.201 2.772a.522.522 0 0 0-.084.158c-.8 2.536-2.236 4.775-3.938 6.145a.502.502 0 0 0-.178.483c.278 1.451 1.207 3.44 4.057 4.679c.337.146.86.26 1.523.403c2.477.536 6.622 1.435 7.639 5.232a.5.5 0 0 0 .966-.26c-1.175-4.387-5.871-5.404-8.393-5.95c-.585-.127-1.09-.236-1.336-.344c-1.86-.808-3.006-2.039-3.411-3.665c1.727-1.483 3.172-3.771 3.998-6.337c.877-1.14 1.359-2.314 1.359-3.317c0-.669-.216-1.227-.644-1.663C27.189 4.489 23.19.076 18.227.005l-.149-.002c-4.873.026-8.889 4.323-9.24 9.83c-.626.46-.944 1.105-.944 1.924c0 1.183.669 2.598 1.84 3.896c.809 2.223 2.063 4.176 3.556 5.543c-.403 1.632-1.55 2.867-3.414 3.676c-.241.105-.721.22-1.277.352c-2.541.604-7.269 1.729-8.453 6.147a.5.5 0 0 0 .354.612z"
						/></svg
					>
					<span class="text-center ml-4 text-base">{links.name}</span>
				</a>
			</div>
		{/each}
		<div class="grid grid-cols-4 gap-4 items-center align-middle mx-3 my-5">
			<div
				class="bg-yellow-200 dark:bg-yellow-100/30 rounded-full items-center text-slate-900 dark:text-slate-50 text-center p-3 ring-1 ring-transparent hover:ring-yellow-300 ring-offset-2 ring-offset-transparent"
			>
				<Icon name={'facebook'} className={'material-icons w-12'} />
			</div>
			<div
				class="bg-yellow-200 dark:bg-yellow-100/30 rounded-full items-center text-slate-900 dark:text-slate-50 text-center p-3 ring-1 ring-transparent hover:ring-yellow-300 ring-offset-2 ring-offset-transparent"
			/>
			<div
				class="bg-yellow-200 dark:bg-yellow-100/30 rounded-full items-center text-slate-900 dark:text-slate-50 text-center p-3 ring-1 ring-transparent hover:ring-yellow-300 ring-offset-2 ring-offset-transparent"
			/>
			<div
				class="bg-yellow-200 dark:bg-yellow-100/30 rounded-full items-center text-slate-900 dark:text-slate-50 text-center p-3 ring-1 ring-transparent hover:ring-yellow-300 ring-offset-2 ring-offset-transparent"
			/>
		</div>
	</div>
</div>

<style>
</style>
