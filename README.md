# Alfred-SAP-Quick-Login
SAP快捷登录Alfred捷径

## 必须条件
- [X] 安装Alfred
- [X] 安装Python2.7
- [X] 安装Parallels Desktop
- [X] Parallels Desktop已安装Windows虚拟机
- [X] Windows虚拟机已安装SAP GUI for Windows

## 安装
1.下载Releases

2.导入Alfred

3.填写环境变量shortcut_dir:SAP的快捷方式文件shortcut.ini的绝对路径

4.填写环境变量VM_UUID:安装了SAP GUI for Windows的虚拟机的UUID

可在macOS中运行下列命令查询:
```
prlctl list
```

## 使用
1.Windows虚拟机保持运行

2.Alfred指令:
```
sap <关键字>(自动搜索shortcut.ini中的条目)
```
