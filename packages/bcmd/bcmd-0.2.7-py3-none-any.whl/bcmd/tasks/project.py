import importlib.resources
import os
from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bfile, binput, bpath, btask
from beni.bfunc import syncCall

from . import venv

app: Final = btask.newSubApp('project 工具')


@app.command()
@syncCall
async def gen_init_py(
    workspace_path: Path = typer.Argument(None, help='workspace 路径'),
):
    '将指定目录下的所有文件生成 __init__.py 文件'

    async def makeInitFiles(p: Path):
        if p.name == '__pycache__':
            return
        if p.name.startswith('.'):
            return
        if workspace_path != p:
            initFile = p / '__init__.py'
            if not initFile.exists():
                bcolor.printYellow(initFile)
                await bfile.writeText(initFile, '')
        for x in bpath.listDir(p):
            await makeInitFiles(x)

    if not workspace_path:
        workspace_path = Path.cwd()
    await makeInitFiles(workspace_path)
    bcolor.printGreen('OK')


@app.command()
@syncCall
async def new():
    currentPath = bpath.get(os.getcwd())
    for _ in currentPath.glob('**/*'):
        await binput.confirm(f'当前路径为非空目录，确认是否要继续？')
        break
    venv.venv(
        packages=['benimang'],
        path=currentPath,
        quiet=True,
    )
    with importlib.resources.path('bcmd.resources', 'project') as path:
        for p in bpath.listDir(path):
            bpath.copy(p, currentPath / p.name)
    bcolor.printGreen('OK')
