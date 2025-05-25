import os

from analyze.Perceptron import Perceptron

perceptrons = [Perceptron(0.01, 26, x) for x in os.listdir('analyze/pliki do train i test/pliki do train i test/Train')]
print(len(perceptrons))
def count_chars(string):
    if len(string) == 0:
        return [0]
    letters = [0 for _ in range(26)]
    suma = 0
    for char in string:
        if not char.isalpha() or not char.isascii():
            continue
        letters[ord(char.lower()) - ord('a')] += 1
    for char in letters:
        suma += char
    return [lab / suma for lab in letters]

def read_file(dir_path, file):
    letters = [0 for _ in range(26)]
    with open(dir_path + "/" + str(file), encoding="utf8") as f:
        suma = 0
        for line in f:
            for char in line:
                if char.isalpha() and char.isascii():
                    letters[ord(char.lower()) - ord('a')] += 1
        for char in letters:
            suma += char
    return [lab / suma for lab in letters]

def learning_process(t_data):
    learn(t_data, perceptrons)

def read_files(path_name):
    l = []
    for (dir_path, dir_names, file_names) in os.walk(path_name):
        if len(file_names) == 0:
            continue
        for file in file_names:
            if not os.path.isdir(os.path.join(dir_path, file)):
                l.append([read_file(dir_path, file), dir_path.split("\\")[-1]])
    return l

training_data = read_files('analyze/pliki do train i test/pliki do train i test/Train')
test_data = read_files("analyze/pliki do train i test/pliki do train i test/Test")

def analyze(text, **kwargs):
    if kwargs.get('data_form') == "String":
        text = count_chars(text)
    outputs = []
    for perc in perceptrons:
        outputs.append([perc.language.split("\\")[-1], perc.compute(text)])
    result = max(outputs, key= lambda pe: pe[1])
    print(result)
    if result[1] > 0.5:
        return result[0]
    return None

def learn(t_data, perceptron):
    for p in perceptron:
        epoque = 0
        while True:
            to_break = 0
            for inputs, language in t_data:
                if language != p.language:
                    continue
                decision = 1 if language == p.language else -1
                e = 0.5 * (decision - p.compute(inputs)) ** 2
                p.learn(inputs, e)
                epoque += 1
                if e < 0.00001:
                    to_break = 1
                    break
            if to_break:
                break
def read_weights():
    with open('analyze/save.txt', 'r') as file:
        for i, e in enumerate(file):
            new_weights = [float(x) for x in e.split(";")]
            perceptrons[i].weights = new_weights
def load():
    read_weights()
    if not test:
        clear_weights()
        learn(training_data, perceptrons)



def save_weights():
    global perceptrons
    with open("save.txt", "w") as file:
        for p in perceptrons:
            weights_str = [str(weight) for weight in p.weights]
            file.write(";".join(weights_str) + '\n')
def test():
    correct = 0
    for x in range(len(test_data)):
        testing = analyze(test_data[x][0])
        b = testing[0] == test_data[x][1].split("_")[0]
        if b:
            correct += 1
    return correct == len(test_data)

def clear_weights():
    global perceptrons
    perceptrons = [Perceptron(0.01, 26, x) for x in os.listdir('analyze/pliki do train i test/pliki do train i test/Train')]