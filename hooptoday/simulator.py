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

    team1 = rosters[rosters['team'] == team]
    team2 = rosters[rosters['team'] == other_team]

    #team1.sortby(x=> x.totalstats)
    #team2.sortby(x=> x.totalstats)

    #take 10 of  team

    return team1, team2
    

def simulate_nba_game(team, other_team):

    team1,team2 = get_teams(team,other_team)

    team1, team1score = get_team_stats(team1)
    team2, team2score = get_team_stats(team2)

    print(team1score)
    print(team2score)

    return (team1, team1score, team2, team2score)
    


def get_team_stats(team):

    


    columns_to_sum=['Three_rtg','Two_rtg','Free_throw_rtg','Pass_rtg','draw_foul_rtg','stamina','usageRate','rebound_rtg','steal_rtg','block_rtg','make_ast_prob']
    # Calculate the sum of selected columns for each player
    team['TotalStats'] = team[columns_to_sum].sum(axis=1)

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

    
    
    total_defense = team['steal_rtg'].sum() + team['block_rtg'].sum() + team['rebound_rtg'].sum()
    #for( player in otherTeam.teamplayers)
    #    otherTeamDefense += player.defrtg
    
    defenseMultiplier = total_defense/(len(team))/100


    for q in range(0,4):
        for i in range(0,5):

            start_usg = team['usageRate'][i]
            if(start_usg < 75):
                minutes1 = randint(6,9)
            else:
                minutes1 = int(start_usg/10)+randint(-1,0)
            minutes2 = 12 - minutes1
            
            team_stats[i].minutesPlayed += minutes1
            team_stats[i+5].minutesPlayed += minutes2
            
            #Assists
            assists_1 = (randint(0,20) * (minutes1/40) * ((team['make_ast_prob'][i]+team['Pass_rtg'][i])/200))
            team_stats[i].assists += int(assists_1)

            assists_2 = (randint(0,20) * (minutes2/40) * ((team['make_ast_prob'][i+5]+team['Pass_rtg'][i+5])/200))
            team_stats[i+5].assists += int(assists_2)

            #Rebounds
            #75 is 6'3, to add bonus for height
            rebounds_1 = (randint(0,20) * (minutes1/40) * ((team['rebound_rtg'][i])/100) * (1+(team['height'][i] - 72)/50))
            team_stats[i].rebounds += int(rebounds_1)
            
            rebounds_2 = (randint(0,20) * (minutes2/40) * ((team['rebound_rtg'][i+5])/100) * (1+(team['height'][i+5] - 72)/50))
            team_stats[i+5].rebounds += int(rebounds_2)

            #Turnovers
            to_1 = (randint(0,15) * (minutes1/40) * (1-((50 - team['turnover_prob'][i])/100)))
            team_stats[i].turnovers += int(to_1)

            to_2 = (randint(0,15) * (minutes2/40) * (1-((50 - team['turnover_prob'][i+5])/100)))
            team_stats[i+5].turnovers += int(to_2)

            #Free Throws
            randintFreeThrows1 = (randint(0,15) * (minutes1/40) * ((team['usageRate'][i] + 50)/100))
            team_stats[i].freeThrowsTaken += int(randintFreeThrows1)

            randintFreeThrows2 = (randint(0,15) * (minutes2/40) * ((team['usageRate'][i+5] + 50)/100))
            team_stats[i+5].freeThrowsTaken += int(randintFreeThrows2)


            free_rating_adjusted = team['Free_throw_rtg'][i] + randint(-10,10)
            if(free_rating_adjusted > 100):
                free_rating_adjusted = 100
            if(free_rating_adjusted < 0):
                free_rating_adjusted = 0
            
            freeThrowsMade1 = (randintFreeThrows1 * (free_rating_adjusted/100))
            team_stats[i].freeThrowsMade += int(freeThrowsMade1)

            freeThrowsMade2 = (randintFreeThrows2 * ((team['Free_throw_rtg'][i+5])/100))
            team_stats[i+5].freeThrowsMade += int(freeThrowsMade2)


            #Field Goals
            #Starters
            fieldGoalsTaken1 = (randint(10,33) * (minutes1/40) * ((team['usageRate'][i])/100))
            team_stats[i].fieldGoalsTaken += int(fieldGoalsTaken1)

            #Bench
            fieldGoalsTaken2 = (randint(10,33) * (minutes2/40) * ((team['usageRate'][i+5])/100))
            team_stats[i+5].fieldGoalsTaken += int(fieldGoalsTaken2)

            
            #Three Point Field Goals
            #rand_threes = randint(0,int(fieldGoalsTaken1))

            rand_threes = (team['take_three_prob'][i]/100) * (fieldGoalsTaken1) * (1/randint(1,3))
            threeGoalsTaken1 = int(rand_threes)
            team_stats[i].threeGoalsTaken += threeGoalsTaken1


            rand_threes = (team['take_three_prob'][i+5]/100) * (fieldGoalsTaken2) * (1/randint(1,3))
            threeGoalsTaken2 = int(rand_threes)
            team_stats[i+5].threeGoalsTaken += threeGoalsTaken2

        
            threeGoalsMade1 = ((randint(0,int(threeGoalsTaken1))) * ((team['Three_rtg'][i])/100) * (defenseMultiplier))
            
            if(threeGoalsMade1 > threeGoalsTaken1):
                threeGoalsMade1 = threeGoalsTaken1
            
            team_stats[i].threeGoalsMade += int(threeGoalsMade1)

            
            threeGoalsMade2 = ((randint(0,int(team_stats[i+5].threeGoalsTaken))) * ((team['Three_rtg'][i+5])/100) * defenseMultiplier)
            if(threeGoalsMade2 > threeGoalsTaken2):
                threeGoalsMade2 = threeGoalsTaken2
            
            team_stats[i+5].threeGoalsMade += int(threeGoalsMade2)

            #2 Point Field Goals And Total Points
            twoPointTaken1 = int(fieldGoalsTaken1 - threeGoalsTaken1)
            twoPointMade1 = ((randint(0,twoPointTaken1)) * ((team['Two_rtg'][i])/100) * defenseMultiplier)
            if(twoPointMade1 > twoPointTaken1):
                twoPointMade1 = int(twoPointTaken1)
            

            team_stats[i].fieldGoalsMade += int(twoPointMade1 + threeGoalsMade1)

            team_stats[i].points += int((3*threeGoalsMade1) + (2*twoPointMade1) + freeThrowsMade1)



            twoPointTaken2 =  int(fieldGoalsTaken2 - threeGoalsTaken2)
            twoPointMade2 = ((randint(0,twoPointTaken2)) * ((team['Two_rtg'][i+5])/100) * defenseMultiplier )
            if(twoPointMade2 > twoPointTaken2):
                twoPointMade2 = int(twoPointTaken2)
            

            team_stats[i+5].fieldGoalsMade += int(twoPointMade2 + threeGoalsMade2)

    
            team_stats[i+5].points += int((3*threeGoalsMade2) + (2*twoPointMade2) + freeThrowsMade2)

            teammatePoints = int((3*threeGoalsMade1) + (2*twoPointMade1) + freeThrowsMade1 + (3*threeGoalsMade2) + (2*twoPointMade2) + freeThrowsMade2)
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

            steals2 = (randint(0,10) * (minutes2/40) * ((team['steal_rtg'][i+5]/100)))
            team_stats[i+5].steals += int(steals2)

            #Blocks
            blocks1 = (randint(0,10) * (minutes1/40) * ((team['block_rtg'][i]/100)))
            team_stats[i].blocks += int(blocks1)

            blocks2 = (randint(0,10) * (minutes2/40) * ((team['block_rtg'][i+5])/100))
            team_stats[i+5].blocks += int(blocks2)

    
    teamscore.total = teamscore.quarter1 + teamscore.quarter2 + teamscore.quarter3 + teamscore.quarter4 + teamscore.overtime

        

    return team_stats, teamscore
    