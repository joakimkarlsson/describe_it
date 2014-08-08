#!/usr/bin/env python
import subprocess as sp
import sys
from os.path import join, dirname, realpath


TITLE_FAIL = 'ACH!'
TITLE_SUCCEED = 'YAY!'
MESSAGE_SUCCEED = 'Tests passed!'
MESSAGE_FAIL = 'Tests failed!'

def null_notify(res):
    pass


def win32_notify(res):
    if res:
        sp.call(
            ['toast', '-t', TITLE_FAIL, '-m', MESSAGE_FAIL, '-silent'])
    else:
        sp.call(
            ['toast', '-t', TITLE_SUCCEED, '-m', MESSAGE_SUCCEED, '-silent'])


def macos_notify(res):
    message = MESSAGE_FAIL if res else MESSAGE_SUCCEED
    title = TITLE_FAIL if res else TITLE_SUCCEED
    sp.call(
        ['osascript', '-e', 'display notification "{message}" '
         'with title "{title}"'.format(message=message,
                                       title=title)])


def notify(res):
    notifiers = {
        'win32': win32_notify,
        'darwin': macos_notify
    }
    notifier = notifiers.get(sys.platform, null_notify)
    notifier(res)


def script_dir():
    return dirname(realpath(__file__))


def setup_script():
    return join(script_dir(), 'setup.py')


def main():
    res = sp.call([sys.executable, setup_script(), 'test'])
    notify(res)
    return res


if __name__ == '__main__':
    sys.exit(main())
