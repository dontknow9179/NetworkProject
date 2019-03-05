# 计算机网络PJ设计文档 
+ 概述 

  本次project实现了基于SocketAPI的聊天室应用，提交文件夹目录下各文件分别为：
  /.idea pycharm相关 
  NetworkPJ/ChatClient.py 客户端程序 
  NetworkPJ/ChatServer.py 服务端程序 
  NetworkPJ/dollars2.gif 登录界面图标

+ 登录

  用户发送数据：0 + 用户名
  服务端接收数据，检查聊天室是否满员，用户名是否存在：
  1. 若聊天室满员：返回 ‘8’ -> 用户收到聊天室满员提示 
  2. 若用户名存在：返回 ‘7’ -> 用户收到重复命名提示 
  3. 若成功登录，服务端发送给全体：0 + 登录用户名，所有登录用户会收到该用户的登陆提示。使用了一个键为用户名，值为连接的字典来存放登录的用户信息。

+ 登出

  当用户退出时，服务器先从字典中将对应项删除，之后关闭连接，向剩余的所有连接发送该用户登出消息。
  
  数据格式为： 1 + 登出用户名。接收用户进行输出与用户窗体更新。

+ 群聊（窗口标题内含有用户名）

  用户发送数据：2 + 用户名 + 聊天信息
  
  服务端接收数据，将该数据发送给所有不是发送方的用户
  
  其他用户接收到数据：2 + 用户名 + 聊天信息， 更新对话窗口
  
  发送方不需要收到数据直接在本地更新

+ 私聊

  用户发送私聊：3 + @接收者 + 聊天信息
  
  服务端接收数据，检查接收者是否存在
  1. 若接收者存在，服务端将信息只转发给该用户，形式：3 + 发送者 + @接收者 + 聊天信息 
  2. 若不存在，服务端发送错误信息给发起私聊用户， 形式：6 + 错误信息
  发送方不需要收到数据直接在本地更新

+ 消息的数据格式

  操作码 内容（不定长）
  
  0（登录） 用户名
  
  1（登出） 用户名
  
  2（群聊） 发送方+发送的消息内容
  
  3（私聊） 发送方+接收方+消息内容
  
  6（发送失败） 失败原因
  
  7（用户名重复） 无
  
  8（聊天室已满） 无
  
  9（连接出错） 无
