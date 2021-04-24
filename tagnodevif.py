import requests
import json
import urllib3
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

example_info = """Example:

    python3 tagnodevif.py -u admin -p VMware1\!VMware1\! -n 192.168.31.245 -s K8SC3_Transmit -k k8s-03-cluster
"""

parser = argparse.ArgumentParser(epilog=example_info, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-n", "--nsxip", help="NSX Manager IP")
parser.add_argument("-s", "--seg", help="Node VIF Segment Name")
parser.add_argument("-u", "--nsxuser", help="NSX Manager Username")
parser.add_argument("-p", "--passwd", help="NSX Manager Password")
parser.add_argument("-k", "--kubecluster", help="Kubernetes Cluster Name")
args = parser.parse_args()


# 公共变量
nsxmanger_ip = args.nsxip
transmit_seg = args.seg
nsxmanager_user = args.nsxuser
nsxmanager_passwd = args.passwd
k8s_cluster_name = args.kubecluster
headers = {
    'Content-type': 'application/json'
    }

def get_portid():
    payload = {}
    url = "https://" + nsxmanger_ip + "/policy/api/v1/infra/segments/" + transmit_seg + "/ports/"
    session = requests.session()
    session.verify = False
    session = session.get(url, headers=headers, data=json.dumps(payload), auth=(nsxmanager_user,nsxmanager_passwd), verify = False)
    session = json.loads(session.text)
    return session

def get_vif():
    url = "https://" + nsxmanger_ip + "/api/v1/fabric/vifs"
    payload = {}
    session = requests.session()
    session.verify = False
    session = session.get(url, headers=headers, data=json.dumps(payload), auth=(nsxmanager_user,nsxmanager_passwd), verify = False)
    session = json.loads(session.text)
    return session

def get_vms():
    url = "https://" + nsxmanger_ip + "/api/v1/fabric/virtual-machines"
    payload = {}
    session = requests.session()
    session.verify = False
    session = session.get(url, headers=headers, data=json.dumps(payload), auth=(nsxmanager_user,nsxmanager_passwd), verify = False)
    session = json.loads(session.text)
    return session

def tag_vif():
    url = "https://" + nsxmanger_ip + "/policy/api/v1/infra/segments/" + transmit_seg + "/ports/" + vif_id
    payload = {
              "tags": [
                {
                  "scope": "ncp/cluster",
                  "tag": k8s_cluster_name
                },
                {
                  "scope": "ncp/node_name",
                  "tag": computer_name
                }
              ]
    }
    session = requests.session()
    session.verify = False
    session = session.patch(url, headers=headers, data=json.dumps(payload), auth=(nsxmanager_user,nsxmanager_passwd), verify = False)
    return session
    

# 获取该Seg下的端口信息
ports_info = get_portid()
ports_info_list = ports_info["results"]

# 获取所有接口信息详细描述
vif_info = get_vif()
vif_info_list = vif_info["results"]
#print(vif_info_list)

# 获取所有虚拟机信息
vms_info = get_vms()
vms_info_list = vms_info["results"]
#print(vms_info_list)

# 主程序, 为VM Node VIF打上NCP所需的标签
for port in ports_info_list:
    #print(port["attachment"]["id"])
    #print(port["id"])
    for vif in vif_info_list:
        for k, v in vif.items():
            if port["attachment"]["id"] == v:
                #print(port["id"])
                #print(vif["owner_vm_id"])
                for vm in vms_info_list:
                    for k1, v1 in vm.items():
                        if vif["owner_vm_id"] == v1:
                            #print(vm["guest_info"]["computer_name"])
                            computer_name = vm["guest_info"]["computer_name"]
                            vif_id = port["id"]
                            tag_result = tag_vif()
                            if str(tag_result) == "<Response [200]>":
                                print(computer_name + "'s VIF has been successfully tagged.")
