# Wunderworlds Resolution Improvement

Author: CEDipEngineering

## Goal:
    
The goal of this project was to help improve the quality of the pdf cards generated by Wunderworlds' deck export to print feature. I found that the resolution, contrast and sharpness were somewhat lackluster, and so designed this very simple project to try and improve the quality. It's by no means perfect, but it seemed to help a little from what I can tell.

## Usage:

This project was developed using Python 3.8.10, and as such, needs a similar version to function.

To use this project, first install the necessary requirements (mostly to add the libraries used to manipulate pdf files and PIL).

    $ pip install -r requirements.txt

Once this is done, simply run:

    $ python src/main.py <PATH_TO_ORIGINAL_FILE.pdf> <PATH_TO_OUTPUT_FILE.pdf>

And you're done! The program will save the improved cards to the new pdf.