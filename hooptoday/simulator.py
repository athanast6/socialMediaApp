from random import randint
import logging
import pandas as pd
import numpy as np

from .utils import *



class Player:
    def __init__(self):
        self.name = ""
        self.assists = 0
        self.blocks = 0
        self.fieldGoalsMade = 0
        self.fieldGoalsTaken = 0
        self.freeThrowsMade = 0
        self.freeThrowsTaken = 0
        self.minutesPlayed = 0
        self.points = 0
        self.rebounds = 0
        self.steals = 0
        self.threeGoalsMade = 0
        self.threeGoalsTaken = 0
        self.turnovers = 0
        self.energy = 99

class TeamScore:
    def __init__(self):
        self.quarter1 = 0
        self.quarter2 = 0
        self.quarter3 = 0
        self.quarter4 = 0
        self.overtime = 0
        self.total = 0


rng = np.random.default_rng()




def get_teams(team,other_team):
    #get the two teams to simulate the game
    #need to have a form or something that is submitted with the team names
    predicted_stats = get_predicted_stats()

    team1 = predicted_stats[predicted_stats['Team'] == team]
    team2 = predicted_stats[predicted_stats['Team'] == other_team]

    #team1.sortby(x=> x.totalstats)
    #team2.sortby(x=> x.totalstats)

    #take 10 of  team

    return team1, team2


def get_teams_defense(team,other_team):
    #get the two teams to simulate the game
    #need to have a form or something that is submitted with the team names
    defense_ratings = get_defense_ratings()

    team1_defense = defense_ratings[defense_ratings['Key'] == team]
    team2_defense = defense_ratings[defense_ratings['Key'] == other_team]

    #team1.sortby(x=> x.totalstats)
    #team2.sortby(x=> x.totalstats)

    #take 10 of  team

    return team1_defense, team2_defense
    

def simulate_ncaa_game(team, other_team):

    team1,team2 = get_teams(team,other_team)
    team1_defense, team2_defense =  get_teams_defense(team,other_team)

    team1, team1score = get_team_stats(team1, team2_defense)
    team2, team2score = get_team_stats(team2, team1_defense)


    return (team1, team1score, team2, team2score)
    


def get_team_stats(team, other_team_defense):

    #Team is a list
    # Create a DataFrame from the list


    columns_to_sum=['Games','Minutes','Points','Rebounds','Assists','BlockedShots','Steals']
    # Calculate the sum of selected columns for each player
    totalStats = team[columns_to_sum].sum(axis=1)
    team['TotalStats'] = totalStats

    # Sort the DataFrame by the total stats in descending order
    team = team.sort_values(by='TotalStats', ascending=False)

    team.index = range(len(team))

    team.reset_index(drop=True, inplace=True)



    # Create a list of players and initialize their attributes
    team_stats = [Player() for _ in range(10)]

    # Set attributes for each player
    index=int(0)
    for player in team_stats:
        player.name = team.loc[index,'Name']
        player.assists = 0
        player.blocks = 0
        player.fieldGoalsMade = 0
        player.fieldGoalsTaken = 0
        player.freeThrowsMade = 0
        player.freeThrowsTaken = 0
        player.minutesPlayed = 0
        player.points = 0
        player.rebounds = 0
        player.steals = 0
        player.threeGoalsMade = 0
        player.threeGoalsTaken = 0
        player.turnovers = 0
        player.energy = 99
        index+=1

    teamscore = TeamScore()
    
    minutes1 = 0
    minutes2 = 0


    def_fg_multiplier = other_team_defense['FG_DEF']   # good defense (houston) = -0.47
    def_ft_multiplier = other_team_defense['FT_DEF']   # bad defense (detroit mercy) = 0.1



    #DIVIDE THESE VALUES BY TEAM AVERAGES FOR 2PA, 3PA and FTA
    #THEN MULTIPLY BY THE OTHER DEFENSIVE MULTIPLIERS
    off_2fg_pg = team['2FGAPG'].sum()
    off_3fg_pg = team['3FGAPG'].sum()
    off_ft_pg = team['FTAPG'].sum()

    two_multiplier = (off_2fg_pg/36.738) * def_fg_multiplier + 0.25
    three_multiplier = (off_3fg_pg/21.934) * def_fg_multiplier + 0.25
    ft_multiplier = (off_ft_pg/21.934) * def_ft_multiplier + 0.25


    print(two_multiplier)
    print(three_multiplier)
    print(ft_multiplier)
    


    for i in range(0,5):

        #stamina = team['stamina'][i]/100
        mpg_std = 2
        minutes1 = min(int(rng.normal(team['MPG'][i],mpg_std)),40)
        #minutes1 = int(randint(15,20)*stamina)
        minutes2 = 40 - minutes1
        
        team_stats[i].minutesPlayed += minutes1
        team_stats[9-i].minutesPlayed += minutes2
        
        #Assists
        #assists_1 = (randint(0,5) * ((team['make_ast_prob'][i]+team['Pass_rtg'][i])/200) * (minutes1/20))
        apg_std = 1
        assists_1 = rng.normal(team['APG'][i],apg_std)
        team_stats[i].assists += max(0,int(assists_1))

        
        assists_2 = rng.normal(team['APG'][9-i],apg_std)
        team_stats[9-i].assists += max(0,int(assists_2))

        #Rebounds
        #75 is 6'3, to add bonus for height
        #rebounds_1 = (randint(0,5) * ((team['rebound_rtg'][i])/100) * (1+(team['Height'][i] - 72)/50))
        rpg_std = 1
        rebounds_1 = rng.normal(team['RPG'][i],rpg_std)
        team_stats[i].rebounds += max(0,int(rebounds_1))
        
        #rebounds_2 = (randint(0,5) * ((team['rebound_rtg'][9-i])/100) * (1+(team['Height'][9-i] - 72)/50))
        rebounds_2 = rng.normal(team['RPG'][9-i],rpg_std)
        team_stats[9-i].rebounds += max(0,int(rebounds_2))

        #Turnovers
        #to_1 = (randint(0,5) * (minutes1/40) * (1-((50 - team['turnover_prob'][i])/100)))
        to_1 = rng.normal(team['TOPG'][i],1)
        team_stats[i].turnovers += max(0,int(to_1))

        #to_2 = (randint(0,5) * (minutes2/40) * (1-((50 - team['turnover_prob'][9-i])/100)))
        to_2 = rng.normal(team['TOPG'][i],1)
        team_stats[9-i].turnovers += max(0,int(to_2))




        #Free Throws
        #Average free throw attempts for ncaa team: 18.9


        #randintFreeThrows1 = (randint(0,8) * ((team['draw_foul_rtg'][i])/100) * (minutes1/20))
        randintFreeThrows1 = rng.normal(team['FTAPG'][i],1)
        randintFreeThrows1 = int(randintFreeThrows1 + (randintFreeThrows1 * ft_multiplier))

        if(randintFreeThrows1<0):
            randintFreeThrows1=0
        team_stats[i].freeThrowsTaken += randintFreeThrows1

        #randintFreeThrows2 = (randint(0,8) * ((team['draw_foul_rtg'][9-i])/100) * (minutes1/20))
        randintFreeThrows2 = rng.normal(team['FTAPG'][9-i],1)
        randintFreeThrows2 = int(randintFreeThrows2 + (randintFreeThrows2 * ft_multiplier))

        if(randintFreeThrows2<0):
            randintFreeThrows2=0

        team_stats[9-i].freeThrowsTaken += randintFreeThrows2


        free_rating_adjusted = team['FreeThrowsPercentage'][i] + randint(-10,10)
        if(free_rating_adjusted > 100):
            free_rating_adjusted = 100
        if(free_rating_adjusted < 0):
            free_rating_adjusted = 0
        
        freeThrowsMade1 = (randintFreeThrows1 * (free_rating_adjusted/100))
        team_stats[i].freeThrowsMade += int(freeThrowsMade1)

        freeThrowsMade2 = (randintFreeThrows2 * ((team['FreeThrowsPercentage'][9-i])/100))
        team_stats[9-i].freeThrowsMade += int(freeThrowsMade2)


        #Field Goals
        #Starters
        #Average field goals taken for ncaa team: 58.4

        twoPointTaken1 = rng.normal(team['2FGAPG'][i],2)
        twoPointTaken1 = int(twoPointTaken1 + (twoPointTaken1 * two_multiplier))
        twoPointTaken1 = max(0,twoPointTaken1)
        twoPointMade1 = int(twoPointTaken1 * ((team['TwoPointersPercentage'][i])/100))
        if(twoPointMade1>twoPointTaken1):
            twoPointMade1=twoPointTaken1
        

        #Bench
        twoPointTaken2 = rng.normal(team['2FGAPG'][9-i],1)
        twoPointTaken2 = int(twoPointTaken2 + (twoPointTaken2 * two_multiplier))
        twoPointTaken2 = max(0,int(twoPointTaken2))
        twoPointMade2 = int(twoPointTaken2 * ((team['TwoPointersPercentage'][9-i])/100))
        if(twoPointMade2>twoPointTaken2):
            twoPointMade2=twoPointTaken2
        



        #Three Point Field Goals
        threeGoalsTaken1 = rng.normal(team['3FGAPG'][i],2)
        team_stats[i].threeGoalsTaken +=  max(0,int(threeGoalsTaken1 + (threeGoalsTaken1 * three_multiplier)))
        threeGoalsMade1 = int(threeGoalsTaken1 * ((team['ThreePointersPercentage'][i])/100))
        team_stats[i].threeGoalsMade +=  max(0,threeGoalsMade1)


        threeGoalsTaken2 = rng.normal(team['3FGAPG'][9-i],1)
        team_stats[9-i].threeGoalsTaken +=  max(0,int(threeGoalsTaken2 + (threeGoalsTaken2 * three_multiplier)))
        threeGoalsMade2 = int(threeGoalsTaken2 * ((team['ThreePointersPercentage'][9-i])/100))
        team_stats[9-i].threeGoalsMade +=  max(0,threeGoalsMade2)

        



        team_stats[i].fieldGoalsMade += int(twoPointMade1 + threeGoalsMade1)
        team_stats[i].fieldGoalsTaken += max(0,int(twoPointTaken1) + int(threeGoalsTaken1))
        team_stats[i].points += int((3*int(threeGoalsMade1)) + (2*int(twoPointMade1)) + int(freeThrowsMade1) )


        team_stats[9-i].fieldGoalsMade += int(twoPointMade2 + threeGoalsMade2)
        team_stats[9-i].fieldGoalsTaken += max(0,int(twoPointTaken2) + int(threeGoalsTaken2))
        team_stats[9-i].points += int((3*int(threeGoalsMade2)) + (2*int(twoPointMade2)) + int(freeThrowsMade2))






        teammatePoints = int((3*int(threeGoalsMade1)) + (2*int(twoPointMade1)) + int(freeThrowsMade1) + (3*int(threeGoalsMade2)) + (2*int(twoPointMade2)) + int(freeThrowsMade2))
        teamscore.total += teammatePoints
        



        #Defense
        #Steals
        steals1 = rng.normal(team['SPG'][i],1)
        team_stats[i].steals +=  max(0,int(steals1))

        steals2 = rng.normal(team['SPG'][9-i],1)
        team_stats[9-i].steals +=  max(0,int(steals2))

        #Blocks
        blocks1 = rng.normal(team['BPG'][i],1)
        team_stats[i].blocks +=  max(0,int(blocks1))

        blocks2 = rng.normal(team['BPG'][9-i],1)
        team_stats[9-i].blocks +=  max(0,int(blocks2))

        

        

    return team_stats, teamscore



def simulate_x_games(team, other_team, num_games):

    team1_forsim,team2_forsim = get_teams(team,other_team)

    team1_defense, team2_defense =  get_teams_defense(team,other_team)

    team1_wins = 0
    team2_wins = 0
    overtimes = 0

    team1_points = 0
    team2_points = 0

    for x in range(0,num_games):

        

        team1, team1score = get_team_stats(team1_forsim, team2_defense)
        team2, team2score = get_team_stats(team2_forsim, team1_defense)

        team1_points += team1score.total
        team2_points += team2score.total

        if(team1score.total > team2score.total):
            team1_wins += 1
        elif(team2score.total > team1score.total):
            team2_wins += 1
        else:
            overtimes +=1

    return(team1_wins, team2_wins, overtimes, team1_points, team2_points)