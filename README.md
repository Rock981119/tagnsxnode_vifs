# Tag NSX K8s VM Node Vifs
###### tags: NSX-T
*限于本人英语水平, 英文部分大多来自谷歌翻译
Limited to my English proficiency, most of the English part comes from Google Translate*

## 用途 / Purpose
当NSX-T使用NCP与K8s集成时, 需要为每个VM Node虚拟接口打标签, 以标识容器流量来自哪个节点和哪个集群. 本脚本是帮助大家批量去为VM Node VIF打标签.

When NSX-T uses NCP to integrate with K8s, you need to tag each VM Node virtual interface to identify which node and which cluster the container traffic comes from. This script is to help you tag VM Node VIFs in batches.

## 图示 / Diagram

## 限制条件 / Limitation
1. 适用于初次部署使用<br>Suitable for greenfield deployment
2. 确保Node Vif所在的Segment中没有其他无关的接口, 否则脚本未包含处理该错误的逻辑<br>Make sure that there are no other irrelevant interfaces in the segment where Node Vif is located, otherwise the script does not contain the logic to handle the error
3. 脚本仅仅为Vif打上NCP集成所必要的两个标签: ncp/cluster; ncp/node_node<br>he script only marks Vif with two labels necessary for NCP integration: ncp/cluster; ncp/node_node
4. 脚本采用Patch API Call, 如果接口上已有别的标签会被覆盖掉<br>The script uses Patch API Call, if there are other tags on the interface, it will be overwritten
5. 仅在上游K8s环境集成中测试过<br>Only tested in the upstream K8s environment integration
6. Python3 with requests Module
7. **每个VM Node必须安装VM Tools**(可以是开源版VM Tools)<br>Each VM Node must install VM Tools (it can be an open source version of VM Tools)

## 例子 / Example
```
agnsxnode_vifs [main] python3 tagnodevif.py -h
usage: tagnodevif.py [-h] [-n NSXIP] [-s SEG] [-u NSXUSER]
                     [-p PASSWD] [-k KUBECLUSTER]

optional arguments:
  -h, --help            show this help message and exit
  -n NSXIP, --nsxip NSXIP
                        NSX Manager IP
  -s SEG, --seg SEG     Node VIF Segment Name
  -u NSXUSER, --nsxuser NSXUSER
                        NSX Manager Username
  -p PASSWD, --passwd PASSWD
                        NSX Manager Password
  -k KUBECLUSTER, --kubecluster KUBECLUSTER
                        Kubernetes Cluster Name

Example:

    python3 tagnodevif.py -u admin -p VMware1\!VMware1\! -n 192.168.31.245 -s K8SC3_Transmit -k k8s-03-cluster
```
```
tagnsxnode_vifs [main] python3 tagnodevif.py -u admin -p VMware1\!VMware1\! -n 192.168.31.245 -s K8SC3_Transmit -k k8s-03-cluster
ubuk8s-c3-vm01's VIF has been successfully tagged.
ubuk8s-c3-vm02's VIF has been successfully tagged.
ubuk8s-c3-vm03's VIF has been successfully tagged.
```
效果 / Result
![](https://i.imgur.com/6kMdTlP.png)
