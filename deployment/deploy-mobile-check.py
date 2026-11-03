from pathlib import Path
import subprocess

target = Path('/var/www/dzp-start/dashboard-test')
config = Path('/etc/nginx/conf.d/dzp1125-mobile-check.conf')
if target.exists() or config.exists():
    raise SystemExit('Destination already exists; inspect before replacing.')
target.mkdir(mode=0o755)
(target / 'index.html').write_bytes(Path('/tmp/dzp-mobile-check.html').read_bytes())
(target / 'index.html').chmod(0o644)
config.write_text('''server {
    listen 80;
    listen [::]:80;
    server_name dzp1125.me;
    root /var/www/dzp-start/dashboard-test;
    index index.html;
    server_tokens off;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header Referrer-Policy "no-referrer" always;
    add_header Content-Security-Policy "default-src 'none'; style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'" always;
    location / { try_files $uri $uri/ =404; }
    location ~ /\\. { deny all; }
}
''', encoding='utf-8')
try:
    subprocess.run(['nginx', '-t'], check=True)
    subprocess.run(['systemctl', 'reload', 'nginx'], check=True)
except Exception:
    config.unlink()
    raise
print('Public static confirmation page installed; private dashboard unchanged.')
