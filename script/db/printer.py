from app.lib.cli import CLIColor


class ProgressPrinter(object):

    def __init__(self, quiet=False, width=40):
        self.quiet = quiet
        self.width = width

    def results(self, successes, skips, failures):
        if self.quiet:
            return

        print "Done:",

        if successes:
            print CLIColor.ok_green("{} successful,".format(len(successes))),
        else:
            print "0 successful,",

        print "{} skipped,".format(len(skips)),

        if failures:
            print CLIColor.ok_green("{} failed".format(len(failures))),
        else:
            print "0 failed"

    def line(self):
        if not self.quiet:
            print "-" * self.width

    def begin_status_line(self, item):
        if not self.quiet:
            print item + (" " * (self.width - 8 - len(item))),

    def status_success(self):
        if not self.quiet:
            print "Success"

    def status_skip(self):
        if not self.quiet:
            print "   Skip"

    def status_fail(self):
        if not self.quiet:
            print "   Fail"
