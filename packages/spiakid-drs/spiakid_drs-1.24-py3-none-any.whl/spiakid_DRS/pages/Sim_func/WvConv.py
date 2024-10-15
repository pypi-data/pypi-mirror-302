import numpy as np
from scipy import interpolate
from scipy.optimize import least_squares
import scipy.signal as sg

def conv(CalibData, pxnbr):
    mt = np.zeros(shape = (pxnbr, pxnbr, len(CalibData)))
    num = 0

    for i in CalibData.keys():
        
        
        for px in CalibData[i]:
            
            a = np.histogram(CalibData[i][px][1], bins = 50)
            y = a[0]
            x = a[1]
            x = x[:-1]
            val = sg.find_peaks(y, width=5)
            sigma, mu, amp = fit_gauss(y, x, x[val[0][0]])
            x,y = int(list(px.split(sep='_'))[0]),int(list(px.split(sep='_'))[1])
            mt[x,y,num] = mu
            # print(x,y, mu)
        num = num + 1
    
    mt_wvph =np.zeros(shape=(pxnbr, pxnbr), dtype = object)
    mt_phwv =np.zeros(shape=(pxnbr, pxnbr), dtype = object)
    for i in range(pxnbr):
        for j in range(pxnbr):
            mt_phwv[i,j] = interpolate.CubicSpline( mt[i,j,:][::-1],np.array(list(CalibData.keys()))[::-1], bc_type='not-a-knot')
            mt_wvph[i,j] = interpolate.CubicSpline( np.array(list(CalibData.keys())), mt[i,j,:], bc_type='not-a-knot')
             


    return(mt_wvph, mt_phwv)

def fit_gauss(data,time,center):
        def model(x,u):
            return( x[2]/(x[0]*np.sqrt(2*np.pi))*np.exp(-((u-x[1])**2/(2*x[0]**2))))
        
        def fun (x,u,y):
            return( model(x,u)-y)

        def Jac (x,u,y):
            J = np.empty((u.size,x.size))
            J[:,0] = x[2]*np.exp(-(u-x[1])**2/(2*x[0]**2))/(x[0]**4*np.sqrt(2*np.pi))*(u-x[0]-x[1])*(u+x[0]-x[1])
            J[:,1] = x[2]/(x[0]**3*np.sqrt(2*np.pi))*np.exp(-(u-x[1])**2/(2*x[0]**2))*(u-x[1])
            J[:,2] = 1/(x[0]*np.sqrt(2*np.pi))*np.exp(-(u-x[1])**2/(2*x[0]**2))
            return J
        dat = np.array(data)
        t = np.array(time)
        x0 = np.array([1,center,1000])
        res = least_squares(fun, x0, args=(t, dat), jac=Jac, bounds= ([0,0,0],[np.inf,np.inf,np.inf]))
        return res.x[0],res.x[1],res.x[2]