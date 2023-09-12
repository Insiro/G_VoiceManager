from config import Config
from mod_apply import ModApplier

config = Config.load()
modi = ModApplier(config)
modi.set_input_path(config.backup_path)
modi.move_and_link()
modi.clear_mod_source()
state = modi.prepare_mod_source("fem_wanderer_11")
state = modi.pack_mod_files(0)
modi.save_mod_file("fem_wanderer_11", 1)

modi.apply("fem_wanderer_11")
# os.unlink(config.sym_path)
