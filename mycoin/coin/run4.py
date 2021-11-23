import stocastic_future
import sys

symbol = sys.argv[1]
leverage = int(sys.argv[2])
importance = float(sys.argv[3])


sfd = stocastic_future.StocasticFutureDeal(symbol + '/USDT', '15m', leverage)
sfd.run(10, 6, 6, importance, 14)