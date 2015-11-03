#!/bin/bash


APPS="joker_auth joker_tools joker_model_1 joker_model_2 joker_model_4"


reset_all() {
    rm -rf reset.log

    printf "%-70s" "Cleaning up migrations..."
    for app in $APPS; do
        rm -rf $app/migrations
    done
    printf "done\n"

    printf "%-70s" "Making migrations..."
    for app in $APPS; do
        python manage.py makemigrations $app >>reset.log 2>&1
    done
    printf "done\n"

    printf "%-70s" "Migrating..."
    python manage.py migrate >>reset.log 2>&1
    python manage.py migrate joker_auth --database=auth_db >>reset.log 2>&1
    printf "done\n"
}


reset_all
