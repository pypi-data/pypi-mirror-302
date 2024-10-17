from yunhu.openapi import Openapi
import time

def main():
    openapi = Openapi("a2c89824e6604da6ac196347f388c984")
    res = openapi.SetBotBoardAll("text", "py测试111", time.time() + 600)
    print(res.content)
    
    
if __name__ == '__main__':
    main()