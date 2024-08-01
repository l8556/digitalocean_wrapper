# -*- coding: utf-8 -*-
from typing import Optional

import digitalocean

from .auth import Token
from .digitalocean_prodjects import DigitalOceanProjects
from .droplet import Droplet
from .ssh_key import SSHKey


class DigitalOceanWrapper:

    def __init__(self):
        self.__token = Token().get()
        self.manager = digitalocean.Manager(token=self.__token)
        self.project = DigitalOceanProjects(manager=self.manager)
        self.droplet = Droplet(do_token=self.__token, manager=self.manager, project=self.project)
        self.ssh_key = SSHKey(manager=self.manager, do_token=self.__token)

    def get_ssh_keys(self) -> list[digitalocean.SSHKey]:
        return self.ssh_key.get_all()

    def get_all_ssh_keys_id(self) -> list:
        return self.ssh_key.get_all_id()

    def get_ssh_key_id_by_name(self, ssh_key_name: str) -> Optional[int]:
        return self.ssh_key.get_id_by_name(ssh_key_name=ssh_key_name)
