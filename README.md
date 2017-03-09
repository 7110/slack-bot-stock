# Slack bot for Stock

### points
* get stock info on Slack
* written by _Python_
* be able to save user stock info to DB


### how to use
* 銘柄コードを聞く  
`search [銘柄名(部分一致可)]`  
* 銘柄の現在価格等を聞く  
`get [銘柄コード]`  
* 銘柄の登録、登録銘柄の更新  
`register [銘柄コード] [株式数] [取得価格]`  
* 登録銘柄の消去  
`delete [銘柄コード]`  
* 登録銘柄の現在価格等を聞く  
`check`  


### how to make bot (on Slack)
  * click [App & integrations]
  * search [Bots]
  * add [Congiguration]
  * get [API TOKEN]


### how to deploy to Heroku
`brew install heroku`  
`heroku login`  
`git init`  
`heroku git:remote -a slack-bot-stock`  
`git add .`  
`git commit`  
`git push heroku master`  
`heroku ps:scale slack-bot-stock=1`  

`heroku config:add API_TOKEN=[your api token]`  

`heroku run bash`  
`python run.py`  
