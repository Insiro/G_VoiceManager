from src.config import Config
from src.mod_tool import ModTool

config = Config.load()
tool = ModTool(config)


# tool.move_and_link_original()


modName = "fem_wanderer_11"

# # insert Mod Source
tool.set_input_path()
tool.clear_mod_source()
state = tool.prepare_mod_source(modName)

# # Mod Generate
state = tool.pack_mod_files(modName, state)

# # Apply
tool.apply(modName)
# tool.restore(False)
# tool.restore(False)
# tool.restore(True)
