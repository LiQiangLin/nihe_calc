def fai_moistair(t,ts,B,v):
    pv = pq_moistair(t,ts,B,v)
    ps_t = ps(t)
    if pv <= 0:
        fai_moistair = -1
    fai_moistair = pv / ps_t
    return fai_moistair


def ps(t):
    from math import log
    T_t = t + 273.15
    if t >= -0.4773383:
        ps = 31.465564 - 3142.305 / T_t - 8.2 * (log(T_t) / log(10)) + 0.0024804 * T_t
    else:
        ps = -6.757169 - 2445.5646 / T_t + 8.2312 * (log(T_t) / log(10)) - 0.01677006 * T_t + 0.0000120514 * T_t * T_t
    ps = 10 ** ps
    ps = 101325 / 760 * ps
    return ps

def pq_moistair(t,ts,B,v):
    a = 0.00001 * (65 + 6.75 / v)
    ps_ts = ps(ts)                                          #由湿球温度求饱和压力ps
    pq = ps_ts - a * (t - ts) * B                           #根据ps求pq
    if pq < 0:
        ts_1 = ts
        ts_2 = t
        while True:                                         #迭代
            tsm = (ts_1 + ts_2) / 2
            ps_ts = ps(tsm)
            ps_tt = a * (t - tsm) * B
            err = abs(2 * (ps_ts - ps_tt) / (ps_ts + ps_tt))
            if err < 0.0000000001:
                break
            elif ps_ts < ps_tt:
                ts_1 = tsm
            else:
                ts_2 = tsm
        pq_moistair = 0
    pq_moistair = pq
    return pq_moistair

def d_moistair(t,ts,B,v):
    pv = pq_moistair(t,ts,B,v)
    d_moistair = 0.62198 * pv /(B - pv)
    return d_moistair

def nambda_moistair(t,ts,B,v):
    nambdaa = (2.4587 + 0.0075855 * t - 0.00000169 * t ** 2) * 10 ** (-2)           #干空气的导热系数（W/(m.K))
    nambdav = (1.6 + 0.006179 * t + 0.000027535 * t ** 2) * 10 ** (-2)              #水蒸气的导热系数（W/(m.K))
    miua = (17.4945 + 0.04799 * t - 0.000033256 * t ** 2) * 10 ** (-6)              #干空气的动力粘度（Pa·s)
    miuv = (8.1804 + 0.04011 * t - 0.000017858 * t ** 2) * 10 ** (-6)               #水蒸气的动力粘度（Pa·s)
    d = d_moistair(t, ts, B, v)                                                   #根据湿球温度ts(℃)求得的湿空气的含湿量d(kg/kg干空气)
    nambda_moistair = 4.56724 * nambdaa / (1 + 0.8881 * (miua / miuv) ** 0.5) ** 2 * (1 / (1 + 1.60746 * d) + nambdav / (nambdaa * (1 + miuv / (miua * d))))
    return nambda_moistair

def pq_fai_moistair(t,fai,B,v):
    a = 0.00001 *(65 + 6.75 / v)
    ps_fai = ps(t)
    pq_fai_moistair = ps_fai * fai
    return pq_fai_moistair

def rou_moistair(t,ts,B,v):
    T_t = t + 273.15
    PV = pq_moistair(t, ts, B, v)                              #pv(Pa)是根据湿球温度ts(℃)求得的水蒸气的分压力
    rou_moistair = 0.003484 * B / T_t - 0.001317 * PV / T_t    #求密度
    return rou_moistair

def miu_moistair(t,ts,B,v):
    miua = (17.4945 + 0.04799 * t - 0.000033256 * t ** 2) * 10 ** (-6)     #干空气的动力粘度（Pa·s)
    miuv = (8.1804 + 0.04011 * t - 0.000017858 * t ** 2) * 10 ** (-6)      #水蒸气的动力粘度（Pa·s)
    d = d_moistair(t, ts, B, v)                                          #根据湿球温度ts(℃)求得的湿空气的含湿量d(kg/kg干空气)
    miu_moistair = miua * (1 + 1.268 * d * miuv / miua) / (1 + 1.268 * d)
    return miu_moistair

def deq(s1,sf,do,dertaf):
    return 2 * (s1 - 1.0444 * do - 2 * dertaf) * (sf - dertaf) / ((s1 - 1.0444 * do - 2 * dertaf) + (sf - dertaf))

def wm(s1,sf,v,do,dertaf):
    return s1 * sf * v / ((s1 - 1.0444 * do - 2 * dertaf) * (sf - dertaf))

def lp(np,s2):
    return np * s2

def ref(t,ts,B,v,s1,sf,do,dertaf):
    roua = rou_moistair(t,ts,B,v)
    wma = wm(s1,sf,v,do,dertaf)
    deqa = deq(s1,sf,do,dertaf)
    miua = miu_moistair(t,ts,B,v)
    return roua * wma * deqa / miua