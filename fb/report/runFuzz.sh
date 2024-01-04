# ./bin/bash
cmake -DCMAKE_C_COMPILER=clang-10 -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
      -DCMAKE_C_FLAGS='-fsanitize=fuzzer-no-link,address -fprofile-instr-generate -fcoverage-mapping -g -ggdb3 -O2' \
      ../ -GNinja
ninja

# clean up
rm -rf pf-* fuzz-*.log slow-unit-* all_prof_files default.profdata src.info src_report.info html_output

export ASAN_OPTIONS=detect_leaks=0 
#set the fuzzer profile output format
export LLVM_PROFILE_FILE='pf-%p' 
#run the target in parallel. This will run 8 fuzz jobs in parallel, restrict each run to 10 iterations, and 
#overall will run 100 jobs, using the seed folder SEED, and the corpus folder CORPUS
./src/doom_fuzz -runs=50  CORPUS SEED -jobs=1 -workers=1 -detect_leaks=0 >/dev/null
#check if we have generated any profile files
ls pf-*
#you should see few files like pf-2044576, etc.
# collect all the prof file paths into a single file
ls pf-* > all_prof_files
# merge all prof files into a single file 
llvm-profdata-10 merge -sparse -f all_prof_files -o default.profdata
# export the above file into a format that can be easily parsed
llvm-cov-10 export ./src/doom_fuzz -instr-profile=default.profdata -format=lcov > src.info
# generate text report
lcov -a src.info -o src_report.info
# generate a html visualization of the same report
genhtml -o html_output src_report.info

# clean up
# rm -rf pf-* slow-unit-* all_prof_files default.profdata src.info src_report.info 
