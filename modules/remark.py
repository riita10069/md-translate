import subprocess


def mdToJson(filename):
    subprocess.check_call('remark --use remark-directive --tree-out < ' + filename + '> output.json', shell=True)


def jsonToMd(filename):
    subprocess.check_call('remark -u remark-directive --tree-in < output.json > ' + filename, shell=True)
