import subprocess


def mdToJson(filename):
    filename = '"'+filename+'"'
    subprocess.check_call('remark --use remark-directive --tree-out < ' + filename + '> output.json', shell=True)


def jsonToMd(filename):
    filename = '"'+filename+'"'
    subprocess.check_call('remark -u remark-directive --tree-in < output.json > ' + filename, shell=True)
