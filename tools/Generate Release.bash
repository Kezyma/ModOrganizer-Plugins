#!/bin/bash

run_dir=$(cd "$(dirname "$0")" && pwd)
cd "$run_dir" || exit

echo "Deleting existing release."
rm -rf "../release"

echo "Creating new release directory."
mkdir -p "../release/zip"

echo "Searching for plugins."
for plugin_dir in ../src/plugin/*; do
  if [ -d "$plugin_dir" ]; then
    plugin_name=$(basename "$plugin_dir")

    if [ "$plugin_name" == "curationclub" ]; then
      echo "Skipping $plugin_name."
      continue
    fi

    echo "Creating release for $plugin_name."
    mkdir -p "../release/$plugin_name/"{base,common,plugin}

    echo "Copying plugin files into release."
    cd "../"
    rsync -ar "src/plugin/$plugin_name/" "release/$plugin_name/plugin/$plugin_name/"
    rsync -ar "src/base/" "release/$plugin_name/base/"
    rsync -ar "src/common/" "release/$plugin_name/common/"
    rsync -ar "src/${plugin_name}_init.py" "release/$plugin_name/"

    cd "$run_dir" || exit

    echo "Renaming plugin init file."
    cd "../release/$plugin_name" || exit
    mv "${plugin_name}_init.py" "__init__.py"

    echo "Zipping released mods."
    echo "Zipping $plugin_name."
    cd "../"
    zip -r "zip/$plugin_name.zip" "$plugin_name"
  fi
done
