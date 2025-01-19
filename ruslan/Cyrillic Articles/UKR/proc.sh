#!/bin/bash
DIRECTORY=${1:-.}
for FILE in "$DIRECTORY"/*; do
    if [ -f "$FILE" ]; then
        echo "Processing file: $FILE"
		BASENAME=$(basename "$FILE")       
        FILENAME="${BASENAME%.*}"      
        EXTENSION="${BASENAME##*.}"  
        NEW_FILENAME="${FILENAME}_OCR.${EXTENSION}"
		ocrmypdf -l ukr --deskew $FILE UKROCR/$NEW_FILENAME
    fi
done