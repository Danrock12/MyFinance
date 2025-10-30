<script lang="ts">
  import { page } from '$app/stores';
  import MenuBar from '$lib/MenuBar.svelte';
</script>

{#if $page.url.pathname !== '/'}
  <MenuBar />
{/if}

<slot />