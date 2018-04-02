import curses

stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)


win = curses.newwin(5, 50, 1, 1)



def print_ultrasound(us_reading):
  raw_data = us_reading.raw()

  graphs = [[], [], []]

  for reading in raw_data:
    graphs[0].append( '|' if reading['can_move'][0] else '.')

  
  win.addstr(graphs[0], curses.color_pair(1))
  win.refresh()