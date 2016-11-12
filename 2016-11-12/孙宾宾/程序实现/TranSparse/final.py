#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict
import datetime
import matplotlib.pyplot as plt
import numpy as np

infile = open("train.txt", "r")
entity2id = open("entity2id.txt", "w")
relation2id = open("relation2id.txt", "w")
entity_head_file = open("entity_head_file.txt", "w")
relation_file = open("relation_file.txt", "w")

# 建立两个顺序化字典：实体字典entity_dic，关系字典relation_dic
entity_dic = OrderedDict()
relation_dic = OrderedDict()
entity_head_dic = OrderedDict()
li = []


def text_statistics(file):
	entity_id = 0
	relation_id = 0
	for line in file.readlines():
		arr = line.strip().split("\t")
		if arr[0] not in entity_dic.keys():
			entity_id += 1
			entity_dic[arr[0]] = "%05d" % entity_id
		if arr[0] not in entity_head_dic.keys():
			entity_head_dic.setdefault(arr[0], []).append([arr[2]])
		elif arr[2] not in entity_head_dic[arr[0]][0]:
			entity_head_dic[arr[0]][0].append(arr[2])
		if arr[1] not in relation_dic.keys():
			relation_id += 1
			relation_dic[arr[1]] = ["%05d" % relation_id]
			relation_dic.setdefault(arr[1], []).append(1)
			relation_dic.setdefault(arr[1], []).append([arr[0]])
			relation_dic.setdefault(arr[1], []).append([arr[2]])
		else:
			relation_dic[arr[1]][1] += 1
			if arr[0] not in relation_dic[arr[1]][2]:
				relation_dic[arr[1]][2].append(arr[0])
			if arr[2] not in relation_dic[arr[1]][3]:
				relation_dic[arr[1]][3].append(arr[2])
		if arr[2] not in entity_dic.keys():
			entity_id += 1
			entity_dic[arr[2]] = "%05d" % entity_id
	# 输出到文件
	for k in entity_dic:
		entity2id.write(k + "\t" + str(entity_dic[k]) + "\n")
	for k in entity_head_dic:
		entity_head_file.write(k + "\t对应尾实体数：" + str(len(entity_head_dic[k][0]))+ "\n")
	for k in relation_dic:
		relation2id.write(k + "\t" + str(relation_dic[k][0]) + "\n")
		relation_file.write(k + "\t连接三元组数：" + str(relation_dic[k][1])
		                 + "\t头实体数：" + str(len(relation_dic[k][2]))
		                 + "\t尾实体数：" + str(len(relation_dic[k][3]))
		                 + "\n" )
		li.append(relation_dic[k][1])
	return entity_dic, relation_dic, entity_head_dic


def draw_mapping():
	# 作图
	plt.figure(figsize=(25, 6))
	x = np.arange(len(relation_dic.keys()))
	plt.barh(x, li, color='#99CC01', yerr=0.000001)
	ax = plt.gca()
	ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
	ax.yaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
	plt.yticks(np.arange(len(relation_dic.keys())) + 0.4, relation_dic.keys(), size=10)
	# plt.xticks(rotation=-60)
	plt.title('Heterogeneity in train.txt')
	plt.ylabel('relation name')
	plt.xlabel('number of entity pairs')
	plt.savefig('Heterogeneity.png')
	return


starttime = datetime.datetime.now()

# 生成相关文本
text_statistics(infile)
# 作图
draw_mapping()

endtime = datetime.datetime.now()
print (endtime - starttime).seconds

infile.close()
entity2id.close()
relation2id.close()
relation_file.close()
entity_head_file.close()
