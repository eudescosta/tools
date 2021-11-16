
to create app in ocp
``` oc new-app https://github.com/eudescosta/webhook ```

``` oc svn/webhook ```

to get installed resources
``` oc get all --selector app=webhook -o name ```

to delete installed resources
``` oc delete all --selector app=webhook -o name ```