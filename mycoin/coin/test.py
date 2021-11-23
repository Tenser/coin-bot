from api_manager import ApiManager
import time
import requests
import json
import sys

standard = float(sys.argv[1])

am = ApiManager()
    
am.run(standard)