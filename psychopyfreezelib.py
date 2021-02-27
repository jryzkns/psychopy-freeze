from distutils.dir_util import copy_tree, remove_tree
from shutil import copyfile
import os

class PsychopyFreezeLib:

    venv_name = 'gen'
    pkgs_path = os.path.join(venv_name, 'Lib', 'site-packages')
    
    # names of packages that need to be injected post-hoc
    posth_names = (
        'arabic_reshaper',
        'freetype',
        'matplotlib',
        'psychopy')

    # files/dirs in the final build folder that can be 
    # removed before sending to a self extracting archive
    hitlist = (
        'tests', 'testing',
        '__pycache__', 
        'imageio', 'imageio_ffmpeg',
        'images', 'sample_data',
        # TODO: lib2to3?
        )

    def __init__(self, build_name, main_dir, main_file, export_path, splash_path="SPLASH.bmp"):
        self.build_name = build_name
        self.pyinstaller_build_dest = os.path.join('dist', self.build_name)
        self.main_dir = main_dir
        self.main_file_path = main_file
        self.export_path = export_path
        self.splash_path = splash_path

        self.assets_path = os.path.join(main_dir,'assets')
        self.has_assets = os.path.isdir(self.assets_path)
        if self.has_assets:
            self.has_assets = [] != os.listdir(self.assets_path)

    def run_all(self, nocache=True):
        self.pyinstaller_build()
        self.module_inject()
        self.prune_build()
        self.NSIS_build()
        if nocache: self.clean_build()

    def pyinstaller_build(self):

        os.system(' '.join([    
            'pyinstaller',
            '--name', self.build_name,
            '--add-data' if self.has_assets else '',
            ('\"' + ';'.join([os.path.join(self.assets_path, '*'), 'assets']) + '\"')
                if self.has_assets else '',
            '--noconsole',
            self.main_file_path,
            '--noconfirm']))

    def module_inject(self):
        for module_name in self.posth_names:
            copy_tree(  os.path.join(self.pkgs_path, module_name),
                        os.path.join(self.pyinstaller_build_dest, module_name))

    def prune_build(self):
        for root, directories, filenames in os.walk(self.pyinstaller_build_dest):
            for directory in directories: 
                p_ = os.path.join(root, directory)
                if directory in self.hitlist:
                    remove_tree(p_)

    def NSIS_build(self):
        copyfile(self.splash_path, os.path.join(self.pyinstaller_build_dest, "SPLASH.bmp"))
        with open(os.path.join(self.pyinstaller_build_dest, 'setup.nsi'), 'w') as setup_file:
            setup_file.write('\n'.join([
                f'Name \"{self.build_name}\"',
                f'OutFile {self.export_path}',
                'SilentInstall silent',
                "Function .onInit",
                " SetOutPath $TEMP",
                " File /oname=spltmp.bmp \"SPLASH.bmp\"",
                " splash::show 10000 $TEMP\spltmp",
                " Pop $0",
                " Delete $TEMP\spltmp.bmp",
                "FunctionEnd", 
                'Section',
                'InitPluginsDir',
                'SetOutPath \"$PLUGINSDIR\"',
                'File /r \"*\"',
                f'ExecWait \'\"$PLUGINSDIR\{self.build_name}.exe\"\'',
                'SectionEnd']))
        os.system(" ".join(['makensis', os.path.join(self.pyinstaller_build_dest, 'setup.nsi')]))

    def clean_build(self):
        if os.path.exists('dist'): remove_tree('dist')
        if os.path.exists('build'): remove_tree('build')
