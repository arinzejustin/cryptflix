<script lang="ts">
	import Loader from '$lib/Loader.svelte';
	import Plan from '../components/Plan.svelte';
	import { onMount } from 'svelte';
	import Badge from '@smui-extra/badge';
	import { fly } from 'svelte/transition';
	import API from '$lib/api';
	import { getStorage } from '$lib/storage';
	import { goto } from '$app/navigation';

	export let loading = true,
		src: string,
		open: boolean,
		height: number,
		plan: string;

	let shadow = false,
		menu = false,
		active = false;

	var logout = async () => {
			try {
				const req = await API.get('/logout', '', { Authorization: token });
				if (req.ok) goto('/0auth/login', { keepFocus: true, replaceState: true });
			} catch (error) {
				goto('/0auth/logout', { replaceState: true });
			}
		},
		token: any;

	onMount(() => {
		addEventListener('scroll', () => {
			if (window.scrollY > 50) shadow = true;
			else shadow = false;
		});
		if (window.scrollY > 50) shadow = true;
		//@ts-ignore
		height = document.querySelector('#header')!.offsetHeight;
		onresize = () => {
			//@ts-ignore
			height = document.querySelector('#header')!.offsetHeight;
		};
		token = getStorage('token');
	});
</script>

<header class="relative">
	<div
		id="header"
		class="fixed bg-white transition-all duration-500 dark:bg-black text-slate-700 dark:text-slate-100 right-0 top-0 border-solid border-b border-color {open
			? 'left-[256px]'
			: 'left-0'} {shadow
			? 'shadow-lg dark:shadow-md dark:shadow-slate-400 backdrop-blur-md bg-white/[0.75] dark:bg-black/[0.65]'
			: ''}"
	>
		<div class="flex flex-row items-center align-middle justify-between mx-4 py-3.5 md:py-4">
			<div class="flex flex-row items-center align-middle justify-between">
				<div class="md:hidden">
					<svg
						class="text-slate-700 dark:text-white w-8 h-8"
						xmlns="http://www.w3.org/2000/svg"
						width="1em"
						height="1em"
						viewBox="0 0 24 24"
						><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
							fill="currentColor"
							d="M4 18q-.425 0-.712-.288Q3 17.425 3 17t.288-.712Q3.575 16 4 16h16q.425 0 .712.288q.288.287.288.712t-.288.712Q20.425 18 20 18Zm0-5q-.425 0-.712-.288Q3 12.425 3 12t.288-.713Q3.575 11 4 11h16q.425 0 .712.287q.288.288.288.713t-.288.712Q20.425 13 20 13Zm0-5q-.425 0-.712-.287Q3 7.425 3 7t.288-.713Q3.575 6 4 6h16q.425 0 .712.287Q21 6.575 21 7t-.288.713Q20.425 8 20 8Z"
						/></svg
					>
				</div>
				<div />
			</div>
			<div class="md:mr-4 relative">
				{#if loading}
					<div class="mr-4 md:mr-6">
						<Loader width={'30px'} height={'30px'} />
					</div>
				{:else}
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<div
						class="flex flex-row justify-between cursor-pointer align-middle items-center"
						on:click={() => (menu = !menu)}
					>
						<img
							{src}
							srcset="{src} 2x"
							alt=""
							class="border-solid border-2 border-color w-8 h-8 md:w-10 md:h-10 rounded-full"
						/>
						<div>
							<svg
								class="text-slate-700 dark:text-slate-500 w-4 h-4 ml-1.5 md:ml-3"
								xmlns="http://www.w3.org/2000/svg"
								width="1em"
								height="1em"
								viewBox="0 0 24 24"
								><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><g
									transform="rotate({menu ? '90' : '-90'} 12 12)"
									><path
										fill="currentColor"
										d="M15.125 21.1L6.7 12.7q-.15-.15-.212-.325q-.063-.175-.063-.375t.063-.375q.062-.175.212-.325l8.425-8.425q.35-.35.875-.35t.9.375q.375.375.375.875t-.375.875L9.55 12l7.35 7.35q.35.35.35.862q0 .513-.375.888t-.875.375q-.5 0-.875-.375Z"
									/></g
								></svg
							>
						</div>
					</div>
					{#if menu}
						<div
							in:fly={{ y: 200 }}
							out:fly={{ x: 200 }}
							data-popover
							data-popper-placement="bottom"
							role="tooltip"
							class="absolute z-10 app-inset m-0 left-0 right-0 top-0 border-solid pt-2 dark:shadow-slate-400 inline-block w-64 text-sm font-light text-slate-700 transition-opacity duration-300 bg-white dark:bg-black border rounded-md shadow-md dark:text-slate-50 border-color"
							style="transform: translate(-202px, 55px)"
						>
							<div class="">
								<div
									class="flex flex-row justify-between align-middle items-center border-b-2 p-2 border-solid border-color"
								>
									<div class="ml-1">
										<p
											class="text-slate-700 relative inline-block dark:text-slate-50 pt-1.5 pr-2 text-xl font-semibold font-nunito"
										>
											Arinze Justin
											<Badge class="px-2">{plan}</Badge>
										</p>
									</div>
									<div>
										{#if plan == 'Share 2'}
											<svg
												class="w-7 h-7"
												xmlns="http://www.w3.org/2000/svg"
												width="1em"
												height="1em"
												viewBox="0 0 24 24"
												><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><g
													fill="none"
													stroke="skyblue"
													stroke-width="1.5"
													><path
														d="M11.607 2.342a.6.6 0 0 1 .787 0l1.948 1.692a.6.6 0 0 0 .445.145l2.572-.224a.6.6 0 0 1 .636.463l.582 2.514a.6.6 0 0 0 .275.38l2.212 1.33a.6.6 0 0 1 .243.748l-1.008 2.376a.6.6 0 0 0 0 .468l1.008 2.376a.6.6 0 0 1-.243.749l-2.212 1.33a.6.6 0 0 0-.275.379l-.582 2.514a.6.6 0 0 1-.636.463l-2.572-.224a.6.6 0 0 0-.445.144l-1.949 1.693a.6.6 0 0 1-.787 0l-1.948-1.693a.6.6 0 0 0-.445-.144l-2.572.224a.6.6 0 0 1-.636-.463l-.582-2.514a.6.6 0 0 0-.275-.38l-2.212-1.33a.6.6 0 0 1-.243-.748l1.008-2.376a.6.6 0 0 0 0-.468L2.693 9.39a.6.6 0 0 1 .243-.749l2.212-1.33a.6.6 0 0 0 .275-.379l.582-2.514a.6.6 0 0 1 .636-.463l2.572.224a.6.6 0 0 0 .445-.145l1.949-1.692Z"
													/><path
														stroke-linecap="round"
														stroke-linejoin="round"
														d="m9 13l2 2l5-5"
													/></g
												></svg
											>
										{:else}
											<button
												on:click={(() => (menu = !menu), (active = !active))}
												class="bg-blue-600 rounded-md text-sm p-1 hover:shadow-lg">Upgrade</button
											>
										{/if}
									</div>
								</div>
								<div class="pt-3 group/item px-2">
									<!-- svelte-ignore a11y-missing-content -->
									<a
										href="/app/profile"
										class="flex flex-auto px-2 items-center group-hover/item:bg-slate-500/30 rounded-md transition-all duration-500 py-3"
									>
										<svg
											class="w-6 h-6 mr-3 text-slate-700 dark:text-slate-50"
											xmlns="http://www.w3.org/2000/svg"
											width="1.13em"
											height="1em"
											viewBox="0 0 36 32"
											><rect x="0" y="0" width="36" height="32" fill="none" stroke="none" /><path
												fill="currentColor"
												d="M.5 31.983a.503.503 0 0 0 .612-.354c1.03-3.843 5.216-4.839 7.718-5.435c.627-.149 1.122-.267 1.444-.406c2.85-1.237 3.779-3.227 4.057-4.679a.5.5 0 0 0-.165-.473c-1.484-1.281-2.736-3.204-3.526-5.416a.492.492 0 0 0-.103-.171c-1.045-1.136-1.645-2.337-1.645-3.294c0-.559.211-.934.686-1.217a.5.5 0 0 0 .243-.408C10.042 5.036 13.67 1.026 18.12 1l.107.007c4.472.062 8.077 4.158 8.206 9.324a.498.498 0 0 0 .178.369c.313.265.459.601.459 1.057c0 .801-.427 1.786-1.201 2.772a.522.522 0 0 0-.084.158c-.8 2.536-2.236 4.775-3.938 6.145a.502.502 0 0 0-.178.483c.278 1.451 1.207 3.44 4.057 4.679c.337.146.86.26 1.523.403c2.477.536 6.622 1.435 7.639 5.232a.5.5 0 0 0 .966-.26c-1.175-4.387-5.871-5.404-8.393-5.95c-.585-.127-1.09-.236-1.336-.344c-1.86-.808-3.006-2.039-3.411-3.665c1.727-1.483 3.172-3.771 3.998-6.337c.877-1.14 1.359-2.314 1.359-3.317c0-.669-.216-1.227-.644-1.663C27.189 4.489 23.19.076 18.227.005l-.149-.002c-4.873.026-8.889 4.323-9.24 9.83c-.626.46-.944 1.105-.944 1.924c0 1.183.669 2.598 1.84 3.896c.809 2.223 2.063 4.176 3.556 5.543c-.403 1.632-1.55 2.867-3.414 3.676c-.241.105-.721.22-1.277.352c-2.541.604-7.269 1.729-8.453 6.147a.5.5 0 0 0 .354.612z"
											/></svg
										>
										<span class="ml-1 text-lg">Profile</span>
									</a>
								</div>
								<div class="group/item px-2">
									<!-- svelte-ignore a11y-missing-content -->
									<a
										href="/app/settings"
										class="flex flex-auto px-2 items-center group-hover/item:bg-slate-500/30 rounded-md transition-all duration-500 py-3"
									>
										<svg
											class="w-6 h-6 text-slate-700 dark:text-slate-50 mr-3"
											xmlns="http://www.w3.org/2000/svg"
											width="1em"
											height="1em"
											viewBox="0 0 24 24"
											><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><g
												transform="rotate(180 12 12)"
												><path
													fill="currentColor"
													d="m9.25 22l-.4-3.2q-.325-.125-.612-.3q-.288-.175-.563-.375L4.7 19.375l-2.75-4.75l2.575-1.95Q4.5 12.5 4.5 12.337v-.675q0-.162.025-.337L1.95 9.375l2.75-4.75l2.975 1.25q.275-.2.575-.375q.3-.175.6-.3l.4-3.2h5.5l.4 3.2q.325.125.613.3q.287.175.562.375l2.975-1.25l2.75 4.75l-2.575 1.95q.025.175.025.337v.675q0 .163-.05.338l2.575 1.95l-2.75 4.75l-2.95-1.25q-.275.2-.575.375q-.3.175-.6.3l-.4 3.2Zm2.8-6.5q1.45 0 2.475-1.025Q15.55 13.45 15.55 12q0-1.45-1.025-2.475Q13.5 8.5 12.05 8.5q-1.475 0-2.488 1.025Q8.55 10.55 8.55 12q0 1.45 1.012 2.475Q10.575 15.5 12.05 15.5Z"
												/></g
											></svg
										>
										<span class="ml-1 text-lg">Settings</span>
									</a>
								</div>
								<div class="pb-3 group/item px-2">
									<!-- svelte-ignore a11y-missing-content -->
									<a
										href="/help"
										on:click={(e) => e.preventDefault()}
										class="flex flex-auto px-2 items-center group-hover/item:bg-slate-500/30 rounded-md transition-all duration-500 py-3"
									>
										<svg
											class="w-6 h-6 mr-3 text-slate-700 dark:text-slate-50"
											xmlns="http://www.w3.org/2000/svg"
											width="1em"
											height="1em"
											viewBox="0 0 24 24"
											><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><g
												fill="none"
												stroke="currentColor"
												stroke-width="1.5"
												><path
													stroke-linecap="round"
													stroke-linejoin="round"
													d="M20 11a8 8 0 1 0-16 0"
												/><path
													d="M2 15.438v-1.876a2 2 0 0 1 1.515-1.94l1.74-.436a.6.6 0 0 1 .745.582v5.463a.6.6 0 0 1-.746.583l-1.74-.435A2 2 0 0 1 2 15.439Zm20 0v-1.876a2 2 0 0 0-1.515-1.94l-1.74-.436a.6.6 0 0 0-.745.582v5.463a.6.6 0 0 0 .745.583l1.74-.435A2 2 0 0 0 22 15.439ZM20 18v.5a2 2 0 0 1-2 2h-3.5"
												/><path d="M13.5 22h-3a1.5 1.5 0 0 1 0-3h3a1.5 1.5 0 0 1 0 3Z" /></g
											></svg
										>
										<span class="ml-1 text-lg">Help</span>
									</a>
								</div>
								<div class="border-color border-solid border-t-2 py-3 group/item px-2">
									<!-- svelte-ignore a11y-missing-content -->
									<a
										href="/0auth/logout"
										on:click={(e) => (e.preventDefault(), logout())}
										class="flex justify-center px-2 text-center items-center  group-hover/item:bg-slate-500/30 rounded-md transition-all duration-500 py-3"
									>
										<svg
											class="w-6 h-6 mr-3 text-slate-700 dark:text-slate-50"
											xmlns="http://www.w3.org/2000/svg"
											width="1em"
											height="1em"
											viewBox="0 0 24 24"
											><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><g
												transform="rotate(-90 12 12)"
												><path
													fill="currentColor"
													d="M11 13V3h2v10Zm1 8q-1.85 0-3.488-.712q-1.637-.713-2.862-1.938t-1.938-2.862Q3 13.85 3 12q0-2 .825-3.775T6.15 5.15L7.6 6.6q-1.25.95-1.925 2.375T5 12q0 2.9 2.05 4.95Q9.1 19 12 19q2.925 0 4.962-2.05Q19 14.9 19 12q0-1.6-.663-3.025Q17.675 7.55 16.4 6.6l1.45-1.45q1.5 1.3 2.325 3.075Q21 10 21 12q0 1.85-.712 3.488q-.713 1.637-1.925 2.862q-1.213 1.225-2.85 1.938Q13.875 21 12 21Z"
												/></g
											></svg
										>
										<span class="ml-1 text-lg">Sign Out</span>
									</a>
								</div>
							</div>
							<div
								data-popper-arrow
								style="transform: translate(210px, 0px)"
								class="absolute left-0"
							/>
						</div>
					{/if}
				{/if}
			</div>
		</div>
	</div>
</header>
<Plan {active} />

<style>
	[data-popper-arrow]::after,
	[data-popper-arrow]::before {
		@apply content-[''] visible transform rotate-45;
	}
	[data-popover][role='tooltip'][data-popper-placement^='bottom'] > [data-popper-arrow] {
		@apply -top-[7px] shadow-md;
	}
	[data-popper-arrow],
	[data-popper-arrow]::before {
		@apply h-3 absolute w-3 bg-inherit;
	}
	[data-popover][role='tooltip'][data-popper-placement^='bottom'] > [data-popper-arrow]::after,
	[data-popover][role='tooltip'][data-popper-placement^='bottom'] > [data-popper-arrow]::before {
		@apply border-l-2 border-t-2;
	}

	[data-popper-arrow]::after {
		@apply absolute w-[14px] bg-inherit h-[14px];
	}
</style>
