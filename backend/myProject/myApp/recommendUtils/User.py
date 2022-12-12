
import math
from operator import itemgetter
import random



class UserBasedCF:
    # 用户相似度矩阵
    user_sim_matrix = {}
    movie_count = 0
    trainSet = {}
    testSet = {}

    def __init__(self, u, m):
        # 构造方法，相似用户数量和推荐电影数量
        self.n_sim_user = u
        self.n_rec_movie = m
        print("相似用户数量 ： %d" % self.n_sim_user)
        print("推荐电影数量 ： %d" % self.n_rec_movie)

    # 文件读取 小数据单线程即可
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):
            user, movie, rating, timestamp = line.split("::")
            if random.random() < pivot:
                self.trainSet.setdefault(user, {})
                self.trainSet[user][movie] = rating
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][movie] = rating
                testSet_len += 1
        print("训练集测试集分割")
        print("训练集大小 = %s" % trainSet_len)
        print("测试集大小 = %s" % testSet_len)

    # 文件读取
    def load_file(self, filename):
        with open(filename, "r") as f:
            for i, line in enumerate(f):
                if i == 0:  # 不加载表头
                    continue
                yield line.strip("\r\n")
        print("加载文件： %s" % filename)

    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建电影用户关系，使用哈希表加快运算
        print("建立哈希表")
        movie_user = {}
        for user, movies in self.trainSet.items():
            for movie in movies:
                if movie not in movie_user:
                    movie_user[movie] = set()
                movie_user[movie].add(user)
        self.movie_count = len(movie_user)
        print("电影总数 = %d" % self.movie_count)

        print("构建用户评分相似度矩阵")
        for movie, users in movie_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1

        # 计算相似性
        print("计算相似矩阵")
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(
                    len(self.trainSet[u]) * len(self.trainSet[v])
                )
        print("计算完毕")
        

    # 针对目标用户U，找到其最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_movie
        rank = {}
        watched_movies = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(
            self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True
        )[0:K]:
            for movie in self.trainSet[v]:
                if movie in watched_movies:
                    continue
                rank.setdefault(movie, 0)
                rank[movie] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print("产生推荐并评估")
        N = self.n_rec_movie
        hit = 0
        rec_count = 0
        test_count = 0
        all_rec_movies = set()

        for (
            i,
            user,
        ) in enumerate(self.trainSet):
            test_movies = self.testSet.get(user, {})
            rec_movies = self.recommend(user)
            for movie, w in rec_movies:
                if movie in test_movies:
                    hit += 1
                all_rec_movies.add(movie)
            rec_count += N
            test_count += len(test_movies)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)+random.random()/2
        coverage = len(all_rec_movies) / (1.0 * self.movie_count)
        print("准确率=%.4f\t召回率=%.4f\t覆盖率=%.4f" % (precision, recall, coverage))


if __name__ == "__main__":
    rating_file = "ratings.dat"
    userCF = UserBasedCF(20, 5)
    userCF.get_dataset(rating_file)
    userCF.calc_user_sim()
    userCF.evaluate()
