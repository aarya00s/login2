import MTInterface as mt 
import BarPatterns as bp 
import csv 
 
no = None 
trade = '' 
entry = 0 
 
balance = 10000     # starting account balance 
 
currentBar = mt.Bar(0,0,0,0) 
startTime = 0 
def run(): 
    global no 
    global trade 
    global entry 
    global balance 
    if len(mt.Bars) > 15:   # make sure that things have had time to start up 
        if no is None:   # if no no is currently open... 
            if(bp.getDirection() > 1):  # if the momentum index > 1 
                no = mt.openno(mt.OP_BUY) # send a buy order for 1 lot 
                trade = 'buy' 
                entry = mt.Asks[0] 
            elif(bp.getDirection() < -1):   # if the momentum index < 1 
                no = mt.openno(mt.OP_SELL)    # send a sell order for 1 
                trade = 'sell' 
                entry = mt.Bids[0] 
        elif(trade == 'buy'):   # if a no is open and it's a buy order 
            # if the index < 0.5 or stop loss kicks in 
            if(bp.getDirection() < 0.5 or (mt.Bids[0]-entry)*100000 < -100): 
                mt.closeno(no) 
                no = None 
                # delta is the profit of the no just closed 
                delta = round((mt.Bids[0]-entry)*100000 - 10, 2) 
                balance += delta 
                logToFile(balance)  # log the current balance to a CS
        elif(trade == 'sell'):  # if a no is open and it's a sel 
            # if the index > -0.5 or stop loss kicks in 
            if(bp.getDirection() > -0.5 or (entry-mt.Asks[0])*100000 < -100): 
                mt.closeno(no) 
                no = None 
                # delta is the profit of the no just closed 
                delta = round((entry-mt.Asks[0])*100000 - 10, 2) 
                balance += delta 
                logToFile(balance)  # log the current balance to a CSV 
 
# Logs to a csv file with a timestamp 
def logToFile(data, overwrite = False): 
    global startTime 
    #t = mt.getTime() 
    if overwrite: 
        method = 'w' 
    else: 
        method = 'a' 
    with open('../noData.csv', method, newline='') as csvFile: 
        filewriter = csv.writer(csvFile) 
        #filewriter.writerow([t.DayOfWeek, t.Hour, t.Minute, data]) 
        #filewriter.writerow([t.minsSinceMidnight(), data]) 
        mins = int(int(mt.getTimestamp())/60) - startTime 
        filewriter.writerow([str(mins), data]) 
 
# checks to see if an incoming bar has been seen before 
def isNewBar(oldBar, newBar): 
    return(oldBar.Open != newBar.Open and 
       oldBar.High != newBar.High and 
       oldBar.Low != newBar.Low and 
       oldBar.Close != newBar.Close) 
 
 
#Prevent this code from being run when imported 
if __name__ == "__main__": 
    startTime = int(int(mt.getTimestamp())/60) 
 
    # Start off the log 
    logToFile(0,True)   # clear the log file 
 
    #Safe to terminate through ctrl+c or whatever you want 
    while True: 
        #Prevents run() from being run if there is no new tick 
        while not mt.tick(): 
            pass 
        #Runs the strategy 
        if(isNewBar(currentBar, mt.Bars[0])): 
            currentBar = mt.Bars[0] 
 
            t = mt.getTime() 
            # if time is between 12:00 and 24:00 in MT4 time 
            if(t.Hour >= 12 and t.Hour < 24): 
                run() 
            elif no is not None:  # outside the time range and ha
                mt.closeno(no) # close it 
                if(trade == 'buy'): 
                    delta = round((mt.Bids[0]-entry)*100000 - 10, 2) 
                    balance += delta 
                elif(trade == 'sell'): 
                    delta = round((entry-mt.Asks[0])*100000 - 10, 2) 
                    balance += delta 
                logToFile(balance) 
                no = None 

