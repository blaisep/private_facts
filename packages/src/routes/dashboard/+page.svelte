<script>
  import { enhance } from '$app/forms'
  import { beforeNavigate } from '$app/navigation'
  import Loading from '$lib/components/loading.svelte'
  import Modal from '$lib/components/modal.svelte'
  import { fade } from 'svelte/transition'

  let { form } = $props()
  let capKey = $state()
  let capKeyInput = $state()
  let list = $state()
  let listForm = $state()
  let modalTitle = $state()
  let modalText = $state()
  let newCapKey = $state()
  let checked = $state(false)
  let loading = $state(false)
  let showModal = $state(false)
  let showDelModal = $state(false)
  let showUploadModal = $state(false)
  let showAddFolderModal = $state(false)


  const submitKey = () => {
    capKey = capKeyInput
  }

  const persistCapKey = () => {
    capKey = newCapKey
    newCapKey = undefined
  }

  const enhanceForm = () => {
    showDelModal = false
    showUploadModal = false
    showAddFolderModal = false
    loading = true

    return async ({ result, update }) => {
      await update()
      loading = false

      if (result.status === 200) {
        switch (result.data.endpoint) {
          case 'createCapKey': {
            newCapKey = result.data.capKey
            break
          }
          case 'listDirectories': {
            capKey = result.data.capKey
            list = result.data.list
            break
          }
          case 'uploadFile': {
            listForm.requestSubmit()
            break
          }
          case 'deletePath': {
            listForm.requestsubmit()
            break
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

  // Store cap key in a variable for use while current page
  // is on screen
  $effect(() => {
    if (form?.capKey) capKey = form.capKey
  })

  // Show errors
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

{#if loading}
  <div class='loader' transition:fade|local>
    <Loading />
  </div>
{/if}

<h1>Dashboard</h1>

{#if !capKey && !newCapKey}
  <div class='cap-key-div add'>
    <form action='?/listDirectories' method='post' enctype='form-data' use:enhance={enhanceForm} bind:this={listForm}>
      <label for='capKeyInput'>Cap key:</label>
      <input type='text' name='capKeyInput' value={capKey} />

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

  {#if list}
    <ul>
      {#each Object.keys(list[1].children) as item}
        <li>{item}</li>
      {/each}
    </ul>
  {/if}

  <button onclick={() => showAddFolderModal = true}>Add folder</button>
  <button onclick={() => showUploadModal = true}>Upload file</button>
  <button onclick={() => showDelModal = true}>Unlink file / folder</button>
  <button onclick={() => capKey = undefined}>Change cap key</button>
{/if}

<!-- Modals -->

<Modal {showModal} escape={() => showModal = false}>
  <h2>{modalTitle}</h2>
  <p>{modalText}</p>
  <button onclick={() => showModal = false}>Ok</button>
</Modal>

<Modal showModal={showDelModal} escape={() => showDelModal = false}>
  <h2>Unlink</h2>
  <p>Specify path of file or folder to unlink.</p>
  <p>Ex.: /Documents/File-1.txt</p>

  <form action='?/deletePath' method='post' enctype='form-data' use:enhance={enhanceForm}>
    <input type='hidden' name='capKey' value={capKey} />

    <label for='path'>Path:</label>
    <input type='text' name='path' class='path-input' />

    <div class='form-actions'>
      <button onclick={() => showDelModal = false}>Cancel</button>
      <button type='submit'>Confirm</button>
    </div>
  </form>
</Modal>

<Modal showModal={showUploadModal} escape={() => showUploadModal = false}>
  <h2>Upload file</h2>

  <form action='?/uploadFile' method='post' enctype='multipart/form-data' use:enhance={enhanceForm}>
    <input type='hidden' name='capKey' value={capKey} />

    <div class='file-input'>
      <label for='file'>File:</label>
      <input type='file' name='file' placeholder='file' required />
    </div>

    <label for='path'>Path:</label>
    <input type='text' name='path' class='path-input' />

    <div class='form-actions'>
      <button onclick={() => showUploadModal = false}>Cancel</button>
      <button type='submit'>Upload</button>
    </div>
  </form>
</Modal>

<Modal showModal={showAddFolderModal} escape={() => showAddFolderModal = false}>
  <h2>Add folder</h2>

  <form action='?/createDirectory' method='post' enctype='form-data' use:enhance={enhanceForm}>
    <input type='hidden' name='capKey' value={capKey} />

    <div class='new-folder-input'>
      <label for='dirName'>New folder name:</label>
      <input type='text' name='dirName' />

      <label for='path'>Path:</label>
      <input type='text' name='path' />
    </div>

    <div class='form-actions'>
      <button onclick={() => showAddFolderModal = false}>Cancel</button>
      <button type='submit'>Confirm</button>
    </div>
  </form>
</Modal>

<style> 
  .cap-key-div form {
    display: flex;
    flex-direction: column;
    text-align: left;
  }

  .cap-key-div form button {
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

  .form-actions {
    display: flex;
    justify-content: center;
  }

  .path-input {
    width: 30em;
  }

  .new-folder-input {
    text-align: left;
    display: flex;
    flex-direction: column;
  }
</style>
