# Theta-Staking-Rewards
A basic command line tool to obtain Theta Network stake reward transaction information from the offical API.

Enter your public wallet address and you will receive a CSV file including all staking rewards transactions associated with the wallet. The CSV file is not currently sorted, so you'll need to do that yourself (a queuing system has been employed for writing data from multiple threads, but a queue has not been implemented for delegating requests) - This shouldn't matter when importing into another portfolio manager, as the timestamp is included.

## Dependencies
* Requests (https://pypi.org/project/requests/)

