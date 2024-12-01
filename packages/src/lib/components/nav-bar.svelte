<script>
  import { goto } from '$app/navigation'
</script>

<nav class='nav-bar'>
  <div class='cluster nav-left'>
    <ul>
      <li><button onclick={() => goto('/')}>Home</button></li>
    </ul>
  </div>

  <div class='cluster nav-right'>
    <ul>
      <li><button onclick={() => goto('/dashboard')}>Dashboard</button></li>
    </ul>
  </div>
</nav>

<style>
  .nav-bar {
    height: var(--navbar-height);
    display: flex;
    background: var(--theme-background);
    border-bottom: solid thin var(--border-color);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  ul {
    margin: 0;
    padding: 0;
  }

  li {
    list-style: none;
  }

  .cluster ul {
    display: flex;
    height: 100%;
  }

  .cluster li {
    display: flex;
  }

  .nav-left {
    margin: 0 auto 0 0;
  }

  .nav-right {
    margin: 0 0 0 auto;
  }

  button {
    margin: 0;
    background: transparent;
    color: var(--theme-color);
    border: none;
    width: 100%;
    height: 100%;
    padding: 0 1em;
    text-align: left;
  }
</style>
