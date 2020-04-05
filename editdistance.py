import time,json

# 抽奖问答库
class LotteryQuizLibrary(object):
    def __init__(self):
        # 抽奖活动开始之前时间区间
        self.luckydraw_before_start = '2019-06-19 15:00:00'
        self.luckydraw_before_end = '2019-06-19 15:30:00'
        # 抽奖活动中时间区间
        self.luckydraw_going_start = '2019-06-20 05:00:00'
        self.luckydraw_going_end = '2019-06-20 05:30:00'
        # 抽奖活动结束时间区间
        self.luckydraw_end_start = '2019-06-20 5:00:00'
        self.luckydraw_end_end = '2019-06-20 5:30:00'


    def answerForQuestion(self,question,atCount = 0):
        # 判断@次数
        if atCount > 2:
            timeStype = self.time_interval()

            # 判断时间范围
            timeType = self.time_interval()

            if timeType != 'none':
                question_list = self.selectLuckyDB(timeType)
                index = self.questions(question_list, question)
                return question_list[index]['answer']
            else:
                return '时间不在范围内';

        else:
            return '再来一次，@我';

    # 匹配到最相似的问题
    def questions(self, list, questionstring):
        a = []
        get_max = 0.0
        max_index = 0
        for index in range(len(list)):
            e = self.minEditDist(list[index], questionstring)
            if e > get_max:
                max_index = index
                get_max = e
            a.append(e)
        print('\n')
        print(a)
        print('最大值是：')
        print(get_max)
        print('最大值数组下标:')
        print(max_index)
        return max_index


    # 查询当前时间是在抽奖活动之前还是抽奖活动之后还是抽奖进行中
    def time_interval(self):
        if (self.date_time_scope(self.luckydraw_before_start, self.luckydraw_before_end)):
            return 'before'
        elif (self.date_time_scope(self.luckydraw_going_start, self.luckydraw_going_end)):
            return 'going'
        elif (self.date_time_scope(self.luckydraw_end_start, self.luckydraw_end_end)):
            return 'end'
        else:
            return 'none'



    #基础公共方法（外部不需要调用）
    def minEditDist(self, sm, sn):
        m, n = len(sm) + 1, len(sn) + 1
        # create a matrix (m*n)
        matrix = [[0] * n for i in range(m)]
        matrix[0][0] = 0
        for i in range(1, m):
            matrix[i][0] = matrix[i - 1][0] + 1

        for j in range(1, n):
            matrix[0][j] = matrix[0][j - 1] + 1

        '''
        for i in range(m):
            print(matrix[i])

        print("********************")
        '''
        cost = 0
        for i in range(1, m):
            for j in range(1, n):
                if sm[i - 1] == sn[j - 1]:
                    cost = 0
                else:
                    cost = 1

                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)

        '''
        for i in range(m):
            print(matrix[i])
        '''
        e = matrix[m - 1][n - 1]

        l1 = len(sm)
        l2 = len(sn)
        n = l1 if l1 > l2 else l2
        # 相似度  1- （边界距离/最大字符串长度）
        return (1 - (e / n))


    # 判断当前时间是否在一个时间范围内
    def date_time_scope(self, startTime, endTime, currentTime=0):
        start = int(time.mktime(time.strptime(startTime, '%Y-%m-%d %H:%M:%S')) * 1000)
        end = int(time.mktime(time.strptime(endTime, '%Y-%m-%d %H:%M:%S')) * 1000)
        if currentTime == 0:
            currentTime = int(time.time()) * 1000

        if currentTime > start and currentTime < end:
            return True
        else:
            return False

    def selectLuckyDB(self,timeType):
        from TmallAdmin_Data import models
        # question_list = models.luckyanswers.objects.all().values()
        question_list = models.luckyanswers.objects.filter(type=timeType).values()
        list1 = []
        for question in list(question_list):
            # print(question)
            list1.append(question)
            # print(user_1.name,user_1.phone)
            # print(user_1.name,user_1.phone)
            # print(user_1.name,user_1.phone)
        # print(user_list[0]['name'])
        d = {}
        d["list"] = list1
        print(json.dumps(d))
        print(222)
        print(list1[0]['question'])
        return question_list






if __name__ == "__main__":
    # str1 = '活动几点结束'
    # str2 = '这次抽奖活动什么时候结束'
    # e = minEditDist(str1,str2)
    # print(e)
    '''
    a = [
        "你吃放了吗",
        '吃了？',
        '你有没有吃饭',
        '吃了吗！！！'
    ]
    index = questions(a,"吃了吗")
    print('匹配到相似度最高的是：')
    print(a[index])
    '''
    # a = date_time_scope("2019-06-12 12:00:00",'2019-06-19 20:00:00')
    # print(a)

    # c = time_interval()
    # print(c)
    c = LotteryQuizLibrary()
    b = c.selectLuckyDB()
    print(1)
    print(b[0]['question'])

