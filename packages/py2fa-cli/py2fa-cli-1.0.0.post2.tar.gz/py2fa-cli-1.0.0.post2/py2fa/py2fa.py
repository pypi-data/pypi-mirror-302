"""Calculate one-time passwords for two-factor authentication."""

import json
import os
import stat
import sys
from time import time

from pyotp import TOTP
from xdg import BaseDirectory


def _is_world_accessible(path):
    return os.stat(path).st_mode & stat.S_IRWXO


def _load_secrets():
    cfg_path = BaseDirectory.load_first_config('py2fa/secrets.json')
    if cfg_path is None:
        print('ERR: Secrets file does not exist!')
        return None

    if _is_world_accessible(cfg_path):
        print('ERR: Secrets file is world-accessible, change its permissions first.')
        return None

    try:
        with open(cfg_path, encoding='utf-8') as cfg:
            return json.load(cfg)
    except PermissionError:
        print('ERR: Not permitted to access secrets file, verify permissions!')
        return None
    except json.JSONDecodeError:
        print('ERR: Failed to decode secrets file, verify JSON format!')
        return None


def main():
    if len(sys.argv) != 2:
        print(f'usage: {os.path.basename(sys.argv[0])} <secret_name>')
        sys.exit(0)

    secrets = _load_secrets()
    if secrets is None:
        print('ERR: Failed to load secrets file!')
        sys.exit(1)

    try:
        secret = secrets[sys.argv[1]]
    except KeyError:
        print(f'ERR: No secret for {sys.argv[1]} is available!')
        sys.exit(1)

    totp = TOTP(secret)
    valid_for = 30.0 - time() % 30

    print(f'One-time password: {totp.now()} (valid for {valid_for:.1f} seconds)')


if __name__ == '__main__':
    main()
