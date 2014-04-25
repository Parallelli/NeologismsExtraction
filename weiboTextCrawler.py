#usage:
#crawl raw weibo text data from sina weibo users(my followees)
#in total, there are 20080 weibo tweets, because there is uplimit for crawler

# -*- coding: utf-8 -*-
import weibo

APP_KEY = 'your app_key'
APP_SECRET = 'your app_secret'
CALL_BACK = 'your call back url'

def run():
	token = "your access token gotten from call_back url"
	client = weibo.APIClient(APP_KEY, APP_SECRET, CALL_BACK)
	client.set_access_token(token,12345)

	followlist = client.friendships.friends.get(screen_name='蜀云Parallelli',count=200)
	wb_raw = open('weibo_raw_userlistweibo_big.txt','w')
	weiboCnt = 0
	usernames = {}
	for fl in followlist.users:
		pg = 1
		wbres = client.statuses.user_timeline.get(screen_name=fl.screen_name,page=pg)
		while (pg <= 3):
			wbres = client.statuses.user_timeline.get(screen_name=fl.screen_name,page=pg)
			if fl.screen_name not in usernames:
				usernames[fl.screen_name]=1

			for wb in wbres.statuses:
				weiboCnt += 1
				wb_raw.write(wb.text.encode('utf-8')+'\n')
			pg += 1
	followlist = client.friendships.friends.get(screen_name='尹欢欢欢',count=200)
	for fl in followlist.users:
		pg = 1
		if fl.screen_name in usernames: 
			continue
		wbres = client.statuses.user_timeline.get(screen_name=fl.screen_name,page=pg)
		while (pg <= 3):
			wbres = client.statuses.user_timeline.get(screen_name=fl.screen_name,page=pg)
			if fl.screen_name not in usernames:
				usernames[fl.screen_name]=1

			for wb in wbres.statuses:
				weiboCnt += 1
				wb_raw.write(wb.text.encode('utf-8')+'\n')
			pg += 1
	print weiboCnt
	wb_raw.close()
	
if __name__ == "__main__":
	run()