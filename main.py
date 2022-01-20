from asyncore import write
import pydriller
import argparse
from csv import reader
import csv

import shutil
import subprocess

import git

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Extract process metrics')
    ap.add_argument('--pathA', required=True)
    ap.add_argument('--pathB', required=True)
    ap.add_argument('--commits', required=True, help='csv with list of commits to compare commitA and commitB')
    ap.add_argument('--projectName', required=True)
    ap.add_argument('--absolutePath', required=True)
    ap.add_argument('--mode', required=True,help='mode - tag for commits with tag, csv - for csv of commits')
    args = ap.parse_args()

    #folder with repo: projectA and projectB

    pathA = pydriller.Git(args.pathA)
    pathB = pydriller.Git(args.pathB)
    repo = git.Repo(args.pathA)
    tags = repo.tags
   
    release = 1
    commit_A = ''
    commit_B = ''
    bocArray = {}
    if(args.mode == 'tag'):
        for tag in tags:
           
            hashCurrent = pathB.get_commit_from_tag(tag.name).hash
            pathA.checkout(hashCurrent)
            if(commit_B == ''):
                hashPrevious = None
            filesA = pathA.files()
            filesA = [x for x in filesA if x.endswith('.java')]
            
            csvPath = args.absolutePath + args.projectName + "-results-processMetrics.csv"
                     
            if(release ==1):
                commit_A = tag
                f = open(csvPath, "w")
                writer = csv.writer(f)
                row = ['project', 'commit', 'commitprevious', 'class','BOC','TACH','FCH', 'LCH','CHO','FRCH','CHD','WCD' ,'WFR','ATAF','LCA','LCD','CSB','CSBS','ACDF']
                writer.writerow(row)
                f.close()
            else:
                project = args.projectName
                commit = hashCurrent
                commitprevious = hashPrevious
                boc = release
                tach = 0
                fch = 0
                lch = release
                cho = 0
                frch = 0
                chd = 0
                wcd = 0
                wfr = 0
                ataf = 0
                lca = 0
                csb = 0
                csbs = 0
                acdf = 0
                hashPrevious = pathA.get_commit_from_tag(commit_A.name).hash
                pathB.checkout(hashPrevious)
                filesB = pathB.files()
                filesB = [x for x in filesB if x.endswith('.java')]
                for file in filesA:
                    if(file not in bocArray):
                        bocClass = {file,release}
                        bocArray.append(bocClass)
                        boc = release
                    else:
                        boc = bocArray.get(file)
                    row = [args.projectName, hashCurrent, hashPrevious, file,boc,'TACH','FCH', 'LCH','CHO','FRCH','CHD','WCD' ,'WFR','ATAF','LCA','LCD','CSB','CSBS','ACDF']

            commit_A = tag
            release +=1