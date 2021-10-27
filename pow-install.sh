#!/usr/bin/env bash

set -eo pipefail
shopt -s nullglob

pow_base_url="https://raw.githubusercontent.com/gabrys/pow/main"

case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)
    os="linux"
	 ;;
  Darwin-x86_64)
    os="macos"
	 ;;
  *)
    os=""
	 ;;
esac

# Where we'll install pow Python files:
pow_dir=""
pow_dir_candidates=(
 /opt/pow
 /usr/local/pow
 ~/.pow
)

# Where we'll install pow script:
bin_dir=""
bin_dir_candidates=(
  ~/.local/bin
  ~/bin
  /usr/local/bin
  /usr/bin
  /opt/bin
)

die() {
  echo "$@" 1>&2
  exit 1
}

is_good_path() {
  [ -d "$1" ] || return 1
  [ -w "$1" ] || return 1

  for dir in "${bin_dir_candidates[@]}"; do
    if [ "$1" = "$dir" ]; then
	   return 0
	 fi
  done

  return 1
}

if [ "$os" = "" ]; then
  die "Unsupported OS/CPU. Only x86_64 Linux and Macs are supported by this installer"
fi

IFS=':' read -r -a path_dirs <<< "$PATH"

for dir in "${path_dirs[@]}"; do
  if is_good_path "$dir"; then
  	 bin_dir="$dir"
    break
  fi
done

current_pow_location=""
if command -v pow > /dev/null; then
  current_pow_location="$(command -v pow)"
  if [ "$bin_dir" != "" ] && [ "$current_pow_location" != "$bin_dir/pow" ]; then
    die "Found previous pow script installed at $current_pow_location. Please remove and retry"
  fi
fi

for dir in "${pow_dir_candidates[@]}"; do
  if [ -d "$dir" ]; then
    pow_dir="$dir"
	 break
  fi
done

if [ "$pow_dir" != "" ] && ! [ -w "$pow_dir" ]; then
  die "Found a directory to install pow to ($dir) but it's not accessible for writing. Please remove and retry"
fi

if [ "$pow_dir" = "" ]; then
  for dir in "${pow_dir_candidates[@]}"; do
    mkdir -p "$dir" 2>/dev/null || true
	 if [ -d "$dir" ]; then
	   pow_dir="$dir"
		break
	 fi
  done
fi

if [ "$pow_dir" = "" ]; then
  die "Couldn't find an appropriate directory to install pow into (tried ${pow_dir_candidates[*]})"
fi

echo "Putting pow files to $pow_dir and installing the pow script to $bin_dir/pow"

curl -sL "$pow_base_url/$os/pow-runner" > "$pow_dir/pow-runner"
curl -sL "$pow_base_url/src/pow.py" > "$pow_dir/pow.py"
chmod +x "$pow_dir/pow-runner"

cat > "$bin_dir/pow" <<< "#!/usr/bin/env bash
exec $pow_dir/pow-runner $pow_dir/pow.py \"\$@\""
chmod +x "$bin_dir/pow"

echo "Done. Verify by calling pow"
