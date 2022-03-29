param ([String]$implementation = "cpython")

$compose_file = "docker-compose.${implementation}.yml"

docker-compose --file $compose_file up --build --exit-code-from hypothesis_sqlalchemy-${implementation}

$STATUS = $LastExitCode

docker-compose --file $compose_file down --remove-orphans

if ($STATUS -eq 0)
{
    echo "${implementation} tests passed"
}
else
{
    echo "${implementation} tests failed"
}

exit $STATUS
