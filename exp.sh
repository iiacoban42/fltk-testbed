DOCKER_BUILDKIT=1 docker build . --tag gcr.io/qpe-project-14/fltk
docker push gcr.io/qpe-project-14/fltk
cd charts
helm uninstall -n test orchestrator
helm install orchestrator ./orchestrator --namespace test -f fltk-values.yaml
cd ..
