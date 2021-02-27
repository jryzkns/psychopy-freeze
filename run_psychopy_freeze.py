from psychopyfreezelib import PsychopyFreezeLib

# The folder where the experiment resides in
exp_path = "" 

# The file to run the experiment
exp_file = ""

# the name to give your experiment build, this doesn't really matter
build_name = ""

# where to put the final finished exe, and the name as well
exe_path = ""

ppylibinst = PsychopyFreezeLib(
            build_name,
            exp_path,
            exp_file,
            exe_path
        )

ppylibinst.run_all()
