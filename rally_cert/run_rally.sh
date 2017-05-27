#!/bin/bash

cd ${SCENARIOS_DIR}
SCENARIOS=`find ${SCENARIOS_NAMES} \( -name "*.json" -or -name "*.yaml" \) | uniq`
cd -

if (( $? != 0 )); then
    echo "ERROR: Can't find scenarios, check again!!!"
fi

for SCENARIO in ${SCENARIOS}; do
    BASENAME=$(basename -s .json -s .yaml ${SCENARIO})
    LOG=${BASENAME}.log

    echo ${BASENAME}

    rally --debug --log-dir ${ARTIFACTS_DIR} --log-file $LOG \
        task start --tag ${BASENAME} --task-args-file ${JOB_PARAMS_CONFIG} \
        ${SCENARIOS_DIR}/$SCENARIO #2>&1 | tee ${ARTIFACTS_DIR}/rally.log | grep -Ew "ITER|ERROR" || true
done
