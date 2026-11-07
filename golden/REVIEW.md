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
- `tasks/configure-pod-container/configure-service-account.md`, section: *Configure Service Accounts for Pods > Use the default service account to access the API server*
  > [Configure Service Accounts for Pods > Use the default service account to access the API server]
  > When Pods contact the API server, Pods authenticate as a particular
  > ServiceAccount (for example, `default`). There is always at least one
  > ServiceAccount in each namespace.
  > Every Kubernetes namespace contains at least one ServiceAccount: the default
  > ServiceAccount for that namespace, named `default`.
  > If you do not specify a ServiceAccount when you create a Pod, Kubernetes
  > automatically assigns the ServiceAccount named `default` in that namespace.
  > You can fetch the details for a Pod you have created. For example:
  > ```shell
  > kubectl get pods/<podname> -o yaml
  > ```
  > In the output, you see a field `spec.serviceAccountName`.
  > Kubernetes automatically
  > sets that value if you don't specify it when you create a Pod.
  > An application running inside a Pod can access the Kubernetes API using
  > automatically mounted service account credentials.
  > See accessing the Cluster to learn more.
  > When a Pod authenticates as a ServiceAccount, its level of access depends on the
  > authorization plugin and policy
  > in use.
  > When a Pod authenticates as a ServiceAccount, its level of access depends on the
  > authorization plugin and policy
  > in use.
  > The API credentials are automatically revoked when the Pod is deleted, even if
  > finalizers are in place. In particular, the API credentials are revoked 60 seconds
  > beyond the `.metadata.deletionTimestamp` set on the Pod (the deletion timestamp
  > is typically the time that the **delete** request was accepted plus the Pod's
  > termination grace period).
  > [Configure Service Accounts for Pods > Use the default service account to access the API server > Opt out of API credential automounting]
  > If you don't want the kubelet
  > to automatically mount a ServiceAccount's API credentials, you can opt out of
  > the default behavior.
  > You can opt out of automounting API credentials on `/var/run/secrets/kubernetes.io/serviceaccount/token`
  > for a service account by setting `automountServiceAccountToken: false` on the ServiceAccount:
  > For example:
  > ```yaml
  > apiVersion: v1
  > kind: ServiceAccount
  > metadata:
  >   name: build-robot
  > automountServiceAccountToken: false
  > ...
  > ```
  > You can also opt out of automounting API credentials for a particular Pod:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: my-pod
  > spec:
  >   serviceAccountName: build-robot
  >   automountServiceAccountToken: false
  >   ...
  > ```
  > If both the ServiceAccount and the Pod's `.spec` specify a value for
  > `automountServiceAccountToken`, the Pod spec takes precedence.

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 2 (Youssef Zemzem, 2026-11-07): added the section that documents the default ServiceAccount being assigned

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
- `tasks/debug/debug-application/debug-init-containers.md`, section: *Debug Init Containers > Getting details about Init Containers*
  > [Debug Init Containers > Getting details about Init Containers]
  > View more detailed information about Init Container execution:
  > ```shell
  > kubectl describe pod <pod-name>
  > ```
  > For example, a Pod with two Init Containers might show the following:
  > ```
  > Init Containers:
  >   <init-container-1>:
  >     Container ID:    ...
  >     ...
  >     State:           Terminated
  >       Reason:        Completed
  >       Exit Code:     0
  >       Started:       ...
  >       Finished:      ...
  >     Ready:           True
  >     Restart Count:   0
  >     ...
  >   <init-container-2>:
  >     Container ID:    ...
  >     ...
  >     State:           Waiting
  >       Reason:        CrashLoopBackOff
  >     Last State:      Terminated
  >       Reason:        Error
  >       Exit Code:     1
  >       Started:       ...
  >       Finished:      ...
  >     Ready:           False
  >     Restart Count:   3
  >     ...
  > ```
  > You can also access the Init Container statuses programmatically by reading the
  > `status.initContainerStatuses` field on the Pod Spec:
  > ```shell
  > kubectl get pod nginx --template '{{.status.initContainerStatuses}}'
  > ```
  > This command will return the same information as above in raw JSON.
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

*Drafting note:* golden v2 draft (2026-11-07) | self-check: aligned with the referenced text | human review v2 batch 2 (Youssef Zemzem, 2026-11-07): added the section that documents kubectl describe pod for init containers

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `termination-message`

**Question** (en, troubleshooting): How can a container report why it failed, so the reason shows up in the Pod's status?

**Reference answer:** Write the reason to the termination message file (`/dev/termination-log` by default); it appears in the container's last terminated state (`lastState.terminated.message`, e.g. via `kubectl get pod <pod> --output=yaml`). `terminationMessagePolicy: FallbackToLogsOnError` uses the logs if the file is empty.

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 2 (Youssef Zemzem, 2026-11-07): question now refers to the Pod status, as documented, instead of kubectl describe

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `oomkilled`

**Question** (en, troubleshooting): My container keeps getting OOMKilled. Why?

**Reference answer:** It uses more memory than its memory limit, so it can be terminated (OOMKilled); the kubelet restarts it if its restart policy allows.

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 2 (Youssef Zemzem, 2026-11-07): removed the undocumented recommendations

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `pending-insufficient-memory`

**Question** (en, troubleshooting): My pod stays Pending with an 'Insufficient memory' event. What does that mean?

**Reference answer:** Its memory request is larger than the memory available on any node, so the Pod can't be scheduled and stays Pending.

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 2 (Youssef Zemzem, 2026-11-07): removed the undocumented recommendations

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `imagepullbackoff`

**Question** (en, troubleshooting): My pod is stuck in ImagePullBackOff. What are the common causes?

**Reference answer:** The image can't be pulled: usually a wrong image name or tag, or an image that isn't in the registry. `kubectl describe pod` shows the events.

**Relevant documentation:**
- `tasks/debug/debug-application/debug-pods.md`, section: *Debug Pods > Diagnosing the problem*
  > [Debug Pods > Diagnosing the problem]
  > The first step in troubleshooting is triage. What is the problem?
  > Is it your Pods, your Replication Controller or your Service?
  >    * Debugging Pods
  >    * Debugging Replication Controllers
  >    * Debugging Services
  > [Debug Pods > Diagnosing the problem > Debugging Pods]
  > The first step in debugging a Pod is taking a look at it. Check the current
  > state of the Pod and recent events with the following command:
  > ```shell
  > kubectl describe pods ${POD_NAME}
  > ```
  > Look at the state of the containers in the pod. Are they all `Running`?
  > Have there been recent restarts?
  > Continue debugging depending on the state of the pods.
  > [Debug Pods > Diagnosing the problem > Debugging Pods > My pod stays pending]
  > If a Pod is stuck in `Pending` it means that it can not be scheduled onto a node.
  > Generally this is because there are insufficient resources of one type or another
  > that prevent scheduling. Look at the output of the `kubectl describe ...` command above.
  > There should be messages from the scheduler about why it can not schedule your pod.
  > Reasons include:
  > * **You don't have enough resources**: You may have exhausted the supply of CPU
  >   or Memory in your cluster, in this case you need to delete Pods, adjust resource
  >   requests, or add new nodes to your cluster. See Compute Resources document
  >   for more information.
  > * **You are using `hostPort`**: When you bind a Pod to a `hostPort` there are a
  >   limited number of places that pod can be scheduled. In most cases, `hostPort`
  >   is unnecessary, try using a Service object to expose your Pod.  If you do require
  >   `hostPort` then you can only schedule as many Pods as there are nodes in your Kubernetes cluster.
  > [Debug Pods > Diagnosing the problem > Debugging Pods > My pod stays waiting]
  > If a Pod is stuck in the `Waiting` state, then it has been scheduled to a worker node,
  > but it can't run on that machine. Again, the information from `kubectl describe ...`
  > should be informative. The most common cause of `Waiting` pods is a failure to pull the image.
  > There are three things to check:
  > * Make sure that you have the name of the image correct.
  > * Have you pushed the image to the registry?
  > * Try to manually pull the image to see if the image can be pulled. For example,
  >   if you use Docker on your PC, run `docker pull <image>`.
  > [Debug Pods > Diagnosing the problem > Debugging Pods > My pod stays terminating]
  > If a Pod is stuck in the `Terminating` state, it means that a deletion has been
  > issued for the Pod, but the control plane is unable to delete the Pod object.
  > This typically happens if the Pod has a finalizer
  > and there is an admission webhook
  > installed in the cluster that prevents the control plane from removing the
  > finalizer.
  > To identify this scenario, check if your cluster has any
  > ValidatingWebhookConfiguration or MutatingWebhookConfiguration that target
  > `UPDATE` operations for `pods` resources.
  > If the webhook is provided by a third-party:
  > - Make sure you are using the latest version.
  > - Disable the webhook for `UPDATE` operations.
  > - Report an issue with the corresponding provider.
  > If you are the author of the webhook:
  > - For a mutating webhook, make sure it never changes immutable fields on
  >   `UPDATE` operations. For example, changes to containers are usually not allowed.
  > - For a validating webhook, make sure that your validation policies only apply
  >   to new changes. In other words, you should allow Pods with existing violations
  >   to pass validation. This allows Pods that were created before the validating
  >   webhook was installed to continue running.
  > [Debug Pods > Diagnosing the problem > Debugging Pods > My pod is crashing or otherwise unhealthy]
  > Once your pod has been scheduled, the methods described in
  > Debug Running Pods
  > are available for debugging.
  > [Debug Pods > Diagnosing the problem > Debugging Pods > My pod is running but not doing what I told it to do]
  > If your pod is not behaving as you expected, it may be that there was an error in your
  > pod description (e.g. `mypod.yaml` file on your local machine), and that the error
  > was silently ignored when you created the pod.  Often a section of the pod description
  > is nested incorrectly, or a key name is typed incorrectly, and so the key is ignored.
  > For example, if you misspelled `command` as `commnd` then the pod will be created but
  > will not use the command line you intended it to use.
  > The first thing to do is to delete your pod and try creating it again with the `--validate` option.
  > For example, run `kubectl apply --validate -f mypod.yaml`.
  > If you misspelled `command` as `commnd` then will give an error like this:
  > ```shell
  > I0805 10:43:25.129850   46757 schema.go:126] unknown field: commnd
  > I0805 10:43:25.129973   46757 schema.go:129] this may be a false alarm, see https://github.com/kubernetes/kubernetes/issues/6842
  > pods/mypod
  > ```
  > The next thing to check is whether the pod on the apiserver
  > matches the pod you meant to create (e.g. in a yaml file on your local machine).
  > For example, run `kubectl get pods/mypod -o yaml > mypod-on-apiserver.yaml` and then
  > manually compare the original pod description, `mypod.yaml` with the one you got
  > back from apiserver, `mypod-on-apiserver.yaml`. There will typically be some
  > lines on the "apiserver" version that are not on the original version. This is
  > expected. However, if there are lines on the original that are not on the apiserver
  > version, then this may indicate a problem with your pod spec.
  > [Debug Pods > Diagnosing the problem > Debugging Replication Controllers]
  > Replication controllers are fairly straightforward. They can either create Pods or they can't.
  > If they can't create pods, then please refer to the
  > instructions above to debug your pods.
  > You can also use `kubectl describe rc ${CONTROLLER_NAME}` to introspect events
  > related to the replication controller.
  > [Debug Pods > Diagnosing the problem > Debugging Services]
  > Services provide load balancing across a set of pods. There are several common problems that can make Services
  > not work … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `exec-shell`

**Question** (en, command): How do I open a shell inside a running container?

**Reference answer:** `kubectl exec --stdin --tty <pod> -- /bin/bash`; when the Pod has several containers, choose one with `--container` (`-c`).

**Relevant documentation:**
- `tasks/debug/debug-application/get-shell-running-container.md`, section: *Get a Shell to a Running Container > Getting a shell to a container*
  > [Get a Shell to a Running Container > Getting a shell to a container]
  > In this exercise, you create a Pod that has one container. The container
  > runs the nginx image. Here is the configuration file for the Pod:
  > Example file `application/shell-demo.yaml`:
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: shell-demo
  > spec:
  >   volumes:
  >   - name: shared-data
  >     emptyDir: {}
  >   containers:
  >   - name: nginx
  >     image: nginx
  >     volumeMounts:
  >     - name: shared-data
  >       mountPath: /usr/share/nginx/html
  >   hostNetwork: true
  >   dnsPolicy: Default
  > ```
  > Create the Pod:
  > ```shell
  > kubectl apply -f https://k8s.io/examples/application/shell-demo.yaml
  > ```
  > Verify that the container is running:
  > ```shell
  > kubectl get pod shell-demo
  > ```
  > Get a shell to the running container:
  > ```shell
  > kubectl exec --stdin --tty shell-demo -- /bin/bash
  > ```
  > The double dash (`--`) separates the arguments you want to pass to the command from the kubectl arguments.
  > In your shell, list the root directory:
  > ```shell
  > # Run this inside the container
  > ls /
  > ```
  > In your shell, experiment with other commands. Here are
  > some examples:
  > In your shell, experiment with other commands. Here are
  > some examples:
  > ```shell
  > # You can run these example commands inside the container
  > ls /
  > cat /proc/mounts
  > cat /proc/1/maps
  > apt-get update
  > apt-get install -y tcpdump
  > tcpdump
  > apt-get install -y lsof
  > lsof
  > apt-get install -y procps
  > ps aux
  > ps aux | grep nginx
  > ```
- `tasks/debug/debug-application/get-shell-running-container.md`, section: *Get a Shell to a Running Container > Opening a shell when a Pod has more than one container*
  > [Get a Shell to a Running Container > Opening a shell when a Pod has more than one container]
  > If a Pod has more than one container, use `--container` or `-c` to
  > specify a container in the `kubectl exec` command. For example,
  > suppose you have a Pod named my-pod, and the Pod has two containers
  > named _main-app_ and _helper-app_. The following command would open a
  > shell to the _main-app_ container.
  > ```shell
  > kubectl exec -i -t my-pod --container main-app -- /bin/bash
  > ```
  > The short options `-i` and `-t` are the same as the long options `--stdin` and `--tty`
  > ##
  > * Read about kubectl exec

*Drafting note:* golden v2 draft (2026-11-07) | self-check: aligned with the referenced text

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `port-forward`

**Question** (en, command): How do I reach a pod's port from my laptop without exposing it?

**Reference answer:** `kubectl port-forward pods/<name> 28015:27017` forwards local port 28015 to port 27017 of the Pod; it also accepts `deployment/` and `service/` targets.

**Relevant documentation:**
- `tasks/access-application-cluster/port-forward-access-application-cluster.md`, section: *Use Port Forwarding to Access Applications in a Cluster > Forward a local port to a port on the Pod*
  > [Use Port Forwarding to Access Applications in a Cluster > Forward a local port to a port on the Pod]
  > 1. `kubectl port-forward` allows using resource name, such as a pod name, to select a matching pod to port forward to.
  >    ```shell
  >    # Change mongo-75f59d57f4-4nd6q to the name of the Pod
  >    kubectl port-forward mongo-75f59d57f4-4nd6q 28015:27017
  >    ```
  >    which is the same as
  >    ```shell
  >    kubectl port-forward pods/mongo-75f59d57f4-4nd6q 28015:27017
  >    ```
  >    or
  >    ```shell
  >    kubectl port-forward deployment/mongo 28015:27017
  >    ```
  >    or
  >    ```shell
  >    kubectl port-forward replicaset/mongo-75f59d57f4 28015:27017
  >    ```
  >    or
  >    ```shell
  >    kubectl port-forward service/mongo 28015:27017
  >    ```
  >    Any of the above commands works. The output is similar to this:
  >    ```
  >    Forwarding from 127.0.0.1:28015 -> 27017
  >    Forwarding from [::1]:28015 -> 27017
  >    ```
  >    `kubectl port-forward` does not return. To continue with the exercises, you will need to open another terminal.
  > 2. Start the MongoDB command line interface:
  >    ```shell
  >    mongosh --port 28015
  >    ```
  > 3. At the MongoDB command line prompt, enter the `ping` command:
  >    ```
  >    db.runCommand( { ping: 1 } )
  >    ```
  >    A successful ping request returns:
  >    ```
  >    { ok: 1 }
  >    ```
  > [Use Port Forwarding to Access Applications in a Cluster > Forward a local port to a port on the Pod > Optionally let _kubectl_ choose the local port {#let-kubectl-choose-local-port}]
  > If you don't need a specific local port, you can let `kubectl` choose and allocate
  > the local port and thus relieve you from having to manage local port conflicts, with
  > the slightly simpler syntax:
  > ```shell
  > kubectl port-forward deployment/mongo :27017
  > ```
  > The `kubectl` tool finds a local port number that is not in use (avoiding low ports numbers,
  > because these might be used by other applications). The output is similar to:
  > ```
  > Forwarding from 127.0.0.1:63753 -> 27017
  > Forwarding from [::1]:63753 -> 27017
  > ```

*Drafting note:* golden v2 draft (2026-11-07) | self-check: aligned with the referenced text

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `logs-one-container`

**Question** (en, command): How do I stream the logs of one specific container in a multi-container pod?

**Reference answer:** `kubectl logs -f <pod> -c <container>`.

**Relevant documentation:**
- `reference/kubectl/generated/kubectl_logs/_index.md`, section: *(whole document)*
  > [kubectl logs]
  > ##
  > Print the logs for a container in a pod or specified resource. If the pod has only one container, the container name is optional.
  > ```
  > kubectl logs [-f] [-p] (POD | TYPE/NAME) [-c CONTAINER]
  > ```
  > ##
  > ##
  > ```
  >   # Return snapshot logs from pod nginx with only one container
  >   kubectl logs nginx
  >   # Return snapshot logs from pod nginx, prefixing each line with the source pod and container name
  >   kubectl logs nginx --prefix
  >   # Return snapshot logs from pod nginx, limiting output to 500 bytes
  >   kubectl logs nginx --limit-bytes=500
  >   # Return snapshot logs from pod nginx, waiting up to 20 seconds for it to start running.
  >   kubectl logs nginx --pod-running-timeout=20s
  >   # Return snapshot logs from pod nginx with multi containers
  >   kubectl logs nginx --all-containers=true
  >   # Return snapshot logs from all pods in the deployment nginx
  >   kubectl logs deployment/nginx --all-pods=true
  >   # Return snapshot logs from all containers in pods defined by label app=nginx
  >   kubectl logs -l app=nginx --all-containers=true
  >   # Return snapshot logs from all pods defined by label app=nginx, limiting concurrent log requests to 10 pods
  >   kubectl logs -l app=nginx --max-log-requests=10
  >   # Return snapshot of previous terminated ruby container logs from pod web-1
  >   kubectl logs -p -c ruby web-1
  >   # Begin streaming the logs from pod nginx, continuing even if errors occur
  >   kubectl logs nginx -f --ignore-errors=true
  >   # Begin streaming the logs of the ruby container in pod web-1
  >   kubectl logs -f -c ruby web-1
  >   # Begin streaming the logs from all containers in pods defined by label app=nginx
  >   kubectl logs -f -l app=nginx --all-containers=true
  >   # Display only the most recent 20 lines of output in pod nginx
  >   kubectl logs --tail=20 nginx
  >   # Show all logs from pod nginx written in the last hour
  >   kubectl logs --since=1h nginx
  >   # Show all logs with timestamps from pod nginx starting from August 30, 2024, at 06:00:00 UTC
  >   kubectl logs nginx --since-time=2024-08-30T06:00:00Z --timestamps=true
  >   # Show logs from a kubelet with an expired serving certificate
  >   kubectl logs --insecure-skip-tls-verify-backend nginx
  >   # Return snapshot logs from first container of a job named hello
  >   kubectl logs job/hello
  >   # Return snapshot logs from container nginx-1 of a deployment named nginx
  >   kubectl logs deployment/nginx -c nginx-1
  > ```
  > ##
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  > <tr>
  > <td colspan="2">--all-containers</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Get all containers' logs in the pod(s).</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--all-pods</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Get logs from all pod(s). Sets prefix to true.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-c, --container string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Print the logs of this container</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-f, --follow</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Specify if the logs should be streamed.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-h, --help</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>help for logs</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--ignore-errors</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If watching / following pod logs, allow for any errors that occur to be non-fatal</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--insecure-skip-tls-verify-backend</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Skip verifying the identity of the kubelet that logs are requested from.  In theory, an attacker could provide invalid log content back. You might want to use this if your kubelet serving certificates have expired.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--limit-bytes int</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Maximum bytes of logs to return. Defaults to no limit.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--max-log-requests int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 5</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Specify maximum number of concurrent logs to follow when using by a selector. Defaults to 5.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--pod-running-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 20s</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The length of time (like 5s, 2m, or 3h, higher than zero) to wait until at least one pod is running</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--prefix</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Prefix each log line with the log source (pod name and container name)</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-p, --previous</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If true, print the logs for the previous instance of the container in a pod if it exists.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-l, --selector string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Selector (label query) to filter on, supports '=', '==', '!=', 'in', 'notin'.(e.g. -l key1=value1,key2=value2,key3 in (value3)). Matching objects must satisfy all of the specified label constraints.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--since duration</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Only return logs newer than a relative duration like 5s, 2m, or 3h. Defaults to all logs. Only one of since-time / since may be used.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--since-time string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Only … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `kubectl-explain`

**Question** (en, command): How can I read the documentation of a field like spec.containers from the command line?

**Reference answer:** `kubectl explain pods.spec.containers` (add `--recursive` to see nested fields).

**Relevant documentation:**
- `reference/kubectl/generated/kubectl_explain/_index.md`, section: *(whole document)*
  > [kubectl explain]
  > ##
  > Describe fields and structure of various resources.
  >  This command describes the fields associated with each supported API resource. Fields are identified via a simple JSONPath identifier:
  >         &lt;type&gt;.&lt;fieldName&gt;[.&lt;fieldName&gt;]
  >  Information about each field is retrieved from the server in OpenAPI format.
  > Use "kubectl api-resources" for a complete list of supported resources.
  > ```
  > kubectl explain TYPE [--recursive=FALSE|TRUE] [--api-version=api-version-group] [-o|--output=plaintext|plaintext-openapiv2]
  > ```
  > ##
  > ```
  >   # Get the documentation of the resource and its fields
  >   kubectl explain pods
  >   # Get all the fields in the resource
  >   kubectl explain pods --recursive
  >   # Get the explanation for deployment in supported api versions
  >   kubectl explain deployments --api-version=apps/v1
  >   # Get the documentation of a specific field of a resource
  >   kubectl explain pods.spec.containers
  >   # Get the documentation of resources in different format
  >   kubectl explain deployment --output=plaintext-openapiv2
  > ```
  > ##
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  > <tr>
  > <td colspan="2">--api-version string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Get different explanations for particular API version (API group/version)</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-h, --help</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>help for explain</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--output string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: "plaintext"</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Format in which to render the schema (plaintext, plaintext-openapiv2)</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--recursive</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Print the fields of fields (Currently only 1 level deep)</p></td>
  > </tr>
  > </tbody>
  > </table>
  > ##
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  > <tr>
  > <td colspan="2">--as string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Username to impersonate for the operation. User could be a regular user or a service account in a namespace.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--as-group strings</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Group to impersonate for the operation, this flag can be repeated to specify multiple groups.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--as-uid string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>UID to impersonate for the operation.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--cache-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: "$HOME/.kube/cache"</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Default cache directory</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--certificate-authority string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Path to a cert file for the certificate authority</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--client-certificate string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Path to a client certificate file for TLS</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--client-key string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Path to a client key file for TLS</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--cluster string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The name of the kubeconfig cluster to use</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--context string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The name of the kubeconfig context to use</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--context string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The name of the kubeconfig context to use</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--default-not-ready-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 300</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Indicates the tolerationSeconds of the toleration for notReady:NoExecute that is added by default to every pod that does not already have such a toleration.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--default-unreachable-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 300</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Indicates the tolerationSeconds of the toleration for unreachable:NoExecute that is added by default to every pod that does not already have such a toleration.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--disable-compression</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If true, opt-out of response compression for all requests to the server</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--insecure-skip-tls-verify</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If true, the server's certificate will not be checked for validity. This will make your HTTPS connections insecure</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--kubeconfig string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Path to the kubeconfig file to use for CLI requests.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--match-server-version</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Require server version to match client version</p></td>
  > </tr>
  > <tr>
  > <td … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `kubectl-top`

**Question** (en, command): How do I see the current CPU and memory usage of my pods?

**Reference answer:** `kubectl top pod`; it needs the Metrics Server running in the cluster.

**Relevant documentation:**
- `reference/kubectl/generated/kubectl_top/_index.md`, section: *(whole document)*
  > [kubectl top]
  > ##
  > Display resource (CPU/memory) usage.
  >  The top command allows you to see the resource consumption for nodes or pods.
  >  This command requires Metrics Server to be correctly configured and working on the server.
  > ```
  > kubectl top [flags]
  > ```
  > ##
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  > <tr>
  > <td colspan="2">-h, --help</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>help for top</p></td>
  > </tr>
  > </tbody>
  > </table>
  > ##
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  > <tr>
  > <td colspan="2">--as string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Username to impersonate for the operation. User could be a regular user or a service account in a namespace.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--as-group strings</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Group to impersonate for the operation, this flag can be repeated to specify multiple groups.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--as-uid string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>UID to impersonate for the operation.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--cache-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: "$HOME/.kube/cache"</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Default cache directory</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--certificate-authority string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Path to a cert file for the certificate authority</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--client-certificate string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Path to a client certificate file for TLS</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--client-key string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Path to a client key file for TLS</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--cluster string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The name of the kubeconfig cluster to use</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--cluster string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The name of the kubeconfig cluster to use</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--context string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The name of the kubeconfig context to use</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--default-not-ready-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 300</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Indicates the tolerationSeconds of the toleration for notReady:NoExecute that is added by default to every pod that does not already have such a toleration.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--default-unreachable-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 300</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Indicates the tolerationSeconds of the toleration for unreachable:NoExecute that is added by default to every pod that does not already have such a toleration.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--disable-compression</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If true, opt-out of response compression for all requests to the server</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--insecure-skip-tls-verify</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If true, the server's certificate will not be checked for validity. This will make your HTTPS connections insecure</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--kubeconfig string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Path to the kubeconfig file to use for CLI requests.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--match-server-version</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Require server version to match client version</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-n, --namespace string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If present, the namespace scope for this CLI request</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-n, --namespace string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If present, the namespace scope for this CLI request</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--password string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Password for basic authentication to the API server</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--profile string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: "none"</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Name of profile to capture. One of (none|cpu|heap|goroutine|threadcreate|block|mutex)</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--profile-output string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: "profile.pprof"</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Name of the file to write the profile to</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--request-timeout string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: "0"</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The length of time to wait before giving up on a single server request. Non-zero values should contain a corresponding time unit (e.g. 1s, 2m, 3h). A value of zero means don't timeout requests.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-s, --server string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>The address and port of the Kubernetes API server</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--storage-driver-buffer-duration duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `switch-context`

**Question** (en, command): How do I switch kubectl between two clusters?

**Reference answer:** Define clusters, users and contexts in your kubeconfig, then switch with `kubectl config use-context <context>`.

**Relevant documentation:**
- `tasks/access-application-cluster/configure-access-multiple-clusters.md`, section: *Configure Access to Multiple Clusters > Define clusters, users, and contexts*
  > [Configure Access to Multiple Clusters > Define clusters, users, and contexts]
  > Suppose you have two clusters, one for development work and one for test work.
  > In the `development` cluster, your frontend developers work in a namespace called `frontend`,
  > and your storage developers work in a namespace called `storage`. In your `test` cluster,
  > developers work in the default namespace, or they create auxiliary namespaces as they
  > see fit. Access to the development cluster requires authentication by certificate. Access
  > to the test cluster requires authentication by username and password.
  > Create a directory named `config-exercise`. In your
  > `config-exercise` directory, create a file named `config-demo` with this content:
  > ```yaml
  > apiVersion: v1
  > kind: Config
  > preferences: {}
  > clusters:
  > - cluster:
  >   name: development
  > - cluster:
  >   name: test
  > users:
  > - name: developer
  > - name: experimenter
  > contexts:
  > - context:
  >   name: dev-frontend
  > - context:
  >   name: dev-storage
  > - context:
  >   name: exp-test
  > ```
  > A configuration file describes clusters, users, and contexts. Your `config-demo` file
  > has the framework to describe two clusters, two users, and three contexts.
  > Go to your `config-exercise` directory. Enter these commands to add cluster details to
  > your configuration file:
  > Go to your `config-exercise` directory. Enter these commands to add cluster details to
  > your configuration file:
  > ```shell
  > kubectl config --kubeconfig=config-demo set-cluster development --server=https://1.2.3.4 --certificate-authority=fake-ca-file
  > kubectl config --kubeconfig=config-demo set-cluster test --server=https://5.6.7.8 --insecure-skip-tls-verify
  > ```
  > Add user details to your configuration file:
  > Storing passwords in Kubernetes client config is risky. A better alternative would be to use a credential plugin and store them separately. See: client-go credential plugins
  > ```shell
  > kubectl config --kubeconfig=config-demo set-credentials developer --client-certificate=fake-cert-file --client-key=fake-key-seefile
  > kubectl config --kubeconfig=config-demo set-credentials experimenter --username=exp --password=some-password
  > ```
  > - To delete a user you can run `kubectl --kubeconfig=config-demo config unset users.<name>`
  > - To remove a cluster, you can run `kubectl --kubeconfig=config-demo config unset clusters.<name>`
  > - To remove a context, you can run `kubectl --kubeconfig=config-demo config unset contexts.<name>`
  > Add context details to your configuration file:
  > Add context details to your configuration file:
  > ```shell
  > kubectl config --kubeconfig=config-demo set-context dev-frontend --cluster=development --namespace=frontend --user=developer
  > kubectl config --kubeconfig=config-demo set-context dev-storage --cluster=development --namespace=storage --user=developer
  > kubectl config --kubeconfig=config-demo set-context exp-test --cluster=test --namespace=default --user=experimenter
  > ```
  > Open your `config-demo` file to see the added details. As an alternative to opening the
  > `config-demo` file, you can use the `config view` command.
  > ```shell
  > kubectl config --kubeconfig=config-demo view
  > ```
  > The output shows the two clusters, two users, and three contexts:
  > The output shows the two clusters, two users, and three contexts:
  > ```yaml
  > apiVersion: v1
  > clusters:
  > - cluster:
  >     certificate-authority: fake-ca-file
  >     server: https://1.2.3.4
  >   name: development
  > - cluster:
  >     insecure-skip-tls-verify: true
  >     server: https://5.6.7.8
  >   name: test
  > contexts:
  > - context:
  >     cluster: development
  >     namespace: frontend
  >     user: developer
  >   name: dev-frontend
  > - context:
  >     cluster: development
  >     namespace: storage
  >     user: developer
  >   name: dev-storage
  > - context:
  >     cluster: test
  >     namespace: default
  >     user: experimenter
  >   name: exp-test
  > current-context: ""
  > kind: Config
  > preferences: {}
  > users:
  > - name: developer
  >   user:
  >     client-certificate: fake-cert-file
  >     client-key: fake-key-file
  > - name: experimenter
  >   user:
  >     # Documentation note (this comment is NOT part of the command output).
  >     # Storing passwords in Kubernetes client config is risky.
  >     # A better alternative would be to use a credential plugin
  >     # and store the credentials separately.
  >     # See https://kubernetes.io/docs/reference/access-authn-authz/authentication/#client-go-credential-plugins
  >     password: some-password
  >     username: exp
  > ```
  > The `fake-ca-file`, `fake-cert-file` and `fake-key-file` above are the placeholders
  > for the pathnames of the certificate files. You need to change these to the actual pathnames
  > of certificate files in your environment.
  > Sometimes you may want to use Base64-encoded data embedded here instead of separate
  > certificate files; in that case you need to add the suffix `-data` to the keys, for example,
  > `certificate-authority-data`, `client-certificate-data`, `client-key-data`.
  > Each context is a triple (cluster, user, namespace). For example, the
  > `dev-frontend` context says, "Use the credentials of the `developer`
  > user to access the `frontend` namespace of the `development` cluster".
  > Set the current context:
  > ```shell
  > kubectl config --kubeconfig=config-demo use-context dev-frontend
  > ```
  > Now whenever you enter a `kubectl` command, the action will apply to the cluster,
  > and namespace listed in the `dev-frontend` context. And the command will use
  > the credentials of the user listed in the `dev-frontend` context.
  > To see only the configuration information associated with
  > the current context, use the `--minify` flag.
  > ```shell
  > kubectl config --kubeconfig=config-demo view --minify
  > ```
  > ```shell
  > kubectl config --kubeconfig=config-demo view --minify
  > ```
  > The output shows configuration information associated with the `dev-frontend` context:
  > ```yaml
  > apiVersion: v1
  > clusters:
  > - cluster:
  >     certificate-authority: fake-ca-file
  >     server: https://1.2.3.4
  >   name: development
  > contexts:
  > - context:
  >     cluster: development
  >     namespace: frontend
  >     user: developer
  >   name: dev-frontend
  > current-context: dev-frontend
  > kind: Config
  > preferences: {}
  > users:
  > - name: developer
  >   user:
  >  … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `rollout-status`

**Question** (en, command): How do I check whether a Deployment rollout has finished?

**Reference answer:** `kubectl rollout status deployment/<name>`.

**Relevant documentation:**
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
- `concepts/workloads/controllers/deployment.md`, section: *Deployments > Deployment status*
  > [Deployments > Deployment status]
  > A Deployment enters various states during its lifecycle. It can be progressing while
  > rolling out a new ReplicaSet, it can be complete, or it can fail to progress.
  > [Deployments > Deployment status > Progressing Deployment]
  > Kubernetes marks a Deployment as _progressing_ when one of the following tasks is performed:
  > * The Deployment creates a new ReplicaSet.
  > * The Deployment is scaling up its newest ReplicaSet.
  > * The Deployment is scaling down its older ReplicaSet(s).
  > * New Pods become ready or available (ready for at least MinReadySeconds).
  > When the rollout becomes “progressing”, the Deployment controller adds a condition with the following
  > attributes to the Deployment's `.status.conditions`:
  > * `type: Progressing`
  > * `status: "True"`
  > * `reason: NewReplicaSetCreated` | `reason: FoundNewReplicaSet` | `reason: ReplicaSetUpdated`
  > You can monitor the progress for a Deployment by using `kubectl rollout status`.
  > [Deployments > Deployment status > Complete Deployment]
  > Kubernetes marks a Deployment as _complete_ when it has the following characteristics:
  > * All of the replicas associated with the Deployment have been updated to the latest version you've specified, meaning any
  > updates you've requested have been completed.
  > * All of the replicas associated with the Deployment are available.
  > * No old replicas for the Deployment are running.
  > When the rollout becomes “complete”, the Deployment controller sets a condition with the following
  > attributes to the Deployment's `.status.conditions`:
  > * `type: Progressing`
  > * `status: "True"`
  > * `reason: NewReplicaSetAvailable`
  > This `Progressing` condition will retain a status value of `"True"` until a new rollout
  > is initiated. The condition holds even when availability of replicas changes (which
  > does instead affect the `Available` condition).
  > You can check if a Deployment has completed by using `kubectl rollout status`. If the rollout completed
  > successfully, `kubectl rollout status` returns a zero exit code.
  > You can check if a Deployment has completed by using `kubectl rollout status`. If the rollout completed
  > successfully, `kubectl rollout status` returns a zero exit code.
  > ```shell
  > kubectl rollout status deployment/nginx-deployment
  > ```
  > The output is similar to this:
  > ```
  > Waiting for rollout to finish: 2 of 3 updated replicas are available...
  > deployment "nginx-deployment" successfully rolled out
  > ```
  > and the exit status from `kubectl rollout` is 0 (success):
  > ```shell
  > echo $?
  > ```
  > ```
  > 0
  > ```
  > [Deployments > Deployment status > Failed Deployment]
  > Your Deployment may get stuck trying to deploy its newest ReplicaSet without ever completing. This can occur
  > due to some of the following factors:
  > * Insufficient quota
  > * Readiness probe failures
  > * Image pull errors
  > * Insufficient permissions
  > * Limit ranges
  > * Application runtime misconfiguration
  > One way you can detect this condition is to specify a deadline parameter in your Deployment spec:
  > (`.spec.progressDeadlineSeconds`). `.spec.progressDeadlineSeconds` denotes the
  > number of seconds the Deployment controller waits before indicating (in the Deployment status) that the
  > Deployment progress has stalled.
  > The following `kubectl` command sets the spec with `progressDeadlineSeconds` to make the controller report
  > lack of progress of a rollout for a Deployment after 10 minutes:
  > ```shell
  > kubectl patch deployment/nginx-deployment -p '{"spec":{"progressDeadlineSeconds":600}}'
  > ```
  > The output is similar to this:
  > ```
  > deployment.apps/nginx-deployment patched
  > ```
  > Once the deadline has been exceeded, the Deployment controller adds a DeploymentCondition with the following
  > attributes to the Deployment's `.status.conditions`:
  > * `type: Progressing`
  > * `status: "False"`
  > * `reason: ProgressDeadlineExceeded`
  > This condition can also fail early and is then set to status value of `"False"` due to reasons as `ReplicaSetCreateError`.
  > Also, the deadline is not taken into account anymore once the Deployment rollout completes.
  > See the Kubernetes API conventions for more information on status conditions.
  > Kubernetes takes no action on a stalled Deployment other than to report a status condition with
  > `reason: ProgressDeadlineExceeded`. Higher level orchestrators can take advantage of it and act accordingly, for
  > example, rollback the Deployment to its previous version.
  > If you pause a Deployment rollout, Kubernetes does not check progress against your specified deadline.
  > You can safely pause a Deployment rollout in the middle of a rollout and resume without triggering
  > the condition for exceeding the deadline.
  > You may experience transient errors with your Deployments, either due to a low timeout that you have set or
  > due to any other kind of error that can be treated as transient. For example, let's suppose you have
  > insufficient quota. If you describe the Deployment you will notice the following section:
  > ```shell
  > kubectl describe deployment nginx-deployment
  > ```
  > The output is similar to this:
  > ```
  > <...>
  > Conditions:
  >   Type            Status  Reason
  >   ----            ------  ------
  >   Available       True    MinimumReplicasAvailable
  >   Progressing     True    ReplicaSetUpdated
  >   ReplicaFailure  True    FailedCreate
  > <...>
  > ```
  > If you run `kubectl get deployment nginx-deployment -o yaml`, the Deployment status is similar to this:
  > If you run `kubectl get deployment nginx-deployment -o yaml`, the Deployment status is similar to this:
  > ```
  > status:
  >   availableReplicas: 2
  >   conditions:
  >   - lastTransitionTime: 2016-10-04T12:25:39Z
  >     lastUpdateTime: 2016-10-04T12:25:39Z
  >     message: Replica set "nginx-deployment-4262182780" is progressing.
  >     reason: ReplicaSetUpdated
  >     status: "True"
  >     type: Progressing
  >   - lastTransitionTime: 2016-10-04T12:25:42Z
  >     lastUpdateTime: 2016-10-04T12:25:42Z
  >     message: Deployment has minimum availability.
  >     reason: MinimumReplicasAvailable
  >     status: "True"
  >     type: Available
  >   - lastTransitionTime: 2016-10-04T12:25:39Z
  >     lastUpdateTime: 2016-10-04T12:25:39Z
  >     message: 'Error … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `kubectl-diff`

**Question** (en, command): How can I preview what applying a manifest would change in the cluster?

**Reference answer:** `kubectl diff -f ./my-manifest.yaml`.

**Relevant documentation:**
- `reference/kubectl/quick-reference.md`, section: *kubectl Quick Reference > Compares the current state of the cluster against the state that the cluster would be in if the manifest was applied.*
  > [kubectl Quick Reference > Compares the current state of the cluster against the state that the cluster would be in if the manifest was applied.]
  > kubectl diff -f ./my-manifest.yaml

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `replicaset-or-deployment`

**Question** (en, concept): Should I create ReplicaSets directly or use Deployments?

**Reference answer:** Use Deployments: they manage ReplicaSets and add declarative rolling updates. Create a ReplicaSet directly only if you need custom update orchestration or no updates at all.

**Relevant documentation:**
- `concepts/workloads/controllers/replicaset.md`, section: *ReplicaSet > When to use a ReplicaSet*
  > [ReplicaSet > When to use a ReplicaSet]
  > A ReplicaSet ensures that a specified number of pod replicas are running at any given
  > time. However, a Deployment is a higher-level concept that manages ReplicaSets and
  > provides declarative updates to Pods along with a lot of other useful features.
  > Therefore, we recommend using Deployments instead of directly using ReplicaSets, unless
  > you require custom update orchestration or don't require updates at all.
  > This actually means that you may never need to manipulate ReplicaSet objects:
  > use a Deployment instead, and define your application in the spec section.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---
