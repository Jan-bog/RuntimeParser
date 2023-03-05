# RuntimeParser

This program loads a .json file given user's input and calculates the sum of runtimes associated with both individual operations and the sum of runtimes of each piece of software itself

## Handling user input:
- The user is first prompted to enter the .json file to analyse. At this step, they might either make typos, input a directory instead, or name a file that the program lacks permission to read. In such cases, exceptions are raised that provide information as to what they did wrong and lets them continue
- In case of not specifying the '.json', that file extension is appended to the input after having checked if another extension has been provided, in which case an exception is thrown, informing the user that only .json files are supported
- For any other exceptions, a generic Exception handler is used

## Handling faulty .json entries:
- I considered an entry invalid if either:
    - Any of the name-value pairs were missing
    - The operation's declared length was either below 0 or non-numeric
- In case of a missing name-value pair, if the missing name was the length, there was no way that I could think of for obtaining meaningful information from such entry
- Except in the potential case of missing software name or operation name, the runtime of listed operation could still be added and prove useful, and listed length could be added to its corresponding software respectively, which I did
- In case of potential typos, the Lovenshtein distance between a new name (for either software or operation) could be computed and the decision to either insert it as a new key or increment the entry with the shortest distance could be made. However, an approach like that could result in undesirable outcomes, e.g. if there was a piece of software named "Investor", it would become synonymous with "Inventor" (or vice versa) if such approach was used
- Finally, if the operation's length is either <= 0 (maybe there is some literally magical operation that takes 0s to perform, but its being an invalid entry seems more likely (and besides, adding 0 to a number doesn't change it anyway)) or non-numeric, it is omitted (if it is a typo, even after removing all non-numeric characters there's still a chance that one of the digits is a result of the typo itself)
