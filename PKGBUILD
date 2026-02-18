# Maintainer: Ashley <info@meisgaming.net>
pkgname=cowtotext
pkgver=1.0.0
pkgrel=1
pkgdesc="Real-time audio transcription and translation tool using Whisper and Argos Translate"
arch=('x86_64')
url="https://github.com/MeIsGaming/cow-to-text"
license=('MIT')
depends=('python' 'ffmpeg' 'libpulse')
makedepends=('python-build' 'python-installer' 'python-wheel')
source=("${url}/archive/v${pkgver}.tar.gz")
sha256sums=('REPLACE_WITH_ACTUAL_SHA256SUM')

build() {
    cd "${pkgname}-${pkgver}"
    python -m build --wheel --no-isolation
}

package() {
    cd "${pkgname}-${pkgver}"
    python -m installer --destdir="$pkgdir" dist/*.whl
    
    # Install script
    install -Dm755 cowtotext.py "$pkgdir/usr/bin/cowtotext"
    
    # Install license
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
    
    # Install README
    install -Dm644 README.md "$pkgdir/usr/share/doc/${pkgname}/README.md"
}
