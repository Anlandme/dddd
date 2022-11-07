#!/bin/bash

PROJ_DIR=$(dirname $(pwd))


function config() {
  if [[ ! $1 ]]; then
    if [[ ! $PROJ_ENV ]]; then
      PROJ_ENV='prod'
    else
      PROJ_ENV=$PROJ_ENV
    fi
  else
    PROJ_ENV=$1
  fi

  CONF_DIR="${PROJ_DIR}/conf_${PROJ_ENV}"
  cp ${CONF_DIR}/* ${PROJ_DIR}/conf/
  echo "[SUCCESS] cp conf_${PROJ_ENV}/* conf/"
}


config $1
echo "Usage Example: ./config.sh [dev|test|prod|prod_xxx] (default param is prod)"
