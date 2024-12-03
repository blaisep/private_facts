<script>
  import { enhance } from '$app/forms'
  import { beforeNavigate } from '$app/navigation'
  import Modal from '$lib/components/modal.svelte'

  let { form } = $props()
  let capKey = $state()
  let capKeyInput = $state()
  let newCapKey = $state()
  let modalTitle = $state()
  let modalText = $state()
  let checked = $state(false)
  let showModal = $state(false)

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

      if (result.status === 200) {
        switch (result.data.endpoint) {
          case 'createCapKey': {
            newCapKey = result.data.capKey
          }
          case 'listDirectories': {
            capKey = result.data.capKey
          }
        }
      }
    }
  }

  beforeNavigate(({ cancel }) => {
    if (newCapKey && !capKey) {
      cancel()
      modalTitle = 'Warning'
      modalText = 'Please confirm you copied and saved the cap key.'
      showModal = true
    }
  })

  $effect(() => {
    if (form?.capKey) capKey = form.capKey
  })

  $effect(() => console.log({ form }))

  $effect(() => {
    if (form?.error) {
      modalTitle = 'Error'
      modalText = form.error
      showModal = true
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
    <form action='?/listDirectories' method='post' enctype='form-data' use:enhance={enhanceForm}>
      <label for='capKeyInput'>Cap key:</label>
      <input type='text' name='capKeyInput' />

      <button type='submit'>Submit</button>
    </form>

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

  <ul>
    {#each form?.list as item}
      {#if item === 'dirnode'}
        <li>/</li>
      {:else}
        <li>{Object.keys(item.children)[0]}</li>
      {/if}
    {/each}
  </ul>

  <button>Add folder</button>
  <button>Upload file</button>
  <button onclick={() => capKey = undefined}>Change cap key</button>
{/if}

<Modal {showModal} escape={() => showModal = false}>
  <h2>{modalTitle}</h2>
  <p>{modalText}</p>
  <button onclick={() => showModal = false}>Ok</button>
</Modal>

<style>
  form {
    display: flex;
    flex-direction: column;
    text-align: left;
  }

  form button {
    margin: 0 0 1em auto;
  }

  form input {
    margin: 1em 0;
  }

  .cap-key-div {
    max-width: 45em;
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

  ul {
    list-style: none;
    text-align: left;
    background: var(--shade-color);
    padding: 1em;
    border: solid thin var(--border-color);
  }
</style>
