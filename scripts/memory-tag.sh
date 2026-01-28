#!/bin/bash
# Clarke's Memory Tagging System
# Add searchable tags to memory entries

ACTION="$1"
shift

show_usage() {
    echo "Usage:"
    echo "  memory-tag.sh add <file> <tag1> [tag2] [tag3]    - Add tags to a file"
    echo "  memory-tag.sh find <tag>                          - Find all entries with tag"
    echo "  memory-tag.sh list                                - List all tags used"
    echo ""
    echo "Tags format: #topic (e.g., #security #automation #health)"
}

add_tags() {
    local file="$1"
    shift
    local tags="$@"
    
    if [ ! -f "$file" ]; then
        echo "❌ File not found: $file"
        exit 1
    fi
    
    # Add tags to end of file if not already present
    for tag in $tags; do
        # Ensure tag starts with #
        [[ "$tag" != \#* ]] && tag="#$tag"
        
        if ! grep -q "$tag" "$file"; then
            echo "$tag" >> "$file"
            echo "✅ Added tag: $tag"
        else
            echo "ℹ️  Tag already exists: $tag"
        fi
    done
}

find_by_tag() {
    local tag="$1"
    [[ "$tag" != \#* ]] && tag="#$tag"
    
    echo "🔍 Finding entries tagged with: $tag"
    echo ""
    
    # Search in all memory files
    find /root/clawd/memory /root/clawd -maxdepth 1 -name "*.md" -type f -exec grep -l "$tag" {} \; | while read -r file; do
        filename=$(basename "$file")
        echo "📄 $file"
        grep --color=always -C 2 "$tag" "$file"
        echo ""
    done
}

list_all_tags() {
    echo "📋 All tags in memory system:"
    echo ""
    
    find /root/clawd/memory /root/clawd -maxdepth 1 -name "*.md" -type f -exec grep -oh '#[a-zA-Z0-9_-]*' {} \; | sort | uniq -c | sort -rn
}

case "$ACTION" in
    add)
        add_tags "$@"
        ;;
    find)
        find_by_tag "$1"
        ;;
    list)
        list_all_tags
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
