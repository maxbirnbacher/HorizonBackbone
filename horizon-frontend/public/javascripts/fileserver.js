function showUpload() {
    let modal = `
    <div
      class="pf-v5-c-modal-box pf-m-md"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-md-title"
      aria-describedby="modal-md-description"
    >
      <div class="pf-v5-c-modal-box__close">
        <button class="pf-v5-c-button pf-m-plain" type="button" aria-label="Close" onclick="document.body.removeChild(this.parentElement.parentElement)">
          <i class="fas fa-times" aria-hidden="true"></i>
        </button>
      </div>
      <header class="pf-v5-c-modal-box__header">
        <h1 class="pf-v5-c-modal-box__title" id="modal-md-title">Modal title</h1>
      </header>
      <div class="pf-v5-c-modal-box__body" id="modal-md-description">
        Static text describing modal purpose. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
        quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
        consequat.
      </div>
      <footer class="pf-v5-c-modal-box__footer">Modal footer</footer>
    </div>
    `

    // append modal to body
    document.body.insertAdjacentHTML('beforeend', modal);
}