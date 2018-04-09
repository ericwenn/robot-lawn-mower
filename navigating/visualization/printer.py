import curses
import curses.ascii as asc
import time
import locale


class Vis(object):
  def __init__(self, scr):
    self.scr = scr
    self.readings = {}
    self.screens = [
      (1, 1),
      (1, 27),
      (1, 53),
      (17, 1),
      (17, 27),
      (33, 1),
      (33, 27)
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
      
      if reading['type'] == 'ultrasound' or reading['type'] == 'camera':
        self.render_sensor(key, reading)
      
      if reading['type'] == 'can_move_forward':
        self.render_can_move(key, reading)
    
    #self.scr.refresh()


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

  def render_sensor(self, key, reading):
    raw_data = reading['data'][-1].raw()
    graphs = []
    if len(raw_data[0]['payload']['can_move']) == 3:
      graphs = [["L"], ["M"], ["R"]]
    else:
      graphs = [["L"], ["R"]]

    
    for d in raw_data:
      for i in range(len(d['payload']['can_move'])):
        graphs[i].append( '*' if d['payload']['can_move'][0] else '_')

    freshness = reading['data'][-1].freshness()
    certainty = reading['data'][-1].certainty()
    verdict = reading['data'][-1].verdict()

    reading['screen'].clear()

    row = 1

    reading['screen'].addstr(1, 2, key)
    row += 1

    for g in graphs:
      reading['screen'].addstr(row, 2, " ".join(g), curses.color_pair(2))
      row += 1
      
    row += 2

    reading['screen'].addstr(row, 2, 'Freshness')
    reading['screen'].addstr(row, 15, str(freshness), self.color(0, 1, freshness))
    row +=1

    reading['screen'].addstr(row, 2, 'Certainty')
    reading['screen'].addstr(row, 15, str(certainty), self.color(0, 1, certainty))
    row +=1

    reading['screen'].addstr(row, 2, 'Verdict')
    reading['screen'].addstr(row, 15, str(verdict), self.color(-1, 1, verdict))
    row +=1

    reading['screen'].border()
    reading['screen'].refresh()
  
  def render_can_move(self, key, reading):
    data = reading['data'][-1]

    reading['screen'].clear()
    reading['screen'].addstr(1, 2, key)
    
    reading['screen'].addstr(2, 2, 'Verdict')
    reading['screen'].addstr(2, 15, str(data[0]), self.color(-1, 1, data[0]))

    reading['screen'].addstr(3, 2, 'Certainty')
    reading['screen'].addstr(3, 15, str(data[1]), self.color(-1, 1, data[1]))

    reading['screen'].border()
    reading['screen'].refresh()


def _create(screen):
  return Vis(screen)

def create_visualizer():
  return curses.wrapper(_create)
