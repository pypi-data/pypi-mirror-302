#! /usr/bin/env bash

function test_blue_objects_list() {
    abcli_select

    abcli_upload

    abcli_list cloud

    abcli_list local

    abcli_list "$abcli_path_bash/tests/*.sh"
}
