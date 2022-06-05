SetLocal
git add *
set /p "ch=Name_Commit? (Text)"
git commit -m "%ch%"
git push
