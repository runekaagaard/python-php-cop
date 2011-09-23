<?php

if(!empty($_SERVER['HTTP_X_REQUESTED_WITH']) 
    && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest'
    && defined('PHPCOP_LOGFILE_PATH_AJAX')
    && PHPCOP_LOGFILE_PATH_AJAX) 
{
    ini_set('error_log', PHPCOP_LOGFILE_PATH_AJAX); 
} elseif (defined('PHPCOP_LOGFILE_PATH') && PHPCOP_LOGFILE_PATH) {
    ini_set('error_log', PHPCOP_LOGFILE_PATH); 
}

ini_set('display_errors', FALSE);
ini_set('html_errors', FALSE);
ini_set('log_errors', TRUE);
ini_set('xdebug.auto_trace', 1);
ini_set('xdebug.collect_assignments', 1);
ini_set('xdebug.collect_params', 4);
ini_set('xdebug.collect_return', 1);
ini_set('xdebug.scream', 1);
ini_set('xdebug.show_local_vars', 1);
ini_set('xdebug.trace_format', 1);
ini_set('xdebug.auto_trace', 1);


