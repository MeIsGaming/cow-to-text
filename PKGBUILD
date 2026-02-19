# Maintainer: Ashley <info@meisgaming.net>
pkgname=cowtotext
pkgver=1.0.0
pkgrel=3
pkgdesc="Real-time audio transcription and translation tool using Whisper and Argos Translate"
arch=('x86_64')
url="https://github.com/MeIsGaming/cow-to-text"
license=('MIT')
depends=('python' 'ffmpeg' 'libpulse')
makedepends=('git' 'python-build' 'python-installer' 'python-wheel' 'python-pip')
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

    # Bundle runtime Python dependencies in an isolated vendor directory
    python -m pip install \
        --no-cache-dir \
        --disable-pip-version-check \
        --target "$pkgdir/usr/lib/cowtotext/vendor" \
        -r requirements.txt

    # Ensure launcher uses bundled dependencies
    install -dm755 "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/cowtotext" << 'EOF'
#!/bin/sh
export PYTHONPATH="/usr/lib/cowtotext/vendor${PYTHONPATH:+:$PYTHONPATH}"
exec /usr/bin/python -m cowtotext_main "$@"
EOF
    chmod 755 "$pkgdir/usr/bin/cowtotext"
    
    # Install license and docs
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
    install -Dm644 README.md "$pkgdir/usr/share/doc/${pkgname}/README.md"
}
