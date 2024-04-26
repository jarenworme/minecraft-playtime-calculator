import os, glob

# path to folder holding log files
path = "./logs"

# global variables to keep track of info through iterations
i = 0
total_mins = 0

# main loop
for filename in glob.glob(os.path.join(path, '*.log')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:

        # get the first line of the log which contains the start time
        first_line_full = f.readline()

        # format 1 (original) possibilites:
        # [10:55:54] [main/INFO]:
        # [11:36:01] [Render thread/INFO]: Environment: authHost='https://authserver.mojang.com'
        # [00:25:44] [Server thread/INFO]: Saving and pausing game...
        # [00:00:00] [Client thread/ERROR]: ########## GL ERROR ##########
        # [11:55:25] [Datafixer Bootstrap/INFO]: 180 Datafixer optimizations took 177 milliseconds

        # format 2 (alt):
        # [08Aug2019 20:51:47.542] [main/INFO]

        # determine the format
        test = first_line_full[12]
        if test == 'm' or test == "R" or test == 'S' or test == 'C' or test == 'D': # could probably improve this with regex
            fhour = int(first_line_full[1:3])
            fmin = int(first_line_full[4:6])
        else:
            fhour = int(first_line_full[11:13])
            fmin = int(first_line_full[14:16])


        # get all file lines to then grab the last one easily
        lines = f.read().splitlines()

        # skip iteration for files that only log one line
        if len(lines) < 2:
            continue

        # get the last line of the log which contains the session end time
        last_line_full = lines[-1]

        # even some alt format files have end lines in the other format, so we need to check again

        # format 1 (original) possibilities:
        # [14:21:06] [Render thread/INFO]: Stopping!
        # [23:30:22] [Server thread/INFO]: Saving chunks for level
        # [18:01:23] [Worker-Main-8/INFO]: WorldEdit for Forge (version 7.2.7+9f3e795) is loaded
        # [19:02:27] [Client thread/INFO]: Stopping!
        # [21:03:50] [Thread-19/INFO]: paulscode.sound.CommandThread.run(CommandThread.java:121)
        # [18:54:52] [main/INFO]: Stopping!

        # format 2 (alt):
        # [31May2021 21:26:19.700] [Render thread/INFO] [net.minecraft.client.Minecraft/]: Stopping!

        # determine the format
        test = last_line_full[12]
        if test == 'R' or test == 'S' or test == 'W' or test == 'C' or test == 'T' or test == 'm':
            lhour = int(last_line_full[1:3])
            lmin = int(last_line_full[4:6])
        else:
            lhour = int(last_line_full[11:13])
            lmin = int(last_line_full[14:16])

        # convert hours to minutes and add them together
        fhour = fhour * 60
        lhour = lhour * 60
        fsum = fhour + fmin
        lsum = lhour + lmin

        # subtracting the mins value of the start-of-log hour from the end-of-log hour gives minutes played per log
        mins_played = lsum - fsum

        if i < 0: #error checking, change 0 to a number to get a sense of the info being calculated, or substitute into above code
            print("iteration: ", i)
            print("file: ", filename)
            print("first line: ", first_line_full[0:23]) # lines can be long, so only print relevant info
            print(fhour)
            print(fmin)
            print(lhour)
            print(lmin)
            print(fsum)
            print(lsum)
            print(mins_played)
            print("\n")

        # update global counter with minutes calculated from the current file
        total_mins = total_mins + mins_played

    # successful iteration, increment i
    i += 1

# make use of the error checking above for any files that may be a different format that mine, or corrupted.
# if everything is fine, it will print these success messages telling you your total playtimes!

# add any files you may have computed manually due to its size or corruption
large_files = 0
corrupted_files = 0 

total_mins = total_mins + large_files + corrupted_files
print("minutes played from log files:", total_mins)

hours = total_mins // 60
print("this translates to about " + str(hours) + " hours!")
print("\n")


