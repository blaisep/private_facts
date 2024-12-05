<div class='overlay'></div>

<div class="wrap">
  <svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
    <rect width="10" height="10">
      <animate
        attributeName="rx"
        values="0;5;0"
        dur="1s"
        repeatCount="indefinite" />
    </rect>
  </svg>
</div>

<style>
  .wrap {
    position: absolute;
    z-index: 51;
    opacity: 0.6;
    width: 3em;
    left: calc(50% - 3em);
    top: calc(50% - 2em);
  }

  .overlay {
    position: fixed;
    z-index: 50;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: var(--shade-loading);
  }
</style>
