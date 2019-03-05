import numpy as np
def RGB2XYZ(RGB):
    #the operator @ cannot accept 2 lists, but can accept 1 list and 1 nd-array
    #matrix M according to http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    def Inverse_sRGB_Companding(x):
        if x > 0.04045:
            return ((x + 0.055) / 1.055)** 2.4
        else:
            return x / 12.92
    # multiple with 100 isn't said in the website
    tmp_RGB=np.array([[100*Inverse_sRGB_Companding(np.asscalar(x)/255.0) for x in list(RGB)]]).T
    M_AdobeRGB = np.array(
        [[0.5767309,  0.1855540,  0.1881852],
        [0.2973769,  0.6273491,  0.0752741],
        [0.0270343,  0.0706872,  0.9911085]])
    M_sRGB=np.array(
        [[0.4124564,  0.3575761,  0.1804375],
        [0.2126729,  0.7151522,  0.0721750],
        [0.0193339,  0.1191920,  0.9503041]])
    M_CIERGB = np.array(
        [[0.4887180,  0.3106803,  0.2006017],
         [0.1762044,  0.8129847,  0.0108109],
         [0.0000000,  0.0102048,  0.9897952]])
    return np.matmul(M_sRGB,tmp_RGB)
def XYZ2LAB(XYZ):
    #f(x) according to http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
    def f(t):
        if t > 216/24389:
            return t ** (1 / 3)
        else:
            return (24389 / 27 * t + 16) / 116            
    #because XYZ is like [[1],[2],[3]]. XYZ[0] will be array([1]). So it should be XYZ[0,0].
    #Or use np.asscalar()
    return np.array(
        [[116*f(XYZ[1,0] / 100.0)-16,
        500*(f(XYZ[0,0] / 95.13) - f(XYZ[1,0] / 100.0)),
        200*(f(XYZ[1,0] / 100.0) - f(XYZ[2,0] / 108.8))]]).T
def RGB2LAB(RGB):
    return XYZ2LAB(RGB2XYZ(RGB))
def deltaE_CIE76(LAB1, LAB2):
    deltaL = LAB2[0,0] - LAB1[0,0]
    deltaA = LAB2[1,0] - LAB1[1,0]
    deltaB = LAB2[2,0] - LAB1[2,0]
    return (deltaL ** 2 + deltaA ** 2 + deltaB ** 2)** (1/2)

RGB1 = np.array([[int(x) for x in [0xC9, 0xC4, 0xBE]]]).T
RGB2 = np.array([[int(x) for x in [0xC6, 0xC4, 0xC5]]]).T
print(RGB2XYZ(RGB1))
print(RGB2XYZ(RGB2))
print(RGB2LAB(RGB1))
print(RGB2LAB(RGB2))
print("deltaE =", deltaE_CIE76(RGB2LAB(RGB1), RGB2LAB(RGB2)))

 




