from PdfManipulator import PdfManipulator
from ImageImprover import ImageImprover
from random import randint

VERBOSE = True

def main(pdf_path: str, output_path: str):
    
    if VERBOSE: print("Beginning card extraction from {}".format(pdf_path))
    # Extractor
    PM = PdfManipulator(pdf_path)
    images = PM.get_cards()
    if VERBOSE: print("Extraction successfull! Found {} cards!\nBeginning image processing improvements...".format(len(images)))
    
    # Improver
    II = ImageImprover()
    improved_images = II.improve_all(images)
    # II._compare_debug(images[example])
    if VERBOSE: print("Improvements successfull! Saving changes...")
    PM.dump_changes(output_path, improved_images)
    if VERBOSE: print("Successfully saved to new file! Find your improved pdf at {}".format(output_path))


if __name__ == "__main__":
    path = "data/Tooth_and_Claw.pdf"
    output = "data/Tooth_and_Claw_cleaned.pdf"
    main(path, output)