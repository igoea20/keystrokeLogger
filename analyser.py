
#what combinations do we want to look for?


class analyse:

#this class should utilise the scraper so it is receiving tuples of data
#containing (event, key, time)


    def key_length(data_tuples):
    #receives an array of tuples
    #take the first tuple, store the values and then remove it (pop)
    #search for the next instance of the key
    #when found store the data and then remove it
        current_tupl = data_tuples[0]
        key = current_tupl[1]
        time1 = current_tupl[2]
        index = 0

        #remove tuple
        data_tuples.pop(0)

        for tuple in data_tuples:
            if( tuple[1]== key):
                time2 = current_tupl[2]
                data_tuples.pop(index)
                break
            index++

        time_between_release = time2 - time1
        data_pair = (key, time_between_release)
        return data_pair


    def calculate_release_times(data_tuples):
        #call key_length to calculate the time
        #write to file

        #while the array of tuples is not empty
        while(data_tuples):
            analysed_data = key_length(data_tuples)
            write_to_file(analysed_data)


    #takes in a tuple containing (key, time pressed, time released) and writes it
    def write_to_file(analysed_data):
        myfile = open("analysis.txt", "a")
        store = "Key: " + analysed_data[0] + " Time between press and release:  " + analysed_data[1] + "\n"
        myfile.write(store)
        myfile.close()


    def unused():
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

#call the scraper here and process it into a list of tuples
analyse.calculate_release_times(data_lines)


myfile.close()
