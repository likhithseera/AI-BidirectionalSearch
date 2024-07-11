import os
from pathlib import Path
import csv
import re

# Function to create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("The new directory is created!")
    else:
        print("The directory Exists!")

# Function to execute commands and return command string
def execute_command(maze, algorithm, index, k):
    file = algorithm[:index] if "," in algorithm else algorithm
    command = f"python pacman.py -l {maze} -z .5 -p SearchAgent -a fn={algorithm} --frameTime 0 > ./outputs/output{k:03d}_{maze}_{file}.txt"
    print("Command executing:", command)
    os.system(command)

# Function to create CSV from the result log.
def generateCSVResult(resultFile, outputFile):
    # Define a regular expression pattern to extract numerical data
    pattern1 = r'Total Cost: (\d+) Nodes: (\d+)\n'
    pattern2 = r'Score: (\d+) Result: (\w+)\n'

    # Open the text file in read mode
    with open(resultFile, 'r') as file:
        # Read the entire content of the file
        text = file.read()

    mazes = ["contoursMaze", "openMaze", "smallMaze", "mediumMaze", "bigMaze1", "bigMaze2", "bigMaze3", "bigMaze4", "bigMaze5", "bigMaze6", "bigMaze7", "bigMaze8", "bigMaze9", "bigMaze10", "bigMaze11", "bigMaze12", "bigMaze13", "bigMaze14", "bigMaze15"]
    algorithms = ["bfs", "dfs", "ucs", "astar", "bds_mmMan", "bds_mmEuc", "bds_mm0"]

    # Find matches using regex pattern
    matches1 = re.findall(pattern1, text)
    matches2 = re.findall(pattern2, text)

    # Check if the number of matches is as expected
    expected_count = len(mazes) * len(algorithms)
    if len(matches1) != expected_count or len(matches2) != expected_count:
        print("Error: Number of matches doesn't match the expected count.")
        return

    # Write data to CSV file
    with open(outputFile, 'w', newline='') as csvfile:
        fieldnames = ['Maze', 'Algorithm', 'Total_Cost', 'Nodes_Expanded', 'Total_Score', 'Result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        match_index = 0
        for m in mazes:
            for a in algorithms:
                if match_index < len(matches1) and match_index < len(matches2):
                    m1 = matches1[match_index]
                    m2 = matches2[match_index]
                    writer.writerow({'Maze': m, 'Algorithm': a, 'Total_Cost': m1[0], 'Nodes_Expanded': m1[1], 'Total_Score': m2[0], 'Result': m2[1]})
                    match_index += 1
                else:
                    writer.writerow({'Maze': m, 'Algorithm': a, 'Total_Cost': '0', 'Nodes_Expanded': '0', 'Total_Score': '0', 'Result': None})

    print("Data has been successfully written to file:", outputFile)

# Main function
def main():
    output_path = str(Path.cwd()) + "/outputs"
    create_directory(output_path)

    algorithms = ["bfs", "dfs", "ucs", "astar,heuristic=manhattanHeuristic", "bds_mmMan,heuristic=manhattanHeuristic", "bds_mmEuc,heuristic=euclideanHeuristic", "bds_mm0"]
    mazes = ["contoursMaze", "openMaze", "smallMaze", "mediumMaze"]

    k = 0
    # Running algorithms for small mazes
    for maze in mazes:
        for algorithm in algorithms:
            index = algorithm.index(",") if "," in algorithm else len(algorithm)
            execute_command(maze, algorithm, index, k)
            k += 1

    # Running algorithms for big mazes
    for j in range(1, 16):
        for algorithm in algorithms:
            index = algorithm.index(",") if "," in algorithm else len(algorithm)
            execute_command(f"bigMaze{j}", algorithm, index, k)
            k += 1

    # Reading and writing all files into result file
    read_files = os.listdir(output_path)
    print(read_files)
    with open(os.path.join(output_path, 'Result.txt'), 'w') as outfile:
        for file_name in read_files:
            file_path = os.path.join(output_path, file_name)
            print("File:", file_path)
            if "_" in file_name:
                file_key = file_name[file_name.rindex("_", 0, file_name.rindex("_") - 1) + 1:file_name.rindex(".")]
                outfile.write(f"{file_key}\n")
                with open(file_path, "r") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")
            else:
                continue
    
    # Generating CSV file from the log files from result.txt to Output.csv
    generateCSVResult(os.path.join(output_path, 'Result.txt'), os.path.join(output_path, 'Output.csv'))
    
if __name__ == "__main__":
    main()
