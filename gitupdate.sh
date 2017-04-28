check_remove(){
	if [ $1 = "master" ]; then 
		return 
	fi
	if git ls-remote --heads | grep -sw $1>/dev/null; then
		echo $1 Still on remote
		git checkout $1
		git merge -m"merged in remote/$1" refs/remotes/origin/$1 || exit -1
		git merge -m"merged in master" refs/remotes/origin/master || exit -1
    	if [ $1 = "pynn_0.8" ]; then
    	    if git ls-remote --heads | grep -sw release_candidate>/dev/null; then
	    	    git merge -m "merged in release_candidate" refs/remotes/origin/release_candidate || exit -1
	    	fi
	    fi
		git checkout -q master
		return
	#else
	#	echo refs/remotes/origin/$1 not found
	fi		
	if git merge-base --is-ancestor refs/heads/$1 refs/remotes/origin/master; then
		if git merge-base --is-ancestor refs/remotes/origin/master refs/heads/$1 ; then
		     	echo $1 Same as Master
		else
			git branch -d $1 || exit -1
			echo $1 deleted
		fi
	else
		echo $1 not merged
	fi
}


update(){
	cd $1 || return
	echo
	pwd
	if [ -d .git ]; then
	    git fetch
	    echo ok
	    git checkout -q master || exit -1
	    git merge -m "merged in remote master" refs/remotes/origin/master || exit -1
	    git gc --prune=now || exit -1
	    for branch in $(git for-each-ref --format='%(refname)' refs/heads/); do
		    check_remove ${branch:11}
	    done
        git checkout -q master
	    if [ -n "$2" ]; then
            git checkout -q $2
        fi
	else
	    echo "Not a git repsoitory"
	fi
	cd ..
}

for D in *; do
	if [ $D = "sPyNNaker7ExtraModelsPlugin" ]; then
		echo "skipping sPyNNaker7ExtraModelsPlugin"
    elif  [ $D = "sPyNNaker8ExtraModelsPlugin" ]; then
		echo "skipping sPyNNaker8ExtraModelsPlugin"
	elif [ -d "${D}" ]; then
        update "${D}" $1 
    fi
done

