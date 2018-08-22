#!/usr/bin/env python3

from alfred import Alfred

if __name__ == "__main__":
    alfred = Alfred()
    alfred.add_commands()
    alfred.add_menus()
    alfred.launch()
