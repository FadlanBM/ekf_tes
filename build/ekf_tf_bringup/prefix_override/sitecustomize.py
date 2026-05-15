import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/fadlan/Documents/EKF_TES/install/ekf_tf_bringup'
