from framework.db import models
from framework.config import config
from framework.dependency_management.dependency_resolver import BaseComponent
from framework.dependency_management.interfaces import ResourceInterface
from framework.lib.general import cprint
import os
import logging
from framework.utils import FileOperations

class ResourceDB(BaseComponent, ResourceInterface):

<<<<<<< HEAD
    COMPONENT_NAME = "resource"

    def __init__(self):
        self.register_in_service_locator()
        self.config = self.get_component("config")
        self.db_config = self.get_component("db_config")
        self.target = self.get_component("target")
        self.db = self.get_component("db")
        self.LoadResourceDBFromFile(self.config.get_profile_path("RESOURCES_PROFILE"))
=======
class ResourceDB(object):
    def __init__(self, Core):
        self.Core = Core
        self.LoadResourceDBFromFile(self.Core.Config.get_profile_path("RESOURCES_PROFILE"))
>>>>>>> 266a0088788706b7914038e7c568bc3a6621f4b8

    def LoadResourceDBFromFile(self, file_path): # This needs to be a list instead of a dictionary to preserve order in python < 2.7
        logging.info("Loading Resources from: " + file_path + " ..")
        resources = self.GetResourcesFromFile(file_path)
        # Delete all old resources which are not edited by user
        # because we may have updated the resource
        self.db.session.query(models.Resource).filter_by(dirty=False).delete()
        # resources = [(Type, Name, Resource), (Type, Name, Resource),]
        for Type, Name, Resource in resources:
<<<<<<< HEAD
            self.db.session.add(models.Resource(resource_type = Type, resource_name = Name, resource = Resource))
        self.db.session.commit()

    def GetResourcesFromFile(self, resource_file):
        resources = set()
        ConfigFile = FileOperations.open(resource_file, 'r').read().splitlines() # To remove stupid '\n' at the end
=======
            # TODO: Need more filtering to avoid duplicates when users are allowed to edit resources from interface
            # if self.Core.DB.session.query(models.Resource).filter_by(resource_type = Type, resource_name = Name, resource = Resource).count() == 0:
            self.Core.DB.session.add(models.Resource(resource_type = Type, resource_name = Name, resource = Resource))
        self.Core.DB.session.commit()

    def GetResourcesFromFile(self, resource_file):
        resources = set()
        ConfigFile = self.Core.open(resource_file, 'r').read().splitlines() # To remove stupid '\n' at the end
>>>>>>> 266a0088788706b7914038e7c568bc3a6621f4b8
        for line in ConfigFile:
            if '#' == line[0]:
                continue # Skip comment lines
            try:
                Type, Name, Resource = line.split('_____')
                # Resource = Resource.strip()
                resources.add((Type, Name, Resource))
            except ValueError:
                cprint("ERROR: The delimiter is incorrect in this line at Resource File: "+str(line.split('_____')))
        return resources

    def GetReplacementDict(self):
        configuration = self.db_config.GetReplacementDict()
        configuration.update(self.target.GetTargetConfig())
        configuration.update(self.config.GetReplacementDict())
        return configuration

    def GetRawResources(self, ResourceType):
        filter_query = self.db.session.query(models.Resource.resource_name, models.Resource.resource).filter_by(resource_type = ResourceType)
        # Sorting is necessary for working of ExtractURLs, since it must run after main command, so order is imp
        sort_query = filter_query.order_by(models.Resource.id)
        raw_resources = sort_query.all()
        return raw_resources

    def GetResources(self, ResourceType):
        replacement_dict = self.GetReplacementDict()
        raw_resources = self.GetRawResources(ResourceType)
        resources = []
        for name, resource in raw_resources:
            resources.append([name, self.config.MultipleReplace(resource, replacement_dict)])
        return resources

    def GetRawResourceList(self, ResourceList):
        raw_resources = self.db.session.query(models.Resource.resource_name, models.Resource.resource).filter(models.Resource.resource_type.in_(ResourceList)).all()
        return raw_resources

    def GetResourceList(self, ResourceTypeList):
        replacement_dict = self.GetReplacementDict()
        raw_resources = self.GetRawResourceList(ResourceTypeList)
        resources = []
        for name, resource in raw_resources:
            resources.append([name, self.config.MultipleReplace(resource, replacement_dict)])
        return resources
