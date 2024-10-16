from importlib import metadata
from nautobot.extras.plugins import PluginConfig

__version__ = metadata.version(__name__)


class SFPInventoryConfig(PluginConfig):
    name = 'nautobot_sfp_inventory'
    verbose_name = 'SFP Inventory'
    description = 'A plugin for SFP inventory management'
    version = __version__
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = 'nautobot_sfp_inventory'
    searchable_models = ["sfp", "sfptype"]

    def ready(self):
        super().ready()


config = SFPInventoryConfig
