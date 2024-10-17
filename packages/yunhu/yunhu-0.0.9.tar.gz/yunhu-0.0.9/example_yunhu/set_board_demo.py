from yunhu.openapi import Openapi
import time
import json
import requests

def main():
    openapi = Openapi("token")
    res = openapi.SetBotBoardAll("text", "py测试333", int(time.time()) + 600)
    print(res.text)

    
    
if __name__ == '__main__':
    main()