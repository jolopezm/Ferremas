export default function Header() {
    return (
        <div>
          <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
              <a class="navbar-brand" href="http://localhost:3000/home">Ferremas</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                  <a class="nav-link" href="http://localhost:3000/home">Home</a>
                  <a class="nav-link" href="http://localhost:3000/about">About</a>
                </div>
              </div>
            </div>
          </nav>
      </div>
    )
}