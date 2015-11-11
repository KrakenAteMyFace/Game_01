import cx_Freeze

executables = [cx_Freeze.Executable("main.py"),cx_Freeze.Executable("entity.py"),cx_Freeze.Executable("constants.py")]

cx_Freeze.setup(
    name="2D Shooter",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["resources\crosshair.png","resources\hud_back.png","resources\hud_front.png","resources\player.png"]}},
    executables = executables

    )