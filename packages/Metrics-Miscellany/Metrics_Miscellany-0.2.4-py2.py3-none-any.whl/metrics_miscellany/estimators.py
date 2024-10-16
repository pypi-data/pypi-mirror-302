import statsmodels.api as sm
from statsmodels.stats import correlation_tools
import numpy as np
from numpy.linalg import lstsq
import warnings
import pandas as pd
from . import gmm
from . GMM_class import GMM
from . import utils
from .datamat import DataMat, DataVec

def ols(X,y,cov_type='HC3',PSD_COV=False):
    """OLS estimator of b in y = Xb + u.

    Returns both estimate b as well as an estimate of Var(b).

    The estimator used for the covariance matrix depends on the
    optional argument =cov_type=.

    If optional flag PSD_COV is set, then an effort is made to ensure that
    the estimated covariance matrix is positive semi-definite.  If PSD_COV is
    set to a positive float, then this will be taken to be the smallest eigenvalue
    of the 'corrected' matrix.
    """
    n,k = X.shape

    est = sm.OLS(y,X).fit()
    b = pd.DataFrame({'Coefficients':est.params.values},index=X.columns)
    if cov_type=='HC3':
        V = est.cov_HC3
    elif cov_type=='OLS':
        XX = X.T@X
        if np.linalg.eigh(XX)[0].min()<0:
            XX = correlation_tools.cov_nearest(XX,method='nearest')
            warnings.warn("X'X not positive (semi-) definite.  Correcting!  Estimated variances should not be affected.")
        V = est.resid.var()*np.linalg.inv(XX)
    elif cov_type=='HC2':
        V = est.cov_HC2
    elif cov_type=='HC1':
        V = est.cov_HC1
    elif cov_type=='HC0':
        V = est.cov_HC0
    else:
        raise ValueError("Unknown type of covariance matrix.")

    if PSD_COV:
        if PSD_COV is True:
            PSD_COV = (b**2).min()
        s,U = np.linalg.eigh((V+V.T)/2)
        if s.min()<PSD_COV:
            oldV = V
            V = U@np.diag(np.maximum(s,PSD_COV))@U.T
            warnings.warn("Estimated covariance matrix not positive (semi-) definite.\nCorrecting! Norm of difference is %g." % np.linalg.norm(oldV-V))

    V = pd.DataFrame(V,index=X.columns,columns=X.columns)

    return b,V

def tsls(X,y,Z,return_Omega=False):
    """
    Two-stage least squares estimator.
    """

    n,k = X.shape

    Qxz = X.T@Z/n

    zzinv = utils.inv(Z.T@Z/n)
    b = lstsq(Qxz@zzinv@Qxz.T,Qxz@zzinv@Z.T@y/n,rcond=None)[0]

    b = pd.Series(b.squeeze(),index=X.columns)

    # Cov matrix
    e = y.squeeze() - X@b

    #Omega = Z.T@(e**2).dg()@Z/n
    # Rather than forming even a sparse nxn matrix, just use element-by-element multiplication
    ZTe = Z.T.multiply(e)
    Omega = ZTe@ZTe.T/n

    #Omega = pd.DataFrame(e.var()*Z.T.values@Z.values/n,columns=Z.columns,index=Z.columns)

    if return_Omega:
        return b,Omega
    else:
        A = (Qxz@zzinv@Qxz.T).inv
        V = A@(Qxz@zzinv@Omega@zzinv@Qxz.T)@A.T/n
        return b,V
