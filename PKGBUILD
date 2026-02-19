# Maintainer: Ashley <info@meisgaming.net>
pkgname=cowtotext
pkgver=1.0.0
pkgrel=2
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

    # Build wheel
    python -m build --wheel --no-isolation
}

package() {
    cd cow-to-text

    # Install wheel files into package root
    python -m installer --destdir="$pkgdir" dist/*.whl
    
    # Install license and docs
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
    install -Dm644 README.md "$pkgdir/usr/share/doc/${pkgname}/README.md"
}
