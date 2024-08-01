# -*- coding: utf-8 -*-
from functools import wraps

import digitalocean


def ssh_key_exists(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):

        if not self.ssh_key:
            return print("[red]|ERROR| Ssh key was not found.")
        elif not isinstance(self.ssh_key, digitalocean.SSHKey):
            return print("[red]|ERROR| Ssh key must be of type digitalocean.SSHKey")

        return method(self, *args, **kwargs)

    return wrapper


class SSHKeyInfo:

    def __init__(self, ssh_key: digitalocean.SSHKey):
        self.ssh_key = ssh_key

    @ssh_key_exists
    def get_name(self) -> str:
        return self.ssh_key.name

    @ssh_key_exists
    def get_pub_key(self):
        return self.ssh_key.public_key

    @ssh_key_exists
    def get_id(self):
        return self.ssh_key.id

