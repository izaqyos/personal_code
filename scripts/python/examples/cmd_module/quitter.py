import cmd

class Quitter(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "Quitter: "

    def do_quit(self, line):
        """Quits you out of Quitter."""
        print "Quitting..."
        return 1

if __name__ == '__main__':
        quitter = Quitter()
        quitter . cmdloop()