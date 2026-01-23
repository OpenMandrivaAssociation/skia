#!/bin/sh
rm -rf skia
V=$(cat *.spec |grep '^Version:' |head -n1 |awk '{ print $2; }' |cut -d. -f1)
git clone -b chrome/m${V} --depth=1 https://github.com/google/skia.git
cd skia
rm -rf .git
INTERESTING=false
cat DEPS |while read l; do
	l="$(echo $l |sed -e 's,#.*,,' |tr "'" '"')"
	[ -z "$l" ] && continue
	if [ "$l" = "deps = {" ]; then
		INTERESTING=true
		continue
	fi
	[ "$l" = '"bin": {' ] && INTERESTING=false
	$INTERESTING || continue
	D=$(echo $l |cut -d'"' -f2)
	G=$(echo $l |cut -d'"' -f4)
	# skia.googlesource.com and chromium.googlesource.com's github
	# and gitlab mirrors are defunct -- but still referenced in
	# skia 144
	# fortunately determining the real upstream repository is
	# as easy as removing the mirror's prefix
	G=$(echo $G |sed -e 's,skia\.googlesource\.com/external/,,;s,chromium\.googlesource\.com/external/,,')
	echo $l - $G
	if echo $D |grep -q /; then
		SD=$(dirname $D)
		mkdir -p $SD
		pushd $SD
	fi
	R=$(echo $G|cut -d'@' -f1)
	C=$(echo $G|cut -d'@' -f2)
	chmod 0755 .
	git clone --depth=1 $R $(basename $D)
	cd $(basename $D)
	git fetch --depth=1 origin $C
	git reset $C --hard
	git checkout -b skia $C || :
	rm -rf .git
	cd ..
	if echo $D |grep -q /; then
		popd
	fi
done
cd ..
tar cf skia-${V}.$(date +%Y%m%d).tar skia
zstd -f --rm --ultra -22 *.tar
