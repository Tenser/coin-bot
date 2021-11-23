import sys
import stocastic

market = sys.argv[1] + '/KRW'
importance = float(sys.argv[2])
gap = float(sys.argv[3])

sd = stocastic.StocasticDeal(market)
sd.run(10, 6, 6, importance, '15m', gap)
