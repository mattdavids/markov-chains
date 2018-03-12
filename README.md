# Markov Chains

This program generates Markov Chain states and stores them as dictionaries in CSV files. It can then either generate a specified amount of random text based on a specific source, or can find the average sentence of a source.  

### Average Sentence

As as quick aside, average sentence isn't a typical measure of text. It comes from the concept of expected value. When rolling a six sided die, the expected value would be a 3.5 which is (1 + 2 + 3 + 4 + 5 + 6)/6. While this value does not ever appear on the die, it is the most likely expected result. In the same sense, the average sentence of a source may never appear, but it would be the most likely expected result.   

## Initialization

Run each of the Data files to generate the csv databases necessary to run the main program. You will need to put a Twitter API key into your environmental variables or in plaintext in the TwitterData.py file for it to work.   
  
- The current settings on ShakespeareData.py will take half an hour to complete.  
- The current settings on WikiData.py will take 12 hours to complete and at least 10 Gb of free ram.  
- The current settings on TwitterData.py will take somewhere around a day to complete.  

## Text Generation

You can then run the chain.py file to generate text using various inputs. Text generation for Wikipedia will take a few minutes.  
