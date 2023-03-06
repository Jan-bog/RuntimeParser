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
            exceptional = ""
            if entry['length'] <= 0:
                raise LengthError
            curlen = entry['length']
            if 'operation' in entry:
                if entry['operation'] in runtimes['total']:
                    runtimes['total'][entry['operation']] += curlen
                else:
                    runtimes['total'][entry['operation']] = curlen
            else:
                exceptional = "No operation listed"
            if 'software' in entry:
                if entry['software'] in runtimes['persoftware']:
                    runtimes['persoftware'][entry['software']] += curlen
                else:
                    runtimes['persoftware'][entry['software']] = curlen
            else:
                exceptional = "No software listed"
            if exceptional != "":
                raise KeyError(exceptional)
        except KeyError as e:
            print(f"Warning: {exceptional}!")
        except TypeError as e:
            print(f"Warning: Couldn't parse operation's length! Ignoring entry")
        except LengthError as e:
            print(f"Warning: Operation's length listed as 0 or below. Ignoring entry. Possible typo!")
    
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
                print(f"Error: File {filename} not found! Make sure it's located in the same directory as the program or use the full path to the file")
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
    
"""
Answers to posited questions:

## Handling user input:
- The user is first prompted to enter the .json file to analyse. At this step, they might either make typos,
input a directory instead, or name a file that the program lacks permission to read.
In such cases, exceptions are raised that provide information as to what they did wrong and lets them continue
- In case of not specifying the '.json', that file extension is appended to the input after having checked if another extension has been provided,
in which case an exception is thrown, informing the user that only .json files are supported
- For any other exceptions, a generic Exception handler is used

## Handling faulty .json entries:
- I considered an entry invalid if either:
    - Any of the name-value pairs were missing
    - The operation's declared length was either below 0 or non-numeric
- In case of a missing name-value pair, if the missing name was the length,
there was no way that I could think of for obtaining meaningful information from such entry
- Except in the potential case of missing software name or operation name,
the runtime of listed operation could still be added and prove useful,
and listed length could be added to its corresponding software respectively, which I did
- In case of potential typos, the Lovenshtein distance between a new name (for either software or operation)
could be computed and the decision to either insert it as a new key or increment the entry with the shortest distance could be made.
However, an approach like that could result in undesirable outcomes, e.g. if there was a piece of software named "Investor",
it would become synonymous with "Inventor" (or vice versa) if such approach was used
- Finally, if the operation's length is either <= 0 (maybe there is some literally magical operation that takes 0s to perform,
but its being an invalid entry seems more likely (and besides, adding 0 to a number doesn't change it anyway)) or non-numeric,
it is omitted (if it is a typo, even after removing all non-numeric characters there's still a chance that one of the digits is a result of the typo itself)
"""
