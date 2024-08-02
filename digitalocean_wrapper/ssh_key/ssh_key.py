# -*- coding: utf-8 -*-
from os.path import join, expanduser, isfile
from typing import Optional
from rich import print

import digitalocean
from .ssh_key_info import SSHKeyInfo

class SSHKeyError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            print(self.message)
            return self.message

class SSHKey:
    default_pub_key_path = join(expanduser('~'), '.ssh', 'id_rsa.pub')

    def __init__(self, manager: digitalocean.Manager, do_token: str):
        self.__manager = manager
        self.__token = do_token

    def info(self, ssh_key: digitalocean.SSHKey | str | int) -> SSHKeyInfo:
        return SSHKeyInfo(self._get_ssh_key(ssh_key))

    def get_all(self) -> list[digitalocean.SSHKey]:
        return self.__manager.get_all_sshkeys()

    def create(self, key_name: str, public_key: str = None, stdout: bool = True) -> Optional[digitalocean.SSHKey]:
        if self.check_key_name_exists(key_name=key_name):
            raise SSHKeyError(
                f"[red]|ERROR| The ssh public key named {key_name} already exists on DigitalOcean. Select another name"
            )

        ssh_pub_key = public_key or self.read_default_pub_key()
        ssh_key = self.get_by_pub_key(public_key=ssh_pub_key, stderr=True)

        if ssh_key is not None:
            raise SSHKeyError(
                f"[red]|ERROR| The ssh public key already exists on DigitalOcean under the name: {ssh_key.name}"
            )

        digitalocean.SSHKey(token=self.__token, name=key_name, public_key=ssh_pub_key).create()

        created_key = self._get_ssh_key(key_name)
        if created_key:
            print(f"[green]|INFO| The ssh key `{key_name}` created on DigitalOcean") if stdout else None
            return created_key

        print(f"[red]|ERROR| The ssh key `{key_name}` was not found.") if stdout else None
        return None


    def get_all_ssh_key_names(self) -> list[str]:
        return [ssh_key.name for ssh_key in self.get_all()]

    def get_by_pub_key(self, public_key: str = None, stderr: bool = False) -> Optional[digitalocean.SSHKey]:
        pub_key = public_key or self.read_default_pub_key()

        if pub_key:
            return digitalocean.SSHKey(token=self.__token).load_by_pub_key(pub_key)

        print(f"[red]|WARNING| Cannot find the ssh key {public_key or self.default_pub_key_path}") if stderr else None
        return None

    def get_by_id(self, key_id: int) -> Optional[digitalocean.SSHKey]:
        try:
            return self.__manager.get_ssh_key(ssh_key_id=key_id)
        except digitalocean.DataReadError:
            print(f"[red]|ERROR| SSH key with ID {key_id} was not found.")
            return None

    def get_by_name(self, key_name: str, stderr: bool = False) -> Optional[digitalocean.SSHKey]:
        for ssh_key in self.get_all():
            if ssh_key.name == key_name:
                return ssh_key
        print(f"[red]|WARNING| Cannot find the ssh key") if stderr else None
        return None

    def get_all_id(self):
        ssh_keys = self.get_all()
        if ssh_keys:
            return [key.id for key in ssh_keys]
        return []

    def get_id_by_name(self, ssh_key_name: str, stderr: bool = False) ->  Optional[int]:
        ssh_keys = self.get_all()

        for ssh_key in ssh_keys if ssh_keys else []:
            if ssh_key.name.lower() == ssh_key_name.lower():
                return ssh_key.id

        print(f"[red]|ERROR| Ssh key id for {ssh_key_name} was not found.") if stderr else None
        return None

    def check_key_name_exists(self, key_name: str) -> bool:
        return key_name in self.get_all_ssh_key_names()

    def read_default_pub_key(self, stderr: bool = False) -> Optional[str]:
        if isfile(self.default_pub_key_path):
            with open(self.default_pub_key_path, mode='r') as file:
                return file.read().strip()
        print(f"[red]|ERROR| SSH public key not found at path {self.default_pub_key_path}") if stderr else None
        return None

    def _get_ssh_key(self, ssh_key:  digitalocean.SSHKey | str | int) -> digitalocean.SSHKey:
        if isinstance(ssh_key, digitalocean.SSHKey):
            return ssh_key
        elif isinstance(ssh_key, str):
            return self.get_by_name(key_name=ssh_key)
        elif isinstance(ssh_key, int):
            return self.get_by_id(ssh_key)
