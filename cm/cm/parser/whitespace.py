from helpers import define

p_whitespace = define("""whitespace : SPACES \n| TABS""")
p_indent = define("""indent : TABS \n|""", default='')
p_breakable = define("""breakable : whitespace \n| EOL""")
p_w = define("""w : whitespace w \n|""", default='')
p_b = define("""b : breakable b \n|""", set=False)
p_c = define("""c : b ',' b \n| b""", set=False)
