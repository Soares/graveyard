from config import Config
from api.style import color

box = Config()
box.define('separator', '')
box.define('under-bar', '')
box.define('vline', ' ')
box.define('hline', ' ')
box.define('active-background', color('flashy'))
box.define('active-deselected', color('flashy'))
box.define('active-selected', color('normal'))
box.define('inactive-background', color('disabled'))
box.define('inactive-deselected', color('disabled'))
box.define('inactive-selected', color('disabled'))

bar = box.register('bar', inherit=True)
bar.set('vline', '')
bar.set('hline', '')
bar.define('active', None)
