#-*-  coding: UTF-8 -*- 
class match:
	def __init__(self,data,search_list):
		self.data = data
		self.search_list = search_list
	def similar(self):
		#data = 'The Emergence of Social and Community Intelligence'
		data_hash = []#匹配英文句子中的英文单词hash
		data_lenth = 0#data单词长度
		#计算出hash值相匹配的个数
		for x in self.data.split():
			data_lenth += 1
			data_hash.append(hash(x))
		SameWC = []#存储与目标相匹配的单词个数,[匹配单词数，位置，长度]
		for i,x in enumerate(self.search_list):
			sum = 0
			length = 0
			tem_hash = data_hash.copy()
			for y in x['title'].split():
				length += 1
				if tem_hash:
					for index in range(len(tem_hash)):
						if tem_hash[index] == hash(y):
							sum += 1
							del tem_hash[index]
							break
			if sum != 0:
				SameWC.append([sum,i,length])
		sort_max = 100
		SameWC_max = sorted(SameWC, key = lambda SameWC: SameWC[0], reverse = True)[0:sort_max]
		#print(SameWC_max)

		#计算WordSim(词性相似度)
		#公式：2*(SameWc(A,B))/(len(A)+len(B))
		WordSim = []#args[匹配单词数，位置，长度,WordSim]
		sort_max = 10
		for index in range(len(SameWC_max)):
			tem = 2*SameWC_max[index][0]/(data_lenth+SameWC_max[index][2])
			SameWC_max[index].append(tem)
			WordSim.append(SameWC_max[index])
		WordSim_max = sorted(WordSim, key = lambda WordSim: WordSim[3], reverse= True)[0:sort_max]
		#print(WordSim_max)

		#计算OrdSim(词序相似度)
		#公式:当 OnceWS(A , B) > 1,OrdSim(A,B)=1-RevOrd(A,B)/(|OnceWS(A , B)|-1)
		#     当 OnceWS(A , B) = 1,OrdSim(A,B)=1
		#     当 OnceWS(A , B) = 0,OrdSim(A,B)=0
		#Sim(A,B)=λ1·WordSim(A,B)+λ2·OrdSim(A,B),其中满足λ1+λ2=1,词形相似度起主要作用,词序相似度起次要作用 , 所以要求 λ1>>λ2
		data_OnceWS = []
		λ1 = 0.8
		λ2 = 0.2
		for index in range(data_lenth):
			data_OnceWS.append(index)
		#print(data_OnceWS)
		RevOrd = []#args[匹配单词数，位置，长度,WordSim,[RevOrd],Rev_sum,OrdSim(A,B),Sim(A,B)]
		for x in WordSim_max:
			#print(x)
			tem = []
			tem_hash = data_hash.copy()
			for y in self.search_list[x[1]]['title'].split():
				if tem_hash:
					for index in range(len(tem_hash)):
						if tem_hash[index] == hash(y):
							for i,value in enumerate(data_hash):
								if value == hash(y):
									tem.append(i)
									break
							del tem_hash[index]
							break
			x.append(tem)
			RevOrd.append(x)
		#print(RevOrd)
		for x in RevOrd:
			Rev_sum = 0
			for index in range(len(x[4])):
				if len(x[4]) == index+1:
					break
				else:
					if x[4][index]>x[4][index+1]:
						Rev_sum += 1
			x.append(Rev_sum)
			if x[0] == 1:
				OrdSim = 1
			else:
				OrdSim = 1-Rev_sum/(abs(x[0])-1)
			x.append(OrdSim)
			Sim = λ1*x[3]+λ2*x[6]
			x.append(Sim)
		#print(RevOrd)
		Sim_result = self.search_list[sorted(RevOrd, key = lambda RevOrd: RevOrd[7], reverse= True)[0][1]]
		#print(Sim_result)
		return Sim_result