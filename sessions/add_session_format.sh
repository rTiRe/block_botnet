for file in sessions/*
do
    filename=$(basename -- "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"
    if [ $filename == $extension ]
    then
        mv "sessions/${filename}" "sessions/${filename}.session"
    fi
done
