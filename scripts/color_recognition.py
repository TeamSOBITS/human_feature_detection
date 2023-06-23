#入力: RGB = {int(R), int(G), int(B)}
#出力: string COLOR_NAME (ex: "White", "Black", et.al.)
def decide_color(RGB):
    R = RGB[0] / 256
    G = RGB[1] / 256
    B = RGB[2] / 256
    Max = max(R, G, B)
    Min = min(R, G, B)

    h = Max - Min
    #HSV初期処理、hが0のときに適当に治す(0除算対策)
    if h == 0:
        #print('h:', h, 'Max:', Max, 'Min:', Min)
        S = 1
        h = 1
    else:
        S = (h / Max) * 100 
    V = Max * 100
    
    if Max == R:
        H = 60 * ((G - B) / h)
        if H < 0 :
            H = 360 - abs(H)
    elif Max == G:
        H = 60 * ((B - R) / h) + 120
    elif Max == B:
        H = 60 * ((R - G) / h) + 240
    elif R == G == B:
        H = 0
    print(H, S, V)

    if H >= 0 and H < 30 or H >= 340 and H <= 360:
        if S <= 10 and V > 85:
            return 'White'
        elif S <= 10 and V > 15 and V <= 85:
            return 'Gray'
        elif V <= 15:
            return 'Black'
        else:
            return 'Red'
        
    elif H >= 30 and H < 40:
        if S <= 10 and V > 85:
            return 'White'
        elif S <= 10 and V > 15 and V <= 85:
            return 'Gray'
        elif V <= 15:
            return 'Black'
        elif S >= 50 and V <= 80 and V > 15:
            return 'Brown'
        else:
            return 'Orange'
        
    elif H >= 40 and H < 65:
        if S <= 10 and V > 85:
            return 'White'
        elif S <= 10 and V > 15 and V <= 85:
            return 'Gray'
        elif V <= 15:
            return 'Black'
        else:
            return 'Yellow'
        
    elif H >= 65 and H < 165 :
        if S <= 10 and V > 85:
            return 'White'
        elif S <= 10 and V > 15 and V <= 85:
            return 'Gray'
        elif V <= 15:
            return 'Black'
        else:
            return 'Green'
        
    elif H >= 165 and H < 265:
        if S <= 10 and V > 85:
            return 'White'
        elif S <= 10 and V > 15 and V <= 85:
            return 'Gray'
        elif V <= 15:
            return 'Black'
        else:
            return 'Blue'
        
    elif H >= 265 and H < 340 :
        if S <= 10 and V > 85:
            return 'White'
        elif S <= 10 and V > 15 and V <= 85:
            return 'Gray'
        elif V <= 15:
            return 'Black'
        elif H >= 300 and S > 5 and V >= 80:
            return 'Pink'
        else:
            return 'Purple'
    
    else:
        #print('out of range', RGB, H, S, V)
        pass
