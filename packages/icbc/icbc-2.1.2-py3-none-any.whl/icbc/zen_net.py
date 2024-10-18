# coding:utf-8
from icbc import z
try:
    import tornado.web
except:
    print("引入tornado失败，本模块功能基于tornado，为了方便内网环境无网使用基础模块，最新版本已移除tornado依赖，请另行使用pip install tornado安装以用zen_net功能")
    input()
def post(url, post_data):
    import urllib.request
    try:
        req_data = post_data.encode("utf-8")
    except:
        req_data = post_data
    request = urllib.request.Request(url, req_data)
    response = urllib.request.urlopen(request)
    return response.read()
    
def get(url):
    import urllib.request
    response = urllib.request.urlopen(url)
    return response.read()

def push_web(server, key, web):
    "note:only for gae api,web"
    result = {"api":"web", "key":key, "content":web, "permission":"icbc", "action" : "push"}
    result = z.json_dumps(result)
    post(server, result)

def tornado_server(port=8888):
    "tornado_server标准参考例子"
    import tornado.ioloop
    import tornado.web
    class main_handler(tornado.web.RequestHandler):
        def get(self):
            print(self.get_argument(''))
            self.write("get")
        def post(self):
            client_ip = self.request.remote_ip
            for i in  self.request.arguments:
                print(i)
            s = self.get_arguments("body")
            print(s)
            self.write("post")
    application = tornado.web.Application([(r"/", main_handler), ])
    application.listen(port)
    print("start web")
    tornado.ioloop.IOLoop.instance().start()


def file_server(nado, url=r"/file" , port=8031):
    import tornado.ioloop
    import tornado.web
    class UploadFileHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("""
            <html>
              <body>
                <form action='file' enctype="multipart/form-data" method='post'>
                <input type='submit' value='submit'/>
                <input type='file' name='file'/>
                </form>
              </body>
            </html>""")
        def post(self):
            file_metas = self.request.files['file']
            for meta in file_metas:
                filename = meta['filename']
                filename_save = z.join(nado, filename)
                with open(filename_save, 'wb') as up:
                    up.write(meta['body'])
                self.write(filename + ' finished!')
    address = "http://%s:%d%s" % (z.get_ip() , port, url)
    print(address)
    app = tornado.web.Application([
        (url, UploadFileHandler),
    ])
     
    if __name__ == '__main__':
        app.listen(port)
        tornado.ioloop.IOLoop.instance().start()

url_router=[]
def router_regist(url, handler):
    url_router.append((r"/" + url, handler))
def router_static_regist(url="static", path="./static"):
    url_router.append(('/'+url+'/(.*)', tornado.web.StaticFileHandler, {'path': path}))
def func_static(url="static", path="./static"):
    url_router.append(('/'+url+'/(.*)', tornado.web.StaticFileHandler, {'path': path}))
def func_file(url="file",filepath="static",is_download=True):
    tp_upload="""
<html>

<head>
    <link href="favicon.ico" rel="shortcut icon">
</head>

<body>
    <h2>上传文件</h2>
    <form action="#url_file#" enctype="multipart/form-data" method='post'>
        <input type="submit" value="提交" />
        <input type="file" name="file" />
    </form>
    <h2>上传文本</h2>
    <form action="#url_file#" method="post" id="fff">
        <label for="k">索引:</label>
        <input type="text" id="k" name="key">
        <input type="submit" value="提交"><br>
        <label for="v">文本:</label>
        <textarea id="v" name="value" cols=40 rows=20></textarea><br>
    </form>
    <br>
    <h2>已上传文件</h2>
    <a href="#url_file#?list">文件清单</a>
</body>
</html>
"""
    tp_func_file=tp_upload.replace("#url_file#",url)
    tp_list="""
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
</head>
<style>
    #filelist {
        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
        width: 100%;
        border-collapse: collapse;
    }

    #filelist td,
    #filelist th {
        width: 20px;
        font-size: 1em;
        border: 1px solid #98bf21;
        padding: 3px 7px 2px 7px;
    }

    #filelist th {
        font-size: 1.1em;
        text-align: left;
        padding-top: 5px;
        padding-bottom: 4px;
        background-color: #A7C942;
        color: #ffffff;
    }

    #filelist tr.alt td {
        color: #000000;
        background-color: #EAF2D3;
    }
</style>

<body>
    <h2>已上传文件</h2>
    <table id="filelist">
        <tr>
            <th>时间</th>
            <th>文件名</th>
            <th>大小</th>
        </tr>
        #table content#
    </table>

</body>

</html>"""
    tp_line='<tr><td>%s</td><td><a href="%s">%s</td><td>%s</td></tr>\n'
    def gen_index(folder):
        import os
        path=z.getcwd()
        flist=z.list_file (z.join(path,folder))
        dict_file={}
        result=[]
        for i in flist:
            file_localfull=z.join(path,folder,i)
            file_url=z.join("/",folder,i)
            file_size=os.path.getsize(file_localfull)/1024
            ts=z.fmt(os.path.getatime(file_localfull),"%Y-%m-%d %H:%M")
            dict_file[ts+i]=(ts,file_url,i,"%.0fKB" % file_size)
        result=""
        for i in sorted(dict_file,reverse=True):
            result=result+tp_line%dict_file[i]
        return result    

    class upload_file_handler(tornado.web.RequestHandler):
        def get(self):
            if len(self.get_arguments("list"))>0:
                self.write(tp_list.replace("#table content#",gen_index(filepath)))
            else:
                self.write(tp_func_file)
        def post(self):
            kkk=self.get_body_arguments("key")
            vvv=self.get_body_arguments("value")
            if len(kkk)==1 and len(vvv)==1:
                if kkk[0]=="":
                    filename =z.fmt()+".txt"
                    
                else:
                    filename= kkk[0]+".txt"
                filename_save = z.join(z.folder(filepath),filename)
                with open(filename_save,"w") as up:
                        up.write(vvv[0])
                self.write(filename + ' finished!')
                return
            if "file"in self.request.files:
                file_metas = self.request.files['file']
                for meta in file_metas:
                    filename = meta['filename']
                    filename_save = z.join(z.folder(filepath), filename)
                    with open(filename_save, 'wb') as up:
                        up.write(meta['body'])
                    self.write(filename + ' finished!')
    router_regist(url,upload_file_handler)
    if is_download:
        z.folder(filepath)
        router_static_regist(filepath,filepath)
        
        
    
def basic_server(port=8888,router=None,settings={"gzip" : True,"debug" : True}):
    import tornado.ioloop
    import tornado.web
    z.dbp("服务器启动,服务端口：",port)
    if router ==None:
        router=url_router
        z.dbp("路由采用router_regist模式")
    print("-"*20+"router list"+"-"*20)
    for i in router:
        print(i[0],max((20-len(i[0])),0)*" ",i[1])
    print("-"*50)
    application = tornado.web.Application(router,**settings)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    
##def push_web():
##    z.sleep(2)
##    print("start demo")
##    push_web("http://127.0.0.1:8888/", "test", "ttttttttttttt")
##def test_tornado_server():
##    z.new_thread()
##    tornado_server()
##def test_file_server():
##    file_server("/Users/l/code/test/")
if __name__ == "__main__":
##    print(z.getcwd())
##    file_server(z.getcwd())
    z.taskkill_port(80)
    
    func_file("file",)
    basic_server(80)
