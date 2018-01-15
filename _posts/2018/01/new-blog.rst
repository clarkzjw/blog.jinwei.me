:orphan:

.. _2018newblog:

又一个新的博客
==============

:Publish Date: 2018-01-15

前段时间有朋友和我抱怨博客加载速度太慢了（。之前的博客架在Blogger上，为了让排版稍微美观一些，找了一个第三方的主题，加载了许多外部的
资源，导致网页载入速度非常慢。虽然我自己对于网站在国内的加载速度毫不在意，但是既然还有读者（少的可怜）在看，以及在这极少的读者中有用
户提出了这个问题，那就得解决。前段时间无意中看到一个博客（ `git-pull`_ ），觉得主题简洁而又美观，于是开始
着手改造自己的博客。

.. _git-pull: https://www.git-pull.com/index.html

这次用了「大名鼎鼎」的 `Sphinx`_ ，一个软件开发过程中的文档生成工具来作为博客的静态网页生成引擎。
上手Sphinx非常简单，sphinx-quickstart这个工具和一般的博客生成器一样，集成了很多功能，把Makefile都写好了，可以说是完全开箱即用了。
Sphinx的默认主题是 `Alabaster`_ ，现在你看到的这个主题就是在Alabaster上修改而来的。

Sphinx的文档书写采用的是*.rst格式的文本，即 `reStructuredText`_ ，而不是Markdown。相比
之前，rst比Markdown的语法更加丰富/复杂，同时也提供了更加丰富的功能和可扩展性（虽然我估计我只能用到其中的20%甚至更少啦）。不清楚rst和
Emacs社区的 `Org Mode`_ 相比哪一个的语法更加复杂呢。（

建设博客离不开几件事情。首先当然就是部署运维啦。Sphinx通过Makefile可以生成静态html网页，托管静态html最方便的地方当然是GitHub Pages啦。
最简单粗暴的方法是在本地的环境中写完rst文本，然后本地 make html 通过之后，将html推送到GitHub Pages中。但是这种方式的移植性不高，想写
博客的话必须坐在自己的电脑前，同时依然存在一些手动的工作。所以当然选择Docker啦。但是这次用Docker的姿势和以往不同。平时我们用Docker的时候
最终都是想要得到docker build的产物docker image，然后由image来进行部署。但是我们这次的目标是GitHub Pages，没法部署容器。所以我在
Dockerfile中生成静态html网页，然后在构建的过程中将静态网页push到repo的gh-pages分支中。当然其实不用Docker也能做到这一点。写一个脚本，
然后在CI平台上执行脚本也行，就不做优劣对比了。

值得一提的是，Docker在17.05-ce版本之后引入了multi stage build的功能，可以在Dockerfile中FROM多个基础镜像，在下一个stage可以直接使用
之前stage构建出的产物。以我的博客这个项目为例。假如我是想通过image来部署，那么我最终的产物是静态html文件，那么我可能需要一个nginx的基础
镜像。nginx:alpine 这个基础镜像很小，不到10MB，在Dockerfile里面将html文件COPY进去之后，最终得到的image也只有10MB左右的大小。但是
之前我们为了得到静态html文件，可能得选用一个python的基础镜像，然后再apt/apk安装一些必要的编译工具，最终只是为了几百kb的html文件，但是
构建的镜像已经上百MB了。有了multi stage build之后，这个问题便非常好地被解决了。看了下面的Dockerfile之后，整体思路就非常清晰了。目前我
在本地写完rst文本，然后git push之后，CircleCI会自动进行Dockerfile的构建，然后将编译生成的静态html推送到gh-pages分支。

.. code-block:: bash

    FROM python:3.6.0 as builder
    LABEL maintainer=clarkzjw<hello@jinwei.me>
    RUN pip install virtualenv
    COPY requirements.txt /app/requirements.txt
    COPY bootstrap.py /app/bootstrap.py
    RUN /app/bootstrap.py
    ADD . /app
    WORKDIR /app
    RUN /bin/bash -c "source /app/.venv/bin/activate && make html && make rss && cp rss.xml _build/html"


    FROM alpine:latest
    RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
    RUN apk add --update git openssh-client && rm -rf /var/cache/apk/*
    WORKDIR /html
    ENV COMMIT_USER="clarkzjw"
    ENV COMMIT_EMAIL="hello@jinwei.me"
    ARG GIT_TOKEN=""
    RUN git config --global user.email $COMMIT_EMAIL && git config --global user.name $COMMIT_USER
    RUN git clone https://clarkzjw:$GIT_TOKEN@github.com/clarkzjw/blog.jinwei.me.git /html && git checkout gh-pages
    COPY --from=builder /app/_build/html /html
    RUN echo "`date`" > /html/.lastmodify && git add -A && git commit -m "`date`" && git push origin gh-pages


    FROM nginx:alpine
    COPY --from=builder /app/_build/html /usr/share/nginx/html


另外一个问题是博客的RSS。由于Sphinx最初的设计是作为一个文档生成工具，目前市面上有的和Sphinx结合的RSS生成工具大致有：

- Sphinx-contrib模块中的 `feed <https://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/feed/>`__

- 在sphinxcontrib.feed基础上开发的 `sphinxfeed <https://github.com/junkafarian/sphinxfeed>`__

- 以及更新一点的 `sphinxcontrib-newsfeed <https://pypi.python.org/pypi/sphinxcontrib-newsfeed>`__

其中sphinxcontrib.feed和sphinxfeed的功能性更新都停止在2011年，不兼容Python 3，GitHub上有几个fork，但是也基本没有太多的改进。至于
sphinxcontrib-newsfeed，并不能生成符合RSS规范的输出。。。所以只好自己简单粗暴造一个轮子了！（至少生成的xml能被RSS阅读器认识。。。

至于评论嘛。虽然博客流量小，2017年下来一年也没有10条评论，但是作为一个博客，这个功能还是必须得有！考察了目前市面上的评论方案，Disqus现在
差不多可以算是一家独大了。但是十分不喜欢Disqus。一个页面要加载的无关的数据太多了。然后看到了 `Isso`_ , 第一印象还不错，但是需要自己单独部
署。为了一年10条评论不到的数量级单独部署似乎成本略高。之前还见到了 `Staticman`_ , 但是这个方案和GitHub的issue绑定，一个博客实例对应
GitHub的一个repo，然后每篇文章的评论对应这个repo中的issue。但是我不太能接受，毕竟不能强制每个评论的用户都有GitHub帐号。
今天无意中看到了 `just-comments`_ , 也是一个SaaS解决方案，但是非常地极简，决定先用着试试效果。（

下一步，打算在博客中加入 `漢字標準格式 <https://css.hanzi.co/>`_ 这套排版框架。毕竟现在的页面排版看起来怪怪的，以及并不美观。（

.. _Org Mode: https://orgmode.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Alabaster: https://alabaster.readthedocs.io/en/latest/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _Isso: https://github.com/posativ/isso
.. _Staticman: https://staticman.net
.. _just-comments: https://just-comments.com/
