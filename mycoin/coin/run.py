import sys
import copy_money

cm = copy_money.CopyMoney()
filter_limit = int(sys.argv[1])
buy_limit = int(sys.argv[2])
windows = int(sys.argv[3])
importance = float(sys.argv[4])
cm.run(filter_limit, buy_limit, windows, importance)