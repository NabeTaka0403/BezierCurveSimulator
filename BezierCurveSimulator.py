# BezierCurveSimulator: 制御点を操作してBezier曲線をインタラクティブに描画するプログラム
import scipy.special as scs
import numpy as np
import matplotlib.pyplot as plt 

# ベジェ曲線の次数
DEG_BEZIER = 3

# 制御点をドラッグしたとき
def motion(event):
    global gco
    if gco is None:
        return
    # 離したのが制御点なら、その位置と曲線を再描画
    if gco is not None:
        # gco == 'Line2D(_line[0~3])'
        plot_num = int(str(gco)[12])
        x = event.xdata
        y = event.ydata
        if x<0 or x>5 or y<-1 or y>1: 
            x = p[plot_num, 0]
            y = p[plot_num, 1]
        gco.set_data(x,y)
        p[plot_num] = [x, y]
        print(p)
        P = calc_curve(p)
        b_curve.set_data(P.T[0], P.T[1])
        handle.set_data(p.T[0], p.T[1])
    plt.draw()

# 制御点を掴んだとき
def onpick(event):
    global gco
    gco = event.artist
    # 掴んだのが制御点ではないときは無効
    if int(str(gco)[12]) >= 4:
        gco = None

# 制御点を離したとき
def release(event):
    global gco
    gco = None

# Bernstein関数
def bernstein(n, i, t):
    return scs.comb(n, i) * (1-t)**(n-i) * t**i 

# Spline関数
def bezier(n, t, p):
    p_t = np.zeros(2)
    for i in range(n+1):
        p_t += bernstein(n, i, t) * p[i]
    return p_t

# 描画する曲線を計算
def calc_curve(p):
    list = []
    for t in np.linspace(0, 1, 100):
        list.append(bezier(DEG_BEZIER, t, p))
    P = np.array(list)

    return P

# 起動時のみ実行
if __name__ == "__main__":
    plt.figure(num="BezierCurveSimulator")
    plt.title("BezierCurve (N=" + str(DEG_BEZIER) + ")")

    gco = None

    # 制御点の初期化（両端の点のみ曲線が通る）
    p = np.array([[0,0], [1,1], [4,-1], [5,0]], dtype=np.float)
    print(p)

    # 制御点の描画
    plt.plot(p[0,0], p[0,1], "o", color="orange", picker=15)
    plt.plot(p[1,0], p[1,1], "o", color="orange", picker=15)
    plt.plot(p[2,0], p[2,1], "o", color="orange", picker=15)
    plt.plot(p[3,0], p[3,1], "o", color="orange", picker=15)

    P = calc_curve(p)
    # ベジェ曲線の描画
    b_curve, = plt.plot(P.T[0], P.T[1], color="red", label="bezier curve")
    # 制御点・方向線（ハンドル）の描画
    handle, = plt.plot(p.T[0], p.T[1], "--o", color="blue", label="control points & handle")

    plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=7)

    plt.connect("motion_notify_event", motion)
    plt.connect("pick_event", onpick)
    plt.connect("button_release_event", release)
    plt.show()