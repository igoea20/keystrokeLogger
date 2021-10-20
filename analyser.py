

class analyse:

#need to remove whitespace at top of file


    def key_length(data_lines, line_number):
    #read the first character and store it and the time
    #find the next instance of the character (released)
    #write the info in a filename
        line = data_lines[line_number].rsplit() #remove the \n and split up
        letter = line[2]    #letter should be here
        print(letter)
        time1 = line[0]      #save the time as well

        line_number+=1
        found = False
        time2 = ""

        while found!=True and line_number < len(data_lines):
            line = data_lines[line_number].rsplit()
            event = line[1]
            letter2 = line[2]
        #    print(letter2)
            if event == 'Released:' and letter2 == letter :
                time2 = data_lines[line_number].rsplit()[0]
                found = True
            line_number+=1
        print(f'Time 1 {time1}')
        print(f'Time 2 {time2}')

        myfile = open("analysis.txt", "a")
        store = "Key: " + letter + " Pressed at: " + time1 + " Released at: " + time2 + "\n"
        myfile.write(store)
        myfile.close()



    def print_file(data_lines):
        count = 0
        for data in data_lines:
            count+=1
            print(f'line {count}: {data}')




data_lines = []
myfile = open('log.txt', "r")
data_lines = myfile.readlines()
#analyse.print_file(data_lines)
analyse.key_length(data_lines, 0)


#change this into a string so we can move through it easier

#while there are still characters left to read
#call key_length
#move along a character


myfile.close()
