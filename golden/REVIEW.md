# Golden set review

For each question below:

1. Read the **question**: would a real user ask this? Is it clear and about Kubernetes v1.33?
2. Read the **documentation excerpts**: do they really answer the question? Is an obviously
   better section missing?
3. Read the **reference answer**: is it correct *according to the excerpts*?
4. Tick **exactly one** box (replace `[ ]` with `[x]`). If you pick *Needs changes*, write what
   to change under **Notes**.

**Out-of-scope questions** are tests that the system *refuses* to answer. If the question really
is outside the Kubernetes docs, tick **Correct as written** (it stays in the set as a refusal
test). Tick **Reject** only if it should be removed from the set.

When done, run: `uv run driftrag-golden apply --reviewer "Your Name"`

---

### `run-as-user`

**Question** (en, task): How do I make the processes in a container run as a specific non-root user?

**Reference answer:** Set `runAsUser` in the Pod's `securityContext` (it applies to all containers) or in a container's `securityContext` (which overrides the Pod-level value for that container). `runAsGroup` is shown at Pod level.

**Relevant documentation:**
- `tasks/configure-pod-container/security-context.md`, section: *Configure a Security Context for a Pod or Container > Set the security context for a Pod*
  > [Configure a Security Context for a Pod or Container > Set the security context for a Pod]
  > To specify security settings for a Pod, include the `securityContext` field
  > in the Pod specification. The `securityContext` field is a
  > PodSecurityContext object.
  > The security settings that you specify for a Pod apply to all Containers in the Pod.
  > Here is a configuration file for a Pod that has a `securityContext` and an `emptyDir` volume:
  > Example file `pods/security/security-context.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo
  > spec:
  >   securityContext:
  >     runAsUser: 1000
  >     runAsGroup: 3000
  >     fsGroup: 2000
  >     supplementalGroups: [4000]
  >   volumes:
  >   - name: sec-ctx-vol
  >     emptyDir: {}
  >   containers:
  >   - name: sec-ctx-demo
  >     image: busybox:1.28
  >     command: [ "sh", "-c", "sleep 1h" ]
  >     volumeMounts:
  >     - name: sec-ctx-vol
  >       mountPath: /data/demo
  >     securityContext:
  >       allowPrivilegeEscalation: false
  > ```
  > In the configuration file, the `runAsUser` field specifies that for any Containers in
  > the Pod, all processes run with user ID 1000. The `runAsGroup` field specifies the primary group ID of 3000 for
  > all processes within any containers of the Pod. If this field is omitted, the primary group ID of the containers
  > will be root(0). Any files created will also be owned by user 1000 and group 3000 when `runAsGroup` is specified.
  > Since `fsGroup` field is specified, all processes of the container are also part of the supplementary group ID 2000.
  > The owner for volume `/data/demo` and any files created in that volume will be Group ID 2000.
  > Additionally, when the `supplementalGroups` field is specified, all processes of the container are also part of the
  > specified groups. If this field is omitted, it means empty.
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context.yaml
  > ```
  > Verify that the Pod's Container is running:
  > ```shell
  > kubectl get pod security-context-demo
  > ```
  > Get a shell to the running Container:
  > ```shell
  > kubectl exec -it security-context-demo -- sh
  > ```
  > In your shell, list the running processes:
  > ```shell
  > ps
  > ```
  > ```shell
  > ps
  > ```
  > The output shows that the processes are running as user 1000, which is the value of `runAsUser`:
  > ```none
  > PID   USER     TIME  COMMAND
  >     1 1000      0:00 sleep 1h
  >     6 1000      0:00 sh
  > ...
  > ```
  > In your shell, navigate to `/data`, and list the one directory:
  > ```shell
  > cd /data
  > ls -l
  > ```
  > The output shows that the `/data/demo` directory has group ID 2000, which is
  > the value of `fsGroup`.
  > ```none
  > drwxrwsrwx 2 root 2000 4096 Jun  6 20:08 demo
  > ```
  > In your shell, navigate to `/data/demo`, and create a file:
  > ```shell
  > cd demo
  > echo hello > testfile
  > ```
  > List the file in the `/data/demo` directory:
  > ```shell
  > ls -l
  > ```
  > The output shows that `testfile` has group ID 2000, which is the value of `fsGroup`.
  > ```none
  > -rw-r--r-- 1 1000 2000 6 Jun  6 20:08 testfile
  > ```
  > Run the following command:
  > ```shell
  > id
  > ```
  > The output is similar to this:
  > ```none
  > uid=1000 gid=3000 groups=2000,3000,4000
  > ```
  > ```none
  > uid=1000 gid=3000 groups=2000,3000,4000
  > ```
  > From the output, you can see that `gid` is 3000 which is same as the `runAsGroup` field.
  > If the `runAsGroup` was omitted, the `gid` would remain as 0 (root) and the process will
  > be able to interact with files that are owned by the root(0) group and groups that have
  > the required group permissions for the root (0) group. You can also see that `groups`
  > contains the group IDs which are specified by `fsGroup` and `supplementalGroups`,
  > in addition to `gid`.
  > Exit your shell:
  > ```shell
  > exit
  > ```
  > [Configure a Security Context for a Pod or Container > Set the security context for a Pod > Implicit group memberships defined in `/etc/group` in the container image]
  > By default, kubernetes merges group information from the Pod with information defined in `/etc/group` in the container image.
  > Example file `pods/security/security-context-5.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo
  > spec:
  >   securityContext:
  >     runAsUser: 1000
  >     runAsGroup: 3000
  >     supplementalGroups: [4000]
  >   containers:
  >   - name: sec-ctx-demo
  >     image: registry.k8s.io/e2e-test-images/agnhost:2.45
  >     command: [ "sh", "-c", "sleep 1h" ]
  >     securityContext:
  >       allowPrivilegeEscalation: false
  > ```
  > This Pod security context contains `runAsUser`, `runAsGroup` and `supplementalGroups`.
  > However, you can see that the actual supplementary groups attached to the container process
  > will include group IDs which come from `/etc/group` in the container image.
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context-5.yaml
  > ```
  > Verify that the Pod's Container is running:
  > ```shell
  > kubectl get pod security-context-demo
  > ```
  > Get a shell to the running Container:
  > ```shell
  > kubectl exec -it security-context-demo -- sh
  > ```
  > Check the process identity:
  > ```shell
  > $ id
  > ```
  > The output is similar to this:
  > The output is similar to this:
  > ```none
  > uid=1000 gid=3000 groups=3000,4000,50000
  > ```
  > You can see that `groups` includes group ID `50000`. This is because the user (`uid=1000`),
  > which is defined in the image, belongs to the group (`gid=50000`), which is defined in `/etc/group`
  > inside the container image.
  > Check the `/etc/group` in the container image:
  > ```shell
  > $ cat /etc/group
  > ```
  > You can see that uid `1000` belongs to group `50000`.
  > ```none
  > ...
  > user-defined-in-image:x:1000:
  > group-defined-in-image:x:50000:user-defined-in-image
  > ```
  > Exit your shell:
  > ```shell
  > exit
  > ```
  > _Implicitly merged_ supplementary groups may cause security problems particularly when accessing
  > the volumes (see kubernetes/kubernetes#112879 for details).
  > If you want to avoid this. Please see the below section.
- `tasks/configure-pod-container/security-context.md`, section: *Configure a Security Context for a Pod or Container > Set the security context for a Container*
  > [Configure a Security Context for a Pod or Container > Set the security context for a Container]
  > To specify security settings for a Container, include the `securityContext` field
  > in the Container manifest. The `securityContext` field is a
  > SecurityContext object.
  > Security settings that you specify for a Container apply only to
  > the individual Container, and they override settings made at the Pod level when
  > there is overlap. Container settings do not affect the Pod's Volumes.
  > Here is the configuration file for a Pod that has one Container. Both the Pod
  > and the Container have a `securityContext` field:
  > Example file `pods/security/security-context-2.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo-2
  > spec:
  >   securityContext:
  >     runAsUser: 1000
  >   containers:
  >   - name: sec-ctx-demo-2
  >     image: gcr.io/google-samples/hello-app:2.0
  >     securityContext:
  >       runAsUser: 2000
  >       allowPrivilegeEscalation: false
  > ```
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context-2.yaml
  > ```
  > Verify that the Pod's Container is running:
  > ```shell
  > kubectl get pod security-context-demo-2
  > ```
  > Get a shell into the running Container:
  > ```shell
  > kubectl exec -it security-context-demo-2 -- sh
  > ```
  > ```shell
  > kubectl exec -it security-context-demo-2 -- sh
  > ```
  > In your shell, list the running processes:
  > ```shell
  > ps aux
  > ```
  > The output shows that the processes are running as user 2000. This is the value
  > of `runAsUser` specified for the Container. It overrides the value 1000 that is
  > specified for the Pod.
  > ```
  > USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
  > 2000         1  0.0  0.0   4336   764 ?        Ss   20:36   0:00 /bin/sh -c node server.js
  > 2000         8  0.1  0.5 772124 22604 ?        Sl   20:36   0:00 node server.js
  > ...
  > ```
  > Exit your shell:
  > ```shell
  > exit
  > ```

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 1 (Youssef Zemzem, 2026-11-07): runAsGroup described at Pod level only, as documented

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `linux-capabilities`

**Question** (en, task): How do I add Linux capabilities to a container?

**Reference answer:** Use `securityContext.capabilities` in the container spec and list the capabilities to `add` (e.g. `NET_ADMIN`, `SYS_TIME`).

**Relevant documentation:**
- `tasks/configure-pod-container/security-context.md`, section: *Configure a Security Context for a Pod or Container > Set capabilities for a Container*
  > [Configure a Security Context for a Pod or Container > Set capabilities for a Container]
  > With Linux capabilities,
  > you can grant certain privileges to a process without granting all the privileges
  > of the root user. To add or remove Linux capabilities for a Container, include the
  > `capabilities` field in the `securityContext` section of the Container manifest.
  > First, see what happens when you don't include a `capabilities` field.
  > Here is configuration file that does not add or remove any Container capabilities:
  > Example file `pods/security/security-context-3.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo-3
  > spec:
  >   containers:
  >   - name: sec-ctx-3
  >     image: gcr.io/google-samples/hello-app:2.0
  > ```
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context-3.yaml
  > ```
  > Verify that the Pod's Container is running:
  > ```shell
  > kubectl get pod security-context-demo-3
  > ```
  > Get a shell into the running Container:
  > ```shell
  > kubectl exec -it security-context-demo-3 -- sh
  > ```
  > In your shell, list the running processes:
  > ```shell
  > ps aux
  > ```
  > The output shows the process IDs (PIDs) for the Container:
  > The output shows the process IDs (PIDs) for the Container:
  > ```
  > USER  PID %CPU %MEM    VSZ   RSS TTY   STAT START   TIME COMMAND
  > root    1  0.0  0.0   4336   796 ?     Ss   18:17   0:00 /bin/sh -c node server.js
  > root    5  0.1  0.5 772124 22700 ?     Sl   18:17   0:00 node server.js
  > ```
  > In your shell, view the status for process 1:
  > ```shell
  > cd /proc/1
  > cat status
  > ```
  > The output shows the capabilities bitmap for the process:
  > ```
  > ...
  > CapPrm:	00000000a80425fb
  > CapEff:	00000000a80425fb
  > ...
  > ```
  > Make a note of the capabilities bitmap, and then exit your shell:
  > ```shell
  > exit
  > ```
  > Next, run a Container that is the same as the preceding container, except
  > that it has additional capabilities set.
  > Here is the configuration file for a Pod that runs one Container. The configuration
  > adds the `CAP_NET_ADMIN` and `CAP_SYS_TIME` capabilities:
  > Example file `pods/security/security-context-4.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: security-context-demo-4
  > spec:
  >   containers:
  >   - name: sec-ctx-4
  >     image: gcr.io/google-samples/hello-app:2.0
  >     securityContext:
  >       capabilities:
  >         add: ["NET_ADMIN", "SYS_TIME"]
  > ```
  > Create the Pod:
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/security/security-context-4.yaml
  > ```
  > Get a shell into the running Container:
  > ```shell
  > kubectl exec -it security-context-demo-4 -- sh
  > ```
  > In your shell, view the capabilities for process 1:
  > ```shell
  > cd /proc/1
  > cat status
  > ```
  > The output shows capabilities bitmap for the process:
  > ```
  > ...
  > CapPrm:	00000000aa0435fb
  > CapEff:	00000000aa0435fb
  > ...
  > ```
  > Compare the capabilities of the two Containers:
  > ```
  > 00000000a80425fb
  > 00000000aa0435fb
  > ```
  > In the capability bitmap of the first container, bits 12 and 25 are clear. In the second container,
  > bits 12 and 25 are set. Bit 12 is `CAP_NET_ADMIN`, and bit 25 is `CAP_SYS_TIME`.
  > See capability.h
  > for definitions of the capability constants.
  > Linux capability constants have the form `CAP_XXX`.
  > But when you list capabilities in your container manifest, you must
  > omit the `CAP_` portion of the constant.
  > For example, to add `CAP_SYS_TIME`, include `SYS_TIME` in your list of capabilities.

*Drafting note:* golden v2 draft (2026-11-07) | self-check: aligned with the referenced text | human review v2 batch 1 (Youssef Zemzem, 2026-11-07): question narrowed to adding capabilities (removing them isn't documented in the section)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `pod-service-account`

**Question** (en, task): How do I make a pod use a specific service account?

**Reference answer:** Set `spec.serviceAccountName` in the Pod spec; otherwise the namespace's `default` ServiceAccount is used.

**Relevant documentation:**
- `tasks/configure-pod-container/configure-service-account.md`, section: *Configure Service Accounts for Pods > Use more than one ServiceAccount*
  > [Configure Service Accounts for Pods > Use more than one ServiceAccount {#use-multiple-service-accounts}]
  > Every namespace has at least one ServiceAccount: the default ServiceAccount
  > resource, called `default`. You can list all ServiceAccount resources in your
  > current namespace
  > with:
  > ```shell
  > kubectl get serviceaccounts
  > ```
  > The output is similar to this:
  > ```
  > NAME      SECRETS    AGE
  > default   1          1d
  > ```
  > You can create additional ServiceAccount objects like this:
  > ```shell
  > kubectl apply -f - <<EOF
  > apiVersion: v1
  > kind: ServiceAccount
  > metadata:
  >   name: build-robot
  > EOF
  > ```
  > The name of a ServiceAccount object must be a valid
  > DNS subdomain name.
  > If you get a complete dump of the service account object, like this:
  > ```shell
  > kubectl get serviceaccounts/build-robot -o yaml
  > ```
  > The output is similar to this:
  > ```yaml
  > apiVersion: v1
  > kind: ServiceAccount
  > metadata:
  >   creationTimestamp: 2019-06-16T00:12:34Z
  >   name: build-robot
  >   namespace: default
  >   resourceVersion: "272500"
  >   uid: 721ab723-13bc-11e5-aec2-42010af0021e
  > ```
  > You can use authorization plugins to
  > set permissions on service accounts.
  > To use a non-default service account, set the `spec.serviceAccountName`
  > field of a Pod to the name of the ServiceAccount you wish to use.
  > To use a non-default service account, set the `spec.serviceAccountName`
  > field of a Pod to the name of the ServiceAccount you wish to use.
  > You can only set the `serviceAccountName` field when creating a Pod, or in a
  > template for a new Pod. You cannot update the `.spec.serviceAccountName` field
  > of a Pod that already exists.
  > The `.spec.serviceAccount` field is a deprecated alias for `.spec.serviceAccountName`.
  > If you want to remove the fields from a workload resource, set both fields to empty explicitly
  > on the pod template.
  > [Configure Service Accounts for Pods > Use more than one ServiceAccount {#use-multiple-service-accounts} > Cleanup {#cleanup-use-multiple-service-accounts}]
  > If you tried creating `build-robot` ServiceAccount from the example above,
  > you can clean it up by running:
  > ```shell
  > kubectl delete serviceaccount/build-robot
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `share-process-ns`

**Question** (en, task): How can containers in the same pod see each other's processes?

**Reference answer:** Set `shareProcessNamespace: true` in the Pod spec.

**Relevant documentation:**
- `tasks/configure-pod-container/share-process-namespace.md`, section: *Share Process Namespace between Containers in a Pod > Configure a Pod*
  > [Share Process Namespace between Containers in a Pod > Configure a Pod]
  > Process namespace sharing is enabled using the `shareProcessNamespace` field of
  > `.spec` for a Pod. For example:
  > Example file `pods/share-process-namespace.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: nginx
  > spec:
  >   shareProcessNamespace: true
  >   containers:
  >   - name: nginx
  >     image: nginx
  >   - name: shell
  >     image: busybox:1.28
  >     command: ["sleep", "3600"]
  >     securityContext:
  >       capabilities:
  >         add:
  >         - SYS_PTRACE
  >     stdin: true
  >     tty: true
  > ```
  > 1. Create the pod `nginx` on your cluster:
  >    ```shell
  >    kubectl apply -f https://k8s.io/examples/pods/share-process-namespace.yaml
  >    ```
  > 1. Attach to the `shell` container and run `ps`:
  >    ```shell
  >    kubectl exec -it nginx -c shell -- /bin/sh
  >    ```
  >    If you don't see a command prompt, try pressing enter. In the container shell:
  >    ```shell
  >    # run this inside the "shell" container
  >    ps ax
  >    ```
  >    The output is similar to this:
  >    ```none
  >    PID   USER     TIME  COMMAND
  >        1 root      0:00 /pause
  >        8 root      0:00 nginx: master process nginx -g daemon off;
  >       14 101       0:00 nginx: worker process
  >       15 root      0:00 sh
  >       21 root      0:00 ps ax
  >    ```
  > You can signal processes in other containers. For example, send `SIGHUP` to
  > `nginx` to restart the worker process. This requires the `SYS_PTRACE` capability.
  > ```shell
  > # run this inside the "shell" container
  > kill -HUP 8   # change "8" to match the PID of the nginx leader process, if necessary
  > ps ax
  > ```
  > The output is similar to this:
  > ```none
  > PID   USER     TIME  COMMAND
  >     1 root      0:00 /pause
  >     8 root      0:00 nginx: master process nginx -g daemon off;
  >    15 root      0:00 sh
  >    22 101       0:00 nginx: worker process
  >    23 root      0:00 ps ax
  > ```
  > It's even possible to access the file system of another container using the
  > `/proc/$pid/root` link.
  > ```shell
  > # run this inside the "shell" container
  > # change "8" to the PID of the Nginx process, if necessary
  > head /proc/8/root/etc/nginx/nginx.conf
  > ```
  > The output is similar to this:
  > ```none
  > user  nginx;
  > worker_processes  1;
  > error_log  /var/log/nginx/error.log warn;
  > pid        /var/run/nginx.pid;
  > events {
  >     worker_connections  1024;
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `init-prepare-files`

**Question** (en, task): How do I use an init container to prepare files before my app container starts?

**Reference answer:** The init container writes the files into a shared volume (e.g. `emptyDir`) that the app container also mounts; the app starts only after the init container completes.

**Relevant documentation:**
- `tasks/configure-pod-container/configure-pod-initialization.md`, section: *Configure Pod Initialization > Create a Pod that has an Init Container*
  > [Configure Pod Initialization > Create a Pod that has an Init Container]
  > In this exercise you create a Pod that has one application Container and one
  > Init Container. The init container runs to completion before the application
  > container starts.
  > Here is the configuration file for the Pod:
  > Example file `pods/init-containers.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: init-demo
  > spec:
  >   containers:
  >   - name: nginx
  >     image: nginx
  >     ports:
  >     - containerPort: 80
  >     volumeMounts:
  >     - name: workdir
  >       mountPath: /usr/share/nginx/html
  >   # These containers are run during pod initialization
  >   initContainers:
  >   - name: install
  >     image: busybox:1.28
  >     command:
  >     - wget
  >     - "-O"
  >     - "/work-dir/index.html"
  >     - http://info.cern.ch
  >     volumeMounts:
  >     - name: workdir
  >       mountPath: "/work-dir"
  >   dnsPolicy: Default
  >   volumes:
  >   - name: workdir
  >     emptyDir: {}
  > ```
  > In the configuration file, you can see that the Pod has a Volume that the init
  > container and the application container share.
  > The init container mounts the
  > shared Volume at `/work-dir`, and the application container mounts the shared
  > Volume at `/usr/share/nginx/html`. The init container runs the following command
  > and then terminates:
  > ```shell
  > wget -O /work-dir/index.html http://info.cern.ch
  > ```
  > Notice that the init container writes the `index.html` file in the root directory
  > of the nginx server.
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/init-containers.yaml
  > ```
  > Verify that the nginx container is running:
  > ```shell
  > kubectl get pod init-demo
  > ```
  > The output shows that the nginx container is running:
  > ```
  > NAME        READY     STATUS    RESTARTS   AGE
  > init-demo   1/1       Running   0          1m
  > ```
  > Get a shell into the nginx container running in the init-demo Pod:
  > ```shell
  > kubectl exec -it init-demo -- /bin/bash
  > ```
  > In your shell, send a GET request to the nginx server:
  > ```
  > root@nginx:~# apt-get update
  > root@nginx:~# apt-get install curl
  > root@nginx:~# curl localhost
  > ```
  > The output shows that nginx is serving the web page that was written by the init container:
  > ```html
  > <html><head></head><body><header>
  > <title>http://info.cern.ch</title>
  > </header>
  > <h1>http://info.cern.ch - home of the first website</h1>
  >   ...
  >   <li><a href="http://info.cern.ch/hypertext/WWW/TheProject.html">Browse the first website</a></li>
  >   ...
  > ```
  > ##
  > ##
  > * Learn more about
  >   communicating between Containers running in the same Pod.
  > * Learn more about Init Containers.
  > * Learn more about Volumes.
  > * Learn more about Debugging Init Containers

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `update-image-rollout`

**Question** (en, task): How do I update a Deployment to a new image version and watch the rollout?

**Reference answer:** Change the image (edit and `kubectl apply` the manifest, or `kubectl set image`), then follow it with `kubectl rollout status deployment/<name>`.

**Relevant documentation:**
- `tasks/run-application/run-stateless-application-deployment.md`, section: *Run a Stateless Application Using a Deployment > Updating the deployment*
  > [Run a Stateless Application Using a Deployment > Updating the deployment]
  > You can update the deployment by applying a new YAML file. This YAML file
  > specifies that the deployment should be updated to use nginx 1.16.1.
  > Example file `application/deployment-update.yaml`:
  > ```yaml
  > apiVersion: apps/v1
  > kind: Deployment
  > metadata:
  >   name: nginx-deployment
  > spec:
  >   selector:
  >     matchLabels:
  >       app: nginx
  >   replicas: 2
  >   template:
  >     metadata:
  >       labels:
  >         app: nginx
  >     spec:
  >       containers:
  >       - name: nginx
  >         image: nginx:1.16.1 # Update the version of nginx from 1.14.2 to 1.16.1
  >         ports:
  >         - containerPort: 80
  > ```
  > 1. Apply the new YAML file:
  >    ```shell
  >    kubectl apply -f https://k8s.io/examples/application/deployment-update.yaml
  >    ```
  > 1. Watch the deployment create pods with new names and delete the old pods:
  >    ```shell
  >    kubectl get pods -l app=nginx
  >    ```
- `concepts/workloads/controllers/deployment.md`, section: *Deployments > Updating a Deployment*
  > [Deployments > Updating a Deployment]
  > A Deployment's rollout is triggered if and only if the Deployment's Pod template (that is, `.spec.template`)
  > is changed, for example if the labels or container images of the template are updated. Other updates, such as scaling the Deployment, do not trigger a rollout.
  > Follow the steps given below to update your Deployment:
  > 1. Let's update the nginx Pods to use the `nginx:1.16.1` image instead of the `nginx:1.14.2` image.
  >    ```shell
  >    kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.16.1
  >    ```
  >    or use the following command:
  >    ```shell
  >    kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1
  >    ```
  >    where `deployment/nginx-deployment` indicates the Deployment,
  >    `nginx` indicates the Container the update will take place and
  >    `nginx:1.16.1` indicates the new image and its tag.
  >    The output is similar to:
  >    ```
  >    deployment.apps/nginx-deployment image updated
  >    ```
  >    Alternatively, you can `edit` the Deployment and change `.spec.template.spec.containers[0].image` from `nginx:1.14.2` to `nginx:1.16.1`:
  >    ```shell
  >    kubectl edit deployment/nginx-deployment
  >    ```
  >    The output is similar to:
  >    The output is similar to:
  >    ```
  >    deployment.apps/nginx-deployment edited
  >    ```
  > 2. To see the rollout status, run:
  >    ```shell
  >    kubectl rollout status deployment/nginx-deployment
  >    ```
  >    The output is similar to this:
  >    ```
  >    Waiting for rollout to finish: 2 out of 3 new replicas have been updated...
  >    ```
  >    or
  >    ```
  >    deployment "nginx-deployment" successfully rolled out
  >    ```
  > Get more details on your updated Deployment:
  > * After the rollout succeeds, you can view the Deployment by running `kubectl get deployments`.
  >   The output is similar to this:
  >   ```
  >   NAME               READY   UP-TO-DATE   AVAILABLE   AGE
  >   nginx-deployment   3/3     3            3           36s
  >   ```
  > * Run `kubectl get rs` to see that the Deployment updated the Pods by creating a new ReplicaSet and scaling it
  > up to 3 replicas, as well as scaling down the old ReplicaSet to 0 replicas.
  >   ```shell
  >   kubectl get rs
  >   ```
  >   The output is similar to this:
  >   ```
  >   NAME                          DESIRED   CURRENT   READY   AGE
  >   nginx-deployment-1564180365   3         3         3       6s
  >   nginx-deployment-2035384211   0         0         0       36s
  >   ```
  > * Running `get pods` should now show only the new Pods:
  >   ```shell
  >   kubectl get pods
  >   ```
  >   The output is similar to this:
  >   ```
  >   NAME                                READY     STATUS    RESTARTS   AGE
  >   nginx-deployment-1564180365-khku8   1/1       Running   0          14s
  >   nginx-deployment-1564180365-nacti   1/1       Running   0          14s
  >   nginx-deployment-1564180365-z9gth   1/1       Running   0          14s
  >   ```
  >   Next time you want to update these Pods, you only need to update the Deployment's Pod template again.
  >   Deployment ensures that only a certain number of Pods are down while they are being updated. By default,
  >   it ensures that at least 75% of the desired number of Pods are up (25% max unavailable).
  >   Deployment also ensures that only a certain number of Pods are created above the desired number of Pods.
  >   By default, it ensures that at most 125% of the desired number of Pods are up (25% max surge).
  >   For example, if you look at the above Deployment closely, you will see that it first creates a new Pod,
  >   then deletes an old Pod, and creates another new one. It does not kill old Pods until a sufficient number of
  >   new Pods have come up, and does not create new Pods until a sufficient number of old Pods have been killed.
  >   It makes sure that at least 3 Pods are available and that at max 4 Pods in total are available. In case of
  >   a Deployment with 4 replicas, the number of Pods would be between 3 and 5.
  > * Get details of your Deployment:
  >   ```shell
  >   kubectl describe deployments
  >   ```
  >   The output is similar to this:
  >   ```
  >   Name:                   nginx-deployment
  >   Namespace:              default
  >   CreationTimestamp:      Thu, 30 Nov 2017 10:56:25 +0000
  >   Labels:                 app=nginx
  >   Annotations:            deployment.kubernetes.io/revision=2
  >   Selector:               app=nginx
  >   Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
  >   StrategyType:           RollingUpdate
  >   MinReadySeconds:        0
  >   RollingUpdateStrategy:  25% max unavailable, 25% max surge
  >   Pod Template:
  >     Labels:  app=nginx
  >      Containers:
  >       nginx:
  >         Image:        nginx:1.16.1
  >         Port:         80/TCP
  >         Environment:  <none>
  >         Mounts:       <none>
  >       Volumes:        <none>
  >     Conditions:
  >       Type           Status  Reason
  >       ----           ------  ------
  >       Available      True    MinimumReplicasAvailable
  >       Progressing    True    NewReplicaSetAvailable
  >     OldReplicaSets:  <none>
  >     NewReplicaSet:   nginx-deployment-1564180365 (3/3 replicas created)
  >     Events:
  >       Type    Reason             Age   From                   Message
  >       ----    ------             ----  ----                   -------
  >       Normal  ScalingReplicaSet  2m    deployment-controller  Scaled up replica set nginx-deployment-2035384211 to 3
  >       Normal  ScalingReplicaSet  24s   deployment-controller  Scaled up replica set nginx-deployment-1564180365 to 1
  >       Normal  ScalingReplicaSet  22s   deployment-controller  Scaled down replica set nginx-deployment-2035384211 to 2
  >       Normal  ScalingReplicaSet  22s   deployment-controller  Scaled up replica set nginx-deployment-1564180365 to 2
  >       Normal  ScalingReplicaSet  19s   deployment-controller  Scaled down replica set nginx-deployment-2035384211 to 1
  >       Normal  ScalingReplicaSet  19s   deployment-controller  Scaled up replica set nginx-deployment-1564180365 to 3
  >       Normal  ScalingReplicaSet  14s   deployment-controller  Scaled down replica set nginx-deployment-2035384211 to 0
  >   ```
  >   Here you see that when you first created the Deployment, it created a … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `service-no-traffic`

**Question** (en, troubleshooting): My Service doesn't send traffic to my pods. What should I check?

**Reference answer:** Check that the Service's selector matches the Pods' labels, that it has EndpointSlices with the Pods' addresses, that `port`/`targetPort` are right, and that the Pods are running and ready.

**Relevant documentation:**
- `tasks/debug/debug-application/debug-service.md`, section: *Debug Services > Does the Service have any EndpointSlices?*
  > [Debug Services > Does the Service have any EndpointSlices?]
  > If you got this far, you have confirmed that your Service is correctly
  > defined and is resolved by DNS.  Now let's check that the Pods you ran are
  > actually being selected by the Service.
  > Earlier you saw that the Pods were running.  You can re-check that:
  > ```shell
  > kubectl get pods -l app=hostnames
  > ```
  > ```none
  > NAME                        READY     STATUS    RESTARTS   AGE
  > hostnames-632524106-bbpiw   1/1       Running   0          1h
  > hostnames-632524106-ly40y   1/1       Running   0          1h
  > hostnames-632524106-tlaok   1/1       Running   0          1h
  > ```
  > The `-l app=hostnames` argument is a label selector configured on the Service.
  > The "AGE" column says that these Pods are about an hour old, which implies that
  > they are running fine and not crashing.
  > The "RESTARTS" column says that these pods are not crashing frequently or being
  > restarted.  Frequent restarts could lead to intermittent connectivity issues.
  > If the restart count is high, read more about how to debug pods.
  > Inside the Kubernetes system is a control loop which evaluates the selector of
  > every Service and saves the results into one or more EndpointSlice objects.
  > Inside the Kubernetes system is a control loop which evaluates the selector of
  > every Service and saves the results into one or more EndpointSlice objects.
  > ```shell
  > kubectl get endpointslices -l k8s.io/service-name=hostnames
  > NAME              ADDRESSTYPE   PORTS   ENDPOINTS
  > hostnames-ytpni   IPv4          9376    10.244.0.5,10.244.0.6,10.244.0.7
  > ```
  > This confirms that the EndpointSlice controller has found the correct Pods for
  > your Service.  If the `ENDPOINTS` column is `<none>`, you should check that
  > the `spec.selector` field of your Service actually selects for
  > `metadata.labels` values on your Pods.  A common mistake is to have a typo or
  > other error, such as the Service selecting for `app=hostnames`, but the
  > Deployment specifying `run=hostnames`, as in versions previous to 1.18, where
  > the `kubectl run` command could have been also used to create a Deployment.
- `tasks/debug/debug-application/debug-service.md`, section: *Debug Services > Is the Service defined correctly?*
  > [Debug Services > Is the Service defined correctly?]
  > It might sound silly, but you should really double and triple check that your
  > Service is correct and matches your Pod's port.  Read back your Service
  > and verify it:
  > ```shell
  > kubectl get service hostnames -o json
  > ```
  > ```json
  > {
  >     "kind": "Service",
  >     "apiVersion": "v1",
  >     "metadata": {
  >         "name": "hostnames",
  >         "namespace": "default",
  >         "uid": "428c8b6c-24bc-11e5-936d-42010af0a9bc",
  >         "resourceVersion": "347189",
  >         "creationTimestamp": "2015-07-07T15:24:29Z",
  >         "labels": {
  >             "app": "hostnames"
  >         }
  >     },
  >     "spec": {
  >         "ports": [
  >             {
  >                 "name": "default",
  >                 "protocol": "TCP",
  >                 "port": 80,
  >                 "targetPort": 9376,
  >                 "nodePort": 0
  >             }
  >         ],
  >         "selector": {
  >             "app": "hostnames"
  >         },
  >         "clusterIP": "10.0.1.175",
  >         "type": "ClusterIP",
  >         "sessionAffinity": "None"
  >     },
  >     "status": {
  >         "loadBalancer": {}
  >     }
  > }
  > ```
  > * Is the Service port you are trying to access listed in `spec.ports[]`?
  > * Is the `targetPort` correct for your Pods (some Pods use a different port than the Service)?
  > * If you meant to use a numeric port, is it a number (9376) or a string "9376"?
  > * If you meant to use a named port, do your Pods expose a port with the same name?
  > * Is the port's `protocol` correct for your Pods?
- `tasks/debug/debug-application/debug-service.md`, section: *Debug Services > Are the Pods working?*
  > [Debug Services > Are the Pods working?]
  > At this point, you know that your Service exists and has selected your Pods.
  > At the beginning of this walk-through, you verified the Pods themselves.
  > Let's check again that the Pods are actually working - you can bypass the
  > Service mechanism and go straight to the Pods, as listed by the Endpoints
  > above.
  > These commands use the Pod port (9376), rather than the Service port (80).
  > From within a Pod:
  > ```shell
  > for ep in 10.244.0.5:9376 10.244.0.6:9376 10.244.0.7:9376; do
  >     wget -qO- $ep
  > done
  > ```
  > This should produce something like:
  > ```
  > hostnames-632524106-bbpiw
  > hostnames-632524106-ly40y
  > hostnames-632524106-tlaok
  > ```
  > You expect each Pod in the endpoints list to return its own hostname.  If
  > this is not what happens (or whatever the correct behavior is for your own
  > Pods), you should investigate what's happening there.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `dns-not-resolving`

**Question** (en, troubleshooting): Pods can't resolve service names. How do I debug DNS?

**Reference answer:** From a test Pod run `nslookup kubernetes.default`, check the Pod's `/etc/resolv.conf`, then check that the DNS (CoreDNS) Pods are running and the DNS Service exists.

**Relevant documentation:**
- `tasks/administer-cluster/dns-debugging-resolution.md`, section: *Debugging DNS Resolution > Check the local DNS configuration first*
  > [Debugging DNS Resolution > Check the local DNS configuration first]
  > Take a look inside the resolv.conf file.
  > (See Customizing DNS Service and
  > Known issues below for more information)
  > ```shell
  > kubectl exec -ti dnsutils -- cat /etc/resolv.conf
  > ```
  > Verify that the search path and name server are set up like the following
  > (note that search path may vary for different cloud providers):
  > ```
  > search default.svc.cluster.local svc.cluster.local cluster.local google.internal c.gce_project_id.internal
  > nameserver 10.0.0.10
  > options ndots:5
  > ```
  > Errors such as the following indicate a problem with the CoreDNS (or kube-dns)
  > add-on or with associated Services:
  > ```shell
  > kubectl exec -i -t dnsutils -- nslookup kubernetes.default
  > ```
  > ```
  > Server:    10.0.0.10
  > Address 1: 10.0.0.10
  > nslookup: can't resolve 'kubernetes.default'
  > ```
  > or
  > ```shell
  > kubectl exec -i -t dnsutils -- nslookup kubernetes.default
  > ```
  > ```
  > Server:    10.0.0.10
  > Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local
  > nslookup: can't resolve 'kubernetes.default'
  > ```
- `tasks/administer-cluster/dns-debugging-resolution.md`, section: *Debugging DNS Resolution > Check if the DNS pod is running*
  > [Debugging DNS Resolution > Check if the DNS pod is running]
  > Use the `kubectl get pods` command to verify that the DNS pod is running.
  > ```shell
  > kubectl get pods --namespace=kube-system -l k8s-app=kube-dns
  > ```
  > ```
  > NAME                       READY     STATUS    RESTARTS   AGE
  > ...
  > coredns-7b96bf9f76-5hsxb   1/1       Running   0           1h
  > coredns-7b96bf9f76-mvmmt   1/1       Running   0           1h
  > ...
  > ```
  > The value for label `k8s-app` is `kube-dns` for both CoreDNS and kube-dns deployments.
  > If you see that no CoreDNS Pod is running or that the Pod has failed/completed,
  > the DNS add-on may not be deployed by default in your current environment and you
  > will have to deploy it manually.
- `tasks/administer-cluster/dns-debugging-resolution.md`, section: *Debugging DNS Resolution > Is DNS service up?*
  > [Debugging DNS Resolution > Is DNS service up?]
  > Verify that the DNS service is up by using the `kubectl get service` command.
  > ```shell
  > kubectl get svc --namespace=kube-system
  > ```
  > ```
  > NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)             AGE
  > ...
  > kube-dns     ClusterIP   10.0.0.10      <none>        53/UDP,53/TCP        1h
  > ...
  > ```
  > The service name is `kube-dns` for both CoreDNS and kube-dns deployments.
  > If you have created the Service or in the case it should be created by default
  > but it does not appear, see
  > debugging Services for
  > more information.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `init-stuck`

**Question** (en, troubleshooting): My pod is stuck at Init:0/1. How do I find out what's wrong?

**Reference answer:** A status of `Init:N/M` means N of the Pod's M init containers have completed. Inspect the init containers with `kubectl describe pod` and read their logs with `kubectl logs <pod> -c <init-container>`.

**Relevant documentation:**
- `tasks/debug/debug-application/debug-init-containers.md`, section: *Debug Init Containers > Checking the status of Init Containers*
  > [Debug Init Containers > Checking the status of Init Containers]
  > Display the status of your pod:
  > ```shell
  > kubectl get pod <pod-name>
  > ```
  > For example, a status of `Init:1/2` indicates that one of two Init Containers
  > has completed successfully:
  > ```
  > NAME         READY     STATUS     RESTARTS   AGE
  > <pod-name>   0/1       Init:1/2   0          7s
  > ```
  > See Understanding Pod status for more examples of
  > status values and their meanings.
- `tasks/debug/debug-application/debug-init-containers.md`, section: *Debug Init Containers > Accessing logs from Init Containers*
  > [Debug Init Containers > Accessing logs from Init Containers]
  > Pass the Init Container name along with the Pod name
  > to access its logs.
  > ```shell
  > kubectl logs <pod-name> -c <init-container-2>
  > ```
  > Init Containers that run a shell script print
  > commands as they're executed. For example, you can do this in Bash by running
  > `set -x` at the beginning of the script.
- `tasks/debug/debug-application/debug-init-containers.md`, section: *Debug Init Containers > Understanding Pod status*
  > [Debug Init Containers > Understanding Pod status]
  > A Pod status beginning with `Init:` summarizes the status of Init Container
  > execution. The table below describes some example status values that you might
  > see while debugging Init Containers.
  > Status | Meaning
  > ------ | -------
  > `Init:N/M` | The Pod has `M` Init Containers, and `N` have completed so far.
  > `Init:Error` | An Init Container has failed to execute.
  > `Init:CrashLoopBackOff` | An Init Container has failed repeatedly.
  > `Pending` | The Pod has not yet begun executing Init Containers.
  > `PodInitializing` or `Running` | The Pod has already finished executing Init Containers.

*Drafting note:* golden v2 draft (2026-11-07) | self-check: aligned with the referenced text

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `termination-message`

**Question** (en, troubleshooting): How can a container report why it failed, so I can see it in kubectl describe?

**Reference answer:** Write the reason to the termination message file (`/dev/termination-log` by default); it appears in the container's last terminated state. `terminationMessagePolicy: FallbackToLogsOnError` uses the logs if the file is empty.

**Relevant documentation:**
- `tasks/debug/debug-application/determine-reason-pod-failure.md`, section: *Determine the Reason for Pod Failure > Writing and reading a termination message*
  > [Determine the Reason for Pod Failure > Writing and reading a termination message]
  > In this exercise, you create a Pod that runs one container.
  > The manifest for that Pod specifies a command that runs when the container starts:
  > Example file `debug/termination.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: termination-demo
  > spec:
  >   containers:
  >   - name: termination-demo-container
  >     image: debian
  >     command: ["/bin/sh"]
  >     args: ["-c", "sleep 10 && echo Sleep expired > /dev/termination-log"]
  > ```
  > 1. Create a Pod based on the YAML configuration file:
  >     ```shell
  >     kubectl apply -f https://k8s.io/examples/debug/termination.yaml
  >     ```
  >     In the YAML file, in the `command` and `args` fields, you can see that the
  >     container sleeps for 10 seconds and then writes "Sleep expired" to
  >     the `/dev/termination-log` file. After the container writes
  >     the "Sleep expired" message, it terminates.
  > 1. Display information about the Pod:
  >     ```shell
  >     kubectl get pod termination-demo
  >     ```
  >     Repeat the preceding command until the Pod is no longer running.
  > 1. Display detailed information about the Pod:
  >     ```shell
  >     kubectl get pod termination-demo --output=yaml
  >     ```
  >     The output includes the "Sleep expired" message:
  >     The output includes the "Sleep expired" message:
  >     ```yaml
  >     apiVersion: v1
  >     kind: Pod
  >     ...
  >         lastState:
  >           terminated:
  >             containerID: ...
  >             exitCode: 0
  >             finishedAt: ...
  >             message: |
  >               Sleep expired
  >             ...
  >     ```
  > 1. Use a Go template to filter the output so that it includes only the termination message:
  >     ```shell
  >     kubectl get pod termination-demo -o go-template="{{range .status.containerStatuses}}{{.lastState.terminated.message}}{{end}}"
  >     ```
  > If you are running a multi-container Pod, you can use a Go template to include the container's name.
  > By doing so, you can discover which of the containers is failing:
  > ```shell
  > kubectl get pod multi-container-pod -o go-template='{{range .status.containerStatuses}}{{printf "%s:\n%s\n\n" .name .lastState.terminated.message}}{{end}}'
  > ```
- `tasks/debug/debug-application/determine-reason-pod-failure.md`, section: *Determine the Reason for Pod Failure > Customizing the termination message*
  > [Determine the Reason for Pod Failure > Customizing the termination message]
  > Kubernetes retrieves termination messages from the termination message file
  > specified in the `terminationMessagePath` field of a Container, which has a default
  > value of `/dev/termination-log`. By customizing this field, you can tell Kubernetes
  > to use a different file. Kubernetes use the contents from the specified file to
  > populate the Container's status message on both success and failure.
  > The termination message is intended to be brief final status, such as an assertion failure message.
  > The kubelet truncates messages that are longer than 4096 bytes.
  > The total message length across all containers is limited to 12KiB, divided equally among each container.
  > For example, if there are 12 containers (`initContainers` or `containers`), each has 1024 bytes of available termination message space.
  > The default termination message path is `/dev/termination-log`.
  > You cannot set the termination message path after a Pod is launched.
  > In the following example, the container writes termination messages to
  > `/tmp/my-log` for Kubernetes to retrieve:
  > In the following example, the container writes termination messages to
  > `/tmp/my-log` for Kubernetes to retrieve:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: msg-path-demo
  > spec:
  >   containers:
  >   - name: msg-path-demo-container
  >     image: debian
  >     terminationMessagePath: "/tmp/my-log"
  > ```
  > Moreover, users can set the `terminationMessagePolicy` field of a Container for
  > further customization. This field defaults to "`File`" which means the termination
  > messages are retrieved only from the termination message file. By setting the
  > `terminationMessagePolicy` to "`FallbackToLogsOnError`", you can tell Kubernetes
  > to use the last chunk of container log output if the termination message file
  > is empty and the container exited with an error. The log output is limited to
  > 2048 bytes or 80 lines, whichever is smaller.
  > ##
  > * See the `terminationMessagePath` field in
  >   Container.
  > * See ImagePullBackOff in Images.
  > * Learn about retrieving logs.
  > * Learn about Go templates.
  > * Learn about Pod status and Pod phase.
  > * Learn about container states.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `debug-no-shell`

**Question** (en, troubleshooting): How do I debug a running pod whose image has no shell?

**Reference answer:** Add an ephemeral debug container with `kubectl debug -it <pod> --image=busybox --target=<container>`.

**Relevant documentation:**
- `tasks/debug/debug-application/debug-running-pod.md`, section: *Debug Running Pods > Debugging with an ephemeral debug container*
  > [Debug Running Pods > Debugging with an ephemeral debug container {#ephemeral-container}]
  > Ephemeral containers
  > are useful for interactive troubleshooting when `kubectl exec` is insufficient
  > because a container has crashed or a container image doesn't include debugging
  > utilities, such as with distroless images.
  > [Debug Running Pods > Debugging with an ephemeral debug container {#ephemeral-container} > Example debugging using ephemeral containers {#ephemeral-container-example}]
  > You can use the `kubectl debug` command to add ephemeral containers to a
  > running Pod. First, create a pod for the example:
  > ```shell
  > kubectl run ephemeral-demo --image=registry.k8s.io/pause:3.1 --restart=Never
  > ```
  > The examples in this section use the `pause` container image because it does not
  > contain debugging utilities, but this method works with all container
  > images.
  > If you attempt to use `kubectl exec` to create a shell you will see an error
  > because there is no shell in this container image.
  > ```shell
  > kubectl exec -it ephemeral-demo -- sh
  > ```
  > ```
  > OCI runtime exec failed: exec failed: container_linux.go:346: starting container process caused "exec: \"sh\": executable file not found in $PATH": unknown
  > ```
  > You can instead add a debugging container using `kubectl debug`. If you
  > specify the `-i`/`--interactive` argument, `kubectl` will automatically attach
  > to the console of the Ephemeral Container.
  > ```shell
  > kubectl debug -it ephemeral-demo --image=busybox:1.28 --target=ephemeral-demo
  > ```
  > ```
  > Defaulting debug container name to debugger-8xzrl.
  > If you don't see a command prompt, try pressing enter.
  > / #
  > ```
  > ```
  > Defaulting debug container name to debugger-8xzrl.
  > If you don't see a command prompt, try pressing enter.
  > / #
  > ```
  > This command adds a new busybox container and attaches to it. The `--target`
  > parameter targets the process namespace of another container. It's necessary
  > here because `kubectl run` does not enable process namespace sharing in the pod it
  > creates.
  > The `--target` parameter must be supported by the Container Runtime. When not supported,
  > the Ephemeral Container may not be started, or it may be started with an
  > isolated process namespace so that `ps` does not reveal processes in other
  > containers.
  > You can view the state of the newly created ephemeral container using `kubectl describe`:
  > ```shell
  > kubectl describe pod ephemeral-demo
  > ```
  > ```shell
  > kubectl describe pod ephemeral-demo
  > ```
  > ```
  > ...
  > Ephemeral Containers:
  >   debugger-8xzrl:
  >     Container ID:   docker://b888f9adfd15bd5739fefaa39e1df4dd3c617b9902082b1cfdc29c4028ffb2eb
  >     Image:          busybox
  >     Image ID:       docker-pullable://busybox@sha256:1828edd60c5efd34b2bf5dd3282ec0cc04d47b2ff9caa0b6d4f07a21d1c08084
  >     Port:           <none>
  >     Host Port:      <none>
  >     State:          Running
  >       Started:      Wed, 12 Feb 2020 14:25:42 +0100
  >     Ready:          False
  >     Restart Count:  0
  >     Environment:    <none>
  >     Mounts:         <none>
  > ...
  > ```
  > Use `kubectl delete` to remove the Pod when you're finished:
  > ```shell
  > kubectl delete pod ephemeral-demo
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `oomkilled`

**Question** (en, troubleshooting): My container keeps getting OOMKilled. Why?

**Reference answer:** It uses more memory than its memory limit, so it's terminated (OOMKilled) and restarted according to the restart policy. Raise the limit or reduce the memory use.

**Relevant documentation:**
- `tasks/configure-pod-container/assign-memory-resource.md`, section: *Assign Memory Resources to Containers and Pods > Exceed a Container's memory limit*
  > [Assign Memory Resources to Containers and Pods > Exceed a Container's memory limit]
  > A Container can exceed its memory request if the Node has memory available. But a Container
  > is not allowed to use more than its memory limit. If a Container allocates more memory than
  > its limit, the Container becomes a candidate for termination. If the Container continues to
  > consume memory beyond its limit, the Container is terminated. If a terminated Container can be
  > restarted, the kubelet restarts it, as with any other type of runtime failure.
  > In this exercise, you create a Pod that attempts to allocate more memory than its limit.
  > Here is the configuration file for a Pod that has one Container with a
  > memory request of 50 MiB and a memory limit of 100 MiB:
  > Example file `pods/resource/memory-request-limit-2.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: memory-demo-2
  >   namespace: mem-example
  > spec:
  >   containers:
  >   - name: memory-demo-2-ctr
  >     image: polinux/stress
  >     resources:
  >       requests:
  >         memory: "50Mi"
  >       limits:
  >         memory: "100Mi"
  >     command: ["stress"]
  >     args: ["--vm", "1", "--vm-bytes", "250M", "--vm-hang", "1"]
  > ```
  > In the `args` section of the configuration file, you can see that the Container
  > will attempt to allocate 250 MiB of memory, which is well above the 100 MiB limit.
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/resource/memory-request-limit-2.yaml --namespace=mem-example
  > ```
  > View detailed information about the Pod:
  > ```shell
  > kubectl get pod memory-demo-2 --namespace=mem-example
  > ```
  > At this point, the Container might be running or killed. Repeat the preceding command until the Container is killed:
  > ```shell
  > NAME            READY     STATUS      RESTARTS   AGE
  > memory-demo-2   0/1       OOMKilled   1          24s
  > ```
  > Get a more detailed view of the Container status:
  > ```shell
  > kubectl get pod memory-demo-2 --output=yaml --namespace=mem-example
  > ```
  > The output shows that the Container was killed because it is out of memory (OOM):
  > ```yaml
  > lastState:
  >    terminated:
  >      containerID: 65183c1877aaec2e8427bc95609cc52677a454b56fcb24340dbd22917c23b10f
  >      exitCode: 137
  >      finishedAt: 2017-06-20T20:52:19Z
  >      reason: OOMKilled
  >      startedAt: null
  > ```
  > The Container in this exercise can be restarted, so the kubelet restarts it. Repeat
  > this command several times to see that the Container is repeatedly killed and restarted:
  > ```shell
  > kubectl get pod memory-demo-2 --namespace=mem-example
  > ```
  > The output shows that the Container is killed, restarted, killed again, restarted again, and so on:
  > ```
  > kubectl get pod memory-demo-2 --namespace=mem-example
  > NAME            READY     STATUS      RESTARTS   AGE
  > memory-demo-2   0/1       OOMKilled   1          37s
  > ```
  > ```
  > kubectl get pod memory-demo-2 --namespace=mem-example
  > NAME            READY     STATUS    RESTARTS   AGE
  > memory-demo-2   1/1       Running   2          40s
  > ```
  > View detailed information about the Pod history:
  > ```
  > kubectl describe pod memory-demo-2 --namespace=mem-example
  > ```
  > The output shows that the Container starts and fails repeatedly:
  > ```
  > ... Normal  Created   Created container with id 66a3a20aa7980e61be4922780bf9d24d1a1d8b7395c09861225b0eba1b1f8511
  > ... Warning BackOff   Back-off restarting failed container
  > ```
  > View detailed information about your cluster's Nodes:
  > ```
  > kubectl describe nodes
  > ```
  > ```
  > kubectl describe nodes
  > ```
  > The output includes a record of the Container being killed because of an out-of-memory condition:
  > ```
  > Warning OOMKilling Memory cgroup out of memory: Kill process 4481 (stress) score 1994 or sacrifice child
  > ```
  > Delete your Pod:
  > ```shell
  > kubectl delete pod memory-demo-2 --namespace=mem-example
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `pods-evicted`

**Question** (en, troubleshooting): Why were my pods evicted from a node?

**Reference answer:** The kubelet evicts Pods when node resources such as memory, disk space or PIDs cross eviction thresholds (node-pressure eviction), to reclaim resources.

**Relevant documentation:**
- `concepts/scheduling-eviction/node-pressure-eviction.md`, section: *Node-pressure Eviction*
  > [Node-pressure Eviction]
  > </br>
  > The kubelet monitors resources
  > like memory, disk space, and filesystem inodes on your cluster's nodes.
  > When one or more of these resources reach specific consumption levels, the
  > kubelet can proactively fail one or more pods on the node to reclaim resources
  > and prevent starvation.
  > During a node-pressure eviction, the kubelet sets the phase for the
  > selected pods to `Failed`, and terminates the Pod.
  > Node-pressure eviction is not the same as
  > API-initiated eviction.
  > The kubelet does not respect your configured PodDisruptionBudget
  > or the pod's
  > `terminationGracePeriodSeconds`. If you use soft eviction thresholds,
  > the kubelet respects your configured `eviction-max-pod-grace-period`. If you use
  > hard eviction thresholds, the kubelet uses a `0s` grace period (immediate shutdown) for termination.
  > [Node-pressure Eviction > Self healing behavior]
  > The kubelet attempts to reclaim node-level resources
  > before it terminates end-user pods. For example, it removes unused container
  > images when disk resources are starved.
  > If the pods are managed by a workload
  > management object (such as StatefulSet
  > or Deployment) that
  > replaces failed pods, the control plane (`kube-controller-manager`) creates new
  > pods in place of the evicted pods.
  > [Node-pressure Eviction > Self healing behavior > Self healing for static pods]
  > If you are running a static pod
  > on a node that is under resource pressure, the kubelet may evict that static
  > Pod. The kubelet then tries to create a replacement, because static Pods always
  > represent an intent to run a Pod on that node.
  > The kubelet takes the _priority_ of the static pod into account when creating
  > a replacement. If the static pod manifest specifies a low priority, and there
  > are higher-priority Pods defined within the cluster's control plane, and the
  > node is under resource pressure, the kubelet may not be able to make room for
  > that static pod. The kubelet continues to attempt to run all static pods even
  > when there is resource pressure on a node.
  > [Node-pressure Eviction > Eviction signals and thresholds]
  > The kubelet uses various parameters to make eviction decisions, like the following:
  > - Eviction signals
  > - Eviction thresholds
  > - Monitoring intervals
  > [Node-pressure Eviction > Eviction signals and thresholds > Eviction signals {#eviction-signals}]
  > Eviction signals are the current state of a particular resource at a specific
  > point in time. The kubelet uses eviction signals to make eviction decisions by
  > comparing the signals to eviction thresholds, which are the minimum amount of
  > the resource that should be available on the node.
  > The kubelet uses the following eviction signals:
  > | Eviction Signal          | Description                                                                           | Linux Only |
  > |--------------------------|---------------------------------------------------------------------------------------|------------|
  > | `memory.available`       | `memory.available` := `node.status.capacity[memory]` - `node.stats.memory.workingSet` |            |
  > | `nodefs.available`       | `nodefs.available` := `node.stats.fs.available`                                       |            |
  > | `nodefs.inodesFree`      | `nodefs.inodesFree` := `node.stats.fs.inodesFree`                                     |      •     |
  > | `imagefs.available`      | `imagefs.available` := `node.stats.runtime.imagefs.available`                         |            |
  > | `imagefs.inodesFree`     | `imagefs.inodesFree` := `node.stats.runtime.imagefs.inodesFree`                       |      •     |
  > | `containerfs.available`  | `containerfs.available` := `node.stats.runtime.containerfs.available`                 |            |
  > | `containerfs.inodesFree` | `containerfs.inodesFree` := `node.stats.runtime.containerfs.inodesFree`               |      •     |
  > | `pid.available`          | `pid.available` := `node.stats.rlimit.maxpid` - `node.stats.rlimit.curproc`           |      •     |
  > In this table, the **Description** column shows how kubelet gets the value of the
  > signal. Each signal supports either a percentage or a literal value. The kubelet
  > calculates the percentage value relative to the total capacity associated with
  > the signal.
  > [Node-pressure Eviction > Eviction signals and thresholds > Eviction signals {#eviction-signals} > Memory signals]
  > On Linux nodes, the value for `memory.available` is derived from the cgroupfs instead of tools
  > like `free -m`. This is important because `free -m` does not work in a
  > container, and if users use the node allocatable
  > feature, out of resource decisions
  > are made local to the end user Pod part of the cgroup hierarchy as well as the
  > root node. This script or
  > cgroupv2 script
  > reproduces the same set of steps that the kubelet performs to calculate
  > `memory.available`. The kubelet excludes inactive_file (the number of bytes of
  > file-backed memory on the inactive LRU list) from its calculation, as it assumes that
  > memory is reclaimable under pressure.
  > On Windows nodes, the value for `memory.available` is derived from the node's global
  > memory commit levels (queried through the `GetPerformanceInfo()`
  > system call) by subtracting the node's global `CommitTotal` from the node's `CommitLimit`. Please note that `CommitLimit` can change if the node's page-file size changes!
  > [Node-pressure Eviction > Eviction signals and thresholds > Eviction signals {#eviction-signals} > Filesystem signals]
  > The kubelet recognizes three specific filesystem identifiers that can be used with
  > eviction signals (`<identifier>.inodesFree` or `<identifier>.available`):
  > 1. `nodefs`: The node's main filesystem, used for local disk volumes,
  >     emptyDir volumes not backed by memory, log storage, ephemeral storage,
  >     and more. For example, `nodefs` contains `/var/lib/kubelet`.
  > 1. `imagefs`: An optional filesystem that container runtimes can use to store
  >    container images (which are the read-only layers) and container writable
  >    layers.
  > 1. `containerfs`: An optional filesystem that … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `node-not-ready`

**Question** (en, troubleshooting): One of my nodes shows NotReady. Where do I start?

**Reference answer:** Check `kubectl get nodes` and `kubectl describe node <name>`, then look at the logs on that node (e.g. the kubelet's).

**Relevant documentation:**
- `tasks/debug/debug-cluster/_index.md`, section: *Troubleshooting Clusters > Listing your cluster*
  > [Troubleshooting Clusters > Listing your cluster]
  > The first thing to debug in your cluster is if your nodes are all registered correctly.
  > Run the following command:
  > ```shell
  > kubectl get nodes
  > ```
  > And verify that all of the nodes you expect to see are present and that they are all in the `Ready` state.
  > To get detailed information about the overall health of your cluster, you can run:
  > ```shell
  > kubectl cluster-info dump
  > ```
  > [Troubleshooting Clusters > Listing your cluster > Example: debugging a down/unreachable node]
  > Sometimes when debugging it can be useful to look at the status of a node -- for example, because
  > you've noticed strange behavior of a Pod that's running on the node, or to find out why a Pod
  > won't schedule onto the node. As with Pods, you can use `kubectl describe node` and `kubectl get
  > node -o yaml` to retrieve detailed information about nodes. For example, here's what you'll see if
  > a node is down (disconnected from the network, or kubelet dies and won't restart, etc.). Notice
  > the events that show the node is NotReady, and also notice that the pods are no longer running
  > (they are evicted after five minutes of NotReady status).
  > ```shell
  > kubectl get nodes
  > ```
  > ```none
  > NAME                     STATUS       ROLES     AGE     VERSION
  > kube-worker-1            NotReady     <none>    1h      v1.23.3
  > kubernetes-node-bols     Ready        <none>    1h      v1.23.3
  > kubernetes-node-st6x     Ready        <none>    1h      v1.23.3
  > kubernetes-node-unaj     Ready        <none>    1h      v1.23.3
  > ```
  > ```shell
  > kubectl describe node kube-worker-1
  > ```
  > ```shell
  > kubectl describe node kube-worker-1
  > ```
  > ```none
  > Name:               kube-worker-1
  > Roles:              <none>
  > Labels:             beta.kubernetes.io/arch=amd64
  >                     beta.kubernetes.io/os=linux
  >                     kubernetes.io/arch=amd64
  >                     kubernetes.io/hostname=kube-worker-1
  >                     kubernetes.io/os=linux
  > Annotations:        kubeadm.alpha.kubernetes.io/cri-socket: /run/containerd/containerd.sock
  >                     node.alpha.kubernetes.io/ttl: 0
  >                     volumes.kubernetes.io/controller-managed-attach-detach: true
  > CreationTimestamp:  Thu, 17 Feb 2022 16:46:30 -0500
  > Taints:             node.kubernetes.io/unreachable:NoExecute
  >                     node.kubernetes.io/unreachable:NoSchedule
  > Unschedulable:      false
  > Lease:
  >   HolderIdentity:  kube-worker-1
  >   AcquireTime:     <unset>
  >   RenewTime:       Thu, 17 Feb 2022 17:13:09 -0500
  > Conditions:
  >   Type                 Status    LastHeartbeatTime                 LastTransitionTime                Reason              Message
  >   ----                 ------    -----------------                 ------------------                ------              -------
  >   NetworkUnavailable   False     Thu, 17 Feb 2022 17:09:13 -0500   Thu, 17 Feb 2022 17:09:13 -0500   WeaveIsUp           Weave pod has set this
  >   MemoryPressure       Unknown   Thu, 17 Feb 2022 17:12:40 -0500   Thu, 17 Feb 2022 17:13:52 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
  >   DiskPressure         Unknown   Thu, 17 Feb 2022 17:12:40 -0500   Thu, 17 Feb 2022 17:13:52 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
  >   PIDPressure          Unknown   Thu, 17 Feb 2022 17:12:40 -0500   Thu, 17 Feb 2022 17:13:52 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
  >   Ready                Unknown   Thu, 17 Feb 2022 17:12:40 -0500   Thu, 17 Feb 2022 17:13:52 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
  > Addresses:
  >   InternalIP:  192.168.0.113
  >   Hostname:    kube-worker-1
  > Capacity:
  >   cpu:                2
  >   ephemeral-storage:  15372232Ki
  >   hugepages-2Mi:      0
  >   memory:             2025188Ki
  >   pods:               110
  > Allocatable:
  >   cpu:                2
  >   ephemeral-storage:  14167048988
  >   hugepages-2Mi:      0
  >   memory:             1922788Ki
  >   pods:               110
  > System Info:
  >   Machine ID:                 9384e2927f544209b5d7b67474bbf92b
  >   System UUID:                aa829ca9-73d7-064d-9019-df07404ad448
  >   Boot ID:                    5a295a03-aaca-4340-af20-1327fa5dab5c
  >   Kernel Version:             5.13.0-28-generic
  >   OS Image:                   Ubuntu 21.10
  >   Operating System:           linux
  >   Architecture:               amd64
  >   Container Runtime Version:  containerd://1.5.9
  >   Kubelet Version:            v1.23.3
  >   Kube-Proxy Version:         v1.23.3
  > Non-terminated Pods:          (4 in total)
  >   Namespace                   Name                                 CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
  >   ---------                   ----                                 ------------  ----------  ---------------  -------------  ---
  >   default                     nginx-deployment-67d4bdd6f5-cx2nz    500m (25%)    500m (25%)  128Mi (6%)       128Mi (6%)     23m
  >   default                     nginx-deployment-67d4bdd6f5-w6kd7    500m (25%)    500m (25%)  128Mi (6%)       128Mi (6%)     23m
  >   kube-system                 kube-proxy-dnxbz                     0 (0%)        0 (0%)      0 (0%)           0 (0%)         28m
  >   kube-system                 weave-net-gjxxp                      100m (5%)     0 (0%)      200Mi (10%)      0 (0%)         28m
  > Allocated resources:
  >   (Total limits may be over 100 percent, i.e., overcommitted.)
  >   Resource           Requests     Limits
  >   --------           --------     ------
  >   cpu                1100m (55%)  1 (50%)
  >   memory             456Mi (24%)  256Mi (13%)
  >   ephemeral-storage  0 (0%)       0 (0%)
  >   hugepages-2Mi      0 (0%)       0 (0%)
  > Events:
  > ...
  > ```
  > ```shell
  > kubectl get node kube-worker-1 -o yaml
  > ```
  > ```yaml
  > apiVersion: v1
  > kind: Node
  > metadata:
  >   annotations:
  >     kubeadm.alpha.kubernetes.io/cri-socket: /run/containerd/containerd.sock
  >     node.alpha.kubernetes.io/ttl: "0"
  >     volumes.kubernetes.io/controller-managed-attach-detach: "true"
  >   creationTimestamp: "2022-02-17T21:46:30Z"
  >   labels:
  >     beta.kubernetes.io/arch: amd64
  >     beta.kubernetes.io/os: linux
  >     … (section continues)
- `tasks/debug/debug-cluster/_index.md`, section: *Troubleshooting Clusters > Looking at logs*
  > [Troubleshooting Clusters > Looking at logs]
  > For now, digging deeper into the cluster requires logging into the relevant machines.  Here are the locations
  > of the relevant log files.  On systemd-based systems, you may need to use `journalctl` instead of examining log files.
  > [Troubleshooting Clusters > Looking at logs > Control Plane nodes]
  > * `/var/log/kube-apiserver.log` - API Server, responsible for serving the API
  > * `/var/log/kube-scheduler.log` - Scheduler, responsible for making scheduling decisions
  > * `/var/log/kube-controller-manager.log` - a component that runs most Kubernetes built-in
  >   controllers, with the notable exception of scheduling
  >   (the kube-scheduler handles scheduling).
  > [Troubleshooting Clusters > Looking at logs > Worker Nodes]
  > * `/var/log/kubelet.log` - logs from the kubelet, responsible for running containers on the node
  > * `/var/log/kube-proxy.log` - logs from `kube-proxy`, which is responsible for directing traffic to Service endpoints

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `pending-insufficient-memory`

**Question** (en, troubleshooting): My pod stays Pending with an 'Insufficient memory' event. What does that mean?

**Reference answer:** Its memory request is larger than the memory available on any node, so the scheduler can't place it; lower the request or add capacity.

**Relevant documentation:**
- `tasks/configure-pod-container/assign-memory-resource.md`, section: *Assign Memory Resources to Containers and Pods > Specify a memory request that is too big for your Nodes*
  > [Assign Memory Resources to Containers and Pods > Specify a memory request that is too big for your Nodes]
  > Memory requests and limits are associated with Containers, but it is useful to think
  > of a Pod as having a memory request and limit. The memory request for the Pod is the
  > sum of the memory requests for all the Containers in the Pod. Likewise, the memory
  > limit for the Pod is the sum of the limits of all the Containers in the Pod.
  > Pod scheduling is based on requests. A Pod is scheduled to run on a Node only if the Node
  > has enough available memory to satisfy the Pod's memory request.
  > In this exercise, you create a Pod that has a memory request so big that it exceeds the
  > capacity of any Node in your cluster. Here is the configuration file for a Pod that has one
  > Container with a request for 1000 GiB of memory, which likely exceeds the capacity
  > of any Node in your cluster.
  > Example file `pods/resource/memory-request-limit-3.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: memory-demo-3
  >   namespace: mem-example
  > spec:
  >   containers:
  >   - name: memory-demo-3-ctr
  >     image: polinux/stress
  >     resources:
  >       requests:
  >         memory: "1000Gi"
  >       limits:
  >         memory: "1000Gi"
  >     command: ["stress"]
  >     args: ["--vm", "1", "--vm-bytes", "150M", "--vm-hang", "1"]
  > ```
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/pods/resource/memory-request-limit-3.yaml --namespace=mem-example
  > ```
  > View the Pod status:
  > ```shell
  > kubectl get pod memory-demo-3 --namespace=mem-example
  > ```
  > The output shows that the Pod status is PENDING. That is, the Pod is not scheduled to run on any Node, and it will remain in the PENDING state indefinitely:
  > ```
  > kubectl get pod memory-demo-3 --namespace=mem-example
  > NAME            READY     STATUS    RESTARTS   AGE
  > memory-demo-3   0/1       Pending   0          25s
  > ```
  > View detailed information about the Pod, including events:
  > ```shell
  > kubectl describe pod memory-demo-3 --namespace=mem-example
  > ```
  > The output shows that the Container cannot be scheduled because of insufficient memory on the Nodes:
  > ```
  > Events:
  >   ...  Reason            Message
  >        ------            -------
  >   ...  FailedScheduling  No nodes are available that match all of the following predicates:: Insufficient memory (3).
  > ```

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---
