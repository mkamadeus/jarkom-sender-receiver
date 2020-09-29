downloaded=`md5sum ./out/downloaded | awk '{ print $1 }'`
original=`md5sum $1 | awk '{ print $1 }'`

echo original: $original
echo downloaded: $downloaded

if [ "$downloaded" == "$original" ] 
then
  echo 'md5sum is equal'
  exit
fi

echo -e 'md5sum not equal\n'
# diff ./out/downloaded $1
