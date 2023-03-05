import json
import os

class LengthError(Exception):
    pass

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def processfile(filename='p_ex_1_runtime_parsing.json'):
    keys = ['total', 'persoftware']
    runtimes = {key: {} for key in keys}
    
    try:
        file = open(os.path.join(__location__, filename), 'r')
    except FileNotFoundError as e:
        print(f"Error: File {filename} not found!")
        return None
    except PermissionError as e:
        print(f"Error: Permission denied to read file {filename}!")
        return None
    except IsADirectoryError as e:
        print(f"Error: {filename} is a directory!")
        return None
    except OSError as e:
        print (f"Error: {e}")
        return None

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
    perop = [f'  {key}: {value}' for key, value in sorted(runtimes['total'].items(), key=lambda x: x[1])]
    print(f"Total runtimes per operation:")
    print('\n'.join(perop))
    print('\n')
    persw = [f'  {key}: {value}' for key, value in sorted(runtimes['persoftware'].items(), key=lambda x: x[1])]
    print(f"Total runtimes per software:")
    print('\n'.join(persw))

def main():
    runtimes = processfile()
    if runtimes is None:
        print("Couldn't process file! Exiting...")
        return
    printstats(runtimes)

if __name__ == '__main__':
    main()