import curses
import curses.ascii as asc
import time
import locale

locale.setlocale(locale.LC_ALL, '')

class Vis(object):
  def __init__(self, scr):
    self.scr = scr
    self.readings = {}
    self.screens = [
      (1, 1),
      (17, 1),
      (33, 1),
      (1, 22),
      (17, 22),
      (33, 22)
    ]
    self.screen_index = 0
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)
  
  def cleanup(self):
    curses.endwin()


  def register_reading(self, id, type, reading):
    if not id in self.readings:
      self.readings[id] = {
        'type': type,
        'data': [],
        'screen': None
      }
    
    self.readings[id]['data'].append(reading)

  def render(self):
    for key, reading in self.readings.iteritems():
      if reading['screen'] == None:
        windef = self.screens[self.screen_index]
        reading['screen'] = curses.newwin(15, 25, windef[0], windef[1])
        self.screen_index += 1
      
      if reading['type'] == 'ultrasound':
        self.render_us(key, reading)


  def color(self, minv, maxv, value):
    d = maxv - minv
    slic = float(d) / 3
    upperbound = minv + slic*2
    lowerbound = minv + slic

    if value > upperbound:
      return curses.color_pair(2)
    
    if value > lowerbound:
      return curses.color_pair(3)

    return curses.color_pair(1)

  def render_us(self, key, reading):
    raw_data = reading['data'][-1].raw()
    graphs = [["L"], ["M"], ["R"]]
    for d in raw_data:
      graphs[0].append( "*" if d['can_move'][0] else '_')
      graphs[1].append( "*" if d['can_move'][1] else '_')
      graphs[2].append( "*" if d['can_move'][2] else '_')

    freshness = reading['data'][-1].freshness()
    certainty = reading['data'][-1].certainty()
    verdict = reading['data'][-1].verdict()

    reading['screen'].clear()

    reading['screen'].addstr(1, 2, key)

    reading['screen'].addstr(2, 2, " ".join(graphs[0]).encode('utf-8'), curses.color_pair(2))
    reading['screen'].addstr(3, 2, " ".join(graphs[1]).encode('utf-8'), curses.color_pair(2))
    reading['screen'].addstr(4, 2, " ".join(graphs[2]).encode('utf-8'), curses.color_pair(2))

    reading['screen'].addstr(6, 2, 'Freshness')
    reading['screen'].addstr(6, 15, str(freshness), self.color(0, 1, freshness))

    reading['screen'].addstr(7, 2, 'Certainty')
    reading['screen'].addstr(7, 15, str(certainty), self.color(0, 1, certainty))

    reading['screen'].addstr(8, 2, 'Verdict')
    reading['screen'].addstr(8, 15, str(verdict), self.color(-1, 1, verdict))

    reading['screen'].border()
    reading['screen'].refresh()

def _create(screen):
  return Vis(screen)

def create_visualizer():
  return curses.wrapper(_create)
