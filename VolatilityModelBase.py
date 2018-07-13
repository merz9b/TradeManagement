class VolatilityModelBase():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def create_strike_price_list(self, f_atm, X_n, X_inc):
        X_atm = round(f_atm / X_inc) * X_inc
        idx = list(range(-int(X_n), 0)) + list(range(0, int(X_n)+1))
        return([X_atm + i * X_inc for i in idx])
        
