import numpy as np
import matplotlib.pyplot as plt
# import matplotlib as mpl
from astropy.table import Table
from astropy.io import ascii
from scipy import stats
from tqdm import tqdm_notebook as tqdm
import os

# mpl.rcParams['figure.facecolor'] = 'w'

def readCSV(path,saveFile,outFile):
    return Table.read(path + saveFile+'/Output/'+saveFile+'_'+outFile+'.csv',format='csv',encoding='latin-1')

def readSave(path,saveFile):

    if type(saveFile) != str:
        raise Exception("{} must be string".format(saveFile))

    db = {}

    db['teamCSV'] = readCSV(path,saveFile,'Teams')['TeamID','City','Mascot','Abbrev','Conference']
    db['playerCSV'] = readCSV(path,saveFile,'Players')['PlayerID','Position','FirstName','LastName','TeamID','Team']
    gamesCSV = readCSV(path,saveFile,'Games')
    db['gameCSV'] = gamesCSV[gamesCSV['GameType'] == 'Exhibition']
    pgsCSV = readCSV(path,saveFile,'PlayerGameStats')
    db['pgsCSV'] = pgsCSV[pgsCSV['WeekNumber'] == 16]
#     db['teamCSV']['color'] = ['gold','k','r','maroon','orange','forestgreen','skyblue','purple']

    winMoments, gameCSV = getGameWins(db)
    db['gameCSV'] = gameCSV

    return db

def zScore(x,mean,std):
    return (x-mean)/std

QBstats = ['PassAtt','PassCmp','PassYds','PassInt','PassTD','PassRating','PassLong','SackPct']
RUNstats = ['RushAtt','RushYds','RushTD','Fumbles','RunLong','RushFD']
RECstats = ['Catches','RecYds','RecTD','RecLong','DroppedPasses','RecFD']
BLKstats = ['SacksAllowed','Pancakes']
DEFstats = ['Tackles','TFL','Sacks','Safeties','ForcedFumbles','FumblesRecovered','PassesDefensed','Int','DefensiveTD']
Kstats = ['XPA','XPM','FGA','FGM','Punts','PuntYds','PuntsInside20','FGPct','XPPct','PuntAvg','FGA_U20','FGM_U20','FGA_2029','FGM_2029'
         ,'FGA_3039','FGM_3039','FGA_4049','FGM_4049','FGA_50','FGM_50']
RETstats = ['PuntReturnYds','PuntReturns','KickoffReturnYds','KickoffReturns']
ALLstats = ['Plays','Penalties']

statDic = {
    'QB':ALLstats+QBstats+RUNstats,
    'RB':ALLstats+RUNstats+RECstats+RETstats,
    'FB':ALLstats+RUNstats+RECstats+BLKstats+RETstats,
    'TE':ALLstats+RECstats+BLKstats,
    'WR':ALLstats+RECstats+RETstats,
    'T':ALLstats+BLKstats,
    'G':ALLstats+BLKstats,
    'C':ALLstats+BLKstats,
    'DT':ALLstats+DEFstats,
    'DE':ALLstats+DEFstats,
    'LB':ALLstats+DEFstats,
    'CB':ALLstats+DEFstats+RETstats,
    'FS':ALLstats+DEFstats+RETstats,
    'SS':ALLstats+DEFstats+RETstats,
    'K':ALLstats+Kstats,
    'P':ALLstats+Kstats
}

statALL = ALLstats + QBstats + RUNstats + RECstats + BLKstats + DEFstats + RETstats + Kstats

def getGameWins(db):
    gameCSV = db['gameCSV']
    gameCSV['HWin'] = gameCSV['AwayScore']<gameCSV['HomeScore']
    HPct = (gameCSV['HWin'] == True).sum()/len(gameCSV['HWin'])

    gameCSV['PDiff'] = gameCSV['HomeScore'] - gameCSV['AwayScore']
    mean = np.mean(gameCSV['PDiff'])
    std = np.std(gameCSV['PDiff'])

    return Table(rows=[{'HPct':HPct, 'mean':mean, 'std':std}]), gameCSV

def getTeamInfo(db):
    awayTeam = db['teamCSV'][db['teamCSV']['TeamID'] == db['gameCSV']['AwayTeamID'][0]]
    homeTeam = db['teamCSV'][db['teamCSV']['TeamID'] == db['gameCSV']['HomeTeamID'][0]]
    return awayTeam, homeTeam

def FD(dist):
    dist = np.sort(dist)
    N = len(dist)
#     q25 = dist[int(np.floor(N/4))]
#     q75 = dist[int(np.floor(3*N/4))]
    q25 = np.percentile(dist,25)
    q75 = np.percentile(dist,75)
    return 2*(q75-q25)/N**(1/3)

def statsGraph(gameCSV,moments,stat,path,saveFile,ls='-',winMom=None):
    statTable = gameCSV[stat]
#     print('table:',statTable)
#     dataPlt = plt.figure(figsize=(12,6))
#     plt.title(stat)
    plt.xlabel(stat)
    plt.ylabel('Frequency')
    try:
        if max(statTable)-min(statTable) > 30:
            binSize = FD(statTable)
#             print(binSize)
            binsFD = np.arange(min(statTable),max(statTable)+binSize,binSize)
#             print(binsFD)
            if winMom == None:
                pltLabel = path+saveFile+'\n'+r' $(\mu = %.2f$'%moments['mean'] + r', $\sigma = %.3f)$'%moments['std']
            else:
                pltLabel = path+saveFile+'\n'+r' $(HPct = %.4f'%winMom['HPct'] + r', \mu = %.2f$'%moments['mean'] + r', $\sigma = %.3f)$'%moments['std']
                # plt.axvline(0,c='gray',ls='..')
            plt.hist(statTable,bins=binsFD,histtype='step',label=pltLabel,
                     ls=ls,lw=5,weights=[1/len(statTable)]*len(statTable))
        elif max(statTable) == 1:
            plt.hist(statTable,
                     bins=np.arange(min(statTable),max(statTable)+2,1),histtype='step',
                     label=path+saveFile+'\n'+r' $(\mu = %.2f$'%moments['mean'] + r', $\sigma = %.2f)$'%moments['std'],ls=ls,lw=5,weights=[1/len(statTable)]*len(statTable))
        else:
            plt.hist(statTable,
                     bins=np.arange(min(statTable),max(statTable)+1,1),histtype='step',
                     label=path+saveFile+'\n'+r' $(\mu = %.2f$'%moments['mean'] + r', $\sigma = %.2f)$'%moments['std'],ls=ls,lw=5,weights=[1/len(statTable)]*len(statTable))
    except ValueError:
         plt.hist(statTable,
                 bins=np.arange(min(statTable),max(statTable)+5,5),histtype='step',
                 label=path+saveFile+'\n'+r' $(\mu = %.3f$'%moments['mean'] + r', $\sigma = %.2f)$'%moments['std'],ls=ls,lw=5,weights=[1/len(statTable)]*len(statTable))
    plt.tight_layout()
    plt.legend()
#     plt.savefig(path + saveFile + '/results/playerStats/' + Name + '.png')
#     plt.show()

def getGameStats(path,saveFile,stat,plot=False,second=False,path2=None,saveFile2=None):
    db = readSave(path,saveFile)
    gameCSV = db['gameCSV']
    winMoments, gameCSV = getGameWins(db)

    try:
        mean = np.mean(gameCSV[stat])
        std = np.std(gameCSV[stat])
    except TypeError:
        return('%s is not a numeric statistic'%stat)

    moments = {'mean':mean, 'std':std}

    if second == True:
        if path2 == None or saveFile2 == None:
            raise Exception('You must enter both a path2 and saveFile2')
        db2 = readSave(path2,saveFile2)
        gameCSV2 = db2['gameCSV']
        winMoments2, gameCSV2 = getGameWins(db2)
        try:
            mean2 = np.mean(gameCSV2[stat])
            std2 = np.std(gameCSV2[stat])
        except TypeError:
            return('%s is not a numeric statistic'%stat)

        moments2 = {'mean':mean2, 'std':std2}

    if plot == True:
        try:
            dataPlt = plt.figure(figsize=(12,6),facecolor='w')
            plt.title(stat)
            statsGraph(gameCSV,moments,stat,path,saveFile,winMom=winMoments)
            if second == True:
                statsGraph(gameCSV2,moments2,stat,path2,saveFile2,ls='--',winMom=winMoments2)
        except TypeError:
            print('Cannot plot %s'%stat)

#     if stat == 'PDiff':
#         print('SAVE FILES:')
#         print(saveFile)
#         # print(winMoments)
#         if second == True:
#             print(saveFile2)
#             # print(winMoments2)
# #     return moments

def getPlayerStats(path,saveFile,Name,stat,Team,plot=True,second=False,path2=None,saveFile2=None):
    db = readSave(path,saveFile)
    sep = ' '
    FirstName = Name.split(' ')[0]
    LastName = sep.join(Name.split(' ')[1:])
#     print(LastName)
    player = db['playerCSV'][(db['playerCSV']['FirstName'] == FirstName)
                             & (db['playerCSV']['LastName'] == LastName)
                             & (db['playerCSV']['Team'] == Team)]
    PlayerStats = db['pgsCSV'][db['pgsCSV']['PlayerID'] == player['PlayerID']]
    statList = statDic.get(player['Position'].data[0])

    try:
        mean = np.mean(PlayerStats[stat])
        std = np.std(PlayerStats[stat])
    except TypeError:
        return('%s is not a numeric statistic'%stat)

    moments = {'mean':mean, 'std':std}

    if second == True:
        if path2 == None or saveFile2 == None:
            raise Exception('You must enter both a path2 and saveFile2')
        db2 = readSave(path2,saveFile2)
        player2 = db2['playerCSV'][(db2['playerCSV']['FirstName'] == FirstName)
                                 & (db2['playerCSV']['LastName'] == LastName)
                                 & (db2['playerCSV']['Team'] == Team)]
        PlayerStats2 = db2['pgsCSV'][db2['pgsCSV']['PlayerID'] == player2['PlayerID']]

        try:
            mean2 = np.mean(PlayerStats2[stat])
            std2 = np.std(PlayerStats2[stat])
        except TypeError:
            return('%s is not a numeric statistic'%stat)

        moments2 = {'mean':mean2, 'std':std2}

    if plot == True:
        try:
            dataPlt = plt.figure(figsize=(12,6),facecolor='w')
            plt.title(Name + ' - ' + stat)
            statsGraph(PlayerStats,moments,stat,path,saveFile)
            if second == True:
                statsGraph(PlayerStats2,moments2,stat,path2,saveFile2,ls='--')
        except TypeError:
            print('Cannot plot %s'%stat)

    if plot == False:
#         return moments
        return PlayerStats[statList]
