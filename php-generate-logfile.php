<?php
error_reporting(E_ALL|E_SCRIPT);
define('PATH_BASE', realpath(dirname(__FILE__)));
define('PHPCOP_LOGFILE_PATH', PATH_BASE . '/php.log');
define('PHPCOP_LOGFILE_PATH_AJAX', PATH_BASE . '/php.ajax.log');
require PATH_BASE . '/phpcop_bootstrap.php';

// Generate notice.
function foo($x) {
    $y = 42;
    echo $not_defined;
}
foo(new DateTime());

// Generate warning.
function bar($x) {;}
bar();

// Generate notice.
trigger_error("oops");

// Generate fatal.
require 'foo';
