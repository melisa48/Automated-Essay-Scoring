# Automated Essay Scoring

## Description
This project implements an Automated Essay Scoring system using AI and natural language processing. It can accurately grade essays and provide detailed feedback to students, making the grading process more efficient for teachers.

## Features
- Calculates various metrics for essay analysis
- Provides a numerical score out of 100
- Offers detailed feedback on essay structure, length, vocabulary, and grammar
- Visualizes essay metrics
- Exports analysis results to a JSON file

## Requirements
- Python 3.7+
- NLTK
- language_tool_python
- matplotlib
- tqdm

## Installation
1. Clone this repository:
- `git clone https://github.com/yourusername/automated-essay-scoring.git`
- `cd automated-essay-scoring`
  
2. Install the required packages:
- `pip install nltk language_tool_python matplotlib tqdm`

3. Download necessary NLTK data:
- `import nltk`
- `nltk.download('punkt')`


## Usage
1. Run the script:
- `python main.py`

2. When prompted, enter your essay text.

3. Alternatively, you can analyze an essay from a file:
- `python main.py --essay path/to/your/essay.txt`

4. The program will display the essay score and detailed metrics in the console.

## Contributing
Contributions to improve the Automated Essay Scoring system are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements. 
