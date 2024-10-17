import os
import time
import numpy as np
import alaya_cpp_module
import json
import hashlib
from tqdm import trange
  
class Utils():
  @staticmethod
  def __get_dis_func(metric: str):
    """获取距离函数
    
    Args:
      metric(str): 距离度量
    Returns:
      function: 距离函数"""
    if metric == 'L2' or metric.upper() == 'EUCLIDEAN':
      return lambda a, b: np.linalg.norm(b - a, axis=2)
    elif metric == 'IP' or metric.upper() == 'ANGULAR':
      return lambda a, b: np.dot(a, b.T)
    else:
      raise ValueError(f"not support metric: {metric}")
  
  @staticmethod
  def __epsilon_threshold(data: np.array, topk: int, epsilon: float) -> np.array:
    return data[topk - 1] * (1 + epsilon)
    
  @staticmethod
  def calc_gt(database: np.array, query: np.array, topk=10, metric='L2') -> np.array:
    """计算topk个最近邻
    
    根据给出的database和query, 通过小根堆的方法计算topk个最近邻
    
    Args:
      database(np.array): 数据集, shape=(N, dim)
      query(np.array): 查询数据, shape=(n, dim)
      topk(int): topk, default=10
      metric(str): 距离度量, default=L2
    Returns:
      np.array: topk个最近邻的id, shape=(n, topk)"""
    print('calculate gt...')
    begin_time = time.time()
    ret = alaya_cpp_module.Utils.calc_gt(data_load=database, query=query, top_k=topk, metric=metric)
    print(f'calculate succ, cost {time.time() - begin_time: .2f}')
    return ret
  
  @staticmethod
  def calc_distance(database: np.array, L1: np.array, L2_id: np.array, topk=10, batch_size=10, metric='L2') -> np.array:
    """计算两个向量之间的距
    
    Args:
      database(np.array): 数据集, shape=(N, dim)
      L1(np.array):    第一个向量, shape=(n, dim)
      L2_id(np.array): 第二个向量的id, shape=(n, dim)
      topk(int): topk, default=10
      batch_size(int): 每次计算的数量, default=10
      metric(str): 距离度量， default=L2
    Returns:
      np.array: 两个向量之间的距离, shape=(n, topk)
    """
    if L1.ndim == 1:
      L1.reshape(1, -1)
    if L2_id.ndim == 1:
      L2_id.reshape(1, -1)
    
    dis = Utils.__get_dis_func(metric)
    L1 = L1[:, np.newaxis, :]
    L2_id = L2_id[:, :topk]
    
    len, _ = L2_id.shape
    ret = np.zeros((len, topk))
    for i in range(0, len, batch_size):
      end = min(i + batch_size, len)
      ret[i:end] = dis(L1[i:end], database[L2_id[i:end]])
  
    return ret
  
    
  @staticmethod
  def calc_recall(std_dis: np.array, pred_dis: np.array, topk=10, threshold=__epsilon_threshold, epsilon=1e-3) -> float:
    """计算recall
    
    Args:
      std_dis(np.array): 真实的距离
      pred_dis(np.array): 预测的距离
      topk(int): topk
      threshold(function): 阈值函数
      epsilon(float): 阈值的epsilon
    Returns:
      float: recall
    """
    recalls = np.zeros(len(pred_dis))
    for i in range(len(pred_dis)):
        t = threshold(std_dis[i], topk, epsilon)
        actual = 0
        for d in pred_dis[i][:topk]:
            if d <= t:
                actual += 1
        recalls[i] = actual
    return np.mean(recalls) / float(topk)
    
  @staticmethod
  def calc_recall_id(database, query, std_id, pred_id, topk=10, batch_size=10, metric='L2', threshold=__epsilon_threshold, epsilon=1e-3) -> float:
    """计算recall
    
    根据 std_id 正确的结果和 pred_id 预测的结果, 然后计算recall
    
    Args:
      database(np.array): 数据集, shape=(N, dim)
      query(np.array): 查询向量, shape=(n, dim)
      std_id(np.array): 真实的距离对应的query最近的topk个id, shape=(n, topk)
      pred_id(np.array): 预测的距离对应的query最近的topk个id, shape=(n, topk)
      topk(int): topk, default=10
      batch_size(int): 每次计算的数量, default=10
      metric(str): 距离度量， default=L2
      threshold(function): 阈值函数
      epsilon(float): 阈值的epsilon
    Returns:
      float: recall"""
    return Utils.calc_recall(Utils.calc_distance(database, query, std_id, topk, batch_size, metric),
                      Utils.calc_distance(database, query, pred_id, topk, batch_size, metric),
                      topk,
                      threshold,
                      epsilon
    )

  @staticmethod
  def json_dumps(database, query, gt, pred, trace, topk=10, write_file=None):
    """将搜索的结果保存到json文件
    
    Args:
      database(np.array): 数据集, shape=(N, dim)
      query(np.array): 查询向量, shape=(dim,)
      gt(np.array): 真实的结果, shape=(m,)
      pred(np.array): 预测的结果, shape=(m,)
      trace(np.array): 搜索路径, shape=(trace_size, 2)
      topk(int): topk, default=10
      write_file(str): json文件保存的路径
    Returns:
      str: json字符串"""
    json_dic = {}
    json_dic['metrics'] = {'recall': np.intersect1d(pred, gt).size / topk}
    json_dic['searchGT'] = list(gt)
    json_dic['searchRES'] = list(pred)
    # 特判起点
    json_dic['start_node'] = trace[0][1]
    trace = trace[1:]

    trace_info = []
    # 计算两个点之间的距离
    values = Utils.calc_distance(database, database[trace[:, 0]], trace[:, 1].reshape(-1, 1), topk=1)
    
    # 计算两个点和起点的距离
    trace = trace.reshape(1, -1)
    trace_dis = Utils.calc_distance(database, query.reshape(1, -1), trace, topk=trace.shape[1])
    trace_dis = trace_dis.reshape(-1, 2)
    for a, b, c in zip(trace_dis, trace.reshape(-1, 2), values):
      trace_info.append({
        'distance_s': a[0],
        'distance_t': a[1],
        'source': b[0],
        'target': b[1],
        'value': c[0]
      })
    
    json_dic['traceInfo'] = trace_info
    
    class NumpyEncoder(json.JSONEncoder):
      def default(self, obj):
          if isinstance(obj, np.integer):
              return int(obj)
          elif isinstance(obj, np.floating):
              return float(obj)
          elif isinstance(obj, np.ndarray):
              return obj.tolist()
          return json.JSONEncoder.default(self, obj)

    # Use the custom encoder
    json_ctx = json.dumps(json_dic, cls=NumpyEncoder, indent=2)
    if write_file is not None:
      with open(write_file, 'w', encoding='utf-8') as f:
        f.write(json_ctx)
        
    return json_ctx
      
    

class Alaya():
  # STATIC VARIABLES
  MERGRAPH = "MERGRAPH"
  HNSW = "HNSW"
  NSG = "NSG"
  L2 = "L2"
  IP = "IP"
  EUCLIDEAN = "L2"
  ANGULAR = "IP"
  
  def __init__(self, 
              database: np.array, 
              index_type: str=MERGRAPH,
              metric: str=L2,
              M: int=32, 
              L: int=300,
              level: int=3, 
              optimizer: int=os.cpu_count(),
              num_threads: int=os.cpu_count(),
              index_cache_dir: str="data/alaya_index",
              is_cache_index: bool=True,
              is_rebuild: bool=False
              ):
    """
    Args:
      database(np.array): 数据集
      index_type(str): 索引类型, default=MERGRAPH
      metric(str): 距离度量, default=L2
      M(int): MERGRAPH的M参数, default=32
      L(int): MERGRAPH的L参数, default=300
      level(int): MERGRAPH的level参数, default=3
      optimizer(int): 优化器, default=os.cpu_count()
      num_threads(int): 线程数, default=os.cpu_count()
      index_cache_dir(str): 索引缓存目录, default="data/alaya_index"
      is_cache_index(bool): 是否缓存索引, default=True
      is_rebuild(bool): 是否重新构建索引, default=False
      
    Returns:
      None
    """
    
    # 数据集
    self.database = database
    
    # alaya的建图参数
    self.M = M
    self.L = L
    self.index_type = index_type
    self.level = level
    self.metric = metric
    self.is_rebuild = is_rebuild
    
    self.optimizer = optimizer
    self.num_threads = num_threads
    self.__search = None
    
    # 存图参数
    self.index_cache_dir = index_cache_dir
    self.is_cache_index = is_cache_index
    self.index_name = None
    self.index_file = None
    
    self.__init()

  
  def search(self, query, ef: int=32, rerank_k: int=32, topk: int=10, is_trace: bool=False, is_single=False, save_json_dir: str='data/jsons', json_prefix=None, gt=None):
    """搜索topk个最近邻
    Args:
      query(np.array): 查询数据
      ef(int): ef参数, default=32
      rerank_k(int): 重排序的k, default=32
      topk(int): topk, default=10
      is_trace(bool): 是否记录搜索路径, default=False
      save_json_dir(str): 保存json的目录, default='data/jsons'
      gt(np.array): 真实的结果, default=None
    Returns:
      如果is_trace为False, 返回np.array: 返回topk个最近邻的id
      如果is_trace为True, 返回None, 并且将搜索路径保存到json文件
    """
    if type(query) == list:
      query = np.array(query)
    
    if query.ndim == 1:
      query = query.reshape(1, -1)
    
    if is_trace and not os.path.exists(save_json_dir):
      os.makedirs(save_json_dir)
    
    assert query.shape[1] == self.dim, f"query dim: {query.shape[1]} != {self.dim}"
    
    self.__search.set_ef(ef)
    if is_single:
      return self.__search.search_rerank(query=query, data_load=self.database, k=topk, rerank_k=rerank_k)
      
    if not is_trace:
      return self.__search.batch_search_rerank(query=query, data_load=self.database, k=topk, rerank_k=rerank_k, num_threads=self.num_threads)
    
    # trace search
    preds, traces = self.__search.trace_batch_search_rerank(query=query, data_load=self.database, k=topk, rerank_k=rerank_k, num_threads=self.num_threads)
      
    if gt is None:
      gt = Utils.calc_gt(self.database, query, topk=topk)
    
    if type(gt) == list:
      gt = np.array(gt)
      
    if gt.ndim == 1:
      gt = gt.reshape(-1, 1)
    
    # 如果没有指定名字，使用默认的名字
    if json_prefix is None:
      json_prefix = 'trace_data'
      
    # 如果只有一个query，保存为 {json_prefix}.json
    if len(query) == 1:
      Utils.json_dumps(self.database, query[0], gt[0], preds[0], traces[0], topk=topk, write_file=os.path.join(save_json_dir, f'{json_prefix}.json'))
    else:
    # 如果有多个query， 保存为 {json_prefix}_{i}.json
      for i in trange(len(query)):
        Utils.json_dumps(self.database, query[i], gt[i], preds[i], traces[i], topk=topk, write_file=os.path.join(save_json_dir, f'{json_prefix}_{str(i)}.json'))

    return preds
    
  def __init(self) -> None:
    # 获取索引文件的full_path
    if self.is_cache_index:
      if not os.path.exists(self.index_cache_dir):
        os.makedirs(self.index_cache_dir)
      self.index_name = self.__str__()
      self.index_file = os.path.join(self.index_cache_dir, self.index_name)
    
    graph = None
    # 如果索引文件存在，直接加载
    if self.is_cache_index and os.path.exists(self.index_file) and not self.is_rebuild:
      print("use cache index...")
      graph = alaya_cpp_module.Graph()
      graph.load(self.index_file)
    else:
      print("start build index...")
      index = alaya_cpp_module.Index(index_type=self.index_type, dim=self.dim, metric=self.metric, M = self.M, L=self.L)
      graph = index.build(self.database)
      if self.is_cache_index:
        graph.save(self.index_file)  # 将索引缓存
    
    # 初始化搜索器
    self.__search = alaya_cpp_module.Searcher(graph=graph, data=self.database, metric=self.metric, level=self.level)
    self.__search.optimize(self.optimizer)
    
  def __gene_md5(self) -> str:
    """根据database和建图参数生成唯一的md5码
    
    Args:
      None
    Returns:
      str: md5码
    """
    md5 = hashlib.md5()
    md5.update(memoryview(np.ascontiguousarray(self.database)))
    md5.update(self.index_type.encode())
    md5.update(str(self.M).encode())
    md5.update(self.metric.encode())
    md5.update(str(self.level).encode())
    return md5.hexdigest()
    
  @property
  def dim(self) -> int:
    """返回数据集的维度
    
    Args:
      None
    Returns:
      int: 数据集的维度
    """
    return self.database.shape[1]
  
  def __str__(self) -> str:
    """返回索引的名字
    
    Args:
      None
    Returns:
      str: 索引的名字
    """
    if self.index_name is not None:
      return self.index_name
    return f'Alaya-{self.index_type}-{self.metric}-{self.M}-{self.__gene_md5()}'