# %%
import numpy as np
import h5py
from sklearn import preprocessing


def hdf5_read(fname):
  file = h5py.File(fname, 'r')
  database = np.array(file['train'])
  query = np.array(file['test'])
  gt = np.array(file['neighbors'])
  return database, query, gt


class Dataset:
  def __init__(self):
    self.metric = "L2"      # 如果是欧氏距离选用L2，如果是angular选用"IP"
    self.database = None    # 数据库
    self.query = None       # 查询
    self.gt = None          # 标准答案
    
  def get_dim(self):
    """
    :return: 数据维度
    """
    return self.get_database().shape[1]


  def get_database(self) -> np.ndarray:
    """
    :return: database vectors
    """
    if self.database is None:
      return None
    
    return preprocessing.normalize(self.database) if self.metric == "IP" else self.database

  def get_query(self) -> np.ndarray:
    """
    :return: query vectors
    """
    if self.query is None:
      return None
    
    return preprocessing.normalize(self.query) if self.metric == "IP" else self.query

  def get_gt(self, k=None) -> np.ndarray:
    """
    :param k: topk
    """
    if self.gt is None:
      return None
    
    return self.gt if k is None else self.gt[:, :k]

  def __str__(self) -> str:
    return f"train: {self.get_database().shape if self.database else None}, \n test: {self.get_query().shape if self.query else None}, \n gt  : {self.get_gt().shape if self.gt else None}"


class VECS(Dataset):
  """
  当前VECS数据集的格式为: dim, data x dim,
                     dim, data x dim,
                     dim, data x dim,
                     ... 
  """
  def __init__(self, base_fname=None, query_fname=None, gt_fname=None, metric="L2"):
    super().__init__()
    self.metric = metric

    if base_fname:
      self.load_base(base_fname)
    if query_fname:
      self.load_query(query_fname)
    if gt_fname:
      self.load_gt(gt_fname)
  
  def get_data(self, fname, dtype: np.dtype) -> np.ndarray:
    with open(fname, 'rb') as f:
      dim = np.fromfile(f, dtype=np.int32, count=1)[0]
      f.seek(0, 0)
      return np.fromfile(f, dtype=dtype).reshape(-1, dim + 1)[:, 1:]
  
  
  def load_base(self, fname):
    self.database = self.get_data(fname, np.float32)
    
    
  def load_query(self, fname):
    self.query = self.get_data(fname, np.float32)
  
  
  def load_gt(self, fname):
    self.gt = self.get_data(fname, np.int32)

class NPARRAY(Dataset):
  """
  直接传入numpy数组加载
  """
  def __init__(self, database=None, query=None, gt=None, metric="L2"):
    super().__init__()
    self.metric = metric
    self.database = database
    self.query = query
    self.gt = gt
  
  def load_base(self, database):
    self.database = database
  
  def load_query(self, query):
    self.query = query
  
  def load_gt(self, gt):
    self.gt = gt
    
class HDF5(Dataset):
  """
  从hdf5文件加载数据
  """
  def __init__(self, 
               file_path,
               metric='L2'):
    super().__init__()
    self.metric = metric
    self.database, self.query, self.gt = hdf5_read(file_path)

if __name__ == "__main__":
  pass