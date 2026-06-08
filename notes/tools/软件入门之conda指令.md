# 软件入门之conda指令

此文档感谢实验室2022级本科生曹钧扬整理与分享



创建新环境并安装所需要的包：\>\>conda create \-n ENVNAME python=3\.x pkg1 pkg2=version\)

显示已创建环境：\>\>conda env list

复制环境：\>\>conda create \-\-name \<new\_env\_name\> \-\-clone \<copied\_env\_name\>

删除环境：\>\>conda remove \-\-name \<env\_name\> \-\-all

查找包：\>\>精确查找: conda search \-\-full\-name \<package\_full\_name\>

模糊查找：\>\>conda search

pip查找：\>\>pip search

查看包信息：\>\>ananconda show \<package\_name\>

在当前环境安装需要的包：\>\>conda install pkg\_name或者\>\>pip install pkg\_name；

指定版本安装：\>\>conda install pkg\_name== version或者pip install pkg\_name==version

删除指定包：\>\>conda remove pkg\_name或者pip uninstall pkg\_name

更新所有可升级的 packages：\>\>conda update \-\-all

更改版本时，先卸载再安装：\>\>conda uinstall python再重新安装指定版本

按照requirements安装包：\>\>pip install \-r requirements\.txt

本地文件安装，可以下载安装包的exe文件或者whl文件。exe文件直接双击打开，whl文件在该文件的目录下使用如下命令：\>\>pip install 目录/文件名\(\.\.\.\.\.\.whl\)

查看conda版本：\>\>conda \-\-version或者conda \-V

更新conda至最新版本：\>\>

conda update conda

conda update anaconda

更新包

更新所有包：\>\>

conda upgrade \-\-all

conda update \-\-all

更新指定包: \>\>

conda upgrade \<package\_neme\>

conda update \<package\_neme\> pip

更新包 pip install \-U \<package\_neme\>

pip更新自己 pip install \-U pip

conda导入导出包：\>\>

导出：\>\>conda env export \> environment\.yaml

conda list \-e \> requirements\.txt

导入：\>\>conda env create \-f environment\.yaml

conda install \-\-yes \-\-file requirements\.txt

pip导入导出包：\>\>

导出：\>\>pip freeze \> requirements\.txt

导入：\>\>pip install \-r requirements\.txt

conda换源：\>\>

查看channels：\>\>conda config \-\-show channels

添加国内镜像源：\>\>conda config \-\-add channels \<镜像源地址\>

conda config \-\-set show\_channel\_urls yes

移除国内镜像源：\>\>conda config \-\-remove channels \<镜像源地址\>

conda自动开启/关闭激活base环境：\>\>conda config \-\-set auto\_activate\_base false

conda config \-\-set auto\_activate\_base true

可用的国内源：\>\>

更换清华源：\>\>

conda config \-\-add channels [https://mirrors\.bfsu\.edu\.cn/anaconda/cloud/Paddle/](https://mirrors.bfsu.edu.cn/anaconda/cloud/Paddle/)

conda config \-\-add channels [https://mirrors\.bfsu\.edu\.cn/anaconda/cloud/msys2/](https://mirrors.bfsu.edu.cn/anaconda/cloud/msys2/)

conda config \-\-add channels [https://mirrors\.tuna\.tsinghua\.edu\.cn/anaconda/cloud/conda\-forge/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/)

conda config \-\-add channels [https://mirrors\.bfsu\.edu\.cn/anaconda/pkgs/free/](https://mirrors.bfsu.edu.cn/anaconda/pkgs/free/)

conda config \-\-add channels [https://mirrors\.bfsu\.edu\.cn/anaconda/pkgs/main/](https://mirrors.bfsu.edu.cn/anaconda/pkgs/main/)

conda config \-\-add channels [https://mirrors\.bfsu\.edu\.cn/anaconda/cloud/pytorch/](https://mirrors.bfsu.edu.cn/anaconda/cloud/pytorch/)

conda config \-\-add channels [https://mirrors\.bfsu\.edu\.cn/anaconda/cloud/menpo/](https://mirrors.bfsu.edu.cn/anaconda/cloud/menpo/)

conda config \-\-set show\_channel\_urls yes

pip换源：\>\>

阿里云 [http://mirrors\.aliyun\.com/pypi/simple/](http://mirrors.aliyun.com/pypi/simple/) \-\-trusted\-host [mirrors\.aliyun\.com](http://mirrors.aliyun.com)

中国科技大学 [https://pypi\.mirrors\.ustc\.edu\.cn/simple/](https://pypi.mirrors.ustc.edu.cn/simple/) \-\-trusted\-host [pypi\.mirrors\.ustc\.edu\.cn](http://pypi.mirrors.ustc.edu.cn)

豆瓣 [http://pypi\.douban\.com/simple/](http://pypi.douban.com/simple/) \-\-trusted\-host [pypi\.douban\.com](http://pypi.douban.com)

清华大学 [https://pypi\.tuna\.tsinghua\.edu\.cn/simple/](https://pypi.tuna.tsinghua.edu.cn/simple/) \-\-trusted\-host [pypi\.tuna\.tsinghua\.edu\.cn](http://pypi.tuna.tsinghua.edu.cn)

pip临时使用：\>\>pip install pythonModuleName \-i \<换源地址\>

使用pqi永久换源：\>\>

安装pqi：\>\>pip install pqi

查看pqi帮助信息：\>\>pqi

列举所有支持的pip源：\>\>pqi ls

改变pip源\(阿里云\) ：\>\>pqi use aliyun

显示当前pip源：\>\>pqi show

添加新的pip源\(如添加ustc源\) ：\>\>pqi add ustc [https://mirrors\.ustc\.edu\.cn/pypi/web/simple](https://mirrors.ustc.edu.cn/pypi/web/simple)

移除pip源\(如官方PyPi源\)：\>\>pqi remove pypi

pip添加代理：pip install package\_name \-\-proxy=http://your\_proxy\_server:port

