#!  /bin/env python2.7


""" 
# Script for testing ols() - Ordinary Least Squares
#
# Here how we interpolate (do OLS) in cse_task_BUILD_POS_ESTIMATED.py
#    (September 2016)
#    res = pd.ols(x=df.xx,y=df.yy)
#    slope     = res.beta.x
#    intercept = res.beta.intercept
#    r2        = res.r2
# 
# Here is how we can do it going forward:
#   import statsmodels.api as sm
#   res = sm.OLS(df.yy, sm.add_constant(df.xx), missing='drop').fit()
#   slope     = res.params.xx
#   intercept = res.params.const
#   r2        = res.rsquared
#
# see also:
# http://stackoverflow.com/questions/38836465/how-to-get-the-regression-intercept-using-statsmodels-api
"""
import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

import myutil
reload(myutil)
from myutil import *

import myutil_dt
reload(myutil_dt)
from myutil_dt import *

pd.set_option('mode.chained_assignment','warn')

# ---------------------------------------------------------------
def pd_ols(bag):
    """
    # testing old pd.ols()
    """
    print "-"*50, "\nusing pd.ols\n", "-"*50
    bag.pd_ols_res=pd.ols(x=bag.xx,y=bag.yy)
    # ----------------------------------
    bag.pd_ols_slope     = bag.pd_ols_res.beta.x
    bag.pd_ols_intercept = bag.pd_ols_res.beta.intercept
    bag.pd_ols_r2        = bag.pd_ols_res.r2
    print "bag.pd_ols_slope     = ", bag.pd_ols_slope
    print "bag.pd_ols_intercept = ", round(bag.pd_ols_intercept,8)
    print "bag.pd_ols_r2        = ", bag.pd_ols_r2
    # ----------------------------------
    # print res

# ---------------------------------------------------------------
def sm_ols(bag):
    """
    # testing new sm.OLS()
    """
    print "-"*50, "\nusing sm.OLS\n", "-"*50
    import statsmodels.api as sm
    bag.sm_ols_res = sm.OLS(bag.yy, sm.add_constant(bag.xx), missing='drop').fit()
    # ----------------------------------
    bag.sm_ols_slope     = bag.sm_ols_res.params.xx
    bag.sm_ols_intercept = bag.sm_ols_res.params.const
    bag.sm_ols_r2        = bag.sm_ols_res.rsquared
    print "bag.sm_ols_slope     = ", bag.sm_ols_slope
    print "bag.sm_ols_intercept = ", round(bag.sm_ols_intercept,8)
    print "bag.sm_ols_r2        = ", bag.sm_ols_r2
    # ----------------------------------
    # print bag.sm_ols_res.params
    # print bag.sm_ols_res.summary()

# ---------------------------------------------------------------
def main(bag):
    """
    # main
    """
    myinit(bag)
    bag.mask_log_str = ""
    # ----------------------------------
    # create some data
    bag.aa=DataFrame({'xx':range(8),
                      'yy':[0.0, 2.1, 4.0, 5.8, np.NaN, 10.3, 12.1, 13.8]})
    # bag.aa = bag.aa[:1]
    # bag.aa = bag.aa[:2]
    bag.xx = bag.aa.xx
    bag.yy = bag.aa.yy
    # ----------------------------------
    pd_ols(bag)   # run old pandas OLS
    sm_ols(bag)   # run new statsmodels OLS
    # ----------------------------------
    print"\nDONE\n"

# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    main(bag)
