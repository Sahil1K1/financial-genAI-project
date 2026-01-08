print('\n')
print("stash files changes(changes are saved temporary but these aren't commited)")

# commit
# in order to commit something first it need to added in staged directory which requires git add command
# git commit permanently add changes in github repo where git add allows you add changes in staged directory 
# git add also allows control of which files need to added and it requires no message
# git commit requires message attached with it

# first do git add and then do git commit(helps track of changes in better way)

# once file is added there will be a A(icon at the end of file in tree structure)

# once changes are commited then in order them to reflect into repo we have to run git push command

# commit creates a history line everytime(so for timelines use git commit, to stage them use git add and to push final changes to use git push)

# once changes/modifications are done in personal branch next step is to merge those changes in master branch
# first change branch to master(git checkout master) > then take latest pull from master(very important)(git pull origin master) > merge personal branch into master(git merge SahilPersonalBranch)
# after this there are two possiblilities first is get no conflicts
# another is to get conflict issue(in order to resolve those issues we have to add and commit our changes in master)
# git add . > git commit

# now once the changes are in local(master branch) now we can push these changes to github
# git push origin master

# now once the changes are merged to master, next is to create a tag
# a tag is like a version of project(v1.0.0) and it is used for deployment in later phases.

# in order to create a tag first we need to push all changes of personal branch into github
# then checkout to master branch > take latest pull > merge personal into master(resolve conflict if any)
# push changes to master

# now stay on master and create a tag
# simple and easy tag == git tag
# if we want to add annotations with it like date, email and other information == git tag -a v1.0.0 -m "First stable version"
# once tag is created then push those changes to master
# git push origin v1.0.0

# if user wanted to make some changes in old commits
# first is to make changes in the latest commit then make changes and use git add .(to stage those changes)
# then use git commit --amend (it will open editor to make changes in message)
# if we don't want to change message as well then we can use == git commit --amend --no-edit