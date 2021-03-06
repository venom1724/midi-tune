# legacy sequence generation code here
# switched to using data generators (Sequence) for lower memory requirement
# the new code is in smallbrain.py

def loss_choice(type):
    if type==0 or type==2 or type==3:
        return 'categorical_crossentropy'
    else:
        return 'sparse_categorical_crossentropy'

def vibe_check(d):
    print(max(d), min(d))
    print(np.mean(d), np.median(d))
    print(np.quantile(d,.25), np.quantile(d,.75), np.quantile(d,.95))
    m_value=max(d)#1000
    plt.hist(d,range(m_value), density=True)
    plt.gca().set(title='Frequency histogram for Delta time values', ylabel='Frequency')
    plt.xlim(0,m_value)
    plt.legend()
    plt.show()

def ticks_per_beat_test():
    switches=[132, 914, 1183]
    four_eighty = [ [x[2] for y in thing[:switches[0]] for x in y], [x[2] for y in thing[switches[1]:switches[2]] for x in y] ]
    three_eighty = [ [x[2] for y in thing[switches[0]:switches[1]] for x in y], [x[2] for y in thing[switches[2]:] for x in y] ]

    four=four_eighty[0]+four_eighty[1]
    three=three_eighty[0]+three_eighty[1]

    print(np.mean(four), np.mean(three))
    print(np.median(four), np.median(three))

    m_value=1000
    m_value=max(four+three)
    plt.hist(three,range(m_value), alpha=0.5, label='384 ticks', density=True)
    plt.hist(four,range(m_value),  alpha=0.5, label='480 ticks', density=True)
    plt.gca().set(title='Frequency histogram for Delta time with different ticks_per_beat', ylabel='Frequency')
    plt.xlim(0,500)
    plt.legend()
    plt.show()
    
def make_sequences_basic_one_hot(data,sequence_length):
    s_in = []
    s_out = []
    sequences = []
    prev_notes = deque(maxlen=sequence_length)
    cnt, sz = 0, len(data)
    for notes in data:
        prev_notes.clear()
        print(f'{cnt}/{sz}')
        cnt+=1
        for i in notes:
            if len(prev_notes) == sequence_length:
                sequences.append([np.array(prev_notes),i%12])
            prev_notes.append(i)

    random.shuffle(sequences)

    for i,o in sequences:
        s_in.append(i)
        s_out.append(o)
    
    s_in = np.array(s_in, dtype=np.int8)
    s_out = np.array(s_out, dtype=np.int8)
    s_out = np.reshape(s_out, (len(s_out), 1))

    return to_categorical(s_in, num_classes=88, dtype=np.bool), s_out

def make_sequences_basic_one_half(data,sequence_length):
    s_in = []
    s_out = []
    sequences = []
    prev_notes = deque(maxlen=sequence_length)
    cnt, sz = 0, len(data)
    for notes in data:
        prev_notes.clear()
        print(f'{cnt}/{sz}')
        cnt+=1
        for i in notes:
            if len(prev_notes) == sequence_length:
                sequences.append([np.array(prev_notes),i%12])
            prev_notes.append(i)

    random.shuffle(sequences)

    for i,o in sequences:
        s_in.append(i)
        s_out.append(o)
    
    #s_in = (np.array(s_in)/87.)
    s_in = np.array(s_in, dtype=np.int8)
    s_out = np.array(s_out, dtype=np.int8)
    n_patterns = len(s_in)
    s_in = np.reshape(s_in, (n_patterns, sequence_length, 1))
    s_out = np.reshape(s_out, (n_patterns, 1))

    return s_in, s_out#to_categorical(s_in, num_classes=88, dtype=np.bool), s_out

def make_sequences_basic(data,sequence_length):
    return make_sequences_basic_one_hot(data,sequence_length)
    s_in = []
    s_out = []
    sequences = []
    prev_notes = deque(maxlen=sequence_length)
    cnt, sz = 0, len(data)
    for notes in data:
        print(f'{cnt}/{sz}')
        cnt+=1
        for i in notes:
            if len(prev_notes) == sequence_length:
                sequences.append([np.array(prev_notes),i%12])
            prev_notes.append(i)

    random.shuffle(sequences)

    for i,o in sequences:
        s_in.append(i)
        s_out.append(o)

    #s_in = ((np.array(s_in)/87.)*2.)-1
    s_in = np.array(s_in, dtype=np.int8)
    s_out = np.array(s_out, dtype=np.int8)
    n_patterns = len(s_in)
    #s_in = np.reshape(s_in, (n_patterns, sequence_length, 1))
    s_out = np.reshape(s_out, (n_patterns, 1))

    return s_in, s_out #to_categorical(s_out,num_classes=12, dtype=np.bool)

def make_sequences_duration(data,sequence_length):
    s_in = []
    s_out = []
    sequences = []
    prev_notes = deque(maxlen=sequence_length)
    cnt, sz = 0, len(data)
    
    maxduration = np.max([i[2] for sub in data for i in sub])
    for notes in data:
        print(f'{cnt}/{sz}')
        cnt+=1
        for i in notes:
            if len(prev_notes) == sequence_length:
                sequences.append([np.array(prev_notes),i[0]%12])
            prev_notes.append([
                ((i[0]/87.0)*2)-1, 
                ((i[1]/127.0)*2)-1,
                ((i[2]/maxduration)*2.)-1])

    random.shuffle(sequences)

    for i,o in sequences:
        s_in.append(i)
        s_out.append(o)

    s_in = np.array(s_in)
    s_out = np.array(s_out, dtype=np.uint8)
    #n_patterns = len(s_in)
    #s_in = np.reshape(s_in, (n_patterns, sequence_length, 1))
    #s_out = np.reshape(s_out, (n_patterns, 1))

    return s_in, to_categorical(s_out,num_classes=12, dtype=np.bool)

def make_sequences_delta(data,sequence_length):
    s_in = []
    s_out = []
    sequences = []
    prev_notes = deque(maxlen=sequence_length)
    cnt, sz = 0, len(data)
    for notes in data:
        print(f'{cnt}/{sz}')
        cnt+=1
        for i in notes:
            if len(prev_notes) == sequence_length:
                sequences.append([np.array(prev_notes),i[0]%12])
            prev_notes.append(i)
            #    [((i[0]/87.0)*2)-1, 
            #    ((i[1]/127.0)*2)-1,
            #    ((i[2]/255.)*2.)-1])

    random.shuffle(sequences)

    for i,o in sequences:
        s_in.append(np.concatenate([
            to_categorical(i[:,0], num_classes=88, dtype=np.bool),
            to_categorical(i[:,1], num_classes=128, dtype=np.bool),
            to_categorical(i[:,2], num_classes=256, dtype=np.bool)
        ], axis=1))
        #s_in.append(i)
        s_out.append(o)

    s_in = np.array(s_in, dtype=np.bool)
    s_out = np.array(s_out, dtype=np.uint8)
    #n_patterns = len(s_in)
    #s_in = np.reshape(s_in, (n_patterns, sequence_length, 1))
    #s_out = np.reshape(s_out, (n_patterns, 1))

    return s_in, to_categorical(s_out,num_classes=12, dtype=np.bool)



def make_sequences_choice(data,sequence_length, type):
    if type==0:
        return make_sequences_basic(data,sequence_length)
    if type==1:
        return make_sequences_basic(data,sequence_length)
    if type==2:
        return make_sequences_delta(data,sequence_length)
    if type==3:
        return make_sequences_duration(data,sequence_length)


def create_data():
    print("Loading dataset..")
    data_parsed = [pickle.load(open(f'{data_folder}rick-{data_type}-{x}','rb')) for x in data_split]
    print("generating train..")
    train_x, train_y = make_sequences(data_parsed[0][:config.input_data_size], config.sequence_length, config.input_data_type)
    print("generating test..")
    test_x, test_y = make_sequences(data_parsed[0][:int(config.input_data_size/10)], config.sequence_length, config.input_data_type)
    print("generating validation..")
    validation_x, validation_y = make_sequences(data_parsed[0][:int(config.input_data_size/10)], config.sequence_length, config.input_data_type)
    return train_x, train_y, test_x, test_y, validation_x, validation_y

def load_data():
    train_x =       pickle.load(open(f"{sequence_folder}trainx-{data_type}",        'rb'))
    train_y =       pickle.load(open(f"{sequence_folder}trainy-{data_type}",        'rb'))
    test_x =        pickle.load(open(f"{sequence_folder}testx-{data_type}",         'rb'))
    test_y =        pickle.load(open(f"{sequence_folder}testy-{data_type}",         'rb'))
    validation_x =  pickle.load(open(f"{sequence_folder}validationx-{data_type}",   'rb'))
    validation_y =  pickle.load(open(f"{sequence_folder}validationy-{data_type}",   'rb'))
    return train_x, train_y, test_x, test_y, validation_x, validation_y

def save_data():
    print("saving train..")
    pickle.dump(train_x,open(f"{sequence_folder}trainx-{data_type}",'wb'))
    pickle.dump(train_y,open(f"{sequence_folder}trainy-{data_type}",'wb'))
    print("saving test..")
    pickle.dump(test_x,open(f"{sequence_folder}testx-{data_type}",'wb'))
    pickle.dump(test_y,open(f"{sequence_folder}testy-{data_type}",'wb'))
    print("saving validation..")
    pickle.dump(validation_x,open(f"{sequence_folder}validationx-{data_type}",'wb'))
    pickle.dump(validation_y,open(f"{sequence_folder}validationy-{data_type}",'wb'))