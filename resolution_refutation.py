import numpy as np

class New_Knowledge:
    def __init__(self):
        self.number_of_literals = 100 
        self.percent_match = 100
        self.well_formed_formula = None 
        self.keys = None
        self.index_i = None
        self.index_j = None
        self.completed = False

class resolution_refutation:
    def __init__(self, fileName):
        self.fileName = fileName
        self.KNOWLEDGE_BASE = {}
        self.N = 0
        self.total_knowledge = 0

    def create_knowledge(self):
        file = open(self.fileName, "r")
        self.N = int(file.readline())
        for n in range(self.N):
            self.append_knowledge(file.readline().strip())

        self.append_knowledge('!'+file.readline().strip())
        file.close()
        
    def test_knowledge(self): 
        for K in self.KNOWLEDGE_BASE:
            print(self.KNOWLEDGE_BASE[K]['STEP_COUNT'], self.usefull_knowledge(self.KNOWLEDGE_BASE[K]))
        print('--------')
        output, result = self.comput_knowledge()
        output = np.array(output)
        
        for line in output:
            print(*line)
        
        print(result)

    def literals_checking(self, literals):
        l_leng = len(literals)
        return literals[l_leng - 1], literals.find('!') != -1
        
    def literals_counts(self, s):
        count = 0
        for i in range(len(s)):
            if not (s[i] == '|' or s[i] == '!'):
                count +=1
        return count

    def append_knowledge(self, knowledge):
        knowledgeData = knowledge.split('|')
        tmp_knowledge = {}
        extra_knowledge = []
        for data in knowledgeData:
            data, status = self.literals_checking(data.strip())
            if data in tmp_knowledge and status != tmp_knowledge[data] and not data in extra_knowledge:
                extra_knowledge.append(data)
            tmp_knowledge[data] = status

        for remove in extra_knowledge:
            knowledge.pop(remove)

        if tmp_knowledge:
            self.total_knowledge += 1
            tmp_knowledge['STEP_COUNT'] = self.total_knowledge
            self.KNOWLEDGE_BASE[self.usefull_knowledge(tmp_knowledge)] = tmp_knowledge

    def usefull_knowledge(self, Knowledge):
        keys = sorted(Knowledge.keys())
        or_symbol = False
        ret_val = ''
        for k in keys:
            if k != 'STEP_COUNT':
                if or_symbol: 
                    ret_val += '|'
                else: 
                    or_symbol = True
                if Knowledge[k]:
                    ret_val += k
                else:
                    ret_val += '!'+k
        
        return ret_val

    def knowledge_capture(self, knowledge_1, knowledge_2):
        for k in knowledge_2:
            if k in knowledge_1:
                if knowledge_1[k] != knowledge_2[k]:
                    knowledge_1.pop(k)
            else:
                knowledge_1[k] = knowledge_2[k]
        
        if 'STEP_COUNT' in knowledge_1:
            knowledge_1.pop('STEP_COUNT')
        return knowledge_1

    def comput_knowledge(self):
        output = []
        result = 0
        isUpdated = True
        while isUpdated:
            isUpdated = False
            l = len(self.KNOWLEDGE_BASE)
            if l == 0:
                result = 1
                break
            if l == 1:
                break
            
            tmp = New_Knowledge()
            isBreak = False
            keys = list(self.KNOWLEDGE_BASE.keys())
            for i in range(l):
                K1 = self.KNOWLEDGE_BASE[keys[i]]
                c1 = self.literals_counts(keys[i])
                for j in range(i+1, l):
                    K2 = self.KNOWLEDGE_BASE[keys[j]]
                    K = self.knowledge_capture(K1.copy(), K2)
                    if K:
                        t = self.usefull_knowledge(K)
                        if t not in self.KNOWLEDGE_BASE:
                            c2 = self.literals_counts(keys[j])
                            highCount = c1
                            if c1 < c2:
                                highCount = c2
                            count = self.literals_counts(t)
                            percent = 100 * count / (c1 + c2)

                            if highCount >= count and tmp.number_of_literals >= count and tmp.percent_match > percent:
                                isUpdated = True
                                tmp.number_of_literals = count
                                tmp.percent_match = percent
                                tmp.well_formed_formula = K 
                                tmp.keys = t
                                tmp.index_i = i
                                tmp.index_j = j
                                
                    else :
                        tmp.keys = '{ }'
                        tmp.index_i = i
                        tmp.index_j = j
                        tmp.completed = True
                        result = 1
                        isBreak = True
                        break
                if isBreak:
                    break
            if tmp.index_i != None:
                lst = []
                self.total_knowledge += 1
                lst.append(self.total_knowledge)
                lst.append(tmp.keys)
                from1 = self.KNOWLEDGE_BASE[keys[tmp.index_i]]['STEP_COUNT']
                from2 = self.KNOWLEDGE_BASE[keys[tmp.index_j]]['STEP_COUNT']
                if from1 > from2:
                    tmpFrom = from1
                    from1 = from2
                    from2 = tmpFrom
                lst.append(' ({0}, {1})'.format(from1, from2))
                output.append(lst)
                if not tmp.completed:
                    tmp.well_formed_formula['STEP_COUNT'] = self.total_knowledge
                    self.KNOWLEDGE_BASE[tmp.keys] = tmp.well_formed_formula
                
            if isBreak:
                break
            
        return output, result

print("Input file path:")
filePath = input()
res_refu = resolution_refutation(filePath)
res_refu.create_knowledge()
res_refu.test_knowledge()
