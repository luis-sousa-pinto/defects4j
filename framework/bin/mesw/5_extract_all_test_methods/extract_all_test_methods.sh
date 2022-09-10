#!/bin/bash

projects=(
        Chart
        Cli
        Closure
        Codec
        Collections
        Compress
        Csv
        Gson
        JacksonCore
        JacksonDatabind
        JacksonXml
        Jsoup
        JxPath
        Lang
        Math
        Mockito
        Time
)

for str in "${projects[@]}"; do
        sbatch -J ${str}_extract_test_methods -o /dev/null -e /dev/null SBATCH_extract_proj_methods.sh "$str"
done
