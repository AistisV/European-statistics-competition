# European statistics competition

This repository contains a Python script for **calculating the Influence Index** based on live user input. The Influence Index compares **Gen Z** with **Older Adults** over a specified period.

## Script

- **`influence_index_calculator.py`**: Allows the user to input data points (years) and the corresponding values for both Gen Z and Older Generations. It then calculates the Influence Index based on the provided data.

### How to Use

1. Run the script.
2. Enter the number of data points (years).
3. Input the corresponding values for **Gen Z** and **Older Generations**.
4. The script will output the calculated **Influence Index** based on your inputs.

The Influence Index indicates how trends in Gen Z compare to those in Older Generations over time. Positive values suggest aligned trends, while negative values indicate opposing trends.

### Example

When prompted, input data for Gen Z and Older Generations. For instance:
Enter number of data points (years): 3
Enter 2 values for Gen Z, separated by spaces: 60 61 62 
Enter 2 values for Older Generations, separated by spaces: 30 32 35

The script will output the Influence Index based on these inputs. In this case, the Influence index is 2.5, suggesting that trends in Gen Z and Older Generations are aligned over the specified years.
