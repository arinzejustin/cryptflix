<script lang="ts">
	import { fly } from 'svelte/transition';
	import Tab, { Icon, Label } from '@smui/tab';
	import TabBar from '@smui/tab-bar';
    let tabs = [
    {
      icon: 'message',
      label: 'Message',
    },
    {
      icon: 'archive',
      label: 'archive',
    }
  ];
  let active = tabs[0];
</script>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="container">
    <div class="mb-8">
        <TabBar {tabs} let:tab bind:active class="override relative">
          <Tab {tab}>
            <Icon class="material-icons">{tab.icon}</Icon>
            <Label class="font-open text-slate-900 dark:text-slate-50">{tab.label}</Label>
          </Tab>
        </TabBar>
      </div>
	<div class="pt-8 border-dotted border-color border-2 rounded-md dark:bg-black/70 p-4 w-full" />
</div>
<style>

</style>