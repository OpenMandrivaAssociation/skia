#!/bin/sh
rm -rf skia
git clone --depth=1 https://github.com/google/skia.git
cd skia
rm -rf .git
INTERESTING=false
cat DEPS |while read l; do
	l="$(echo $l |sed -e 's,#.*,,')"
	[ -z "$l" ] && continue
	if [ "$l" = "deps = {" ]; then
		INTERESTING=true
		continue
	fi
	[ "$l" = "'bin': {" ] && INTERESTING=false
	$INTERESTING || continue
	echo $l
	D=$(echo $l |cut -d'"' -f2)
	G=$(echo $l |cut -d'"' -f4)
	if echo $D |grep -q /; then
		SD=$(dirname $D)
		mkdir -p $SD
		pushd $SD
	fi
	R=$(echo $G|cut -d'@' -f1)
	C=$(echo $G|cut -d'@' -f2)
	git clone --depth=1 $R $(basename $D)
	cd $(basename $D)
	git fetch --depth=1 origin $C
	git reset $C --hard
	rm -rf .git
#	git checkout -b skia $C
	cd ..
	if echo $D |grep -q /; then
		popd
	fi
done
cd ..
tar cf skia-$(date +%Y%m%d).tar skia
zstd -f --rm --ultra -22 *.tar
