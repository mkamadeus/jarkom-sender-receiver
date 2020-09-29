DIFF=$(diff ./out/downloaded $1)

if [ "$DIFF" == "" ]
then
  echo "No difference in file, transfer success"
fi