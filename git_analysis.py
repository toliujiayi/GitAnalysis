'''
Created on Nov 19, 2018

@author: jackliu
'''
import matplotlib.pyplot as plt
import numpy as np




number_of_commits = {
    "2014": 0,
    "2015": 0,
    "2016": 0,
    "2017": 0,
    "2018": 0
}

#file changed, insertions, deletions
number_of_changes = {
    "2014": [0, 0, 0],
    "2015": [0, 0, 0],
    "2016": [0, 0, 0],
    "2017": [0, 0, 0],
    "2018": [0, 0, 0]
}


#email: [file changed, insertions, deletions, commit #, name]
contributor_changes = {
}

subsystems = ["doc", "contrib", "config", 
              "src/tutorial",
              "src/tools",
              "src/timezone",
              "src/test",
              "src/template",
              "src/port",
              "src/pl",
              "src/makefiles",
              "src/interfaces",
              "src/include",
              "src/fe_utils",
              "src/common",
              "src/bin",
              "src/backend"
              ]

# subsystem: 
changes_per_language_per_subsystem = {
    }
languages = [
    "c", "h", "css", "cfg", "dsl", "xsl", "xml", "pl", "sgml", "py", "sql", "csv", "conf", "mk", "guess", "m4", "bat",
    "txt", "sh", "in", "out", "po", "sed", "cpp", "java"
    ]

for sub in subsystems:
    changes_per_language_per_subsystem[sub] = set()

if __name__ == '__main__':
    started = False;
    year = None;
    author_name = None;
    author_email = None;
    file_changed = None;
    insertions = None;
    deletions = None;
    
    with open("gitlog.txt") as infile:
        for line in infile:
            line = line.strip()
            if not started:
                started = True
                commit_info = line.split(";")
                year = commit_info[1].split("-")[0]
                number_of_commits[year] += 1;
                
                author_name =  commit_info[2]
                author_email =  commit_info[3]
            elif "|" in line:
                dirs = line.split("/")
                file_part = line.split("|")[0].strip()
                
                extention = None
                if "." in file_part:
                    extention = file_part.split(".")[1]
                
                if dirs[0] == "src":
                    sub = dirs[0] + "/" + dirs[1]
                else:
                    sub = dirs[0]
                    
                if sub in subsystems and extention in languages:
                    changes_per_language_per_subsystem[sub].add(extention)

            elif line:
                summary = {}
                for e in ["file", "insertion", "deletion"]:
                    summary[e] = 0;
                    if e in line:
                        num = line.split(e)[0].split(" ")[-2]
                        summary[e] = int(num)

                number_of_changes[year][0] += summary["file"]
                number_of_changes[year][1] += summary["insertion"]
                number_of_changes[year][2] += summary["deletion"]
                
                if author_email not in contributor_changes:
                    contributor_changes[author_email] = [0, 0, 0, 0, 0, author_name, author_email]
                
                contributor_changes[author_email][0] += summary["file"]
                contributor_changes[author_email][1] += summary["insertion"] + summary["deletion"]
                contributor_changes[author_email][2] += summary["insertion"]
                contributor_changes[author_email][3] += summary["deletion"]
                contributor_changes[author_email][4] += 1
                
            else:
                started = False
                
    contributor_changes_list = contributor_changes.values()
    contributor_changes_list = sorted(contributor_changes_list, key=lambda x:x[1], reverse=True)
    sample = list(map(lambda x:x[1], contributor_changes_list))
    average = np.mean(sample)
    standard_deviation = np.std(sample)
    print(number_of_commits)
    print(number_of_changes)
    print(contributor_changes_list)
    print(changes_per_language_per_subsystem)
    print(average)
    print(standard_deviation)
    
    x = np.array(range(len(sample)))
    y = np.array(sample)
    a = np.array([average]*len(sample))
    plt.plot(x, y, marker='.', linestyle='None')
    plt.plot(x, a, linestyle="dashed")
    plt.show()

                
                
            
            