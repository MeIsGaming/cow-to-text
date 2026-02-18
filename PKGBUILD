# Maintainer: Ashley <info@meisgaming.net>
pkgname=cowtotext
pkgver=1.0.0
pkgrel=1
pkgdesc="Real-time audio transcription and translation tool using Whisper and Argos Translate"
arch=('x86_64')
url="https://github.com/MeIsGaming/cow-to-text"
license=('MIT')
depends=('python' 'ffmpeg' 'libpulse')
makedepends=('git' 'python-build' 'python-installer' 'python-wheel')
optdepends=('cuda: For GPU acceleration')
source=("git+${url}.git#branch=main")
sha256sums=('SKIP')

build() {
    cd cow-to-text
    
    # Create temporary venv for build
    python -m venv build_venv
    source build_venv/bin/activate
    
    # Install build deps and requirements
    pip install --upgrade pip setuptools wheel build installer setuptools_scm
    pip install -r requirements.txt
    
    # Build wheel
    python -m build --wheel --no-isolation
    
    deactivate
}

package() {
    cd cow-to-text
    
    # Install wheel WITH all dependencies to package
    python -m pip install --root="$pkgdir" --no-cache-dir dist/*.whl
    
    # Install license and docs
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
    install -Dm644 README.md "$pkgdir/usr/share/doc/${pkgname}/README.md"
}
