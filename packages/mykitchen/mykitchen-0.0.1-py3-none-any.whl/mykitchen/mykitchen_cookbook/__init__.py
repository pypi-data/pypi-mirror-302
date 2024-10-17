import djp

@djp.hookimpl
def settings(current_settings):
    current_settings["KITCHENAI"]["mykitchen_cookbook"] = "mykitchen.mykitchen_cookbook.kitchen.router"