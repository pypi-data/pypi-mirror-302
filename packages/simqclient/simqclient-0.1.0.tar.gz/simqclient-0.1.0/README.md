# simqclient

SIMQ客户端。SIMQ是一款基于redis的消息队列接口服务。

## 安装

```shell
pip install simqclient
```

## 客户端实例化参数

- base_url: SIMQ服务地址。必填。
- api_key: SIMQ服务认证。与SIMQ服务器保持一致。
- worker: 客户端识别码。默认为：主机名-进程号-线程号。
- api_key_header: SIMQ服务认证请求头。与SIMQ及其代理服务设置保持一致。默认为apikey，一般不设置。
- headers: 额外的请求头，需要根据代理服务器的需求进行设置。一般不设置。

## 服务实例化参数

- execute_timeout: 结果超时时间。默认为5秒。如果是长时间任务，建议使用异步调用。

## 版本

### 0.1.0

- 版本首发。
