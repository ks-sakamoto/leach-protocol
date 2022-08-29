#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Title  ：Leach for WSN
@Author ：Kay
@Date   ：2019-09-27
=================================================='''
import numpy as np
import matplotlib.pyplot as plt

# 如遇中文显示问题可加入以下代码
# 中国語の表示に問題がある場合は、以下のコードを追加できる
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体　デフォルトのフォントを指定
# 解决保存图像是负号'-'显示为方块的问题　画像保存時にマイナス記号"-"の文字化け問題を解決
mpl.rcParams['axes.unicode_minus'] = False


class WSN(object):
    """ The network architecture with desired parameters """
    xm = 200  # Length of the yard
    ym = 200  # Width of the yard
    n = 100  # total number of nodes
    sink = None  # Sink node
    nodes = None  # All sensor nodes set
    # Energy model (all values in Joules)
    # Eelec = ETX = ERX
    # Energy for transferring of each bit:发射单位报文损耗能量:50nJ/bit
    ETX = 50 * (10 ** (-9))
    # Energy for receiving of each bit:接收单位报文损耗能量:50nJ/bit
    ERX = 50 * (10 ** (-9))
    # Transmit Amplifier types
    # Energy of free space model:自由空间传播模型:10pJ/bit/m2
    Efs = 10 * (10 ** (-12))
    # Energy of multi path model:多路径衰减空间能量模型:0.0013pJ/bit/m4
    Emp = 0.0013 * (10 ** (-12))
    EDA = 5 * (10 ** (-9))       # Data aggregation energy:聚合能量 5nJ/bit
    f_r = 0.6                    # fusion_rate:融合率 , 0代表完美融合
    # Message
    CM = 32     # 控制信息大小/bit 制御メッセージサイズ/bit
    DM = 4096   # 数据信息大小/bit データサイズ/bit
    # computation of do
    do = np.sqrt(Efs / Emp)  # 87.70580193070293

    # 恶意传感器节点
    # 悪意ある?センサーノード数
    m_n = 3  # the number of malicious sensor nodes

    # Node State in Network
    n_dead = 0  # The number of dead nodes
    flag_first_dead = 0  # Flag tells that the first node died
    flag_all_dead = 0  # Flag tells that all nodes died
    flag_net_stop = 0  # Flag tells that network stop working:90% nodes died
    round_first_dead = 0  # The round when the first node died
    round_all_dead = 0  # The round when all nodes died
    round_net_stop = 0  # The round when the network stop working

    def dist(x, y):
        """ 判断两个节点之间的一维距离 """
        """ 2つのノード間の1次元距離を決定する """
        distance = np.sqrt(np.power((x.xm - y.xm), 2) +
                           np.power((x.ym - y.ym), 2))
        return distance

    def trans_energy(data, dis):
        if dis > WSN.do:
            energy = WSN.ETX * data + WSN.Emp * data * (dis ** 4)
        else:  # min_dis <= do
            energy = WSN.ETX * data + WSN.Efs * data * (dis ** 2)
        return energy

    def node_state(r):
        nodes = WSN.nodes
        n_dead = 0
        for node in nodes:
            if node.energy <= Node.energy_threshold:
                n_dead += 1
                if WSN.flag_first_dead == 0 and n_dead == 1:
                    WSN.flag_first_dead = 1
                    WSN.round_first_dead = r - Leach.r_empty
        if WSN.flag_net_stop == 0 and n_dead >= (WSN.n * 0.9):
            WSN.flag_net_stop = 1
            WSN.round_net_stop = r - Leach.r_empty
        if n_dead == WSN.n - 1:
            WSN.flag_all_dead = 1
            WSN.round_all_dead = r - Leach.r_empty
        WSN.n_dead = n_dead


class Node(object):
    """ Sensor Node """
    energy_init = 0.5  # initial energy of a node
    # After the energy dissipated in a given node reached a set threshold,
    # that node was considered dead for the remainder of the simulation.
    energy_threshold = 0.001

    def __init__(self):
        """ Create the node with default attributes """
        self.id = None  # 节点编号
        self.xm = np.random.random() * WSN.xm
        self.ym = np.random.random() * WSN.ym
        self.energy = Node.energy_init
        self.type = "N"  # "N" = Node (Non-CH):点类型为普通节点
        # G is the set of nodes that have not been cluster-heads in the last 1/p rounds.
        self.G = 0  # the flag determines whether it's a CH or not:每一周期此标志为0表示未被选为簇头，1代表被选为簇头 フラグが0の場合は非CH, 1の場合はCHとして選択されている
        # The id of its CH：隶属的簇, None代表没有加入任何簇 所属するクラスタ, Noneはクラスタに属していないことを意味する
        self.head_id = None

    def init_nodes():
        """ Initialize attributes of every node in order """
        nodes = []
        # Initial common node
        for i in range(WSN.n):
            node = Node()
            node.id = i
            nodes.append(node)
        # Initial sink node
        sink = Node()
        sink.id = -1
        sink.xm = 0.5 * WSN.xm  # x coordination of base station
        sink.ym = 50 + WSN.ym  # y coordination of base station
        # Add to WSN
        WSN.nodes = nodes
        WSN.sink = sink

    def init_malicious_nodes():
        """ Initialize attributes of every malicious node in order """
        for i in range(WSN.m_n):
            node = Node()
            node.id = WSN.n + i
            WSN.nodes.append(node)

    def plot_wsn():
        nodes = WSN.nodes
        n = WSN.n
        m_n = WSN.m_n
        # base station
        sink = WSN.sink
        # plt.plot([sink.xm], [sink.ym], 'r^',label="基站")
        plt.plot([sink.xm], [sink.ym], 'r^', label="シンク")
        # 正常节点
        n_flag = True
        for i in range(n):
            if n_flag:
                # plt.plot([nodes[i].xm], [nodes[i].ym], 'b+',label='正常节点')
                plt.plot([nodes[i].xm], [nodes[i].ym], 'b+', label='通常のノード')
                n_flag = False
            else:
                plt.plot([nodes[i].xm], [nodes[i].ym], 'b+')
        # 恶意节点
        m_flag = True
        for i in range(m_n):
            j = n + i
            if m_flag:
                # plt.plot([nodes[j].xm], [nodes[j].ym], 'kd',label='恶意节点')
                plt.plot([nodes[j].xm], [nodes[j].ym], 'kd', label='悪意あるノード')
                m_flag = False
            else:
                plt.plot([nodes[j].xm], [nodes[j].ym], 'kd')
        plt.legend()
        plt.xlabel('X/m')
        plt.ylabel('Y/m')
        plt.show()


class Leach(object):
    """ Leach """
    # Optimal selection probablitity of a node to become cluster head
    p = 0.1  # 选为簇头概率 クラスタヘッドの確率
    period = int(1/p)  # 周期 ラウンドのこと?
    heads = None  # 簇头节点列表 クラスタヘッドのノードリスト
    members = None  # 非簇头成员列表 非クラスタヘッドのノードリスト
    # 簇类字典 :{"簇头1":[簇成员],"簇头2":[簇成员],...} クラスタクラス辞書:{"CH1":[クラスタメンバ], "CH2":[クラスタメンバ], "CH3":[...}
    cluster = None
    r = 0  # 当前轮数 現在のラウンド数
    rmax = 5  # 9999 # default maximum round
    r_empty = 0  # 空轮

    def show_cluster():
        fig = plt.figure()
        # 设置标题 タイトルを設定
        # 设置X轴标签 x軸のラベルを設定
        plt.xlabel('X/m')
        # 设置Y轴标签 y軸のラベルを設定
        plt.ylabel('Y/m')
        icon = ['o', '*', '.', 'x', '+', 's']
        color = ['r', 'b', 'g', 'c', 'y', 'm']
        # 对每个簇分类列表进行show クラスタの分類ごとに表示
        i = 0
        nodes = WSN.nodes
        for key, value in Leach.cluster.items():
            cluster_head = nodes[int(key)]
            # print("第", i + 1, "类聚类中心为:", cluster_head)
            for index in value:
                plt.plot([cluster_head.xm, nodes[index].xm], [cluster_head.ym, nodes[index].ym],
                         c=color[i % 6], marker=icon[i % 5], alpha=0.4)
                # 如果是恶意节点 悪意あるノードの場合
                if index >= WSN.n:
                    plt.plot([nodes[index].xm], [nodes[index].ym], 'dk')
            i += 1
        # 显示所画的图 図を表示
        plt.show()

    def optimum_number_of_clusters():
        """ 完美融合下的最优簇头数量 """
        """ 完全融合の下での最適なクラスタヘッド数"""
        N = WSN.n - WSN.n_dead
        M = np.sqrt(WSN.xm * WSN.ym)
        d_toBS = np.sqrt((WSN.sink.xm - WSN.xm) ** 2 +
                         (WSN.sink.ym - WSN.ym) ** 2)
        k_opt = (np.sqrt(N) / np.sqrt(2 * np.pi) *
                 np.sqrt(WSN.Efs / WSN.Emp) *
                 M / (d_toBS ** 2))
        p = int(k_opt) / N
        return p

    def cluster_head_selection():
        """ 根据阈值选择簇头节点 """
        """ 閾値に従ってクラスタヘッドノードを選択 """
        nodes = WSN.nodes
        n = WSN.n  # 非恶意节点 悪意のないノード
        heads = Leach.heads = []  # 簇头列表, 每轮初始化为空 クラスタヘッドのリスト, ラウンドごとに初期化される
        members = Leach.members = []  # 非簇成员成员列表 非クラスタヘッドのノードのリスト
        p = Leach.p
        r = Leach.r
        period = Leach.period
        Tn = p / (1 - p * (r % period))  # 閾値Tn
        print(Leach.r, Tn)
        for i in range(n):
            # After the energy dissipated in a given node reached a set threshold,
            # that node was considered dead for the remainder of the simulation.
            if nodes[i].energy > Node.energy_threshold:  # 节点未死亡 ノードが死んでいない
                if nodes[i].G == 0:  # 此周期内节点未被选为簇头 このサイクルではノードはCHとして選択されていない
                    temp_rand = np.random.random()
#                    print(temp_rand)
                    # 随机数低于阈值节点被选为簇头
                    # 閾値以下のランダムな数のノードがCHとして選択される
                    if temp_rand <= Tn:
                        nodes[i].type = "CH"  # 此节点为周期本轮簇头 このノードはCHとなる
                        # G设置为1，此周期不能再被选择为簇头 or (1/p)-1 Gは1に設定され，この期間はクラスタヘッドまたは(1/p)-1として選択できなくなる
                        nodes[i].G = 1
                        heads.append(nodes[i])
                        # 该节点被选为簇头，广播此消息
                        # このノードはCHとして選択され、このメッセージをブロードキャストする
                        # Announce cluster-head status, wait for join-request messages
                        max_dis = np.sqrt(WSN.xm ** 2 + WSN.ym ** 2)
                        nodes[i].energy -= WSN.trans_energy(WSN.CM, max_dis)
                        # 节点有可能死亡 ノードが死亡する危険性がある
                if nodes[i].type == "N":  # 该节点非簇头节点 クラスタヘッドでないノード
                    members.append(nodes[i])
        m_n = WSN.m_n
        for i in range(m_n):
            j = n + i
            members.append(nodes[j])
        # 如果本轮未找到簇头
        # このラウンドでクラスタヘッドが見つからなかった場合
        if not heads:
            Leach.r_empty += 1
            print("---> 本轮未找到簇头！このラウンドではクラスタヘッドが見つかりませんでした!")
            # Leach.cluster_head_selection()
        print("The number of CHs is:", len(heads), (WSN.n - WSN.n_dead))
        return None  # heads, members

    def cluster_formation():
        """ 进行簇分类 """
        """ クラスタの分類を行う """
        nodes = WSN.nodes
        heads = Leach.heads
        members = Leach.members
        cluster = Leach.cluster = {}  # 簇类字典初始化 クラスタ辞書の初期化
        # 本轮未有簇头，不形成簇
        # クラスタヘッドが存在せず、クラスタを形成しない場合
        if not heads:
            return None
        # 如果簇头存在，将簇头id作为cluster字典的key值
        # クラスタヘッドがぞんざいする場合、ノードIDをクラスタ辞書のkey値にする
        for head in heads:
            cluster[str(head.id)] = []  # 成员为空列表 クラスタのメンバー（空のリスト）
        # print("只有簇头的分类字典:", cluster)
        # 遍历非簇头节点，建立簇
        # 非CHのノードを走査して、クラスタを形成する
        for member in members:
            # 选取距离最小的节点
            # 距離が最少のノードを選択する
            # 簇头节点区域内的广播半径 クラスタヘッド領域におけるブロードキャストの半径
            min_dis = np.sqrt(WSN.xm ** 2 + WSN.ym ** 2)
            head_id = None
            # 接收所有簇头的信息
            # 全てのクラスタヘッドから情報を受信する
            # wait for cluster-head announcements
            member.energy -= WSN.ERX * WSN.CM * len(heads)
            # 判断与每个簇头的距离，加入距离最小的簇头
            # 各CHまでの距離を決定し、距離が最少のCHに参加
            for head in heads:
                tmp = WSN.dist(member, head)
                if tmp <= min_dis:
                    min_dis = tmp
                    head_id = head.id
            member.head_id = head_id  # 已找到簇头 クラスタヘッド発見
            # 发送加入信息，通知其簇头成为其成员
            # クラスタヘッドにメンバーになることを通知するメッセージを送信
            # send join-request messages to chosen cluster-head
            member.energy -= WSN.trans_energy(WSN.CM, min_dis)
            # 簇头接收加入消息
            # クラスタヘッドが参加メッセージを受信
            # wait for join-request messages
            head = nodes[head_id]
            head.energy -= WSN.ERX * WSN.CM
            # 添加到出簇类相应的簇头　対応するクラスタヘッドのリストにノードを追加
            cluster[str(head_id)].append(member.id)
        # 为簇中每个节点分配向其传递数据的时间点
        # クラスタ内の各ノードにデータを送信する時間帯を割り当てる（スケジューリングのステップ）
        # Create a TDMA schedule and this schedule is broadcast back to the nodes in the cluster.
        for key, values in cluster.items():
            head = nodes[int(key)]
            if not values:
                # If there are cluster members, the CH sends schedule by broadcasting
                max_dis = np.sqrt(WSN.xm ** 2 + WSN.ym ** 2)
                head.energy -= WSN.trans_energy(WSN.CM, max_dis)
                for x in values:
                    member = nodes[int(x)]
                    # wait for schedule from cluster-head
                    member.energy -= WSN.ERX * WSN.CM
#        print(cluster)
        return None  # cluster

    def set_up_phase():
        """ セットアップ・フェーズ"""
        Leach.cluster_head_selection()
        Leach.cluster_formation()

    def steady_state_phase():
        """ 簇成员向簇头发送数据，簇头汇集数据然后向汇聚节点发送数据 """
        """ クラスタメンバはCHにデータを送信、CHはデータを集約してからシンクに送信 """
        """ ステディ・フェーズ """
        nodes = WSN.nodes
        cluster = Leach.cluster
        # 如果本轮未形成簇，则退出
        # このラウンドでクラスタは形成されていない場合は終了する
        if not cluster:
            return None
        for key, values in cluster.items():
            head = nodes[int(key)]
            n_member = len(values)  # 簇成员数量 クラスタメンバ数
            # 簇中成员向簇头节点发送数据
            # クラスタ内のメンバがCHにデータを送信する
            for x in values:
                member = nodes[int(x)]
                dis = WSN.dist(member, head)
                # 簇成员发送数据 クラスタメンバがデータを送信
                member.energy -= WSN.trans_energy(WSN.DM, dis)
                head.energy -= WSN.ERX * WSN.DM  # 簇头接收数据 クラスタヘッドがデータを受信
            # The distance of from head to sink
            d_h2s = WSN.dist(head, WSN.sink)
            if n_member == 0:  # 如果没有簇成员,只有簇头收集自身信息发送给基站 クラスタメンバがいない場合はCHのみが情報をシンクに送信する
                energy = WSN.trans_energy(WSN.DM, d_h2s)
            else:
                # 加上簇头本身收集的数据，进行融合后的新的数据包 クラスタメンバのデータとCHのデータを融合したnew_data
                new_data = WSN.DM * (n_member + 1)
                E_DA = WSN.EDA * new_data  # 聚合数据的能量消耗 集計データのエネルギー消費量
                if WSN.f_r == 0:  # f_r为0代表数据完美融合 完全なデータ融合の場合, f_rは0になる
                    new_data_ = WSN.DM
                else:
                    new_data_ = new_data * WSN.f_r
                E_Trans = WSN.trans_energy(new_data_, d_h2s)
                energy = E_DA + E_Trans
            head.energy -= energy

    def leach():
        Leach.set_up_phase()
        Leach.steady_state_phase()

    def run_leach():
        for r in range(Leach.rmax):
            Leach.r = r
            nodes = WSN.nodes
            # 当新周期开始时，G重置为0
            # 新しいラウンドが始まるとG=0にリセットされる
            if (r % Leach.period) == 0:
                print("==============================")
                for node in nodes:
                    node.G = 0
            # 当每一轮开始时，节点类型重置为非簇头节点
            # 各ラウンド開始時にノードタイプが非CHにリセットされる
            for node in nodes:
                node.type = "N"
            Leach.leach()
            WSN.node_state(r)
            if WSN.flag_all_dead:
                print("==============================")
                break
            Leach.show_cluster()


def main():
    Node.init_nodes()
    Node.init_malicious_nodes()
    Node.plot_wsn()
    Leach.run_leach()
    # print("The first node died in Round %d!" % (WSN.round_first_dead))
    # print("The network stop working in Round %d!" % (WSN.round_net_stop))
    # print("All nodes died in Round %d!" % (WSN.round_all_dead))


if __name__ == '__main__':
    main()
