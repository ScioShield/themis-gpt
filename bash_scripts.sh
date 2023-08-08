== script 1 ==
technique_pattern='\[\[rule\.threat\.technique\]\]'

for file in *.toml; do
    # grep returns 0 if the pattern is found, and 1 otherwise
    if ! grep -q "$technique_pattern" "$file"; then
        rm $file
    fi
done

== script 2 ==

find . -type f -exec wc -w {} + | grep -v "total" | awk '$1 > 950 {print $2}' | while read -r file; do
    mv "$file" /tmp/rules/
done