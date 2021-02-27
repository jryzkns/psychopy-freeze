# psychopy-freeze

## Overview

This repository holds a tool that generates a single-file **Windows** executable from a Psychopy experiment.

In broad strokes, it does its job in 2 steps:

 - [PyInstaller] freezing the Psychopy project into a folder with executable
 - [NSIS] packing the folder into a standalone executable

## Setup (IMPORTANT)

This section outlines the components required to get up and running.

### NSIS

NSIS is the tool that needs to be installed in order to pack the folder containing the executable into a single executable, download `NSIS 3.06.1` from here:

https://nsis.sourceforge.io/Download

make sure that `makensis` is in `PATH` after installation. You can check that you have done this properly via the command in cmd/powershell

```ps1
makensis -version 
```

If installed correctly, it should spit out the version number.

### Python Virtual environment

A python virtual environment (venv) is crucial for keeping things clean and some other reasons (that you will see later in this document). Suppose you are going to make a venv named `gen`, then the commands to do so would be the following:

```ps1
# create venv
py -m venv gen

# activate the venv
gen/scripts/activate.bat
```

There will be a new folder in your directory with the name of the venv that is set up.

Please call the venv that you create `gen`!

### Python dependencies

Install up-to-date version of pyinstaller-hooks-contrib. <sub>[why?](https://stackoverflow.com/questions/63052345/pyinstaller-and-opengl-error-importerror-cannot-import-name-opengl-arrays-mod)</sub>

```ps1
git clone https://github.com/pyinstaller/pyinstaller-hooks-contrib.git
cd pyinstaller-hooks-contrib
python setup.py install
cd ..
```

Install psychopy and pyinstaller. Make sure your project is built for the psychopy version that is installed here. Test your psychopy project with this venv to make sure (!!!)

```ps1
pip install psychopy pyinstaller
```

Install other dependencies (this is a volatile section that will grow over time to check back on this often)

```ps1
pip install tornado
```

## Running the psychopy-freeze GUI application

A GUI application has been developed allow people with no programming experience to work with psychopy-freeze. The GUI application additionally requires the `pyQt5` package that could be installed with the following command (run this while your venv is active!):

```ps1
pip install PyQt5
```

On windows, simply double click on `run.bat`. This will enable the venv and run a GUI interface to psychopy-freeze. On other platforms, well they're not supported so there's that.

You can manually run the GUI application by activating your venv then running `main.py` as well.

A typical usage would look something like this:

- Click on the topmost `...` button and select the `experiment folder`
- The program will automatically try to figure out if you have a `main.py` and fill in the next field. If it's not filled in, manually select it by clicking on the second top-most `...` button
- Give the experiment a name, it will default to the name of your `experiment folder`, you can change it if you don't like it
- Press `Generate!`, a file selector will pop up to ask you where you want your finished executable to go. Select your desired location and continue with the build
- Once the build completes, the finished executable will be shown to you via the file explorer

## Running the psychopy-freeze CLI application

If you are looking to feel like a hacker, feel free to check out `run_psychopy_freeze.py` for an example usage of psychopy-freeze.

## Guidelines for successfully setting up an experiment to freeze

- It goes without saying that an experiment should have its own folder, we will refer to this folder as the `experiment folder`
- The python file to run for your experiment should be called `main.py`, in the `experiment folder`
- Any assets that are used in the experiment (basically any file that is used in the experiment that is NOT a `.py` file) needs to be in a folder called `assets`. `assets` needs to be in the same level as `main.py`, all in the `experiment folder`. Even if you don't use assets, you should still make this folder and just leave it blank. To not have to deal with the annoying `\\` path separators in Windows, consider using `os.path.join`.

jryzkns 2020