import curses


def print_ultrasound(scr, us_reading):
  raw_data = us_reading.raw()

  graphs = [[], [], []]

  for reading in raw_data:
    graphs[0].append( '|' if reading['can_move'][0] else '.')

  # print "".join(graphs[0])
  scr.addstr("".join(graphs[0]), curses.color_pair(1))
  scr.refresh()