#!/usr/bin/env python -u
# -*- coding: utf-8 -*-
"""
Copyright 2013 Jacek Markowski, jacek87markowski@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sqlite3
from csv import reader
import os
import platform
import locale
locale.setlocale(locale.LC_ALL, "C")

system = platform.system()
if system == 'Windows':
    new_line = '\r\n'
    from pyfann_win import libfann
elif system == 'Linux':
    new_line = '\n'
    from pyfann import libfann
elif system == 'Darwin':
    new_line = '\r'
else:
    new_line = '\r\n'


class Database(object):
    ''' SQL base'''
    def __init__(self, parent=None):
        '''Creates all nessesary tables in sql'''
        self.mybase = sqlite3.connect(':memory:')
        self.relations_base = self.mybase.cursor()
        #This function creates sql database and tables#
        self.relations_base.execute('''CREATE TABLE results
        (id INTEGER PRIMARY KEY,
        date_txt txt,
        date_num FLOAT,
        home TEXT,
        away TEXT,
        gHomeEnd INTEGER,
        gAwayEnd INTEGER
        fake TEXT NOT NULL DEFAULT "-")''')
        self.relations_base.execute('''CREATE TABLE league
        (id INTEGER PRIMARY KEY,
        team TEXT,
        matches INTEGER DEFAULT 000.0,
        matchesHome INTEGER DEFAULT 000.0,
        matchesAway INTEGER DEFAULT 000.0,
        points INTEGER DEFAULT 0,
        pointsHome INTEGER DEFAULT 0,
        pointsAway INTEGER DEFAULT 0,
        form INTEGER DEFAULT 000.0,
        formHome INTEGER DEFAULT 000.0,
        formAway INTEGER DEFAULT 000.0,
        pointsBB FLOAT DEFAULT 0.000,
        pointsBBHome FLOAT DEFAULT 000.0,
        pointsBBAway FLOAT DEFAULT 000.0,
        formBB FLOAT DEFAULT 000.0,
        formBBHome FLOAT DEFAULT 000.0,
        formBBAway FLOAT DEFAULT 000.0,
        wins INTEGER DEFAULT 000.0,
        draws INTEGER DEFAULT 000.0,
        loses INTEGER DEFAULT 000.0,
        winhome INTEGER DEFAULT 000.0,
        drawhome INTEGER DEFAULT 000.0,
        losehome INTEGER DEFAULT 000.0,
        winaway INTEGER DEFAULT 000.0,
        drawaway INTEGER VARCHAR(2) NOT NULL DEFAULT 0,
        loseaway INTEGER VARCHAR(2) NOT NULL DEFAULT 0,
        goalsscored INTEGER NOT NULL DEFAULT 0,
        goalslost INTEGER NOT NULL DEFAULT 0,
        goalsscoredhome INTEGER NOT NULL DEFAULT 0,
        goalslosthome INTEGER NOT NULL DEFAULT 0,
        goalsscoredaway INTEGER NOT NULL DEFAULT 0,
        goalslostaway INTEGER NOT NULL DEFAULT 0,
        mowins FLOAT DEFAULT 0.0,
        moloses FLOAT DEFAULT 0.0,
        diffgwins FLOAT DEFAULT 0.0,
        diffgloses FLOAT DEFAULT 0.0,
        mowinsHome FLOAT DEFAULT 0.0,
        molosesHome FLOAT DEFAULT 0.0,
        diffgwinsHome FLOAT DEFAULT 0.0,
        diffglosesHome FLOAT DEFAULT 0.0,
        mowinsAway FLOAT DEFAULT 0.0,
        molosesAway FLOAT DEFAULT 0.0,
        diffgwinsAway FLOAT DEFAULT 0.0,
        diffglosesAway FLOAT DEFAULT 0.0,
        f1 INTEGER DEFAULT 000.0,
        f2 INTEGER DEFAULT 000.0,
        f3 INTEGER DEFAULT 000.0,
        f4 INTEGER DEFAULT 000.0,
        f1Home INTEGER DEFAULT 000.0,
        f2Home INTEGER DEFAULT 000.0,
        f1Away INTEGER DEFAULT 000.0,
        f2Away INTEGER DEFAULT 000.0,
        f1BB FLOAT DEFAULT 000.0,
        f2BB FLOAT DEFAULT 000.0,
        f3BB FLOAT DEFAULT 000.0,
        f4BB FLOAT DEFAULT 000.0,
        f1BBHome FLOAT DEFAULT 000.0,
        f2BBHome FLOAT DEFAULT 000.0,
        f1BBAway FLOAT DEFAULT 000.0,
        f2BBAway FLOAT DEFAULT 000.0,
        f1op TEXT,
        f2op TEXT,
        f3op TEXT,
        f4op TEXT,
        f1opHome TEXT,
        f2opHome TEXT,
        f1opAway TEXT,
        f2opAway TEXT,
        bts INTEGER DEFAULT 000.0,
        btsHome INTEGER DEFAULT 000.0,
        btsAway INTEGER DEFAULT 000.0,
        over25 INTEGER DEFAULT 000.0,
        over25Home INTEGER DEFAULT 000.0,
        over25Away INTEGER DEFAULT 000.0,
        under25 INTEGER DEFAULT 000.0,
        under25Home INTEGER DEFAULT 000.0,
        under25Away INTEGER DEFAULT 000.0,
        fake TEXT NOT NULL DEFAULT "-")''')
        self.relations_base.execute('''CREATE TABLE series
        (id INTEGER PRIMARY KEY,
        team TEXT,
        series_wins INTEGER NOT NULL DEFAULT 0,
        series_draws INTEGER NOT NULL DEFAULT 0,
        series_loses INTEGER NOT NULL DEFAULT 0,
        series_winshome INTEGER NOT NULL DEFAULT 0,
        series_drawshome INTEGER NOT NULL DEFAULT 0,
        series_loseshome INTEGER NOT NULL DEFAULT 0,
        series_winsaway INTEGER NOT NULL DEFAULT 0,
        series_drawsaway INTEGER NOT NULL DEFAULT 0,
        series_losesaway INTEGER NOT NULL DEFAULT 0,
        series_noloses INTEGER NOT NULL DEFAULT 0,
        series_noloseshome INTEGER NOT NULL DEFAULT 0,
        series_nolosesaway INTEGER NOT NULL DEFAULT 0,
        series_nowins INTEGER NOT NULL DEFAULT 0,
        series_nowinshome INTEGER NOT NULL DEFAULT 0,
        series_nowinsaway INTEGER NOT NULL DEFAULT 0,
        series_nodraws INTEGER NOT NULL DEFAULT 0,
        series_nodrawshome INTEGER NOT NULL DEFAULT 0,
        series_nodrawsaway INTEGER NOT NULL DEFAULT 0,
        series_bts INTEGER DEFAULT 000.0,
        series_btsHome INTEGER DEFAULT 000.0,
        series_btsAway INTEGER DEFAULT 000.0,
        series_over25 INTEGER DEFAULT 000.0,
        series_over25Home INTEGER DEFAULT 000.0,
        series_over25Away INTEGER DEFAULT 000.0,
        series_under25 INTEGER DEFAULT 000.0,
        series_under25Home INTEGER DEFAULT 000.0,
        series_under25Away INTEGER DEFAULT 000.0)''')
        self.relations_base.execute('''CREATE TABLE scaled
        (id INTEGER PRIMARY KEY,
        team TEXT,
        matches FLOAT DEFAULT 000.0,
        points FLOAT DEFAULT 000.0,
        pointsHome FLOAT DEFAULT 000.0,
        pointsAway FLOAT DEFAULT 000.0,
        pointsBB FLOAT DEFAULT 0.000,
        pointsBBHome FLOAT DEFAULT 000.0,
        pointsBBAway FLOAT DEFAULT 000.0,
        form FLOAT DEFAULT 000.0,
        formHome FLOAT DEFAULT 000.0,
        formAway FLOAT DEFAULT 000.0,
        formBB FLOAT DEFAULT 000.0,
        formBBHome FLOAT DEFAULT 000.0,
        formBBAway FLOAT DEFAULT 000.0,
        points_b FLOAT DEFAULT 000.0,
        pointsHome_b FLOAT DEFAULT 000.0,
        pointsAway_b FLOAT DEFAULT 000.0,
        pointsBB_b FLOAT DEFAULT 0.000,
        pointsBBHome_b FLOAT DEFAULT 000.0,
        pointsBBAway_b FLOAT DEFAULT 000.0,
        form_b FLOAT DEFAULT 000.0,
        formHome_b FLOAT DEFAULT 000.0,
        formAway_b FLOAT DEFAULT 000.0,
        formBB_b FLOAT DEFAULT 000.0,
        formBBHome_b FLOAT DEFAULT 000.0,
        formBBAway_b FLOAT DEFAULT 000.0,
        winhome FLOAT DEFAULT 000.0,
        drawhome FLOAT DEFAULT 000.0,
        losehome FLOAT DEFAULT 000.0,
        winaway FLOAT DEFAULT 000.0,
        drawaway FLOAT DEFAULT 000.0,
        loseaway FLOAT DEFAULT 000.0,
        winhome_b FLOAT DEFAULT 000.0,
        drawhome_b FLOAT DEFAULT 000.0,
        losehome_b FLOAT DEFAULT 000.0,
        winaway_b FLOAT DEFAULT 000.0,
        drawaway_b FLOAT DEFAULT 000.0,
        loseaway_b FLOAT DEFAULT 000.0,
        goalsscored FLOAT NOT NULL DEFAULT 0,
        goalslost FLOAT NOT NULL DEFAULT 0,
        goalsscoredhome FLOAT NOT NULL DEFAULT 0,
        goalslosthome FLOAT NOT NULL DEFAULT 0,
        goalsscoredaway FLOAT NOT NULL DEFAULT 0,
        goalslostaway FLOAT NOT NULL DEFAULT 0,
        goalsscored_b FLOAT NOT NULL DEFAULT 0,
        goalslost_b FLOAT NOT NULL DEFAULT 0,
        goalsscoredhome_b FLOAT NOT NULL DEFAULT 0,
        goalslosthome_b FLOAT NOT NULL DEFAULT 0,
        goalsscoredaway_b FLOAT NOT NULL DEFAULT 0,
        goalslostaway_b FLOAT NOT NULL DEFAULT 0,
        mowins FLOAT DEFAULT 0.0,
        moloses FLOAT DEFAULT 0.0,
        mowinsHome FLOAT DEFAULT 0.0,
        molosesHome FLOAT DEFAULT 0.0,
        mowinsAway FLOAT DEFAULT 0.0,
        molosesAway FLOAT DEFAULT 0.0,
        f1 FLOAT DEFAULT 000.0,
        f2 FLOAT DEFAULT 000.0,
        f3 FLOAT DEFAULT 000.0,
        f4 FLOAT DEFAULT 000.0,
        f1Home FLOAT DEFAULT 000.0,
        f2Home FLOAT DEFAULT 000.0,
        f1Away FLOAT DEFAULT 000.0,
        f2Away FLOAT DEFAULT 000.0,
        f1BB FLOAT DEFAULT 000.0,
        f2BB FLOAT DEFAULT 000.0,
        f3BB FLOAT DEFAULT 000.0,
        f4BB FLOAT DEFAULT 000.0,
        f1BBHome FLOAT DEFAULT 000.0,
        f2BBHome FLOAT DEFAULT 000.0,
        f1BBAway FLOAT DEFAULT 000.0,
        f2BBAway FLOAT DEFAULT 000.0,
        bts INTEGER DEFAULT 000.0,
        btsHome INTEGER DEFAULT 000.0,
        btsAway INTEGER DEFAULT 000.0,
        over25 INTEGER DEFAULT 000.0,
        over25Home INTEGER DEFAULT 000.0,
        over25Away INTEGER DEFAULT 000.0,
        under25 INTEGER DEFAULT 000.0,
        under25Home INTEGER DEFAULT 000.0,
        under25Away INTEGER DEFAULT 000.0,
        series_wins FLOAT DEFAULT 000.0,
        series_draws FLOAT DEFAULT 000.0,
        series_loses FLOAT DEFAULT 000.0,
        series_winshome FLOAT DEFAULT 000.0,
        series_drawshome FLOAT DEFAULT 000.0,
        series_loseshome FLOAT DEFAULT 000.0,
        series_winsaway FLOAT DEFAULT 000.0,
        series_drawsaway FLOAT DEFAULT 000.0,
        series_losesaway FLOAT DEFAULT 000.0,
        series_noloses FLOAT DEFAULT 000.0,
        series_noloseshome FLOAT DEFAULT 000.0,
        series_nolosesaway FLOAT DEFAULT 000.0,
        series_nowins FLOAT DEFAULT 000.0,
        series_nowinshome FLOAT DEFAULT 000.0,
        series_nowinsaway FLOAT DEFAULT 000.0,
        series_nodraws FLOAT DEFAULT 000.0,
        series_nodrawshome FLOAT DEFAULT 000.0,
        series_nodrawsaway FLOAT DEFAULT 000.0,
        series_bts INTEGER DEFAULT 000.0,
        series_btsHome INTEGER DEFAULT 000.0,
        series_btsAway INTEGER DEFAULT 000.0,
        series_over25 INTEGER DEFAULT 000.0,
        series_over25Home INTEGER DEFAULT 000.0,
        series_over25Away INTEGER DEFAULT 000.0,
        series_under25 INTEGER DEFAULT 000.0,
        series_under25Home INTEGER DEFAULT 000.0,
        series_under25Away INTEGER DEFAULT 000.0,
        fake TEXT NOT NULL DEFAULT "-")''')
        self.relations_base.execute('''CREATE TABLE odds
        (id INTEGER PRIMARY KEY,
        name TETX,
        odd_home FLOAT DEFAULT 000.0,
        odd_draw FLOAT DEFAULT 000.0,
        odd_away FLOAT DEFAULT 000.0)''')
    def load_csv(self, folder, name, expt_name = None, r_min = 5,
                 r_max = 50, mode=0,net = None):
        '''mode:
        0-normal
        1-export
        2-simulation'''
        self.clear_tables()
        teams = self.return_teams(folder, name)
        for team in teams:
            item = team[0]
            self.relations_base.execute('''INSERT INTO league(team)
                                    VALUES(?)''', [(item)])
            self.relations_base.execute('''INSERT INTO series(team)
                                    VALUES(?)''', [(item)])
            self.relations_base.execute('''INSERT INTO scaled(team)
                                    VALUES(?)''', [(item)])
        self.relations_base.execute('''INSERT INTO odds(name,odd_home,odd_draw,odd_away)
                                    VALUES("odds",0.0,0.0,0.0)''')
        # Selecting all matches from database to process
        results = self.relations_base.execute('''SELECT
                                date_txt,
                                home,
                                away,
                                gHomeEnd,
                                gAwayEnd
                                FROM results WHERE NOT gHomeEnd='NULL'
                                ORDER BY date_num ASC
                                ''')
        results = results.fetchall()
        # Processing selected matches
        teams_num = len(teams)
        self.match_group = 0
        self.match_group_date = 0
        index = 0

        for i in results:
            day, home, away, fth, fta = i[:]
            rounds_m = self.relations_base.execute('''SELECT
            max(matches) FROM league''')
            rounds = rounds_m.fetchone()
            rounds = rounds[0]
            if mode == 1: # export
                if r_min <= rounds <= r_max:
                    index += 1
                    self.scale_group_check(day)
                    if self.match_group == 1:
                        self.scale_group(teams_num)
                        export_print_file = open(os.path.join('tmp','')+'print','w')
                        print '==== Scaling====', day
                        export_print_file.write('Process data :'+day+' Round %d'%rounds)
                        export_print_file.close()
                    self.export('tmp', home, away, rounds, fth, fta)
                    #self.line = '######write '+str(rounds)+day+home+away
                    #print '######write', rounds, day, home, away

            if mode == 2: # simulation
                if r_min <= rounds <= r_max:
                    self.scale_group_check(day)
                    if self.match_group == 1:
                        self.scale_group(teams_num)
                        #print '==== Scaling for: ', day
                    self.simulation_prediction(home, away, net,mode=0)
                    #print 'Prediction', day, home, away, fth, fta, self.prediction
                    self.simulation_filters(home, away)
                    ### used in simulation module
                    self.date = day
                    self.home = home
                    self.away = away
                    self.fth = fth
                    self.fta = fta
                    self.batch_print()
            self.process_csv(i)
        # final scale for predicting in stats window
        self.scale_group(teams_num)

    def batch_print(self):
        ''' Used in simulator app'''
        pass
    def export(self, expt_name, home, away, rounds, fth, fta):
        ''' Exports data for learning'''
        with open(os.path.join('tmp', '')+'export', 'a') as save:
            scaled_h = self.relations_base.execute('''SELECT
            matches,
            points,
            pointsHome,
            pointsBB,
            pointsBBHome,
            form,
            formHome,
            formBB,
            formBBHome,
            points_b,
            pointsHome_b,
            pointsBB_b,
            pointsBBHome_b,
            form_b,
            formHome_b,
            formBB_b,
            formBBHome_b,
            winhome,
            drawhome,
            losehome,
            winhome_b,
            drawhome_b,
            losehome_b,
            goalsscored,
            goalslost,
            goalsscoredhome,
            goalslosthome,
            goalsscored_b,
            goalslost_b,
            goalsscoredhome_b,
            goalslosthome_b,
            mowins,
            moloses,
            mowinsHome,
            molosesHome,
            f1,
            f2,
            f3,
            f4,
            f1Home,
            f2Home,
            f1BB,
            f2BB,
            f3BB,
            f4BB,
            f1BBHome,
            f2BBHome,
            bts,
            btsHome,
            over25,
            over25Home,
            under25,
            under25Home,
            series_wins,
            series_draws,
            series_loses,
            series_winshome,
            series_drawshome,
            series_loseshome,
            series_noloses,
            series_noloseshome,
            series_nowins,
            series_nowinshome,
            series_nodraws,
            series_nodrawshome,
            series_bts,
            series_btsHome,
            series_over25,
            series_over25Home,
            series_under25,
            series_under25Home
            FROM scaled
            WHERE team="%s"'''%home)
            scaled_h = scaled_h.fetchone()
            scaled_h = str(scaled_h[:])
            scaled_a = self.relations_base.execute('''SELECT
            matches,
            points,
            pointsAway,
            pointsBB,
            pointsBBAway,
            form,
            formAway,
            formBB,
            formBBAway,
            points_b,
            pointsAway_b,
            pointsBB_b,
            pointsBBAway_b,
            form_b,
            formAway_b,
            formBB_b,
            formBBAway_b,
            winaway,
            drawaway,
            loseaway,
            winaway_b,
            drawaway_b,
            loseaway_b,
            goalsscored,
            goalslost,
            goalsscoredaway,
            goalslostaway,
            goalsscored_b,
            goalslost_b,
            goalsscoredaway_b,
            goalslostaway_b,
            mowins,
            moloses,
            mowinsAway,
            molosesAway,
            f1,
            f2,
            f3,
            f4,
            f1Away,
            f2Away,
            f1BB,
            f2BB,
            f3BB,
            f4BB,
            f1BBAway,
            f2BBAway,
            bts,
            btsAway,
            over25,
            over25Away,
            under25,
            under25Away,
            series_wins,
            series_draws,
            series_loses,
            series_winsaway,
            series_drawsaway,
            series_losesaway,
            series_noloses,
            series_nolosesaway,
            series_nowins,
            series_nowinsaway,
            series_nodraws,
            series_nodrawsaway,
            series_bts,
            series_btsAway,
            series_over25,
            series_over25Away,
            series_under25,
            series_under25
            FROM scaled
            WHERE team="%s"'''%away)
            scaled_a = scaled_a.fetchone()
            scaled_a = str(scaled_a[:])

            prediction = self.simulation_prediction(home,away,'default',mode=1)
            prd_line = ','+str(prediction[0])+','+str(prediction[1])+','+str(prediction[2])
            line = scaled_h[1:-1]+','+scaled_a[1:-1]+prd_line+'\n'
            if fth > fta:  #win home
                #save.write(home+'-'+away+'\n')
                save.write(line)
                save.write('-1\n')
            if fth == fta:  #draw
                #save.write(home+'-'+away+'\n')
                save.write(line)
                save.write('0\n')
            if fth < fta:  #win away
                #save.write(home+'-'+away+'\n')
                save.write(line)
                save.write('1\n')
    def export_fix(self, expt_name):
        ''' Count lines,inputs and outputs and write in title'''
        print '=============fix'
        path = os.path.join('export','')
        tmp = reader(open(os.path.join('tmp','')+'export','r'))
        tmp = list(tmp)
        with open(path+expt_name,'w') as fix_file:
            inputs = str(len(tmp[0]))
            outputs = str(len(tmp[1]))
            sets = str(len(tmp)/2)
            title = sets+' ' +inputs+' '+outputs+'\n'
            fix_file.write(title)
            for i in tmp:
                line = str(i)
                line = line.replace('[','')
                line = line.replace(']','')
                line = line.replace(' ','')
                line = line.replace(',',' ')
                line = line.replace("'",'')
                fix_file.write(line+'\n')
            fix_file.close()
            fix_file = open(path+expt_name,'r').readline()
            print fix_file

    def scale_group_check(self, day):
        ''' Checks is scaling has been done for current round'''
        if day != self.match_group_date:
            self.match_group_date = day
            self.match_group = 1

    def scale_group(self, teams):
        '''Scales data only once a day before first match'''
        self.match_group = 0
        ############## scale variables
        max_matches = (teams-1)*2.0 # when each team plays 2 matches
                                  #(at home,at away)
        max_points = max_matches*3
        max_points_h = max_matches*1.5
        max_points_a = max_matches*1.5
        max_form = 12
        max_form_h = 6
        max_form_a = 6
        max_points_bb = max_matches*4
        max_points_bb_h = max_matches*2
        max_points_bb_a = max_matches*2
        max_form_bb = 16
        max_form_bb_h = 8
        max_form_bb_a = 8
        max_goals = max_matches * 3
        max_goals_ha = max_goals/2
        ############## in comparision to max to achieve in season
        self.scale('matches', 'matches', 0, max_matches)
        self.scale('points', 'points', 0, max_points)
        self.scale('pointsHome', 'pointsHome', 0, max_points_h)
        self.scale('pointsAway', 'pointsAway', 0, max_points_a)
        self.scale('pointsBB', 'pointsBB', 0, max_points_bb)
        self.scale('pointsBBHome', 'pointsBBHome', 0, max_points_bb_h)
        self.scale('pointsBBAway', 'pointsBBAway', 0, max_points_bb_a)
        self.scale('form', 'form', 0, max_form)
        self.scale('f1', 'f1', 0, 3)
        self.scale('f2', 'f2', 0, 3)
        self.scale('f3', 'f3', 0, 3)
        self.scale('f4', 'f4', 0, 3)
        self.scale('formHome', 'formHome', 0, max_form_h)
        self.scale('f1Home', 'f1Home', 0, 3)
        self.scale('f2Home', 'f2Home', 0, 3)
        self.scale('formAway', 'formAway', 0, max_form_a)
        self.scale('f1Away', 'f1Away', 0, 3)
        self.scale('f2Away', 'f2Away', 0, 3)
        self.scale('formBB', 'formBB', 0, max_form_bb)
        self.scale('f1BB', 'f1BB', 0, 4)
        self.scale('f2BB', 'f2BB', 0, 4)
        self.scale('f3BB', 'f3BB', 0, 4)
        self.scale('f4BB', 'f4BB', 0, 4)
        self.scale('formBBHome', 'formBBHome', 0, max_form_bb_h)
        self.scale('f1BBHome', 'f1BBHome', 0, 4)
        self.scale('f2BBHome', 'f2BBHome', 0, 4)
        self.scale('formBBAway', 'formBBAway', 0, max_form_bb_a)
        self.scale('f1BBAway', 'f1BBAway', 0, 4)
        self.scale('f2BBAway', 'f2BBAway', 0, 4)
        self.scale('goalsscored', 'goalsscored', 0, max_goals)
        self.scale('goalsscoredhome', 'goalsscoredhome', 0, max_goals_ha)
        self.scale('goalsscoredaway', 'goalsscoredaway', 0, max_goals_ha)
        self.scale('goalslost', 'goalslost', 0, max_goals)
        self.scale('goalslosthome', 'goalslosthome', 0, max_goals_ha)
        self.scale('goalslostaway', 'goalslostaway', 0, max_goals_ha)
        self.scale('bts', 'bts', 0, max_matches)
        self.scale('btsHome','btsHome', 0, max_matches/2)
        self.scale('btsAway','btsAway', 0, max_matches/2)
        self.scale('over25', 'over25', 0, max_matches)
        self.scale('over25Home','over25Home', 0, max_matches/2)
        self.scale('over25Away','over25Away', 0, max_matches/2)
        self.scale('under25', 'under25', 0, max_matches)
        self.scale('under25Home','under25Home', 0, max_matches/2)
        self.scale('under25Away','under25Away', 0, max_matches/2)
        ############## in comparision to others
        self.scale('winhome', 'winhome_b')
        self.scale('drawhome', 'drawhome_b')
        self.scale('losehome', 'losehome_b')
        self.scale('winaway', 'winaway_b')
        self.scale('drawaway', 'drawaway_b')
        self.scale('loseaway', 'loseaway_b')
        self.scale('points', 'points_b')
        self.scale('pointsHome', 'pointsHome_b')
        self.scale('pointsAway', 'pointsAway_b')
        self.scale('pointsBB', 'pointsBB_b')
        self.scale('pointsBBHome', 'pointsBBHome_b')
        self.scale('pointsBBAway', 'pointsBBAway_b')
        self.scale('form', 'form_b')
        self.scale('formHome', 'formHome_b')
        self.scale('formAway', 'formAway_b')
        self.scale('formBB', 'formBB_b')
        self.scale('formBBHome', 'formBBHome_b')
        self.scale('formBBAway', 'formBBAway_b')
        self.scale('goalsscored', 'goalsscored_b')
        self.scale('goalsscoredhome', 'goalsscoredhome_b')
        self.scale('goalsscoredaway', 'goalsscoredaway_b')
        self.scale('goalslost', 'goalslost_b')
        self.scale('goalslosthome', 'goalslosthome_b')
        self.scale('goalslostaway', 'goalslostaway_b')
        ############## mov,mol
        self.scale('mowins', 'mowins', 0, 3)
        self.scale('mowinsHome', 'mowinsHome', 0, 3)
        self.scale('mowinsAway', 'mowinsAway', 0, 3)
        self.scale('moloses', 'moloses', 0, 3)
        self.scale('molosesHome', 'molosesHome', 0, 3)
        self.scale('molosesAway', 'molosesAway', 0, 3)
        ################ series
        self.scale('series_wins', 'series_wins',
                   min_value=0, max_value=10, series=1)
        self.scale('series_draws', 'series_draws',
                   min_value=0, max_value=10, series=1)
        self.scale('series_loses', 'series_loses',
                   min_value=0, max_value=10, series=1)
        self.scale('series_winshome', 'series_winshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_drawshome', 'series_drawshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_loseshome', 'series_loseshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_winsaway', 'series_winsaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_drawsaway', 'series_drawsaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_losesaway', 'series_losesaway'
        , min_value=0, max_value=10, series=1)
        self.scale('series_noloses', 'series_noloses',
                   min_value=0, max_value=10, series=1)
        self.scale('series_noloseshome', 'series_noloseshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nolosesaway', 'series_nolosesaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nowins', 'series_nowins',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nowinshome', 'series_nowinshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nowinsaway', 'series_nowinsaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nodraws', 'series_nodraws',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nodrawshome', 'series_nodrawshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nodrawsaway', 'series_nodrawsaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_bts', 'series_bts',
                   min_value=0, max_value=10, series=1)
        self.scale('series_btsHome', 'series_btsHome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_btsAway', 'series_btsAway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_over25', 'series_over25',
                   min_value=0, max_value=10, series=1)
        self.scale('series_over25Home', 'series_over25Home',
                   min_value=0, max_value=10, series=1)
        self.scale('series_over25Away', 'series_over25Away',
                   min_value=0, max_value=10, series=1)
        self.scale('series_under25', 'series_under25',
                   min_value=0, max_value=10, series=1)
        self.scale('series_under25Home', 'series_under25Home',
                   min_value=0, max_value=10, series=1)
        self.scale('series_under25Away', 'series_under25Away',
                   min_value=0, max_value=10, series=1)



    def scale(self, record_in, record_out, min_value=None, max_value=None,
              series=0):
        ''' Scales data to range(-1,1), Need some tweaks to speed up'''
        if max_value == None:
            if series == 0:
                max_value = self.relations_base.execute('''SELECT max(%s)
                                               FROM league''' %record_in)
            else:
                max_value = self.relations_base.execute('''SELECT max(%s)
                                               FROM series''' %record_in)
            max_value, = max_value.fetchone()
        if min_value == None:
            if series == 0:
                min_value = self.relations_base.execute('''SELECT min(%s)
                                               FROM league''' %record_in)
            else:
                min_value = self.relations_base.execute('''SELECT min(%s)
                                               FROM series''' %record_in)
            min_value, = min_value.fetchone()

        if series == 0:
            teams = self.relations_base.execute('''SELECT %s,team
                                                FROM league''' %record_in)
        else:
            teams = self.relations_base.execute('''SELECT %s,team
                                                FROM series''' %record_in)
        teams = tuple(teams)
        try:
            for i in teams:
                scaled = 2.0*(i[0]-min_value)/(max_value-min_value)-1
                if scaled < -1:
                    scaled = -1
                elif scaled > 1:
                    scaled = 1
                self.relations_base.execute('''UPDATE scaled
                    SET %s=? WHERE team=? ''' %record_out, (scaled, i[1]))
        except:
            print 'Scale: error'

    def simulation_filters(self, home, away):
        ''' Loads into variables actual team stats to compare with filters'''
        # filters variables
        t1_stats = self.relations_base.execute('''SELECT points,pointsHome,
                form,formHome FROM league
                WHERE team="%s"'''%home)
        t1 = list(t1_stats)
        for i in t1:
            self.t1_points = i[0]
            self.t1_points_h = i[1]
            self.t1_form = i[2]
            self.t1_form_h = i[3]
        t1_series = self.relations_base.execute('''SELECT series_wins,
                series_winshome,series_draws,series_drawshome,series_loses,
                series_loseshome,series_nowins,series_nowinshome,
                series_nodraws,series_nodrawshome,series_noloses,
                series_noloseshome
                FROM series
                WHERE team="%s"'''%home)
        t1 = list(t1_series)
        for i in t1:
            self.t1_wins = i[0]
            self.t1_winshome = i[1]
            self.t1_draws = i[2]
            self.t1_drawshome = i[3]
            self.t1_loses = i[4]
            self.t1_loseshome = i[5]
            self.t1_nowins = i[6]
            self.t1_nowinshome = i[7]
            self.t1_nodraws = i[8]
            self.t1_nodrawshome = i[9]
            self.t1_noloses = i[10]
            self.t1_noloseshome = i[11]

        t2_stats = self.relations_base.execute('''SELECT points,pointsHome,
                form,formHome FROM league
                WHERE team="%s"'''%away)
        t2 = list(t2_stats)
        for i in t2:
            self.t2_points = i[0]
            self.t2_points_a = i[1]
            self.t2_form = i[2]
            self.t2_form_a = i[3]
        t2_series = self.relations_base.execute('''SELECT series_wins,
                series_winsaway,series_draws,series_drawsaway,
                series_loses,series_losesaway,series_nowins,
                series_nowinsaway,series_nodraws,series_nodrawsaway,
                series_noloses,series_nolosesaway
                FROM series
                WHERE team="%s"'''%away)
        t2 = list(t2_series)
        for i in t2:
            self.t2_wins = i[0]
            self.t2_winsaway = i[1]
            self.t2_draws = i[2]
            self.t2_drawsaway = i[3]
            self.t2_loses = i[4]
            self.t2_losesaway = i[5]
            self.t2_nowins = i[6]
            self.t2_nowinsaway = i[7]
            self.t2_nodraws = i[8]
            self.t2_nodrawsaway = i[9]
            self.t2_noloses = i[10]
            self.t2_nolosesaway = i[11]

        ####
        # Odds
        ####
        self.odds = self.simulation_prediction(home,away,'default',1)
        self.odd_1 = self.odds_rescale(self.odds[0])
        self.odd_x = self.odds_rescale(self.odds[1])
        self.odd_2 = self.odds_rescale(self.odds[2])
        self.odd_1x = 1/((1/self.odd_1) + (1/self.odd_x))
        self.odd_x2 = 1/((1/self.odd_x) + (1/self.odd_2))
#    def odds_rescale(self,val):
#        ''' Rescaling odds from [-1,1]'''
#        old_range = 2
#        new_range = 19
#        odd = (((val + 1) * new_range) / old_range) + 1
#        odd = round(odd,2)
#        if odd<1:
#            odd = 1
#        return odd
    def process_csv(self, results):
        '''Calculates points,form,series etc.'''
        date, team_home, team_away, goals_home, goals_away = results
        if goals_home > goals_away:
            winner = 1  #home team won
        if goals_home < goals_away:
            winner = 2  #away team won
        if goals_home == goals_away:
            winner = 0  # draw
        goal_diff = abs(goals_home - goals_away) # for margins of wins/loses
        #######
        #points BBrating variables
        #######
        max_ph = self.relations_base.execute('''SELECT max(pointsBBHome)
                                            FROM league''')
        max_ph, = max_ph.fetchone()

        max_pa = self.relations_base.execute('''SELECT max(pointsBBAway)
                                            FROM league''')
        max_pa, = max_pa.fetchone()

        max_f = self.relations_base.execute('''SELECT max(formBB)
                                                FROM league''')
        max_f, = max_f.fetchone()
        team_home_p = self.relations_base.execute('''SELECT pointsBBHome
                                    FROM league
                                    WHERE team="%s"'''%team_home)
        team_home_p = team_home_p.fetchone()
        team_home_p = team_home_p[0]
        team_away_p = self.relations_base.execute('''SELECT pointsBBAway
                                    FROM league
                                    WHERE team="%s"'''%team_away)
        team_away_p = team_away_p.fetchone()
        team_away_p = team_away_p[0]
        team_home_f = self.relations_base.execute('''SELECT formBB
                                    FROM league
                                    WHERE team="%s"'''%team_home)
        team_home_f = team_home_f.fetchone()
        team_home_f = team_home_f[0]
        team_away_f = self.relations_base.execute('''SELECT formBB
                                    FROM league
                                    WHERE team="%s"'''%team_away)
        team_away_f = team_away_f.fetchone()
        team_away_f = team_away_f[0]

        if winner == 1:
            if max_pa > 0:
                bb_rating_h = 3 + ((team_away_p/float(max_pa))+ (team_away_f/float(max_f)))/2
            else:
                bb_rating_h = 3
            if max_ph > 0:
                bb_rating_a = 0 + ((team_home_p/float(max_ph))+ (team_home_f/float(max_f)))/2
            else:
                bb_rating_a = 0
            points_h = 3
            points_a = 0
            form_h = 3
            form_a = 0

        #######
        #margin of wins,margin of loses variables
        #######
            self.relations_base.execute('''UPDATE league SET
            diffgwins=diffgwins+?,
            diffgwinsHome=diffgwinsHome+?
            WHERE team=?''',(goal_diff, goal_diff, team_home))
            self.relations_base.execute('''UPDATE league SET
            diffgloses=diffgloses+?,
            diffglosesAway=diffglosesAway+?
            WHERE team=?''',(goal_diff, goal_diff, team_away))
        #######
        # wine/lose/draw
        #######
            self.relations_base.execute('''UPDATE league SET
            winhome=winhome+1
            WHERE team=?  ''', [(team_home)])
            self.relations_base.execute('''UPDATE league SET
            loseaway=loseaway+1
            WHERE team=?  ''', [(team_away)])
        #######
        # series
        #######
            self.relations_base.execute('''UPDATE series SET
            series_wins=series_wins+1,
            series_winshome=series_winshome+1,
            series_draws=0,
            series_drawshome=0,
            series_loses=0,
            series_loseshome=0,
            series_noloses=series_noloses+1,
            series_noloseshome=series_noloseshome+1,
            series_nowins=0,
            series_nowinshome=0,
            series_nodraws=series_nodraws+1,
            series_nodrawshome=series_nodrawshome+1
            WHERE team=?  ''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_loses=series_loses+1,
            series_losesaway=series_losesaway+1,
            series_draws=0,
            series_drawsaway=0,
            series_wins=0,
            series_winsaway=0,
            series_noloses=0,
            series_nolosesaway=0,
            series_nowins=series_nowins+1,
            series_nowinsaway=series_nowinsaway+1,
            series_nodraws=series_nodraws+1,
            series_nodrawsaway=series_nodrawsaway+1
            WHERE team=?  ''', [(team_away)])

        if winner == 2:
            if max_pa > 0:
                bb_rating_h = 0 + ((team_away_p/float(max_pa))+ (team_away_f/float(max_f)))/2
            else:
                bb_rating_h = 0
            if max_ph > 0:
                bb_rating_a = 3 + ((team_home_p/float(max_ph))+ (team_home_f/float(max_f)))/2
            else:
                bb_rating_a = 3
            points_h = 0
            points_a = 3
            form_h = 0
            form_a = 3
        #######
        #margin of wins,margin of loses variables
        #######
            self.relations_base.execute('''UPDATE league SET
            diffgloses=diffgloses+?,
            diffglosesHome=diffglosesHome+?
            WHERE team=?''',(goal_diff, goal_diff, team_home))
            self.relations_base.execute('''UPDATE league SET
            diffgwins=diffgwins+?,
            diffgwinsAway=diffgwinsAway+?
            WHERE team=?''',(goal_diff, goal_diff, team_away))

        #######
        # wine/lose/draw
        #######
            self.relations_base.execute('''UPDATE league SET
            losehome=losehome+1
            WHERE team=?  ''', [(team_home)])
            self.relations_base.execute('''UPDATE league SET
            winaway=winaway+1
            WHERE team=?  ''', [(team_away)])
        #######
        # series
        #######
            self.relations_base.execute('''UPDATE series SET
            series_wins=0,
            series_winshome=0,
            series_draws=0,
            series_drawshome=0,
            series_loses=series_loses+1,
            series_loseshome=series_loseshome+1,
            series_noloses=0,
            series_noloseshome=0,
            series_nowins=series_nowins+1,
            series_nowinshome=series_nowinshome+1,
            series_nodraws=series_nodraws+1,
            series_nodrawshome=series_nodrawshome+1
            WHERE team=?  ''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_loses=0,
            series_losesaway=0,
            series_draws=0,
            series_drawsaway=0,
            series_wins=series_wins+1,
            series_winsaway=series_winsaway+1,
            series_noloses=series_noloses+1,
            series_nolosesaway=series_nolosesaway+1,
            series_nowins=0,
            series_nowinsaway=0,
            series_nodraws=series_nodraws+1,
            series_nodrawsaway=series_nodrawsaway+1
            WHERE team=?  ''', [(team_away)])
        if winner == 0:
            if max_pa > 0:
                bb_rating_h = 1 + ((team_away_p/float(max_pa))+ (team_away_f/float(max_f)))/2
            else:
                bb_rating_h = 1
            if max_ph > 0:
                bb_rating_a = 1 + ((team_home_p/float(max_ph))+ (team_home_f/float(max_f)))/2
            else:
                bb_rating_a = 1
            points_h = 1
            points_a = 1
            form_h = 1
            form_a = 1
        #######
        # wine/lose/draw
        #######
            self.relations_base.execute('''UPDATE league SET
            drawhome=drawhome+1
            WHERE team=?  ''', [(team_home)])
            self.relations_base.execute('''UPDATE league SET
            drawaway=drawaway+1
            WHERE team=?  ''', [(team_away)])
        #######
        # series
        #######
            self.relations_base.execute('''UPDATE series SET
            series_wins=0,
            series_winshome=0,
            series_draws=series_draws+1,
            series_drawshome=series_drawshome+1,
            series_loses=0,
            series_loseshome=0,
            series_noloses=series_noloses+1,
            series_noloseshome=series_noloseshome+1,
            series_nowins=series_nowins+1,
            series_nowinshome=series_nowinshome+1,
            series_nodraws=0,
            series_nodrawshome=0
            WHERE team=?  ''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_loses=0,
            series_losesaway=0,
            series_draws=series_draws+1,
            series_drawsaway=series_drawsaway+1,
            series_wins=0,
            series_winsaway=0,
            series_noloses=series_noloses+1,
            series_nolosesaway=series_nolosesaway+1,
            series_nowins=series_nowins+1,
            series_nowinsaway=series_nowinsaway+1,
            series_nodraws=0,
            series_nodrawsaway=0
            WHERE team=?  ''', [(team_away)])


    #######
    #points Classic
    #######
        self.relations_base.execute('''UPDATE league SET
        points=points+?,
        pointsHome=pointsHome+?
        WHERE team=?  ''', (points_h, points_h, team_home))
        self.relations_base.execute('''UPDATE league SET
        points=points+?,
        pointsAway=pointsAway+?
        WHERE team=?  ''', (points_a, points_a, team_away))
    #######
    #points BBrating
    #######
        self.relations_base.execute('''UPDATE league SET
        pointsBB=pointsBB+?,
        pointsBBHome=pointsBBHome+?
        WHERE team=?  ''', (bb_rating_h, bb_rating_h, team_home))
        self.relations_base.execute('''UPDATE league SET
        pointsBB=pointsBB+?,
        pointsBBAway=pointsBBAway+?
        WHERE team=?  ''', (bb_rating_a, bb_rating_a, team_away))
    #######
    #form BBrating
    #######
        self.relations_base.execute('''UPDATE league SET
        f4BB=f3BB,
        f3BB=f2BB,
        f2BB=f1BB,
        f1BB=?,
        f2BBHome=f1BBHome,
        f1BBHome=?
        WHERE team=?  ''', (bb_rating_h, bb_rating_h, team_home))
        self.relations_base.execute('''UPDATE league SET
        f4BB=f3BB,
        f3BB=f2BB,
        f2BB=f1BB,
        f1BB=?,
        f2BBAway=f1BBAway,
        f1BBAway=?
        WHERE team=?  ''', (bb_rating_a, bb_rating_a, team_away))

    #######
    #goals
    #######
        self.relations_base.execute('''UPDATE league SET
        goalsscoredhome=goalsscoredhome+?,
        goalslosthome=goalslosthome+?
        WHERE team=?''',(goals_home, goals_away, team_home))
        self.relations_base.execute('''UPDATE league SET
        goalsscoredaway=goalsscoredaway+?,
        goalslostaway=goalslostaway+?
        WHERE team=?''',(goals_away, goals_home, team_away))
    #######
    #form Classic
    #######
        self.relations_base.execute('''UPDATE league SET
        f4op=f3op,
        f3op=f2op,
        f2op=f1op,
        f1op=?,
        f4=f3,
        f3=f2,
        f2=f1,
        f1=?,
        f2opHome=f1opHome,
        f1opHome=?,
        f2Home=f1Home,
        f1Home=?
        WHERE team=?  ''', (team_away, form_h, team_away, form_h, team_home))
        self.relations_base.execute('''UPDATE league SET
        f4op=f3op,
        f3op=f2op,
        f2op=f1op,
        f1op=?,
        f4=f3,
        f3=f2,
        f2=f1,
        f1=?,
        f2opAway=f1opAway,
        f1opAway=?,
        f2Away=f1Away,
        f1Away=?
        WHERE team=?  ''', (team_home, form_a, team_home, form_a, team_away))

    ######
    #matches/form/goals sum
    ######
        self.relations_base.execute('''UPDATE league SET
        matches=winhome+drawhome+losehome+winaway+drawaway+loseaway,
        matchesHome=winhome+drawhome+losehome,
        matchesAway=winaway+drawaway+loseaway,
        form=f1+f2+f3+f4,
        formHome=f1Home+f2Home,
        formAway=f1Away+f2Away,
        formBB=f1BB+f2BB+f3BB+f4BB,
        formBBHome=f1BBHome+f2BBHome,
        formBBAway=f1BBAway+f2BBAway,
        goalsscored=goalsscoredHome+goalsscoredAway,
        goalslost=goalslostHome+goalslostAway''')
    ######
    #margin of winning,losing
    ######
        self.relations_base.execute('''UPDATE league SET
        mowins=diffgwins/matches,
        moloses=diffgloses/matches,
        mowinsHome=diffgwinsHome/matchesHome,
        molosesHome=diffglosesHome/matchesHome,
        mowinsAway=diffgwinsAway/matchesAway,
        molosesAway=diffglosesAway/matchesAway''')
        #####
        #BTS
        #####
        if goals_home > 0 and goals_away > 0:
            self.relations_base.execute('''UPDATE league SET
            bts=bts+1,
            btsHome=btsHome+1
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_bts=series_bts+1,
            series_btsHome=series_btsHome+1
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE league SET
            bts=bts+1,
            btsAway=btsAway+1
            WHERE team=?''', [(team_away)])
            self.relations_base.execute('''UPDATE series SET
            series_bts=series_bts+1,
            series_btsAway=series_btsAway+1
            WHERE team=?''', [(team_away)])
        else:
            self.relations_base.execute('''UPDATE series SET
            series_bts=0,
            series_btsHome=0
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_bts=0,
            series_btsAway=0
            WHERE team=?''', [(team_away)])
        #####
        #under/over 2.5
        #####
        if (goals_home+goals_away) > 2:
            self.relations_base.execute('''UPDATE league SET
            over25=over25+1,
            over25Home=over25Home+1
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_over25=series_over25+1,
            series_over25Home=series_over25Home+1
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE league SET
            over25=over25+1,
            over25Away=over25Away+1
            WHERE team=?''', [(team_away)])
            self.relations_base.execute('''UPDATE series SET
            series_over25=series_over25+1,
            series_over25Away=series_over25Away+1
            WHERE team=?''', [(team_away)])
            self.relations_base.execute('''UPDATE series SET
            series_under25=0,
            series_under25Home=0
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_under25=0,
            series_under25Away=0
            WHERE team=?''', [(team_away)])
        elif (goals_home+goals_away) < 3:
            self.relations_base.execute('''UPDATE league SET
            under25=under25+1,
            under25Home=under25Home+1
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE league SET
            under25=under25+1,
            under25Away=under25Away+1
            WHERE team=?''', [(team_away)])
            self.relations_base.execute('''UPDATE series SET
            series_under25=series_under25+1,
            series_under25Home=series_under25Home+1
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_under25=series_under25+1,
            series_under25Away=series_under25Away+1
            WHERE team=?''', [(team_away)])
            self.relations_base.execute('''UPDATE series SET
            series_over25=0,
            series_over25Home=0
            WHERE team=?''', [(team_home)])
            self.relations_base.execute('''UPDATE series SET
            series_over25=0,
            series_over25Away=0
            WHERE team=?''', [(team_away)])
    def clear_tables(self):
        '''Reamoves all data form tables for new file process '''

        try:
            self.relations_base.execute('''DELETE FROM league_stats
                                            WHERE id''')
        except:
            pass

        try:
            self.relations_base.execute('''DELETE FROM results WHERE id''')
        except:
            pass

        try:
            self.relations_base.execute('''DELETE FROM league WHERE id''')
        except:
            pass
        try:
            self.relations_base.execute('''DELETE FROM scaled WHERE id''')
        except:
            pass
    def simulation_prediction(self, home, away, net, mode=0):
        ''' Predict outcome form match using given net
        mode 0 predicting outcomes (1,x,2)
        mode 1 predictiong odds'''
        path_net = os.path.join('net','')
        path_odds = os.path.join('odds','')
        input_list = []
        t1 = self.relations_base.execute('''SELECT
            matches,
            points,
            pointsHome,
            pointsBB,
            pointsBBHome,
            form,
            formHome,
            formBB,
            formBBHome,
            points_b,
            pointsHome_b,
            pointsBB_b,
            pointsBBHome_b,
            form_b,
            formHome_b,
            formBB_b,
            formBBHome_b,
            winhome,
            drawhome,
            losehome,
            winhome_b,
            drawhome_b,
            losehome_b,
            goalsscored,
            goalslost,
            goalsscoredhome,
            goalslosthome,
            goalsscored_b,
            goalslost_b,
            goalsscoredhome_b,
            goalslosthome_b,
            mowins,
            moloses,
            mowinsHome,
            molosesHome,
            f1,
            f2,
            f3,
            f4,
            f1Home,
            f2Home,
            f1BB,
            f2BB,
            f3BB,
            f4BB,
            f1BBHome,
            f2BBHome,
            bts,
            btsHome,
            over25,
            over25Home,
            under25,
            under25Home,
            series_wins,
            series_draws,
            series_loses,
            series_winshome,
            series_drawshome,
            series_loseshome,
            series_noloses,
            series_noloseshome,
            series_nowins,
            series_nowinshome,
            series_nodraws,
            series_nodrawshome,
            series_bts,
            series_btsHome,
            series_over25,
            series_over25Home,
            series_under25,
            series_under25Home
            FROM scaled
            WHERE team="%s"'''%home)
        t1 = tuple(t1)
        for i in t1[0]:
            input_list.append(i)
        t2 = self.relations_base.execute('''SELECT
            matches,
            points,
            pointsAway,
            pointsBB,
            pointsBBAway,
            form,
            formAway,
            formBB,
            formBBAway,
            points_b,
            pointsAway_b,
            pointsBB_b,
            pointsBBAway_b,
            form_b,
            formAway_b,
            formBB_b,
            formBBAway_b,
            winaway,
            drawaway,
            loseaway,
            winaway_b,
            drawaway_b,
            loseaway_b,
            goalsscored,
            goalslost,
            goalsscoredaway,
            goalslostaway,
            goalsscored_b,
            goalslost_b,
            goalsscoredaway_b,
            goalslostaway_b,
            mowins,
            moloses,
            mowinsAway,
            molosesAway,
            f1,
            f2,
            f3,
            f4,
            f1Away,
            f2Away,
            f1BB,
            f2BB,
            f3BB,
            f4BB,
            f1BBAway,
            f2BBAway,
            bts,
            btsAway,
            over25,
            over25Away,
            under25,
            under25Away,
            series_wins,
            series_draws,
            series_loses,
            series_winsaway,
            series_drawsaway,
            series_losesaway,
            series_noloses,
            series_nolosesaway,
            series_nowins,
            series_nowinsaway,
            series_nodraws,
            series_nodrawsaway,
            series_bts,
            series_btsAway,
            series_over25,
            series_over25Away,
            series_under25,
            series_under25Away
            FROM scaled
            WHERE team="%s"'''%away)
        t2 = tuple(t2)
        for i in t2[0]:
            input_list.append(i)
        locale.setlocale(locale.LC_ALL, "C")
        ann = libfann.neural_net()
        ann.create_from_file(path_odds+'odds.net')
        odds = ann.run(input_list[:])
        for i in odds:
            input_list.append(i)
        ann = libfann.neural_net()
        ann.create_from_file(path_net+str(net))
        prediction = ann.run(input_list[:])
        self.prediction = prediction[0]
        if mode == 0: #prediction
            return self.prediction
        elif mode == 1: #odds
            return odds
    def return_teams(self, folder, name):
        ''' Adds all matches to sql and return list of teams'''
        self.clear_tables()
        file_open = reader(open(folder+name))
        for line in file_open:
            date = line[0]
            date = date[0:7]+date[8:]
            date_num = float(date)
            fth = line[3]
            fta = line[4]
            if fth == '' or fta =='':
                fth = 'NULL'
                fta = 'NULL'
            self.relations_base.execute('''INSERT INTO results(
            date_txt,
            date_num,
            home,
            away,
            gHomeEnd,
            gAwayEnd) VALUES(?,?,?,?,?,?)''',
            (
            line[0],
            date_num,
            line[1],
            line[2],
            fth,
            fta))
        #always sort results according to date
        self.relations_base.execute('''CREATE TEMPORARY TABLE results_copy
        AS SELECT * FROM results ORDER BY date_num ASC''')
        self.relations_base.execute('''DELETE FROM results''')
        self.relations_base.execute('''INSERT INTO results(
                                    date_txt,
                                    date_num,
                                    home,
                                    away,
                                    gHomeEnd,
                                    gAwayEnd)
                                    SELECT
                                    date_txt,
                                    date_num,
                                    home,
                                    away,
                                    gHomeEnd,
                                    gAwayEnd
                                    FROM results_copy''')
        self.relations_base.execute('''DROP TABLE results_copy''')
        # remove duplicates:
        self.relations_base.execute('''delete from results
            where exists (select * from results t2
            where results.date_num = t2.date_num
            and results.home = t2.home
            and results.away = t2.away
            and results.id > t2.id);''')


        teams = self.relations_base.execute('''SELECT DISTINCT home
                                             FROM results''')
        teams = teams.fetchall()
        self.relations_base.execute('''SELECT DISTINCT away FROM results''')
        for i in self.relations_base:
            if i not in teams:
                teams.append(i)
        teams.sort()
        return teams

def main():
    ''' Main function'''
    print 'print a'
    x = Database()
    x.load_csv(os.path.join('leagues', 'current', ''), 'default', expt_name='jhjh',mode = 1)

if __name__ == '__main__':
    main()

