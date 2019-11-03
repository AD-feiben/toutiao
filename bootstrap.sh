#!/bin/bash

BASEDIR=`pwd`
APP_NAME=$(basename ${BASEDIR})
MAIN_PY=main.py

case "$1" in
  start)
    procedure=`ps -ef | grep -w "${BASEDIR}" | grep -w "python" | grep -v "grep" | awk '{print $2}'`
    if [ "${procedure}" = "" ];
    then
      echo "app start ..."
      rm -f nohup.out
      exec nohup python3 ${BASEDIR}/${MAIN_PY} --log-file-prefix ${APP_NAME}.log &
    else
                        echo "${APP_NAME} was start"
                fi
    ;;
  run)
    procedure=`ps -ef | grep -w "${BASEDIR}" |grep -w "python"| grep -v "grep" | awk '{print $2}'`
                if [ "${procedure}" = "" ];
                then
                        echo "${APP_NAME} start ..."
      rm -f nohup.out
                        exec python3 ${BASEDIR}/${MAIN_PY}
                else
                        echo "${APP_NAME} was start"
                fi
                ;;
  stop)
    procedure=`ps -ef | grep -w "${BASEDIR}" | grep -w "python"| grep -v "grep" | awk '{print $2}'`
                if [ "${procedure}" = "" ];
    then
                        echo "${APP_NAME} was stop"
                else
                        kill ${procedure}
                        sleep 2
                        arg_procedure=`ps -ef | grep -w "${BASEDIR}" |grep -w "python"| grep -v "grep" | awk '{print $2}'`
                        if [ "${arg_procedure}" = "" ];
                        then
                                echo "${APP_NAME}(${procedure}) stop success"
                        else
                                kill -9 ${arg_procedure}
                                echo "${APP_NAME} stop error"
                        fi
                fi
                rm -f nohup.out
                ;;
  status)
    procedure=`ps -ef | grep -w "${BASEDIR}" | grep -w "python" | grep -v "grep" | awk '{print $2}'`
                if ["${procedure}" = ""];
    then
                echo "${APP_NAME} not run"
                echo "info:"
                echo nohup.out
    else
                echo "${APP_NAME} is running"
    fi
    ;;
  *)
                echo "usage: $0 [start|run|stop|status]"
                ;;
esac
exit 0
