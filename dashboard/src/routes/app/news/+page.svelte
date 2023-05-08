<script lang="ts">
	import API from '$lib/api';
	import { onMount } from 'svelte';
	import { getStorage } from '$lib/storage';
	import { fly } from 'svelte/transition';
	import Loader from '$lib/Loader.svelte';
	import Dialog, { Content, Actions } from '@smui/dialog';
	import Button, { Label } from '@smui/button';

	let token: any,
		news_list: any[] = [],
		news_loading = true,
		open = false,
		title: string,
		content: string,
		img_url: string,
		link: string;

	var news = async () => {
			try {
				news_list = [];
				var d = new Date(),
					day = d.toLocaleDateString();
				var today = day.split(',')[0],
					pre_format = `${today.split('/')[2]}-${today.split('/')[0]}-${today.split('/')[1]}`;
				d.setDate(d.getDate() - 20);
				var ago = d.toLocaleString(),
					// eslint-disable-next-line no-redeclare
					ago = ago.split(',')[0],
					ago_format = `${ago.split('/')[2]}-${ago.split('/')[0]}-${ago.split('/')[1]}`;
				const req = await API.post(
					'/news',
					JSON.stringify({ query: 'cryptocurrency', from: ago_format, to: pre_format }),
					{ Authorization: token }
				);
				news_list = [...news_list, req.results];
				news_loading = false;
			} catch (error) {}
		},
		read = (art_title: string, art_content: string, art_img_url: string, art_link: string) => {
			open = true;
			title = art_title;
			content = art_content;
			img_url = art_img_url || '/img/default.png';
			link = art_link;
		};

	onMount(() => {
		token = getStorage('token') || '';
		news();
	});
</script>

<svelte:head>
	<title>Latest news about crypto market | cryptflixinvest.com</title>
</svelte:head>

<div
	in:fly={{ x: 300, delay: 1000 }}
	out:fly={{ x: -400, duration: 800 }}
	class="container mt-3 pt-3 md:pt-5"
>
	<div class="override">
		<div
			class="flex flex-row md:mr-2 override w-full items-center align-middle justify-between mb-4 pb-4"
		>
			<div class="w-auto">
				<p class="font-nunito text-xl lg:text-2xl font-bold uppercase text-black dark:text-white">
					News
				</p>
			</div>
			<div class="w-auto">
				<a
					href="/app/transaction/deposit"
					class="rounded-lg w-16 inline px-4 py-3 bg-blue-700 text-white hover:ring-blue-600 transition-all duration-300 ring-2 ring-offset-2 ring-offset-transparent ring-transparent"
				>
					<svg
						class="w-6 h-6 mx-2 text-white inline"
						xmlns="http://www.w3.org/2000/svg"
						width="1.13em"
						height="1em"
						viewBox="0 0 512 512"
					>
						<rect x="0" y="0" width="512" height="512" fill="none" stroke="none" /><path
							fill="currentColor"
							d="M298.9 24.31c-14.9.3-25.6 3.2-32.7 8.4l-97.3 52.1l-54.1 73.59c-11.4 17.6-3.3 51.6 32.3 29.8l39-51.4c49.5-42.69 150.5-23.1 102.6 62.6c-23.5 49.6-12.5 73.8 17.8 84l13.8-46.4c23.9-53.8 68.5-63.5 66.7-106.9l107.2 7.7l-1-112.09l-194.3-1.4zM244.8 127.7c-17.4-.3-34.5 6.9-46.9 17.3l-39.1 51.4c10.7 8.5 21.5 3.9 32.2-6.4c12.6 6.4 22.4-3.5 30.4-23.3c3.3-13.5 8.2-23 23.4-39zm-79.6 96c-.4 0-.9 0-1.3.1c-3.3.7-7.2 4.2-9.8 12.2c-2.7 8-3.3 19.4-.9 31.6c2.4 12.1 7.4 22.4 13 28.8c5.4 6.3 10.4 8.1 13.7 7.4c3.4-.6 7.2-4.2 9.8-12.1c2.7-8 3.4-19.5 1-31.6c-2.5-12.2-7.5-22.5-13-28.8c-4.8-5.6-9.2-7.6-12.5-7.6zm82.6 106.8c-7.9.1-17.8 2.6-27.5 7.3c-11.1 5.5-19.8 13.1-24.5 20.1c-4.7 6.9-5.1 12.1-3.6 15.2c1.5 3 5.9 5.9 14.3 6.3c8.4.5 19.7-1.8 30.8-7.3c11.1-5.5 19.8-13 24.5-20c4.7-6.9 5.1-12.2 3.6-15.2c-1.5-3.1-5.9-5.9-14.3-6.3c-1.1-.1-2.1-.1-3.3-.1zm-97.6 95.6c-4.7.1-9 .8-12.8 1.9c-8.5 2.5-13.4 7-15 12.3c-1.7 5.4 0 11.8 5.7 18.7c5.8 6.8 15.5 13.3 27.5 16.9c11.9 3.6 23.5 3.5 32.1.9c8.6-2.5 13.5-7 15.1-12.3c1.6-5.4 0-11.8-5.8-18.7c-5.7-6.8-15.4-13.3-27.4-16.9c-6.8-2-13.4-2.9-19.4-2.8z"
						/>
					</svg>
					<span>Invest</span>
				</a>
			</div>
		</div>
		<div class="py-4">
			<p class="text-sm md:text-xl text-gray-400">
				Latest and top news of things happening within crypto market
			</p>
		</div>
		{#if news_loading}
			<div class="mt-10 pt-8" out:fly={{ y: -400 }}>
				<Loader width={'50px'} height={'50px'} />
				<p class="text-center pt-8">Loading Articles ......</p>
			</div>
		{:else}
			<div
				in:fly={{ y: 400 }}
				class="grid grid-cols-1 pb-8 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-4 align-middle"
			>
				{#each news_list[0] as article}
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<div
						on:click={() => read(article.title, article.content, article.image_url, article.link)}
						class="border-solid cursor-pointer group/item border-color border rounded-lg hoverbg-slate-100 dark:hover:bg-accent"
					>
						<div class="img_">
							<img
								src={article.image_url || '?'}
								loading="lazy"
								on:error={(e) => { //@ts-ignore
									e.target.src = '/img/default.png';
								}}
								alt=""
								srcset=""
								class="rounded-t-lg hover:opacity-70"
							/>
						</div>
						<div class="py-4 px-2">
							<p class="uppercase text-center font-open">{article.title}</p>
							<div class="flex flex-row items-center my-2 md:my-4 align-middle justify-between">
								<div class="text-gray-400 text-xs">
									<span class="hidden md:inline capitalize">{article.creator} | </span><span
										class="capitalize">{article.pubDate}</span
									>
								</div>
								<div class="text-gray-400 text-xs">
									<span class="capitalize">{article.language}</span> |
									<span class="capitalize">{article.source_id}</span>
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>

<Dialog
	scrimClickAction=""
	escapeKeyAction=""
	bind:open
	surface$style="width: 850px; max-width: calc(100vw - 32px);"
>
	<Content id="large-scroll-content">
		<div class="m-3">
			<div class="flex flex-col md:flex-row justify-center md:justify-between">
				<div class="mb-4">
					<p class="md:font-semibold font-mono uppercase text-black dark:text-white">{title}</p>
				</div>
				<div class="grid grid-cols-3 gap-4 align-middle items-center">
					<button
						aria-label="twitter"
						class="bg-transparent border-none p-0 font-[inherit] text-inherit cursor-pointer"
						><svg viewBox="0 0 64 64" width="32" height="32"
							><rect width="64" height="64" rx="16" ry="16" fill="#00aced" /><path
								d="M48,22.1c-1.2,0.5-2.4,0.9-3.8,1c1.4-0.8,2.4-2.1,2.9-3.6c-1.3,0.8-2.7,1.3-4.2,1.6 C41.7,19.8,40,19,38.2,19c-3.6,0-6.6,2.9-6.6,6.6c0,0.5,0.1,1,0.2,1.5c-5.5-0.3-10.3-2.9-13.5-6.9c-0.6,1-0.9,2.1-0.9,3.3 c0,2.3,1.2,4.3,2.9,5.5c-1.1,0-2.1-0.3-3-0.8c0,0,0,0.1,0,0.1c0,3.2,2.3,5.8,5.3,6.4c-0.6,0.1-1.1,0.2-1.7,0.2c-0.4,0-0.8,0-1.2-0.1 c0.8,2.6,3.3,4.5,6.1,4.6c-2.2,1.8-5.1,2.8-8.2,2.8c-0.5,0-1.1,0-1.6-0.1c2.9,1.9,6.4,2.9,10.1,2.9c12.1,0,18.7-10,18.7-18.7 c0-0.3,0-0.6,0-0.8C46,24.5,47.1,23.4,48,22.1z"
								fill="white"
							/></svg
						></button
					>
					<button
						aria-label="facebook"
						class="bg-transparent border-none p-0 font-[inherit] text-inherit cursor-pointer"
						><svg viewBox="0 0 64 64" width="32" height="32"
							><rect width="64" height="64" rx="16" ry="16" fill="#3b5998" /><path
								d="M34.1,47V33.3h4.6l0.7-5.3h-5.3v-3.4c0-1.5,0.4-2.6,2.6-2.6l2.8,0v-4.8c-0.5-0.1-2.2-0.2-4.1-0.2 c-4.1,0-6.9,2.5-6.9,7V28H24v5.3h4.6V47H34.1z"
								fill="white"
							/></svg
						></button
					>
					<div class="jPxXhc">
						<a href={link} target="_blank" rel="noreferrer">
							<svg
								aria-hidden="true"
								focusable="false"
								role="img"
								height="18"
								width="18"
								xmlns="http://www.w3.org/2000/svg"
								data-icon="hyperlink"
								viewBox="0 0 24 24"
								fill="none"
								class="sc-bdvvtL kUYgTM"
								><path
									fill="#3b97ff"
									d="M15.5 2.25a.75.75 0 0 1 .75-.75h5.5a.75.75 0 0 1 .75.75v5.5a.75.75 0 0 1-1.5 0V4.06l-6.22 6.22a.75.75 0 1 1-1.06-1.06L19.94 3h-3.69a.75.75 0 0 1-.75-.75Z"
								/><path
									fill="#3b97ff"
									d="M2.5 4.25c0-.966.784-1.75 1.75-1.75h8.5a.75.75 0 0 1 0 1.5h-8.5a.25.25 0 0 0-.25.25v15.5c0 .138.112.25.25.25h15.5a.25.25 0 0 0 .25-.25v-8.5a.75.75 0 0 1 1.5 0v8.5a1.75 1.75 0 0 1-1.75 1.75H4.25a1.75 1.75 0 0 1-1.75-1.75V4.25Z"
								/></svg
							>
						</a>
					</div>
				</div>
			</div>
			<div>
				<img src={img_url} alt="" srcset="{img_url} 2x" class="rounded-md my-4 w-full mx-auto" />
				<div class="mt-4 pt-4">
					<p class="text-black dark:text-white indent-8 whitespace-normal">{content}</p>
				</div>
			</div>
		</div>
	</Content>
	<Actions>
		<Button action="accept">
			<Label>Close</Label>
		</Button>
	</Actions>
</Dialog>

<style scoped>
	.img_ img {
		aspect-ratio: 16/9;
	}
	.jPxXhc {
		-webkit-box-pack: center;
		-webkit-box-align: center;
		@apply flex cursor-pointer h-8 w-8 bg-slate-100 text-[#3b97ff] rounded-lg relative items-center justify-center;
	}
</style>
