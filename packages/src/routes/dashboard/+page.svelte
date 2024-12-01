<script>
  import { enhance } from '$app/forms'
  import { beforeNavigate } from '$app/navigation'

  let capKey = $state()
  let capKeyInput = $state()
  let newCapKey = $state()
  let checked = $state(false)

  const submitKey = () => {
    capKey = capKeyInput
  }

  const persistCapKey = () => {
    capKey = newCapKey
    newCapKey = undefined
  }

  const enhanceForm = () => {
    return async ({ result, update }) => {
      await update()
      newCapKey = result.data.capKey
    }
  }

  beforeNavigate(({ cancel }) => {
    if (newCapKey && !capKey) {
      cancel()
      alert('Please confirm you copied and saved the cap key.')
    }
  })
</script>

<svelte:head>
  <title>Private Facts dashboard</title>
  <meta name='description' content='Private Facts dashboard.'>
</svelte:head>
<h1>Dashboard</h1>

{#if !capKey && !newCapKey}
  <div class='cap-key-div add'>
    <div class='cap-key'>
      <label for='capKeyInput'>Cap key:</label>
      <input type='text' name='capKeyInput' bind:value={capKeyInput} />
      <button onclick={submitKey}>Submit</button>
    </div>

    <form action='?/createCapKey' method='post' enctype='form-data' use:enhance={enhanceForm}>
      <button type='submit'>New cap key</button>
    </form>
  </div>
{:else if !capKey && newCapKey}
  <div class='cap-key-div get'>
    <label for='newCapKey'><h2>New cap key</h2></label>
    <input type='text' id='newCapKey' name='newCapKey' value={newCapKey} />

    <div class='warning'>
      <h3>Attention!</h3>

      <p>This is your new cap key. You need it to access your folders and files. It will not be saved nor ever shown again.</p>

      <p><strong>Copy it now and save it somewhere safe.</strong></p>

      <p>If you lose your cap key you will not be able to access your files anymore. You will have to create a new cap key and upload new files and folders.</p>

      <div class='confirm-copy'>
        <input type='checkbox' id='checkbox' name='checkbox' bind:checked />
        <label for='copyCheckbox'>Copied and saved.</label>
      </div>

      <button disabled={!checked} onclick={persistCapKey}>Ok</button>
    </div>
  </div>
{:else}
  <h2>File tree</h2>
  <p>{capKey}</p>
{/if}

<style>
  form, .cap-key {
    display: flex;
  }

  form button {
    margin: 0 0 0 auto;
  }

  .cap-key {
    margin: auto 0 2em 0;
  }

  .cap-key label {
    min-width: 5em;
    margin: auto 0;
  }

  .cap-key input {
    width: 100%;
  }

  .cap-key button {
    min-width: 10em;
    margin: auto 0 auto 1em;
  }

  .cap-key-div {
    max-width: 40em;
    margin: 0 auto;
  }

  .cap-key-div.get {
    display: flex;
    flex-direction: column;
  }

  .confirm-copy {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .confirm-copy input {
    height: unset;
    margin-right: 1em;
    border: solid thin var(--border-color);
    outline: none;
  }

  .warning {
    border: solid thin var(--border-color);
    border-radius: 10px;
    background-color: var(--shade-color);
    padding: 0.5em;
    margin: 2em auto;
  }
</style>
