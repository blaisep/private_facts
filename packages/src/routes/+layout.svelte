<script>
  import NavBar from '$lib/components/nav-bar.svelte'
</script>

<div class='content'>
  <NavBar />

  <slot></slot>
</div>

<style>
  :root {
    --border-color: #aaa;
    --button-color: #f6f6f6;
    --font-family: -apple-system, BlinkMacSystemFont, avenir next, avenir, segoe ui, helvetica neue, helvetica, Cantarell, Ubuntu, roboto, noto, arial, sans-serif;
    --navbar-height: 3em;
    --shade-background: rgba(0, 0, 0, 0.2);
    --shade-color: #eee;
    --theme-background: white;
    --theme-color: #444;
  }

  .content {
    text-align: center;
    margin: auto;
    height: calc(100vh - 6em);
    max-width: 60em;
    overflow: clip;
    overflow-y: auto;
  }

  :global(body) {
    margin: 0;
    font-family: var(--font-family);
    font-weight: 400;
    background: var(--theme-background);
    color: var(--theme-color);
    overflow: clip;
  }

  :global(button) {
    margin: 1em;
    width: 10em;
    height: 2.5em;
    font-family: var(--font-family-text);
    font-weight: 200;
    font-size: 16px;
    background: var(--button-color);
    border: solid thin;
    border-radius: 5px;
  }

  :global(button:hover) {
    cursor: pointer;
  }

  :global(button:disabled) {
    background-color: light-dark(rgba(239, 239, 239, 0.3), rgba(19, 1, 1, 0.3));
    color: light-dark(rgba(16, 16, 16, 0.3), rgba(255, 255, 255, 0.3));
    border-color: light-dark(rgba(118, 118, 118, 0.3), rgba(195, 195, 195, 0.3));
  }

  :global(input) {
    font-size: 0.9em;
    font-weight: 400;
    padding: 0 1em;
    height: 3em;
    border: none;
    border-radius: 2px;
    outline: solid thin var(--border-color);
  }
</style>
