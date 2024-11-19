<script>
  import { goto } from '$app/navigation'
</script>

<svelte:head>
  <title>Home page</title>
  <meta name='description' content='Home page'/>
</svelte:head>

<div class='landing-page'>
  <h1>Private facts</h1>

  <button onclick={() => goto('/auth/login')}>Login</button>
</div>
