<script>
  import { onDestroy } from 'svelte'

  let { data, form } = $props()

  let totpForm
  let count = $state(form?.seconds ?? data.seconds)

  const timer = setInterval(() => count--, 1000)

  onDestroy(() => {
    clearInterval(timer)
  })

  $effect(() => {
    if (count === 0) {
      totpForm.requestSubmit()
    }
  })
</script>

<svelte:head>
  <title>Login page</title>
  <meta name='description' content='Login page'/>
</svelte:head>

<div class='login-content'>
  <h1>Login</h1>

  <p>Token: {form?.token ?? data.token}.</p>
  <p>Valid for {count}s.</p>

  <form action='?/getTotp' method='post' enctype='form-data' bind:this={totpForm}>
  </form>
</div>
