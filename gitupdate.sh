check_remove(){
	if [ $1 = "master" ]; then 
		return 
	fi
	if git ls-remote --heads | grep -sw $1>/dev/null; then
		echo $1 Still on remote
		git checkout $1
		git merge refs/remotes/origin/master || exit -1
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
	git fetch
	git checkout -q master || exit -1
	git merge refs/remotes/origin/master || exit -1
	# for branch in $(git for-each-ref --format='%(refname)' ); do
	#	echo $branch
	# done
	for branch in $(git for-each-ref --format='%(refname)' refs/heads/); do
		check_remove ${branch:11}
	done
	git checkout -q $2
	cd ..
}

for D in *; do
    if [ -d "${D}" ]; then
        update "${D}" $1 
    fi
done

