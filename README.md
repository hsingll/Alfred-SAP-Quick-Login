# Alfred-SAP-Quick-Login
SAP快捷登录Alfred捷径

## 效果预览
暂未录制


## 必须条件
- [X] 安装Alfred
- [X] 安装Python3以及包fuzzywuzzy
- [X] 安装Parallels Desktop
- [X] Parallels Desktop已安装Windows虚拟机
- [X] Windows虚拟机已安装SAP GUI for Windows

## 安装
0.Windows虚拟机中添加如下环境变量到Path(重启才生效):
```
32位SAP GUI版本: C:\Program Files (x86)\SAP\FrontEnd\SAPgui
64位SAP GUI版本: C:\Program Files\SAP\FrontEnd\SAPGUI
```

1.下载Releases

2.导入Alfred

3.填写环境变量`SAPUILandscape`:

启用Landscape布局: SAP的快捷方式文件SAPUILandscape.xml的绝对路径

## 使用
0.Windows虚拟机保持运行

1.输入Alfred指令`sap`选择虚拟机，再输入关键字筛选快捷方式
