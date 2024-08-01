# -*- coding: utf-8 -*-
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
