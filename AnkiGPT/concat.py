import glob

from config import OUTPUT_FOLDER

# Get a list of all files starting with "flashcards" and sort them
files = sorted(glob.glob(f'{OUTPUT_FOLDER}/flashcards*.txt'))

# Open a new file to write concatenated content
with open('combined_flashcards.txt', 'w') as outfile:
    for file in files:
        with open(file, 'r') as infile:
            for line in infile.readlines():
                if ';' in line:
                    outfile.write(line)
            outfile.write('\n')  # Adding a newline for separation between files
