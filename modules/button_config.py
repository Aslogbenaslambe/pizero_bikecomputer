
class Button_Config():

  config = None

  #long press threshold of buttons [sec]
  G_BUTTON_LONG_PRESS = 1

  #GPIO button action (short press / long press) from gui_pyqt
  # call from SensorGPIO.my_callback(self, channel)
  # number is from GPIO.setmode(GPIO.BCM)
  G_BUTTON_DEF = {
    'PiTFT':{
      'MAIN':{
        5:('scroll_prev', ''),
        6:('count_laps', 'reset_count'),
        12:('brightness_control', ''),
        13:('start_and_stop_manual', ''),
        16:('scroll_next', 'enter_menu'),
      },
      'MENU':{
        5:('back_menu', ''),
        6:('', ''),
        12:('press_space', ''),
        13:('press_tab', ''),
        16:('press_down', ''),
      },
    },
    'Papirus':{
      'MAIN':{
        16:('scroll_prev', ''),#SW1(left)
        26:('count_laps', 'reset_count'),#SW2
        20:('start_and_stop_manual', ''),#SW3
        21:('scroll_next', 'enter_menu'),#SW4
      },
      'MENU':{
        16:('back_menu', ''),
        26:('press_space', ''),
        20:('press_tab', ''),
        21:('press_down', ''),
      },
    },
    'DFRobot_RPi_Display':{
      'MAIN':{
        21:('start_and_stop_manual', 'reset_count'),
        20:('scroll_next', 'enter_menu'),
      },
      'MENU':{
        21:('press_space', ''),
        20:('press_down', 'back_menu'),
      },
    },
    # call from ButtonShim
    'Button_Shim' : {
      'MAIN':{
        'A':('scroll_prev', ''),
        'B':('count_laps', 'reset_count'),
        'C':('get_screenshot', ''),
        'D':('start_and_stop_manual', ''),
        'E':('scroll_next', 'enter_menu'),
      },
      'MENU':{
        'A':('back_menu', ''),
        'B':('brightness_control', ''),
        'C':('press_space', ''),
        'D':('press_tab', ''),
        'E':('press_down', ''),
      },
      'MAP':{
        'A':('scroll_prev', ''),
        'B':('map_zoom_minus', ''),
        'C':('change_mode', ''),
        'D':('map_zoom_plus', ''),
        'E':('scroll_next', 'enter_menu'),
      },
      'MAP_1':{
        'A':('map_move_x_minus', 'map_zoom_minus'),
        'B':('map_move_y_minus', 'map_zoom_plus'),
        'C':('change_mode', 'map_change_move'),
        'D':('map_move_y_plus', ''),
        'E':('map_move_x_plus', ''),
      },
      'MAP_2':{
        'A':('map_zoom_minus', ''),
        'B':('map_zoom_plus', ''),
        'C':('change_mode', ''),
        'D':('', ''),
        'E':('map_search_route', ''),
      },
    },
    # call from sensor_ant
    'Edge_Remote':{
      'MAIN':{
        'PAGE':('scroll_prev', 'scroll_next'), 
        'CUSTOM':('change_mode', 'enter_menu'), 
        'LAP':('count_laps', ),
      },
      'MAIN_1':{
        'PAGE':('turn_on_off_light', 'brightness_control'), 
        'CUSTOM':('change_mode', ''), 
        'LAP':('start_and_stop_manual', ),
      },
      'MENU':{
        'PAGE':('press_down', ''),
        'CUSTOM':('press_tab', 'back_menu'),
        'LAP':('press_space', ),
      },
      'MAP':{
        'PAGE':('scroll_prev', 'scroll_next'),
        'CUSTOM':('map_zoom_plus', 'map_zoom_minus'), #plus along route / minus along route
        'LAP':('change_mode', ),  
      },
      'MAP_1':{
        'PAGE':('map_move_x_plus', 'map_move_x_minus'), #west / east
        'CUSTOM':('map_move_y_plus', 'map_move_y_minus'), #north / south
        'LAP':('change_mode', ),  
      },
      'MAP_2':{
        'PAGE':('map_change_move', ''), #useless
        'CUSTOM':('map_search_route', ''), 
        'LAP':('change_mode', ),
      },
    },
  }

  G_PAGE_MODE = 'MAIN'

  #mode group setting changed by change_mode
  G_BUTTON_MODE_IS_CHANGE = False
  G_BUTTON_MODE_PAGES = {
    'MAIN': ['MAIN','MAIN_1'],
    'MAP': ['MAP','MAP_1','MAP_2'],
  }
  G_BUTTON_MODE_INDEX = {
    'MAIN': 0,
    'MAP': 0,
  }

  def __init__(self, config):
      self.config = config

  def press_button(self, button_hard, press_button, index):
    if self.config.gui == None or self.config.gui.stack_widget == None:
      return

    w_index = self.config.gui.stack_widget.currentIndex()
    if w_index == 1:
      if self.config.gui.main_page.widget(self.config.gui.main_page.currentIndex()).__class__.__name__ == 'SimpleMapWidget':
        if not self.G_BUTTON_MODE_IS_CHANGE:
          self.G_PAGE_MODE = 'MAP'
      else:
        if not self.G_BUTTON_MODE_IS_CHANGE:
          self.G_PAGE_MODE = 'MAIN'
      #for no implementation
      if self.G_PAGE_MODE not in self.G_BUTTON_DEF[button_hard]:
        self.G_PAGE_MODE = 'MAIN'
    elif w_index >= 2:
      self.G_PAGE_MODE = 'MENU'

    func_str = self.G_BUTTON_DEF[button_hard][self.G_PAGE_MODE][press_button][index]
    if func_str == '':
      func_str = "dummy"
    func = eval('self.config.gui.'+func_str)
    func()

  def change_mode(self):
    #check MAP
    w = self.config.gui.main_page.widget(self.config.gui.main_page.currentIndex())

    if 'MAIN' in self.G_PAGE_MODE:
      self.change_mode_index("MAIN")
    #if display is MAP: change MAP_1 -> MAP_2 -> MAP -> ...
    elif w.__class__.__name__ == 'SimpleMapWidget':
      self.change_mode_index("MAP")
      #additional: lock current position when normal page
      if not self.G_BUTTON_MODE_IS_CHANGE:
        w.lock_on()
      else:
        w.lock_off()

  def change_mode_index(self, mode):
    self.G_BUTTON_MODE_INDEX[mode] = self.G_BUTTON_MODE_INDEX[mode] + 1
    self.G_BUTTON_MODE_IS_CHANGE = True
    if self.G_BUTTON_MODE_INDEX[mode] >= len(self.G_BUTTON_MODE_PAGES[mode]):
      self.G_BUTTON_MODE_INDEX[mode] = 0
      self.G_BUTTON_MODE_IS_CHANGE = False
    self.G_PAGE_MODE = self.G_BUTTON_MODE_PAGES[mode][self.G_BUTTON_MODE_INDEX[mode]]
