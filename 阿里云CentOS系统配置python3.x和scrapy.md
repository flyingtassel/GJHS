#CentOS+python3.x+scrapy配置
最近搞了个阿里云￥199/年1核2G的ECS，本来打算把去年买的域名拿来备案后做wordpress博客，结果发现北京管局至今还在用幕布拍照，遂作罢。反正闲着也是闲着，干脆拿来跑爬虫得了。
问题是，当初选择的镜像是阿里云推的一个[Plesk可视化管理面板（LAMP全能开发环境 centos7）](https://market.aliyun.com/products/53690006/cmjj019702.html?spm=5176.2020520132.101.5.KS3OMB)，用了用感觉还不错，又已经预装了python2.7.5，懒得再去找其他镜像从头折腾起来，于是就决定在这镜像的基础上开始搞了。

## 主要的坑
### python版本问题
首先众所周知scrapy现在还没正式支持python3（主要是twisted的锅），所以一开始我就打算直接用镜像配好的2.7.5直接上了，没想到居然安装出错，缺少`python.h`。搜了一下这个应该是C编译器的依赖包的问题，再`pip install python-dev`的时候发现：
```
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-build-StuwYn/python-dev/setup.py", line 90, in <module>
        evalall()
      File "/tmp/pip-build-StuwYn/python-dev/setup.py", line 86, in evalall
        print("安装完成!")
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)

```

很明显，且不说这中文提示的编码问题，看到`print`后面的`()`我们就猜到阿里云源上的这个包是python3的……怎么办，换源再试试？等一下，这个时候我才想起来自己手头的scrapy爬虫都是在python3下面写的，就算装好了也跑不起来啊。所以怼上python3势在必行。

可是python3又怎么跟现在的python2和谐共处呢？一番搜索，还真有前辈干过这种事情：[CentOS7.3安装Python3.6](http://blog.csdn.net/hobohero/article/details/54381475)。正好之前用的版本就是3.6.1，就照这个来吧。

#### 安装python3.6可能使用的依赖

\# yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel

#### 下载python3.6编译安装

到python官网下载https://www.python.org
下载最新版源码，这里我用的是3.6.1，可以根据自己版本调整。如果服务器wget速度太慢也可以自己下到本地后用`rz`命令传，找不到该命令的话就先`yum install lrzsz`安装，然后:
\# wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
\# tar -xzvf Python-3.6.1.tgz -C  /tmp
\# cd  /tmp/Python-3.6.1/

把Python3.6.1安装到 `/usr/local` 目录：

\# ./configure --prefix=/usr/local

**注意：这里要使用make altinstall，如果使用make install，在系统中将会有两个不同版本的Python在/usr/bin/目录中。这将会导致很多问题，而且不好处理。**

\# make && make altinstall

装完之后输入`python3 -V`，能看到版本就算OK了。

#### python3.6的环境配置

python3.6程序的执行文件：/usr/local/bin/python3.6
python3.6应用程序目录：/usr/local/lib/python3.6
pip3的执行文件：/usr/local/bin/pip3.6
pyenv3的执行文件：/usr/local/bin/pyenv-3.6

做软连接，更改/usr/bin/python的指向

\# cd /usr/bin

备份原本的python2程序

\# mv  python python.backup

软连接3.6的执行程序到python和python3

\# ln -s /usr/local/bin/python3.6 /usr/bin/python
\# ln -s /usr/local/bin/python3.6 /usr/bin/python3

参考的博文到这里就结束了，实际测试后还需要软连接`pip3`，不然还是装不上依赖包：
\# ln -s /usr/local/bin/pip3.6 /usr/bin/pip3
\# ln -s /usr/local/bin/pyenv-3.6 /usr/bin/pyenv

