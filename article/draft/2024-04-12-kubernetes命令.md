


## 动态伸缩实例

- kubectl scale --replicas=2 deployment/xxxdeployment -n default


## kubesphere更新证书
	1，查看证书到期时间
	./kk certs check-expiration -f sample.yaml

	2，更新证书
	./kk certs renew -f sample.yaml #指定sample.yaml的目的主要是kk通过ssh到配置文件中的主机上执行更新操作
	 
