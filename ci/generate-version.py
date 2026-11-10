import sys
import os
import subprocess


def run(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return ""


def get_version():
    # 取最近一个带标签的 commit，再用 git describe 得到版本号。
    # fork 默认不带标签，git describe 会失败，此时退回兜底版本，
    # 否则 appversion 写成空串会导致 .rc 资源文件的 FILEVERSION 格式非法 (RC2127)。
    commit = run('git rev-list --tags --max-count=1')
    if commit:
        tag = run('git describe --tags ' + commit)
        if tag:
            return tag[1:] if tag.startswith('v') else tag
    return "1.0.0"


if __name__ == '__main__':
    version = get_version()
    version_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../QtScrcpy/appversion")
    )
    with open(version_file, 'w') as f:
        f.write(version)
    sys.exit(0)
