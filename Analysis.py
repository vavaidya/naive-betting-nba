import pandas as pd
import numpy as np

line = pd.read_csv("nba_betting_money_line.csv")
spread = pd.read_csv("nba_betting_spread.csv")
games = pd.read_csv("nba_games_all.csv")

line_spread = line.merge(spread,left_on=['game_id', 'book_id'], right_on = ['game_id', 'book_id'],suffixes =['_line','_spread'])
line_spread.drop(['book_name_spread','team_id_spread','a_team_id_spread'],inplace=True,axis=1)
line_spread.rename(columns={'book_name_line':'book_name','team_id_line':'team1','a_team_id_line':'team2'}, inplace=True)

line_spread_games1 = games.merge(line_spread,left_on=['game_id','team_id'],right_on=['game_id','team1'])
line_spread_games2 = games.merge(line_spread,left_on=['game_id','team_id'],right_on=['game_id','team2'])

# BASE DATA AT game_id, book_name , team_id level
line_spread_games = pd.concat([line_spread_games1,line_spread_games2])
line_spread_games['team_num'] = np.where(line_spread_games['team_id'] == line_spread_games['team1'],1,2)

#Creating fav_returns_line column. For every bet of $100 on favourite we win this amount
line_spread_games['fav_wager_line'] = np.where(line_spread_games['price1_line']<line_spread_games['price2_line'],line_spread_games['price1_line'],line_spread_games['price2_line'])
line_spread_games['fav_returns_line'] = np.where(line_spread_games['fav_wager_line']<0,10000.0/abs(line_spread_games['fav_wager_line']),line_spread_games['fav_wager_line'])

#Creating dogs_returns_line column. For every bet of $100 on inderdog we win this amount
line_spread_games['dogs_wager_line'] = np.where(line_spread_games['price1_line']<line_spread_games['price2_line'],line_spread_games['price2_line'],line_spread_games['price1_line'])
line_spread_games['dogs_returns_line'] = np.where(line_spread_games['dogs_wager_line']<0,10000.0/abs(line_spread_games['dogs_wager_line']),line_spread_games['dogs_wager_line'])

#Creating fav_returns_spread_points column. For every bet of $100 on favourite we win this amount
line_spread_games['fav_wager_spread_points'] = np.where(line_spread_games['spread1']<line_spread_games['spread2'],line_spread_games['price1_spread'],line_spread_games['price2_spread'])
line_spread_games['fav_returns_spread_points'] = np.where(line_spread_games['fav_wager_spread_points']<0,10000.0/abs(line_spread_games['fav_wager_spread_points']),line_spread_games['fav_wager_spread_points'])

#Creating dogs_returns_spread_points column. For every bet of $100 on inderdog we win this amount
line_spread_games['dogs_wager_spread_points'] = np.where(line_spread_games['spread1']<line_spread_games['spread2'],line_spread_games['price2_spread'],line_spread_games['price1_spread'])
line_spread_games['dogs_returns_spread_points'] = np.where(line_spread_games['dogs_wager_spread_points']<0,10000.0/abs(line_spread_games['dogs_wager_spread_points']),line_spread_games['dogs_wager_spread_points'])

#Creating fav_returns_spread_points column. For every bet of $100 on favourite we win this amount
line_spread_games['fav_wager_spread_price'] = np.where(line_spread_games['price1_spread']<line_spread_games['price2_spread'],line_spread_games['price1_spread'],line_spread_games['price2_spread'])
line_spread_games['fav_returns_spread_price'] = np.where(line_spread_games['fav_wager_spread_price']<0,10000.0/abs(line_spread_games['fav_wager_spread_price']),line_spread_games['fav_wager_spread_price'])

#Creating dogs_returns_spread_points column. For every bet of $100 on inderdog we win this amount
line_spread_games['dogs_wager_spread_price'] = np.where(line_spread_games['price1_spread']<line_spread_games['price2_spread'],line_spread_games['price2_spread'],line_spread_games['price1_spread'])
line_spread_games['dogs_returns_spread_price'] = np.where(line_spread_games['dogs_wager_spread_price']<0,10000.0/abs(line_spread_games['dogs_wager_spread_price']),line_spread_games['dogs_wager_spread_price'])


#Keeping home = t
#Dropping unwanted columns

line_spread_games_v2 = line_spread_games[line_spread_games['is_home'] == 't']
drop_cols = ['w', 'l', 'min', 'fgm', 'fga', 'fg_pct', 'fg3m','fg3a',
             'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb','reb', 'ast',
             'stl', 'blk', 'tov', 'pf','fav_wager_line','dogs_wager_line',
             'fav_wager_spread_price','dogs_wager_spread_price','fav_wager_spread_points',
             'dogs_wager_spread_points']
line_spread_games_v2.drop(drop_cols,inplace=True,axis=1)
line_spread_games_v2.rename(columns={'pts':'pts_home','w_pct':'w_pct_home'}, inplace=True)

#Getting points for away team - will help in spread betting
line_spread_games_v2 = line_spread_games_v2.merge(games[['game_id','team_id','pts']].drop_duplicates(),left_on=['game_id','a_team_id'],right_on=['game_id','team_id'])
line_spread_games_v2.drop(['team_id_y'],inplace=True,axis=1)
line_spread_games_v2.rename(columns={'pts':'pts_away','team_id_x':'team_id'}, inplace=True)

#Getting w_pct for away team - will help in w_pct bettings
line_spread_games_v2 = line_spread_games_v2.merge(games[['game_id','team_id','w_pct']].drop_duplicates(),left_on=['game_id','a_team_id'],right_on=['game_id','team_id'])
line_spread_games_v2.drop(['team_id_y'],inplace=True,axis=1)
line_spread_games_v2.rename(columns={'w_pct':'w_pct_away','team_id_x':'team_id'}, inplace=True)

#Creating column for whether favs win - 1:YES 0:NO
line_spread_games_v2['fav_line_wins?'] = np.where(((line_spread_games_v2['price2_line']<line_spread_games_v2['price1_line'])&(line_spread_games_v2['wl']=='W')) | ((line_spread_games_v2['price2_line']>line_spread_games_v2['price1_line'])&(line_spread_games_v2['wl']=='L')),1,0)

#Creating column for whether favs win on points spread- 1:YES 0:NO
line_spread_games_v2['fav_spread_points_wins?'] = np.where( (line_spread_games_v2['spread2'] < line_spread_games_v2['spread1'])&( (line_spread_games_v2['pts_home'] - line_spread_games_v2['pts_away']) > abs(line_spread_games_v2['spread2']) ) |
                                 (line_spread_games_v2['spread1'] < line_spread_games_v2['spread2'])&( (line_spread_games_v2['pts_away'] - line_spread_games_v2['pts_home']) > abs(line_spread_games_v2['spread1']) ),
                                 1,
                                 0)

#Creating column for whether favs win on points price - 1:YES 0:NO
line_spread_games_v2['fav_spread_price_wins?'] = np.where( ((line_spread_games_v2['price2_spread'] < line_spread_games_v2['price1_spread'])&
                                        (line_spread_games_v2['spread2'] < 0)&
                                        ((line_spread_games_v2['pts_home'] - line_spread_games_v2['pts_away']) > abs(line_spread_games_v2['spread2']))) |

                                        ((line_spread_games_v2['price2_spread'] < line_spread_games_v2['price1_spread'])&
                                        (line_spread_games_v2['spread2'] > 0)&
                                        ( ((line_spread_games_v2['pts_away'] - line_spread_games_v2['pts_home']) < line_spread_games_v2['spread2']) | (line_spread_games_v2['pts_home'] > line_spread_games_v2['pts_away']) )) |

                                        ((line_spread_games_v2['price1_spread'] < line_spread_games_v2['price2_spread'])&
                                        (line_spread_games_v2['spread1'] < 0)&
                                        ((line_spread_games_v2['pts_away'] - line_spread_games_v2['pts_home']) > abs(line_spread_games_v2['spread1']))) |

                                        ((line_spread_games_v2['price1_spread'] < line_spread_games_v2['price2_spread'])&
                                        (line_spread_games_v2['spread1'] > 0)&
                                        ( ((line_spread_games_v2['pts_home'] - line_spread_games_v2['pts_away']) < line_spread_games_v2['spread1']) | (line_spread_games_v2['pts_away'] > line_spread_games_v2['pts_home']) )),
                                        1,
                                        0)

#Can filter this by book to get intended df's
line_spread_games_Pinnacle = line_spread_games_v2[line_spread_games_v2['book_name']=='Pinnacle Sports']
line_spread_games_5Dimes = line_spread_games_v2[line_spread_games_v2['book_name']=='5Dimes']
line_spread_games_Bookmaker = line_spread_games_v2[line_spread_games_v2['book_name']=='Bookmaker']
line_spread_games_BetOnline = line_spread_games_v2[line_spread_games_v2['book_name']=='BetOnline']
line_spread_games_Bovada = line_spread_games_v2[line_spread_games_v2['book_name']=='Bovada']
line_spread_games_Intertops = line_spread_games_v2[line_spread_games_v2['book_name']=='Intertops']
line_spread_games_JustBet = line_spread_games_v2[line_spread_games_v2['book_name']=='JustBet']
line_spread_games_Sportsbetting = line_spread_games_v2[line_spread_games_v2['book_name']=='Sportsbetting']
line_spread_games_Heritage = line_spread_games_v2[line_spread_games_v2['book_name']=='Heritage']
line_spread_games_YouWager = line_spread_games_v2[line_spread_games_v2['book_name']=='YouWager']


### BETTING FOR WIN PCT HIGH ALWAYS ###
### STARTS HERE #####
line_spread_games_v3 = line_spread_games_v2.copy()

line_spread_games_v3.dropna(subset=['w_pct_home','w_pct_away'],inplace=True)
line_spread_games_v3.drop(line_spread_games_v3[line_spread_games_v3['w_pct_home']==line_spread_games_v3['w_pct_away']].index,inplace=True)


line_spread_games_v3['bet_home?'] = np.where(line_spread_games_v3['w_pct_home']>line_spread_games_v3['w_pct_away'],1,0)

line_spread_games_v3['home_fav_line?'] = np.where(line_spread_games_v3['price2_line']<line_spread_games_v3['price1_line'],1,0)

line_spread_games_v3['home_fav_spread?'] = np.where(line_spread_games_v3['spread2']<line_spread_games_v3['spread1'],1,0)

line_spread_games_v3['home_fav_spread_price?'] = np.where(line_spread_games_v3['price2_spread']<line_spread_games_v3['price1_spread'],1,0)

### LINE BETTINGS ON WPCT ###
conditions_line = [(line_spread_games_v3['bet_home?']==0) & (line_spread_games_v3['home_fav_line?']==0) & (line_spread_games_v3['fav_line_wins?']==1),
              (line_spread_games_v3['bet_home?']==0) & (line_spread_games_v3['home_fav_line?']==1) & (line_spread_games_v3['fav_line_wins?']==0),
              (line_spread_games_v3['bet_home?']==1) & (line_spread_games_v3['home_fav_line?']==0) & (line_spread_games_v3['fav_line_wins?']==0),
              (line_spread_games_v3['bet_home?']==1) & (line_spread_games_v3['home_fav_line?']==1) & (line_spread_games_v3['fav_line_wins?']==1),]

choices_line = [1,1,1,1]
line_spread_games_v3['Win_line_bet?'] = np.select(conditions_line,choices_line,default = 0)

conditions_line_earnings = [(line_spread_games_v3['Win_line_bet?']==1)&(line_spread_games_v3['fav_line_wins?']==1),
                            (line_spread_games_v3['Win_line_bet?']==1)&(line_spread_games_v3['fav_line_wins?']==0),
                            (line_spread_games_v3['Win_line_bet?']==0)]

choice_line_earnings = [line_spread_games_v3['fav_returns_line'],line_spread_games_v3['dogs_returns_line'],-100]

line_spread_games_v3['wpct_line_winnings'] = np.select(conditions_line_earnings,choice_line_earnings)


### SPREAD POINT BETTINGS ON WPCT ###
conditions_spread = [(line_spread_games_v3['bet_home?']==0) & (line_spread_games_v3['home_fav_spread?']==0) & (line_spread_games_v3['fav_spread_points_wins?']==1),
              (line_spread_games_v3['bet_home?']==0) & (line_spread_games_v3['home_fav_spread?']==1) & (line_spread_games_v3['fav_spread_points_wins?']==0),
              (line_spread_games_v3['bet_home?']==1) & (line_spread_games_v3['home_fav_spread?']==0) & (line_spread_games_v3['fav_spread_points_wins?']==0),
              (line_spread_games_v3['bet_home?']==1) & (line_spread_games_v3['home_fav_spread?']==1) & (line_spread_games_v3['fav_spread_points_wins?']==1),]

choices_spread = [1,1,1,1]
line_spread_games_v3['Win_spread_pt_bet?'] = np.select(conditions_spread,choices_spread,default = 0)

conditions_spread_pt_earnings = [(line_spread_games_v3['Win_spread_pt_bet?']==1)&(line_spread_games_v3['fav_spread_points_wins?']==1),
                            (line_spread_games_v3['Win_spread_pt_bet?']==1)&(line_spread_games_v3['fav_spread_points_wins?']==0),
                            (line_spread_games_v3['Win_spread_pt_bet?']==0)]

choice_spread_pt_earnings = [line_spread_games_v3['fav_returns_spread_points'],line_spread_games_v3['dogs_returns_spread_points'],-100]

line_spread_games_v3['wpct_spread_pt_winnings'] = np.select(conditions_spread_pt_earnings,choice_spread_pt_earnings)


### SPREAD PRICE BETTINGS ON WPCT ###
conditions_spread_prc = [(line_spread_games_v3['bet_home?']==0) & (line_spread_games_v3['home_fav_spread_price?']==0) & (line_spread_games_v3['fav_spread_price_wins?']==1),
              (line_spread_games_v3['bet_home?']==0) & (line_spread_games_v3['home_fav_spread_price?']==1) & (line_spread_games_v3['fav_spread_price_wins?']==0),
              (line_spread_games_v3['bet_home?']==1) & (line_spread_games_v3['home_fav_spread_price?']==0) & (line_spread_games_v3['fav_spread_price_wins?']==0),
              (line_spread_games_v3['bet_home?']==1) & (line_spread_games_v3['home_fav_spread_price?']==1) & (line_spread_games_v3['fav_spread_price_wins?']==1),]

choices_spread_prc = [1,1,1,1]
line_spread_games_v3['Win_spread_prc_bet?'] = np.select(conditions_spread_prc,choices_spread_prc,default = 0)

conditions_spread_prc_earnings = [(line_spread_games_v3['Win_spread_prc_bet?']==1)&(line_spread_games_v3['fav_spread_price_wins?']==1),
                            (line_spread_games_v3['Win_spread_prc_bet?']==1)&(line_spread_games_v3['fav_spread_price_wins?']==0),
                            (line_spread_games_v3['Win_spread_prc_bet?']==0)]

choice_spread_prc_earnings = [line_spread_games_v3['fav_returns_spread_price'],line_spread_games_v3['dogs_returns_spread_price'],-100]

line_spread_games_v3['wpct_spread_prc_winnings'] = np.select(conditions_spread_prc_earnings,choice_spread_prc_earnings)

####### CALCULATING CUMULATIVE METRICS FOR EACH BOOK
books = ['Pinnacle Sports','5Dimes','Bookmaker','BetOnline','Bovada','Intertops','JustBet','Sportsbetting','Heritage','YouWager']


## book:bookname, games:total games, games_won:total games won, w12: 12 year winnings, exp:Expected Value, ci:Capital Investment, wp:Win Percentage
out_lines = pd.DataFrame(columns=['book','games','games_won_l','w12','exp','ci','wp'])

for bookie in books:
    df = line_spread_games_v3[line_spread_games_v3['book_name'] == bookie]
    fields = [bookie,len(df),len(df[df['Win_line_bet?']==1]),df['wpct_line_winnings'].sum(),df['wpct_line_winnings'].sum()/len(df),len(df)*100,len(df[df['Win_line_bet?']==1])*1.0/(len(df))]
    out_lines.loc[len(out_lines)] = fields


out_spread = pd.DataFrame(columns=['book','games','games_won_spread','w12','exp','ci','wp'])

for bookie in books:
    df = line_spread_games_v3[line_spread_games_v3['book_name'] == bookie]
    fields = [bookie,len(df),len(df[df['Win_spread_pt_bet?']==1]),df['wpct_spread_pt_winnings'].sum(),df['wpct_spread_pt_winnings'].sum()/len(df),len(df)*100,len(df[df['Win_spread_pt_bet?']==1])*1.0/(len(df))]
    out_spread.loc[len(out_spread)] = fields


out_spread_prc = pd.DataFrame(columns=['book','games','games_won_spread_points','w12','exp','ci','wp'])

for bookie in books:
    df = line_spread_games_v3[line_spread_games_v3['book_name'] == bookie]
    fields = [bookie,len(df),len(df[df['Win_spread_prc_bet?']==1]),df['wpct_spread_prc_winnings'].sum(),df['wpct_spread_prc_winnings'].sum()/len(df),len(df)*100,len(df[df['Win_spread_prc_bet?']==1])*1.0/(len(df))]
    out_spread_prc.loc[len(out_spread_prc)] = fields

######### PLOTS FOR EACH BOOKIE

import datetime
import matplotlib.pyplot as plt

line_spread_games_v4 = line_spread_games_v3.copy()

line_spread_games_v4 = line_spread_games_v4[['game_date','book_name','wpct_line_winnings']]

line_spread_games_v4  = line_spread_games_v4.groupby(['game_date','book_name'], as_index=False)['wpct_line_winnings'].sum()

books = ['Pinnacle Sports','5Dimes','Bookmaker','BetOnline','Bovada','Intertops','JustBet','Sportsbetting','Heritage','YouWager']

for bookie in books:
    print bookie
    df = line_spread_games_v4[line_spread_games_v4['book_name']==bookie]
    df['game_date'] = pd.to_datetime(df['game_date'])

    df = df.groupby(['game_date']).sum()
    df['cumulative sum'] = df.cumsum()

    totals = df['cumulative sum']
    #get 1 month and 3 month moving averages
    mavg_30 = totals.rolling(window=30, min_periods=10).mean()
    mavg_180 = totals.rolling(window=180, min_periods=10).mean()

    plt.plot(df['cumulative sum'], label = 'daily cumulative return')
    mavg_30.plot(label='30-day average')
    mavg_180.plot(label='180-day average')
    plt.ylabel('Cumulative Total Return ($)')
    plt.xlabel('Date')
    plt.title('Dollar Return for High win% Bets')
    plt.legend(loc='best')
    fig_str1 = 'home_spread_points_time_series_cumulative_return_' + bookie + '.png'
    # plt.savefig(fig_str1, dpi=300)
    plt.show()

    plt.plot(df['wpct_line_winnings'], label = 'daily return')
    plt.ylabel('Daily Return ($)')
    plt.xlabel('Date')
    plt.title('Dollar Return for High win% Bets')
    plt.legend(loc='best')
    fig_str2 = 'home_spread_points_time_series_daily_return_' + bookie + '.png'
    # plt.savefig(fig_str2, dpi=300)
    plt.show()

line_spread_games_v5 = line_spread_games_v3.copy()

line_spread_games_v5['bet_home?'] = 1

### LINE BETTINGS ON HOME ###
conditions_line = [(line_spread_games_v5['bet_home?']==1) & (line_spread_games_v5['home_fav_line?']==0) & (line_spread_games_v5['fav_line_wins?']==0),
                   (line_spread_games_v5['bet_home?']==1) & (line_spread_games_v5['home_fav_line?']==1) & (line_spread_games_v5['fav_line_wins?']==1),]

choices_line = [1,1]
line_spread_games_v5['Win_line_bet?'] = np.select(conditions_line,choices_line,default = 0)

conditions_line_earnings = [(line_spread_games_v5['Win_line_bet?']==1)&(line_spread_games_v5['fav_line_wins?']==1),
                            (line_spread_games_v5['Win_line_bet?']==1)&(line_spread_games_v5['fav_line_wins?']==0),
                            (line_spread_games_v5['Win_line_bet?']==0)]

choice_line_earnings = [line_spread_games_v5['fav_returns_line'],line_spread_games_v5['dogs_returns_line'],-100]

line_spread_games_v5['home_line_winnings'] = np.select(conditions_line_earnings,choice_line_earnings)


####### CALCULATING CUMULATIVE METRICS FOR EACH BOOK
books = ['Pinnacle Sports','5Dimes','Bookmaker','BetOnline','Bovada','Intertops','JustBet','Sportsbetting','Heritage','YouWager']


## book:bookname, games:total games, games_won:total games won, w12: 12 year winnings, exp:Expected Value, ci:Capital Investment, wp:Win Percentage
out_lines = pd.DataFrame(columns=['book','games','games_won_l','w12','exp','ci','wp'])

for bookie in books:
    df = line_spread_games_v5[line_spread_games_v5['book_name'] == bookie]
    fields = [bookie,len(df),len(df[df['Win_line_bet?']==1]),df['home_line_winnings'].sum(),df['home_line_winnings'].sum()/len(df),len(df)*100,len(df[df['Win_line_bet?']==1])*1.0/(len(df))]
    out_lines.loc[len(out_lines)] = fields




### SPREAD PRICE BETTINGS ON HOME ###
conditions_spread_prc = [(line_spread_games_v5['bet_home?']==1) & (line_spread_games_v5['home_fav_spread_price?']==0) & (line_spread_games_v5['fav_spread_price_wins?']==0),
              (line_spread_games_v5['bet_home?']==1) & (line_spread_games_v5['home_fav_spread_price?']==1) & (line_spread_games_v5['fav_spread_price_wins?']==1),]

choices_spread_prc = [1,1]
line_spread_games_v3['Win_spread_prc_bet?'] = np.select(conditions_spread_prc,choices_spread_prc,default = 0)

conditions_spread_prc_earnings = [(line_spread_games_v5['Win_spread_prc_bet?']==1)&(line_spread_games_v5['fav_spread_price_wins?']==1),
                            (line_spread_games_v5['Win_spread_prc_bet?']==1)&(line_spread_games_v5['fav_spread_price_wins?']==0),
                            (line_spread_games_v5['Win_spread_prc_bet?']==0)]

choice_spread_prc_earnings = [line_spread_games_v5['fav_returns_spread_price'],line_spread_games_v5['dogs_returns_spread_price'],-100]

line_spread_games_v5['home_spread_prc_winnings'] = np.select(conditions_spread_prc_earnings,choice_spread_prc_earnings)

####### CALCULATING CUMULATIVE METRICS FOR EACH BOOK
books = ['Pinnacle Sports','5Dimes','Bookmaker','BetOnline','Bovada','Intertops','JustBet','Sportsbetting','Heritage','YouWager']


## book:bookname, games:total games, games_won:total games won, w12: 12 year winnings, exp:Expected Value, ci:Capital Investment, wp:Win Percentage
out_spread_prc = pd.DataFrame(columns=['book','games','games_won_spread_points','w12','exp','ci','wp'])

for bookie in books:
    df = line_spread_games_v5[line_spread_games_v3['book_name'] == bookie]
    fields = [bookie,len(df),len(df[df['Win_spread_prc_bet?']==1]),df['home_spread_prc_winnings'].sum(),df['home_spread_prc_winnings'].sum()/len(df),len(df)*100,len(df[df['Win_spread_prc_bet?']==1])*1.0/(len(df))]
    out_spread_prc.loc[len(out_spread_prc)] = fields
