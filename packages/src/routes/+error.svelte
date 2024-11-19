<script>
  import { page } from '$app/stores'
</script>

<div class='error-page'>
  <h1>Supawiki</h1>

  <h2>Oops... Something went wrong!</h2>

  {#if $page.status === 401}
    <h3>Error {$page.status}: {$page.error?.message}</h3>
    <p>
      Go to <a href="/auth/login">log in</a> page.
    </p>
  {:else}
    <h3>{$page.status}: {$page.error?.message}</h3>
    <p>We are looking into it.</p>
  {/if}
</div>

<style>
  .error-page {
    text-align: center;
  }
</style>
