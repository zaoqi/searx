### Set up a python3 development environment 
```
When you have a python3 environment, pip3 install -r requirements.txt
```
### Now our code has been tracked with git LFS
```
First, you need run brew install git-lfs（Assuming you are in Mac development environment) 
Second, you should run git lfs install before clone codes

```
### How to run a development server
```bash
env FLASK_APP=searx.webapp FLASK_ENV=development FLASK_DEBUG=1 SEARX_SETTINGS_PATH=settings_et_dev.yml python -m flask run
```

### Entropage theme

```
cd searx/static/themes/entropage
npm i
npm start
```

* less: `themes/entropage/less`
* js: `themes/entropage/js/searx_src`