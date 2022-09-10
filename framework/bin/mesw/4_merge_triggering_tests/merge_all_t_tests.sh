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
	out_dir=/home/people/12309511/logging/4_merge_triggering_tests/${str}/
	mkdir --parents "$out_dir"
	sbatch -J ${str}_merge_t_tests -o /dev/null -e ${out_dir}/out_err.err SBATCH_merge_t_tests_by_pid.sh "$str"
done

