from random import randint
import logging
import pandas as pd

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




def get_teams(team,other_team):
    #get the two teams to simulate the game
    #need to have a form or something that is submitted with the team names
    rosters = get_rosters()

    team1 = rosters[rosters['Team'] == team]
    team2 = rosters[rosters['Team'] == other_team]

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
    

def simulate_nba_game(team, other_team):

    team1,team2 = get_teams(team,other_team)
    team1_defense, team2_defense =  get_teams_defense(team,other_team)

    team1, team1score = get_team_stats(team1, team2_defense)
    team2, team2score = get_team_stats(team2, team1_defense)


    return (team1, team1score, team2, team2score)
    


def get_team_stats(team, other_team_defense):

    #Team is a list
    # Create a DataFrame from the list


    columns_to_sum=['Three_rtg','Two_rtg','Free_throw_rtg','Pass_rtg','draw_foul_rtg','stamina','usageRate','rebound_rtg','steal_rtg','block_rtg']
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

    
    
    #total_defense = team['steal_rtg'].sum() + team['block_rtg'].sum() + team['rebound_rtg'].sum()
    #for( player in otherTeam.teamplayers)
    #    otherTeamDefense += player.defrtg
    
    #defenseMultiplier = total_defense/(len(team))/100

    fg_multiplier = other_team_defense['FG_DEF']   # calculated_fg + (fg_multiplier)*(FGA)
    ft_multiplier = other_team_defense['FT_DEF']   # calculated_ft + (ft_multiplier)*(FTA)


    for q in range(0,2):
        for i in range(0,5):

            stamina = team['stamina'][i]/100
            minutes1 = int(randint(15,20)*stamina)
            minutes2 = 20 - minutes1
            
            team_stats[i].minutesPlayed += minutes1
            team_stats[9-i].minutesPlayed += minutes2
            
            #Assists
            assists_1 = (randint(0,5) * ((team['make_ast_prob'][i]+team['Pass_rtg'][i])/200) * (minutes1/20))
            team_stats[i].assists += int(assists_1)

            assists_2 = (randint(0,4) * ((team['make_ast_prob'][9-i]+team['Pass_rtg'][9-i])/200) * (minutes1/20))
            team_stats[9-i].assists += int(assists_2)

            #Rebounds
            #75 is 6'3, to add bonus for height
            rebounds_1 = (randint(0,5) * ((team['rebound_rtg'][i])/100) * (1+(team['Height'][i] - 72)/50))
            team_stats[i].rebounds += int(rebounds_1)
            
            rebounds_2 = (randint(0,5) * ((team['rebound_rtg'][9-i])/100) * (1+(team['Height'][9-i] - 72)/50))
            team_stats[9-i].rebounds += int(rebounds_2)

            #Turnovers
            to_1 = (randint(0,5) * (minutes1/40) * (1-((50 - team['turnover_prob'][i])/100)))
            team_stats[i].turnovers += int(to_1)

            to_2 = (randint(0,5) * (minutes2/40) * (1-((50 - team['turnover_prob'][9-i])/100)))
            team_stats[9-i].turnovers += int(to_2)

            #Free Throws
            #Average free throw attempts for ncaa team: 18.9


            randintFreeThrows1 = (randint(0,8) * ((team['draw_foul_rtg'][i])/100) * (minutes1/20))
            randintFreeThrows1 = randintFreeThrows1 + (randintFreeThrows1 * ft_multiplier)
            team_stats[i].freeThrowsTaken += int(randintFreeThrows1)

            randintFreeThrows2 = (randint(0,8) * ((team['draw_foul_rtg'][9-i])/100) * (minutes1/20))
            randintFreeThrows2 = randintFreeThrows2 + (randintFreeThrows2 * ft_multiplier)
            team_stats[9-i].freeThrowsTaken += int(randintFreeThrows2)


            free_rating_adjusted = team['Free_throw_rtg'][i] + randint(-10,10)
            if(free_rating_adjusted > 100):
                free_rating_adjusted = 100
            if(free_rating_adjusted < 0):
                free_rating_adjusted = 0
            
            freeThrowsMade1 = (randintFreeThrows1 * (free_rating_adjusted/100))
            team_stats[i].freeThrowsMade += int(freeThrowsMade1)

            freeThrowsMade2 = (randintFreeThrows2 * ((team['Free_throw_rtg'][9-i])/100))
            team_stats[9-i].freeThrowsMade += int(freeThrowsMade2)


            #Field Goals
            #Starters
            #Average field goals for ncaa team: 58.4


            fieldGoalsTaken1 = (randint(2,20) * ((team['usageRate'][i])/100) * (minutes1/20))
            fieldGoalsTaken1 = fieldGoalsTaken1 + (fieldGoalsTaken1 * fg_multiplier)
            team_stats[i].fieldGoalsTaken += int(fieldGoalsTaken1)

            #Bench
            fieldGoalsTaken2 = (randint(2,20) * ((team['usageRate'][9-i])/100) * (minutes2/20))
            fieldGoalsTaken2 = fieldGoalsTaken2 + (fieldGoalsTaken2 * fg_multiplier)
            team_stats[9-i].fieldGoalsTaken += int(fieldGoalsTaken2)

            
            #Three Point Field Goals
            #rand_threes = randint(0,int(fieldGoalsTaken1))

            rand_threes1 = (team['take_three_prob'][i]/100) * (fieldGoalsTaken1) * (1/randint(2,3))
            threeGoalsTaken1 = int(rand_threes1)
            team_stats[i].threeGoalsTaken += threeGoalsTaken1


            rand_threes2 = (team['take_three_prob'][9-i]/100) * (fieldGoalsTaken2) * (1/randint(2,3))
            threeGoalsTaken2 = int(rand_threes2)
            team_stats[9-i].threeGoalsTaken += threeGoalsTaken2

        
            threeGoalsMade1 = int((threeGoalsTaken1) * ((team['Three_rtg'][i])/100))
            
            if(threeGoalsMade1 > threeGoalsTaken1):
                threeGoalsMade1 = threeGoalsTaken1
            
            team_stats[i].threeGoalsMade += int(threeGoalsMade1)

            
            threeGoalsMade2 = int((threeGoalsTaken2) * ((team['Three_rtg'][9-i])/100))
            if(threeGoalsMade2 > threeGoalsTaken2):
                threeGoalsMade2 = threeGoalsTaken2
            
            team_stats[9-i].threeGoalsMade += int(threeGoalsMade2)

            #2 Point Field Goals And Total Points
            twoPointTaken1 = int(fieldGoalsTaken1 - threeGoalsTaken1)
            twoPointMade1 = (twoPointTaken1) * ((team['Two_rtg'][i])/100)
            if(twoPointMade1 > twoPointTaken1):
                twoPointMade1 = int(twoPointTaken1)
            

            team_stats[i].fieldGoalsMade += int(twoPointMade1 + threeGoalsMade1)

            team_stats[i].points += int((3*int(threeGoalsMade1)) + (2*int(twoPointMade1)) + int(freeThrowsMade1) )



            twoPointTaken2 =  int(fieldGoalsTaken2 - threeGoalsTaken2)
            twoPointMade2 = (twoPointTaken2) * ((team['Two_rtg'][9-i])/100)
            if(twoPointMade2 > twoPointTaken2):
                twoPointMade2 = int(twoPointTaken2)
            

            team_stats[9-i].fieldGoalsMade += int(twoPointMade2 + threeGoalsMade2)

    
            team_stats[9-i].points += int((3*int(threeGoalsMade2)) + (2*int(twoPointMade2)) + int(freeThrowsMade2))

            teammatePoints = int((3*int(threeGoalsMade1)) + (2*int(twoPointMade1)) + int(freeThrowsMade1) + (3*int(threeGoalsMade2)) + (2*int(twoPointMade2)) + int(freeThrowsMade2))
            if(q==0):
                teamscore.quarter1 += teammatePoints
            if(q == 1):
                teamscore.quarter2 += teammatePoints
            if(q==2):
                teamscore.quarter3 += teammatePoints
            if(q == 3):
                teamscore.quarter4 += teammatePoints
            



            #Defense
            #Steals
            steals1 = (randint(0,10) * (minutes1/40) * ((team['steal_rtg'][i] /100)))
            team_stats[i].steals += int(steals1)

            steals2 = (randint(0,10) * (minutes2/40) * ((team['steal_rtg'][9-i]/100)))
            team_stats[9-i].steals += int(steals2)

            #Blocks
            blocks1 = (randint(0,10) * (minutes1/40) * ((team['block_rtg'][i]/100)))
            team_stats[i].blocks += int(blocks1)

            blocks2 = (randint(0,10) * (minutes2/40) * ((team['block_rtg'][9-i])/100))
            team_stats[9-i].blocks += int(blocks2)

    
    teamscore.total = teamscore.quarter1 + teamscore.quarter2 + teamscore.quarter3 + teamscore.quarter4 + teamscore.overtime

        

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