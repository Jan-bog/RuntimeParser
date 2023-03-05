import json
import os

class LengthError(Exception):
    pass

class FileFormatError(Exception):
    pass

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def processfile(file):
    keys = ['total', 'persoftware']
    runtimes = {key: {} for key in keys}
    
    #file = open(os.path.join(__location__, filename), 'r')

    data = file.read()
    parsed = json.loads(data)

    for entry in parsed:
        try:
            if entry['length'] < 0:
                raise LengthError
            curlen = entry['length']
            if entry['operation'] in runtimes['total']:
                runtimes['total'][entry['operation']] += curlen
            else:
                runtimes['total'][entry['operation']] = curlen
            if entry['software'] in runtimes['persoftware']:
                runtimes['persoftware'][entry['software']] += curlen
            else:
                runtimes['persoftware'][entry['software']] = curlen
        except KeyError as e:
            print(f"Warning: No operation found in entry! Ignoring entry")
        except TypeError as e:
            print(f"Warning: Couldn't parse operation's length! Ignoring entry")
        except LengthError as e:
            print(f"Warning: Operation's length below 0. Ignoring entry. Possible typo!")
    
    print('\n')

    file.close()

    return runtimes

def printstats(runtimes):
    perop = sorted(runtimes['total'].items(), key=lambda x: x[1])[-1]
    print(f"The longest of all operations:\n  {perop[0]}, with a runtime of {perop[1]}")
    print('\n')
    persw = [f'  {key}: {value}' for key, value in sorted(runtimes['persoftware'].items(), key=lambda x: x[1], reverse=True)]
    print(f"Total runtimes per software:")
    print('\n'.join(persw))

def fileretrieval():
    while(True):
        print("Please enter the name of the file you want to process. Enter 'q' to quit")
        filename = input("File name: ")
        if filename == 'q':
            return None
        else:
            try:
                if '.' in filename:
                    if filename.split('.')[-1] != 'json':
                        raise FileFormatError
                if '.json' not in filename:
                    filename += '.json'
                file = open(os.path.join(__location__, filename), 'r')
                return file
            except FileNotFoundError as e:
                print(f"Error: File {filename} not found! Make sure it's located in the same directory as the program")
                continue
            except PermissionError as e:
                print(f"Error: Permission denied to read file {filename}!")
                continue
            except IsADirectoryError as e:
                print(f"Error: {filename} is a directory!")
                continue
            except OSError as e:
                print (f"Error: {e}")
                continue
            except FileFormatError:
                print(f"Error: Unsupported file format! Please use a .json file")
                continue
            except Exception as e:
                print(f"Error: {e}")
                continue

def main():
    file = fileretrieval()
    if file is None:
        print("Program exited by user...")
        return
    
    runtimes = processfile(file)

    printstats(runtimes)

if __name__ == '__main__':
    main()