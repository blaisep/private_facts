<script>
  import { onMount } from 'svelte'

  let {
    showModal = false, wide = true, hideSidebar = false,
    enter, escape, children
  } = $props()

  const handleKeydown = (e) => {
    if (showModal) {
      if (e.keyCode === 27) {
        escape()
      } else if (e.keyCode === 13) {
        enter()
      }
    }
  }

  onMount(() => {
    if (showModal) {
      window.addEventListener("keydown", handleKeydown)
    } else {
      window.removeEventListener("keydown", handleKeydown)
    }
  })
</script>

{#if showModal}
  <div class='modal'>
    <div class="overlay" role='button' tabindex='0' onclick={() => escape()} onkeydown={() => escape()}>
      <div
        class="dark"
        role='button'
        tabindex='0'
        class:narrow={!wide}
        class:hidden={hideSidebar}
        onclick={() => escape()}
        onkeydown={() => escape()}
      ></div>
    </div>

    <div class="wrap">
      {@render children?.()}
    </div>
  </div>
{/if}

<style>
  .modal {
    display: flex;
    position: fixed;
    height: 100%;
    width: 100%;
    left: 0;
    top: 0;
  }

  .wrap {
    z-index: 100;
    margin: auto 1em;
    background-color: var(--theme-background);
    border: solid thin var(--theme-color);
    border-radius: 10px;
    padding: 1em;
    text-align: center;
    width: 100%;
  }

  .overlay {
    position: fixed;
    z-index: 50;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
  }

  .overlay .dark {
    margin-top: 0;
    width: 100%;
    height: 100%;
    background-color: var(--shade-background);
  }

  .overlay .dark::before {
    content: "";
    width: 40px;
    height: 20px;
    position: absolute;
    top: -20px;
    left: 0;
    background-color: var(--shade-background);
    border-radius: 40px 40px 0 0;
  }

  .overlay .dark.narrow::before {
    left: 0;
  }

  .overlay .dark.hidden::before {
    display: none;
  }

  @media (min-width: 45em) {
    .wrap {
      margin: auto;
      padding: 1em 3em;
      width: unset;
    }
  }
</style>
