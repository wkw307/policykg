# coding=utf-8
import json
import time
from text_comparer.vectorizer import compare_texts

#just test
#result = compare_texts("Additional specific requirements to supplement the criteria and requirements of IEEE Std 603(TM) are specified for programmable digital devices. Within the context of this standard, the term programmable digital device is any device that relies on software instructions or programmable logic to accomplish a function. Examples include a computer, a programmable hardware device, or a device with firmware. Systems using these devices will also be referred to as digital safety systems in this standard. The criteria contained herein, in conjunction with criteria in IEEE Std 603, establish minimum functional and design requirements for programmable digital devices used as components of a safety system.".replace(',','').replace('.','').lower().replace('the','').replace('of','').replace('and',''), "Standard methods and basic techniques for high-voltage testing applicable to all types of apparatus for alternating voltages, direct voltages, lightning impulse voltages, switching impulse voltages, and impulse currents are established in this standard. Sections that deal with alternating voltage, direct voltage, and impulse testing are combined in this revision to organize the technical content for ease of use. In addition, the concept of measurement uncertainty in evaluation of high-voltage and high-current tests is introduced in this version.".replace(',','').replace('.','').lower().replace('the','').replace('of','').replace('and',''))
#print(result)
#print "Standard methods and basic techniques for high-voltage testing applicable to all types of apparatus for alternating voltages, direct voltages, lightning impulse voltages, switching impulse voltages, and impulse currents are established in this standard. Sections that deal with alternating voltage, direct voltage, and impulse testing are combined in this revision to organize the technical content for ease of use. In addition, the concept of measurement uncertainty in evaluation of high-voltage and high-current tests is introduced in this version.".replace(',','').replace('.','').lower().replace('the','').replace('of','').replace('and','')
#print "The definitions for physical quantities and units commonly used in applied science andtechnology, and for related terms that concern systems of measurement, are included in thisstandard. Particular emphasis is placed on the International System of Units (Le SystemeInternational d'Unites, SI).".replace(',','').replace('.','').lower().replace('the','').replace('of','').replace('and','')

nodes = []
links = []
policy = json.load(open("policy.json",'r'))
doc = policy['data']

startTime = time.time()

for index, document in enumerate(doc):
    paper = {}
    paper["id"] = document["id"]
    paper["datatype"] = "policy"
    paper["date_publication"] = document["date_publication"][:4]
    #status有的以\r结尾
    paper["status"] = document["status"].replace("\r","")
    nodes.append(paper)

    #计算两个节点abstract的余弦相似度
    for index1, document1 in enumerate(doc):
        #单向比较，abstract属性（字符串）不能为空
        if((index < index1) and document["abstract"].strip() and document1["abstract"].strip()):
                #对进行比较的两个abstract进行简单的预处理（去标点、统一小写、去掉几个停用词）
                #计算短文本余弦相似度：https://github.com/sergeio/text_comparer
                ct = compare_texts(document["abstract"].replace(',','').replace('.','').lower().replace('the','').replace('of','').replace('and',''),document1["abstract"].replace(',','').replace('.','').lower().replace('the','').replace('of','').replace('and',''))
                if(ct > 0.3):
                    #print ct
                    edge = {}
                    edge["source"] = document["id"]
                    edge["target"] = document1["id"]
                    edge["type"] = "relation"
                    edge["value"] = ct
                    links.append(edge)

endTime = time.time()
print endTime - startTime

#导出json文件
_json = {}
_json["nodes"] = nodes
_json["links"] = links
json.dump(_json,open("policy_kg.json","w"))




# just test
# sum = 0
# for index,document in enumerate(doc):
#     for index1,document1 in enumerate(doc):
#         if((index < index1) and document["abstract"].strip() and document1["abstract"].strip()):
#
#             ct = compare_texts(document["abstract"].replace(',','').replace('.','').lower().replace('the','').replace('of','').replace('and',''),document1["abstract"].replace(',','').replace('.','').lower().replace('the','').replace('of','').replace('and',''))
#             if(ct > 0.3):
#                 print ct
#                 sum = sum + 1
# print sum