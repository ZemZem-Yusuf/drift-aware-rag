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

### `termination-message`

**Question** (en, troubleshooting): How can a container report why it failed, so the reason shows up in the Pod's status?

**Reference answer:** Write the reason to the termination message file (`/dev/termination-log` by default); it appears in the container's last terminated state (`lastState.terminated.message`, e.g. via `kubectl get pod <pod> --output=yaml`). With `terminationMessagePolicy: FallbackToLogsOnError`, the end of the logs is used if the file is empty and the container exited with an error.

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 2 (Youssef Zemzem, 2026-11-07): question now refers to the Pod status, as documented, instead of kubectl describe | human review v2 batch 3 (Youssef Zemzem, 2026-11-07): FallbackToLogsOnError: both conditions stated

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `oomkilled`

**Question** (en, troubleshooting): My container keeps getting OOMKilled. Why?

**Reference answer:** It uses more memory than its memory limit, so it can be terminated (OOMKilled); the kubelet restarts it if it can be restarted.

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 2 (Youssef Zemzem, 2026-11-07): removed the undocumented recommendations | human review v2 batch 3 (Youssef Zemzem, 2026-11-07): restart wording aligned with the docs

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `imagepullbackoff`

**Question** (en, troubleshooting): My pod is stuck in ImagePullBackOff. What are the common causes?

**Reference answer:** Kubernetes couldn't pull the container image, for reasons such as an invalid image name or pulling from a private registry without an `imagePullSecret`. It keeps retrying with an increasing back-off delay, up to 300 seconds.

**Relevant documentation:**
- `concepts/containers/images.md`, section: *Images > Updating images > ImagePullBackOff*
  > [Images > Updating images > ImagePullBackOff]
  > When a kubelet starts creating containers for a Pod using a container runtime,
  > it might be possible the container is in Waiting
  > state because of `ImagePullBackOff`.
  > The status `ImagePullBackOff` means that a container could not start because Kubernetes
  > could not pull a container image (for reasons such as invalid image name, or pulling
  > from a private registry without `imagePullSecret`). The `BackOff` part indicates
  > that Kubernetes will keep trying to pull the image, with an increasing back-off delay.
  > Kubernetes raises the delay between each attempt until it reaches a compiled-in limit,
  > which is 300 seconds (5 minutes).
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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 3 (Youssef Zemzem, 2026-11-07): added the ImagePullBackOff section; causes aligned with it

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `kubectl-top`

**Question** (en, command): How do I see the current CPU and memory usage of my pods?

**Reference answer:** `kubectl top pod`; it needs the Metrics Server running in the cluster.

**Relevant documentation:**
- `reference/kubectl/generated/kubectl_top/kubectl_top_pod.md`, section: *(whole document)*
  > [kubectl top pod]
  > ##
  > Display resource (CPU/memory) usage of pods.
  >  The 'top pod' command allows you to see the resource consumption of pods.
  >  Due to the metrics pipeline delay, they may be unavailable for a few minutes since pod creation.
  > ```
  > kubectl top pod [NAME | -l label]
  > ```
  > ##
  > ```
  >   # Show metrics for all pods in the default namespace
  >   kubectl top pod
  >   # Show metrics for all pods in the given namespace
  >   kubectl top pod --namespace=NAMESPACE
  >   # Show metrics for a given pod and its containers
  >   kubectl top pod POD_NAME --containers
  >   # Show metrics for the pods defined by label name=myLabel
  >   kubectl top pod -l name=myLabel
  > ```
  > ##
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  > <tr>
  > <td colspan="2">-A, --all-namespaces</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If present, list the requested object(s) across all namespaces. Namespace in current context is ignored even if specified with --namespace.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--containers</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If present, print usage of containers within a pod.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--field-selector string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Selector (field query) to filter on, supports '=', '==', and '!='.(e.g. --field-selector key1=value1,key2=value2). The server only supports a limited number of field queries per type.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-h, --help</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>help for pod</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--no-headers</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If present, print output without headers.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-l, --selector string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Selector (label query) to filter on, supports '=', '==', '!=', 'in', 'notin'.(e.g. -l key1=value1,key2=value2,key3 in (value3)). Matching objects must satisfy all of the specified label constraints.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--sort-by string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If non-empty, sort pods list using specified field. The field can be either 'cpu' or 'memory'.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--sum</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Print the sum of the resource usage</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--use-protocol-buffers&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: true</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Enables using protocol-buffers to access Metrics API.</p></td>
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
  > <td … (section continues)
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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 3 (Youssef Zemzem, 2026-11-07): added the kubectl top pod page

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `switch-context`

**Question** (en, command): How do I switch kubectl between two clusters?

**Reference answer:** Define clusters, users and contexts in a kubeconfig file, then switch with `kubectl config use-context <context>` (the documented example: `kubectl config --kubeconfig=config-demo use-context dev-frontend`).

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 3 (Youssef Zemzem, 2026-11-07): aligned with the documented command

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `replicaset-or-deployment`

**Question** (en, concept): Should I create ReplicaSets directly or use Deployments?

**Reference answer:** Use Deployments: a Deployment manages ReplicaSets and provides declarative updates to Pods. Create a ReplicaSet directly only if you need custom update orchestration or don't need updates at all.

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

*Drafting note:* golden v2 draft (2026-11-07) | human review v2 batch 3 (Youssef Zemzem, 2026-11-07): 'rolling updates' replaced with the documented 'declarative updates to Pods'

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `job-completions`

**Question** (en, task): How do I run a batch job that must succeed 5 times, with 2 pods running at a time?

**Reference answer:** Set `completions: 5` and `parallelism: 2` in the Job spec.

**Relevant documentation:**
- `concepts/workloads/controllers/job.md`, section: *Jobs > Writing a Job spec*
  > [Jobs > Writing a Job spec]
  > As with all other Kubernetes config, a Job needs `apiVersion`, `kind`, and `metadata` fields.
  > When the control plane creates new Pods for a Job, the `.metadata.name` of the
  > Job is part of the basis for naming those Pods. The name of a Job must be a valid
  > DNS subdomain
  > value, but this can produce unexpected results for the Pod hostnames. For best compatibility,
  > the name should follow the more restrictive rules for a
  > DNS label.
  > Even when the name is a DNS subdomain, the name must be no longer than 63
  > characters.
  > A Job also needs a `.spec` section.
  > [Jobs > Writing a Job spec > Job Labels]
  > Job labels will have `batch.kubernetes.io/` prefix for `job-name` and `controller-uid`.
  > [Jobs > Writing a Job spec > Pod Template]
  > The `.spec.template` is the only required field of the `.spec`.
  > The `.spec.template` is a pod template.
  > It has exactly the same schema as a Pod,
  > except it is nested and does not have an `apiVersion` or `kind`.
  > In addition to required fields for a Pod, a pod template in a Job must specify appropriate
  > labels (see pod selector) and an appropriate restart policy.
  > Only a `RestartPolicy`
  > equal to `Never` or `OnFailure` is allowed.
  > [Jobs > Writing a Job spec > Pod selector]
  > The `.spec.selector` field is optional. In almost all cases you should not specify it.
  > See section specifying your own pod selector.
  > [Jobs > Writing a Job spec > Parallel execution for Jobs {#parallel-jobs}]
  > There are three main types of task suitable to run as a Job:
  > 1. Non-parallel Jobs
  >    - normally, only one Pod is started, unless the Pod fails.
  >    - the Job is complete as soon as its Pod terminates successfully.
  > 1. Parallel Jobs with a *fixed completion count*:
  >    - specify a non-zero positive value for `.spec.completions`.
  >    - the Job represents the overall task, and is complete when there are `.spec.completions` successful Pods.
  >    - when using `.spec.completionMode="Indexed"`, each Pod gets a different index in the range 0 to `.spec.completions-1`.
  > 1. Parallel Jobs with a *work queue*:
  >    - do not specify `.spec.completions`, default to `.spec.parallelism`.
  >    - the Pods must coordinate amongst themselves or an external service to determine
  >      what each should work on. For example, a Pod might fetch a batch of up to N items from the work queue.
  >    - each Pod is independently capable of determining whether or not all its peers are done,
  >      and thus that the entire Job is done.
  >    - when _any_ Pod from the Job terminates with success, no new Pods are created.
  >    - once at least one Pod has terminated with success and all Pods are terminated,
  >      then the Job is completed with success.
  >    - once any Pod has exited with success, no other Pod should still be doing any work
  >      for this task or writing any output. They should all be in the process of exiting.
  > For a _non-parallel_ Job, you can leave both `.spec.completions` and `.spec.parallelism` unset.
  > When both are unset, both are defaulted to 1.
  > For a _fixed completion count_ Job, you should set `.spec.completions` to the number of completions needed.
  > You can set `.spec.parallelism`, or leave it unset and it will default to 1.
  > For a _work queue_ Job, you must leave `.spec.completions` unset, and set `.spec.parallelism` to
  > a non-negative integer.
  > For more information about how to make use of the different types of job,
  > see the job patterns section.
  > [Jobs > Writing a Job spec > Parallel execution for Jobs {#parallel-jobs} > Controlling parallelism]
  > The requested parallelism (`.spec.parallelism`) can be set to any non-negative value.
  > If it is unspecified, it defaults to 1.
  > If it is specified as 0, then the Job is effectively paused until it is increased.
  > Actual parallelism (number of pods running at any instant) may be more or less than requested
  > parallelism, for a variety of reasons:
  > - For _fixed completion count_ Jobs, the actual number of pods running in parallel will not exceed the number of
  >   remaining completions. Higher values of `.spec.parallelism` are effectively ignored.
  > - For _work queue_ Jobs, no new Pods are started after any Pod has succeeded -- remaining Pods are allowed to complete, however.
  > - If the Job  has not had time to react.
  > - If the Job controller failed to create Pods for any reason (lack of `ResourceQuota`, lack of permission, etc.),
  >   then there may be fewer pods than requested.
  > - The Job controller may throttle new Pod creation due to excessive previous pod failures in the same Job.
  > - When a Pod is gracefully shut down, it takes time to stop.
  > [Jobs > Writing a Job spec > Completion mode]
  > Jobs with _fixed completion count_ - that is, jobs that have non null
  > `.spec.completions` - can have a completion mode that is specified in `.spec.completionMode`:
  > - `NonIndexed` (default): the Job is considered complete when there have been
  >   `.spec.completions` successfully completed Pods. In other words, each Pod
  >   completion is homologous to each other. Note that Jobs that have null
  >   `.spec.completions` are implicitly `NonIndexed`.
  > - `Indexed`: the Pods of a Job get an associated completion index from 0 to
  >   `.spec.completions-1`. The index is available through four mechanisms:
  >   - The Pod annotation `batch.kubernetes.io/job-completion-index`.
  >   - The Pod label `batch.kubernetes.io/job-completion-index` (for v1.28 and later). Note
  >     the feature gate `PodIndexLabel` must be enabled to use this label, and it is enabled
  >     by default.
  >   - As part of the Pod hostname, following the pattern `$(job-name)-$(index)`.
  >     When you use an Indexed Job in combination with a
  >     , Pods within the Job can use
  >     the deterministic hostnames to address each other via DNS. For more information about
  >     how to configure this, see Job with Pod-to-Pod Communication.
  >   - From the containerized task, in the environment variable `JOB_COMPLETION_INDEX`.
  >   The Job is considered complete when there is one successfully completed Pod
  >   for each index. For more information about how to use this mode, see
  >   Indexed Job for … (section continues)

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The settings are correct for requesting five completions and a parallelism of two. However, the documentation explicitly says actual parallelism can be more or less than requested. Reword the question to ask for a requested parallelism of two, rather than guaranteeing exactly two Pods running at all times.

---

### `job-ttl`

**Question** (en, task): How do I have finished Jobs deleted automatically?

**Reference answer:** Set `ttlSecondsAfterFinished` on the Job; the TTL controller deletes it (and its Pods) that many seconds after it finishes.

**Relevant documentation:**
- `concepts/workloads/controllers/job.md`, section: *Jobs > Clean up finished jobs automatically*
  > [Jobs > Clean up finished jobs automatically]
  > Finished Jobs are usually no longer needed in the system. Keeping them around in
  > the system will put pressure on the API server. If the Jobs are managed directly
  > by a higher level controller, such as
  > CronJobs, the Jobs can be
  > cleaned up by CronJobs based on the specified capacity-based cleanup policy.
  > [Jobs > Clean up finished jobs automatically > TTL mechanism for finished Jobs]
  > Another way to clean up finished Jobs (either `Complete` or `Failed`)
  > automatically is to use a TTL mechanism provided by a
  > TTL controller for
  > finished resources, by specifying the `.spec.ttlSecondsAfterFinished` field of
  > the Job.
  > When the TTL controller cleans up the Job, it will delete the Job cascadingly,
  > i.e. delete its dependent objects, such as Pods, together with the Job. Note
  > that when the Job is deleted, its lifecycle guarantees, such as finalizers, will
  > be honored.
  > For example:
  > ```yaml
  > apiVersion: batch/v1
  > kind: Job
  > metadata:
  >   name: pi-with-ttl
  > spec:
  >   ttlSecondsAfterFinished: 100
  >   template:
  >     spec:
  >       containers:
  >       - name: pi
  >         image: perl:5.34.0
  >         command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
  >       restartPolicy: Never
  > ```
  > The Job `pi-with-ttl` will be eligible to be automatically deleted, `100`
  > seconds after it finishes.
  > If the field is set to `0`, the Job will be eligible to be automatically deleted
  > immediately after it finishes. If the field is unset, this Job won't be cleaned
  > up by the TTL controller after it finishes.
  > It is recommended to set `ttlSecondsAfterFinished` field because unmanaged jobs
  > (Jobs that you created directly, and not indirectly through other workload APIs
  > such as CronJob) have a default deletion
  > policy of `orphanDependents` causing Pods created by an unmanaged Job to be left around
  > after that Job is fully deleted.
  > Even though the control plane eventually
  > garbage collects
  > the Pods from a deleted Job after they either fail or complete, sometimes those
  > lingering pods may cause cluster performance degradation or in worst case cause the
  > cluster to go offline due to this degradation.
  > You can use LimitRanges and
  > ResourceQuotas to place a
  > cap on the amount of resources that a particular namespace can
  > consume.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The documentation says the Job becomes eligible for deletion after the TTL expires; it does not guarantee deletion at that exact instant. Change the answer to: “Set ttlSecondsAfterFinished on the Job. The TTL controller makes it eligible for deletion after that many seconds and deletes the Job and its dependent Pods.”

---

### `default-storageclass`

**Question** (en, concept): What happens when a PersistentVolumeClaim doesn't name a storage class?

**Reference answer:** If the cluster has a default StorageClass, it's used to dynamically provision a volume for the claim.

**Relevant documentation:**
- `concepts/storage/storage-classes.md`, section: *Storage Classes > Default StorageClass*
  > [Storage Classes > Default StorageClass]
  > You can mark a StorageClass as the default for your cluster.
  > For instructions on setting the default StorageClass, see
  > Change the default StorageClass.
  > When a PVC does not specify a `storageClassName`, the default StorageClass is
  > used.
  > If you set the
  > `storageclass.kubernetes.io/is-default-class`
  > annotation to true on more than one StorageClass in your cluster, and you then
  > create a PersistentVolumeClaim with no `storageClassName` set, Kubernetes
  > uses the most recently created default StorageClass.
  > You should try to only have one StorageClass in your cluster that is
  > marked as the default. The reason that Kubernetes allows you to have
  > multiple default StorageClasses is to allow for seamless migration.
  > You can create a PersistentVolumeClaim without specifying a `storageClassName`
  > for the new PVC, and you can do so even when no default StorageClass exists
  > in your cluster. In this case, the new PVC creates as you defined it, and the
  > `storageClassName` of that PVC remains unset until a default becomes available.
  > You can have a cluster without any default StorageClass. If you don't mark any
  > StorageClass as default (and one hasn't been set for you by, for example, a cloud provider),
  > then Kubernetes cannot apply that defaulting for PersistentVolumeClaims that need
  > it.
  > If or when a default StorageClass becomes available, the control plane identifies any
  > existing PVCs without `storageClassName`. For the PVCs that either have an empty
  > value for `storageClassName` or do not have this key, the control plane then
  > updates those PVCs to set `storageClassName` to match the new default StorageClass.
  > If you have an existing PVC where the `storageClassName` is `""`, and you configure
  > a default StorageClass, then this PVC will not get updated.
  > In order to keep binding to PVs with `storageClassName` set to `""`
  > (while a default StorageClass is present), you need to set the `storageClassName`
  > of the associated PVC to `""`.
- `concepts/storage/dynamic-provisioning.md`, section: *Dynamic Volume Provisioning > Defaulting Behavior*
  > [Dynamic Volume Provisioning > Defaulting Behavior]
  > Dynamic provisioning can be enabled on a cluster such that all claims are
  > dynamically provisioned if no storage class is specified. A cluster administrator
  > can enable this behavior by:
  > - Marking one `StorageClass` object as *default*;
  > - Making sure that the `DefaultStorageClass` admission controller
  >   is enabled on the API server.
  > An administrator can mark a specific `StorageClass` as default by adding the
  > `storageclass.kubernetes.io/is-default-class` annotation to it.
  > When a default `StorageClass` exists in a cluster and a user creates a
  > `PersistentVolumeClaim` with `storageClassName` unspecified, the
  > `DefaultStorageClass` admission controller automatically adds the
  > `storageClassName` field pointing to the default storage class.
  > Note that if you set the `storageclass.kubernetes.io/is-default-class`
  > annotation to true on more than one StorageClass in your cluster, and you then
  > create a `PersistentVolumeClaim` with no `storageClassName` set, Kubernetes
  > uses the most recently created default StorageClass.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The excerpts establish that the default StorageClass is assigned to a PVC without storageClassName. However, dynamic provisioning also requires dynamic provisioning to be enabled, including the DefaultStorageClass admission controller. Change the answer to distinguish default StorageClass assignment from the conditions needed for dynamic provisioning.

---

### `qos-classes`

**Question** (en, concept): What are the Pod QoS classes and how does Kubernetes assign them?

**Reference answer:** Guaranteed (every container has equal CPU and memory requests and limits), Burstable (at least one request or limit, but not Guaranteed) and BestEffort (no requests or limits). The class influences eviction order under node pressure.

**Relevant documentation:**
- `concepts/workloads/pods/pod-qos.md`, section: *Pod Quality of Service Classes > Quality of Service classes*
  > [Pod Quality of Service Classes > Quality of Service classes]
  > Kubernetes classifies the Pods that you run and allocates each Pod into a specific
  > _quality of service (QoS) class_. Kubernetes uses that classification to influence how different
  > pods are handled. Kubernetes does this classification based on the
  > resource requests
  > of the Containers in that Pod, along with
  > how those requests relate to resource limits.
  > This is known as Quality of Service
  > (QoS) class. Kubernetes assigns every Pod a QoS class based on the resource requests
  > and limits of its component Containers. QoS classes are used by Kubernetes to decide
  > which Pods to evict from a Node experiencing
  > Node Pressure. The possible
  > QoS classes are `Guaranteed`, `Burstable`, and `BestEffort`. When a Node runs out of resources,
  > Kubernetes will first evict `BestEffort` Pods running on that Node, followed by `Burstable` and
  > finally `Guaranteed` Pods. When this eviction is due to resource pressure, only Pods exceeding
  > resource requests are candidates for eviction.
  > [Pod Quality of Service Classes > Quality of Service classes > Guaranteed]
  > Pods that are `Guaranteed` have the strictest resource limits and are least likely
  > to face eviction. They are guaranteed not to be killed until they exceed their limits
  > or there are no lower-priority Pods that can be preempted from the Node. They may
  > not acquire resources beyond their specified limits. These Pods can also make
  > use of exclusive CPUs using the
  > `static` CPU management policy.
  > [Pod Quality of Service Classes > Quality of Service classes > Guaranteed > Criteria]
  > For a Pod to be given a QoS class of `Guaranteed`:
  > * Every Container in the Pod must have a memory limit and a memory request.
  > * For every Container in the Pod, the memory limit must equal the memory request.
  > * Every Container in the Pod must have a CPU limit and a CPU request.
  > * For every Container in the Pod, the CPU limit must equal the CPU request.
  > [Pod Quality of Service Classes > Quality of Service classes > Burstable]
  > Pods that are `Burstable` have some lower-bound resource guarantees based on the request, but
  > do not require a specific limit. If a limit is not specified, it defaults to a
  > limit equivalent to the capacity of the Node, which allows the Pods to flexibly increase
  > their resources if resources are available. In the event of Pod eviction due to Node
  > resource pressure, these Pods are evicted only after all `BestEffort` Pods are evicted.
  > Because a `Burstable` Pod can include a Container that has no resource limits or requests, a Pod
  > that is `Burstable` can try to use any amount of node resources.
  > [Pod Quality of Service Classes > Quality of Service classes > Burstable > Criteria]
  > A Pod is given a QoS class of `Burstable` if:
  > * The Pod does not meet the criteria for QoS class `Guaranteed`.
  > * At least one Container in the Pod has a memory or CPU request or limit.
  > [Pod Quality of Service Classes > Quality of Service classes > BestEffort]
  > Pods in the `BestEffort` QoS class can use node resources that aren't specifically assigned
  > to Pods in other QoS classes. For example, if you have a node with 16 CPU cores available to the
  > kubelet, and you assign 4 CPU cores to a `Guaranteed` Pod, then a Pod in the `BestEffort`
  > QoS class can try to use any amount of the remaining 12 CPU cores.
  > The kubelet prefers to evict `BestEffort` Pods if the node comes under resource pressure.
  > [Pod Quality of Service Classes > Quality of Service classes > BestEffort > Criteria]
  > A Pod has a QoS class of `BestEffort` if it doesn't meet the criteria for either `Guaranteed`
  > or `Burstable`. In other words, a Pod is `BestEffort` only if none of the Containers in the Pod have a
  > memory limit or a memory request, and none of the Containers in the Pod have a
  > CPU limit or a CPU request.
  > Containers in a Pod can request other resources (not CPU or memory) and still be classified as
  > `BestEffort`.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `priority-preemption`

**Question** (en, concept): How can important pods push out less important ones when the cluster is full?

**Reference answer:** Create a PriorityClass and set `priorityClassName` on the important Pods; when they can't be scheduled, the scheduler can preempt (evict) lower-priority Pods.

**Relevant documentation:**
- `concepts/scheduling-eviction/pod-priority-preemption.md`, section: *Pod Priority and Preemption > PriorityClass*
  > [Pod Priority and Preemption > PriorityClass]
  > A PriorityClass is a non-namespaced object that defines a mapping from a
  > priority class name to the integer value of the priority. The name is specified
  > in the `name` field of the PriorityClass object's metadata. The value is
  > specified in the required `value` field. The higher the value, the higher the
  > priority.
  > The name of a PriorityClass object must be a valid
  > DNS subdomain name,
  > and it cannot be prefixed with `system-`.
  > A PriorityClass object can have any 32-bit integer value smaller than or equal
  > to 1 billion. This means that the range of values for a PriorityClass object is
  > from -2147483648 to 1000000000 inclusive. Larger numbers are reserved for
  > built-in PriorityClasses that represent critical system Pods. A cluster
  > admin should create one PriorityClass object for each such mapping that they want.
  > PriorityClass also has two optional fields: `globalDefault` and `description`.
  > The `globalDefault` field indicates that the value of this PriorityClass should
  > be used for Pods without a `priorityClassName`. Only one PriorityClass with
  > `globalDefault` set to true can exist in the system. If there is no
  > PriorityClass with `globalDefault` set, the priority of Pods with no
  > `priorityClassName` is zero.
  > The `description` field is an arbitrary string. It is meant to tell users of the
  > cluster when they should use this PriorityClass.
  > [Pod Priority and Preemption > PriorityClass > Notes about PodPriority and existing clusters]
  > -   If you upgrade an existing cluster without this feature, the priority
  >     of your existing Pods is effectively zero.
  > -   Addition of a PriorityClass with `globalDefault` set to `true` does not
  >     change the priorities of existing Pods. The value of such a PriorityClass is
  >     used only for Pods created after the PriorityClass is added.
  > -   If you delete a PriorityClass, existing Pods that use the name of the
  >     deleted PriorityClass remain unchanged, but you cannot create more Pods that
  >     use the name of the deleted PriorityClass.
  > [Pod Priority and Preemption > PriorityClass > Example PriorityClass]
  > ```yaml
  > apiVersion: scheduling.k8s.io/v1
  > kind: PriorityClass
  > metadata:
  >   name: high-priority
  > value: 1000000
  > globalDefault: false
  > description: "This priority class should be used for XYZ service pods only."
  > ```
- `concepts/scheduling-eviction/pod-priority-preemption.md`, section: *Pod Priority and Preemption > Preemption*
  > [Pod Priority and Preemption > Preemption]
  > When Pods are created, they go to a queue and wait to be scheduled. The
  > scheduler picks a Pod from the queue and tries to schedule it on a Node. If no
  > Node is found that satisfies all the specified requirements of the Pod,
  > preemption logic is triggered for the pending Pod. Let's call the pending Pod P.
  > Preemption logic tries to find a Node where removal of one or more Pods with
  > lower priority than P would enable P to be scheduled on that Node. If such a
  > Node is found, one or more lower priority Pods get evicted from the Node. After
  > the Pods are gone, P can be scheduled on the Node.
  > [Pod Priority and Preemption > Preemption > User exposed information]
  > When Pod P preempts one or more Pods on Node N, `nominatedNodeName` field of Pod
  > P's status is set to the name of Node N. This field helps the scheduler track
  > resources reserved for Pod P and also gives users information about preemptions
  > in their clusters.
  > Please note that Pod P is not necessarily scheduled to the "nominated Node".
  > The scheduler always tries the "nominated Node" before iterating over any other nodes.
  > After victim Pods are preempted, they get their graceful termination period. If
  > another node becomes available while scheduler is waiting for the victim Pods to
  > terminate, scheduler may use the other node to schedule Pod P. As a result
  > `nominatedNodeName` and `nodeName` of Pod spec are not always the same. Also, if
  > the scheduler preempts Pods on Node N, but then a higher priority Pod than Pod P
  > arrives, the scheduler may give Node N to the new higher priority Pod. In such a
  > case, scheduler clears `nominatedNodeName` of Pod P. By doing this, scheduler
  > makes Pod P eligible to preempt Pods on another Node.
  > [Pod Priority and Preemption > Preemption > Limitations of preemption > Graceful termination of preemption victims]
  > When Pods are preempted, the victims get their
  > graceful termination period.
  > They have that much time to finish their work and exit. If they don't, they are
  > killed. This graceful termination period creates a time gap between the point
  > that the scheduler preempts Pods and the time when the pending Pod (P) can be
  > scheduled on the Node (N). In the meantime, the scheduler keeps scheduling other
  > pending Pods. As victims exit or get terminated, the scheduler tries to schedule
  > Pods in the pending queue. Therefore, there is usually a time gap between the
  > point that scheduler preempts victims and the time that Pod P is scheduled. In
  > order to minimize this gap, one can set graceful termination period of lower
  > priority Pods to zero or a small number.
  > [Pod Priority and Preemption > Preemption > Limitations of preemption > PodDisruptionBudget is supported, but not guaranteed]
  > A PodDisruptionBudget (PDB)
  > allows application owners to limit the number of Pods of a replicated application
  > that are down simultaneously from voluntary disruptions. Kubernetes supports
  > PDB when preempting Pods, but respecting PDB is best effort. The scheduler tries
  > to find victims whose PDB are not violated by preemption, but if no such victims
  > are found, preemption will still happen, and lower priority Pods will be removed
  > despite their PDBs being violated.
  > [Pod Priority and Preemption > Preemption > Limitations of preemption > Inter-Pod affinity on lower-priority Pods]
  > A Node is considered for preemption only when the answer to this question is
  > yes: "If all the Pods with lower priority than the pending Pod are removed from
  > the Node, can the pending Pod be scheduled on the Node?"
  > Preemption does not necessarily remove all lower-priority
  > Pods. If the pending Pod can be scheduled by removing fewer than all
  > lower-priority Pods, then only a portion of the lower-priority Pods are removed.
  > Even so, the answer to the preceding question must be yes. If the answer is no,
  > the Node is not considered for preemption.
  > If a pending Pod has inter-pod affinity
  > to one or more of the lower-priority Pods on the Node, the inter-Pod affinity
  > rule cannot be satisfied in the absence of those lower-priority Pods. In this case,
  > the scheduler does not preempt any Pods on the Node. Instead, it looks for another
  > Node. The scheduler might find a suitable Node or it might not. There is no
  > guarantee that the pending Pod can be scheduled.
  > Our recommended solution for this problem is to create inter-Pod affinity only
  > towards equal or higher priority Pods.
  > [Pod Priority and Preemption > Preemption > Limitations of preemption > Cross node preemption]
  > Suppose a Node N is being considered for preemption so that a pending Pod P can
  > be scheduled on N. P might become feasible on N only if a Pod on another Node is
  > preempted. Here's an example:
  > *   Pod P is being considered for Node N.
  > *   Pod Q is running on another Node in the same Zone as Node N.
  > *   Pod P has Zone-wide anti-affinity with Pod Q (`topologyKey:
  >     topology.kubernetes.io/zone`).
  > *   There are no other cases of anti-affinity between Pod P and other Pods in
  >     the Zone.
  > *   In order to schedule Pod P on Node N, Pod Q can be preempted, but scheduler
  >     does not perform cross-node preemption. So, Pod P will be deemed
  >     unschedulable on Node N.
  > If Pod Q were removed from its Node, the Pod anti-affinity violation would be
  > gone, and Pod P could possibly be scheduled on Node N.
  > We may consider adding cross Node preemption in future versions if there is
  > enough demand and if we find an algorithm with reasonable performance.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The excerpts explain PriorityClass values and how preemption removes lower-priority Pods to make room for a pending higher-priority Pod. However, they do not explicitly document setting priorityClassName in the Pod spec. Add the relevant Pod priority documentation showing how a Pod selects a PriorityClass.

---

### `sidecar-vs-init`

**Question** (en, concept): What is a sidecar container and how is it different from an init container?

**Reference answer:** Sidecars start before the app containers and keep running alongside them for the Pod's lifetime; init containers run to completion before the app starts.

**Relevant documentation:**
- `concepts/workloads/pods/sidecar-containers.md`, section: *Sidecar Containers > Differences from init containers*
  > [Sidecar Containers > Differences from init containers]
  > Sidecar containers work alongside the main container, extending its functionality and
  > providing additional services.
  > Sidecar containers run concurrently with the main application container. They are active
  > throughout the lifecycle of the pod and can be started and stopped independently of the
  > main container. Unlike init containers,
  > sidecar containers support probes to control their lifecycle.
  > Sidecar containers can interact directly with the main application containers, because
  > like init containers they always share the same network, and can optionally also share
  > volumes (filesystems).
  > Init containers stop before the main containers start up, so init containers cannot
  > exchange messages with the app container in a Pod. Any data passing is one-way
  > (for example, an init container can put information inside an `emptyDir` volume).
  > Changing the image of a sidecar container will not cause the Pod to restart, but will
  > trigger a container restart.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The excerpt supports sidecars running concurrently with the main application and remaining active throughout the Pod lifecycle. It does not explicitly state that sidecars start before application containers. Remove that claim, or add documentation supporting the startup ordering.

---

### `control-plane-components`

**Question** (en, concept): What does each part of the Kubernetes control plane do?

**Reference answer:** kube-apiserver exposes the API, etcd stores cluster data, kube-scheduler assigns Pods to nodes, kube-controller-manager runs the controllers; nodes run the kubelet, kube-proxy and a container runtime.

**Relevant documentation:**
- `concepts/overview/components.md`, section: *Kubernetes Components > Core Components*
  > [Kubernetes Components > Core Components]
  > A Kubernetes cluster consists of a control plane and one or more worker nodes.
  > Here's a brief overview of the main components:
  > [Kubernetes Components > Core Components > Control Plane Components]
  > Manage the overall state of the cluster:
  > kube-apiserver
  > : The core component server that exposes the Kubernetes HTTP API.
  > etcd
  > : Consistent and highly-available key value store for all API server data.
  > kube-scheduler
  > : Looks for Pods not yet bound to a node, and assigns each Pod to a suitable node.
  > kube-controller-manager
  > : Runs controllers to implement Kubernetes API behavior.
  > cloud-controller-manager (optional)
  > : Integrates with underlying cloud provider(s).
  > [Kubernetes Components > Core Components > Node Components]
  > Run on every node, maintaining running pods and providing the Kubernetes runtime environment:
  > kubelet
  > : Ensures that Pods are running, including their containers.
  > kube-proxy (optional)
  > : Maintains network rules on nodes to implement Services.
  > Container runtime
  > : Software responsible for running containers. Read
  >   Container Runtimes to learn more.
  > Your cluster may require additional software on each node; for example, you might also
  > run systemd on a Linux node to supervise local components.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The answer should mention the optional cloud-controller-manager, which is listed as a control-plane component in the excerpt. It should also clarify that kube-proxy is optional, rather than implying every node must run it.

---

### `immutable-configmap`

**Question** (en, concept): Can I make a ConfigMap read-only so nobody changes it by mistake?

**Reference answer:** Yes: set `immutable: true`. Its data can't be changed afterwards; delete and recreate it to change it.

**Relevant documentation:**
- `concepts/configuration/configmap.md`, section: *ConfigMaps > Immutable ConfigMaps*
  > [ConfigMaps > Immutable ConfigMaps {#configmap-immutable}]
  > The Kubernetes feature _Immutable Secrets and ConfigMaps_ provides an option to set
  > individual Secrets and ConfigMaps as immutable. For clusters that extensively use ConfigMaps
  > (at least tens of thousands of unique ConfigMap to Pod mounts), preventing changes to their
  > data has the following advantages:
  > - protects you from accidental (or unwanted) updates that could cause applications outages
  > - improves performance of your cluster by significantly reducing load on kube-apiserver, by
  >   closing watches for ConfigMaps marked as immutable.
  > You can create an immutable ConfigMap by setting the `immutable` field to `true`.
  > For example:
  > ```yaml
  > apiVersion: v1
  > kind: ConfigMap
  > metadata:
  >   ...
  > data:
  >   ...
  > immutable: true
  > ```
  > Once a ConfigMap is marked as immutable, it is _not_ possible to revert this change
  > nor to mutate the contents of the `data` or the `binaryData` field. You can
  > only delete and recreate the ConfigMap. Because existing Pods maintain a mount point
  > to the deleted ConfigMap, it is recommended to recreate these pods.
  > ##
  > ##
  > * Read about Secrets.
  > * Read Configure a Pod to Use a ConfigMap.
  > * Read about changing a ConfigMap (or any other Kubernetes object)
  > * Read The Twelve-Factor App to understand the motivation for
  >   separating code from configuration.

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `downward-api-pod-name`

**Question** (en, concept): How can a container find out its own pod name and namespace?

**Reference answer:** Through the Downward API: expose `metadata.name` and `metadata.namespace` as environment variables (`fieldRef`) or as files in a `downwardAPI` volume.

**Relevant documentation:**
- `concepts/workloads/pods/downward-api.md`, section: *Downward API > Available fields*
  > [Downward API > Available fields]
  > Only some Kubernetes API fields are available through the downward API. This
  > section lists which fields you can make available.
  > You can pass information from available Pod-level fields using `fieldRef`.
  > At the API level, the `spec` for a Pod always defines at least one
  > Container.
  > You can pass information from available Container-level fields using
  > `resourceFieldRef`.
  > [Downward API > Available fields > Information available via `fieldRef` {#downwardapi-fieldRef}]
  > For some Pod-level fields, you can provide them to a container either as
  > an environment variable or using a `downwardAPI` volume. The fields available
  > via either mechanism are:
  > `metadata.name`
  > : the pod's name
  > `metadata.namespace`
  > : the pod's namespace
  > `metadata.uid`
  > : the pod's unique ID
  > `metadata.annotations['<KEY>']`
  > : the value of the pod's annotation named `<KEY>` (for example, `metadata.annotations['myannotation']`)
  > `metadata.labels['<KEY>']`
  > : the text value of the pod's label named `<KEY>` (for example, `metadata.labels['mylabel']`)
  > The following information is available through environment variables
  > **but not as a downwardAPI volume fieldRef**:
  > `spec.serviceAccountName`
  > : the name of the pod's service account
  > `spec.nodeName`
  > : the name of the node where the Pod is executing
  > `status.hostIP`
  > : the primary IP address of the node to which the Pod is assigned
  > `status.hostIPs`
  > : the IP addresses is a dual-stack version of `status.hostIP`, the first is always the same as `status.hostIP`.
  > `status.podIP`
  > : the pod's primary IP address (usually, its IPv4 address)
  > `status.podIP`
  > : the pod's primary IP address (usually, its IPv4 address)
  > `status.podIPs`
  > : the IP addresses is a dual-stack version of `status.podIP`, the first is always the same as `status.podIP`
  > The following information is available through a `downwardAPI` volume
  > `fieldRef`, **but not as environment variables**:
  > `metadata.labels`
  > : all of the pod's labels, formatted as `label-key="escaped-label-value"` with one label per line
  > `metadata.annotations`
  > : all of the pod's annotations, formatted as `annotation-key="escaped-annotation-value"` with one annotation per line
  > [Downward API > Available fields > Information available via `resourceFieldRef` {#downwardapi-resourceFieldRef}]
  > These container-level fields allow you to provide information about
  > requests and limits
  > for resources such as CPU and memory.
  > Container CPU and memory resources can be resized while the container is running.
  > If this happens, a downward API volume will be updated,
  > but environment variables will not be updated unless the container restarts.
  > See Resize CPU and Memory Resources assigned to Containers
  > for more details.
  > `resource: limits.cpu`
  > : A container's CPU limit
  > `resource: requests.cpu`
  > : A container's CPU request
  > `resource: limits.memory`
  > : A container's memory limit
  > `resource: requests.memory`
  > : A container's memory request
  > `resource: limits.hugepages-*`
  > : A container's hugepages limit
  > `resource: requests.hugepages-*`
  > : A container's hugepages request
  > `resource: limits.ephemeral-storage`
  > : A container's ephemeral-storage limit
  > `resource: requests.ephemeral-storage`
  > : A container's ephemeral-storage request
  > [Downward API > Available fields > Information available via `resourceFieldRef` {#downwardapi-resourceFieldRef} > Fallback information for resource limits]
  > If CPU and memory limits are not specified for a container, and you use the
  > downward API to try to expose that information, then the
  > kubelet defaults to exposing the maximum allocatable value for CPU and memory
  > based on the node allocatable
  > calculation.
  > ##
  > You can read about `downwardAPI` volumes.
  > You can try using the downward API to expose container- or Pod-level information:
  > * as environment variables
  > * as files in `downwardAPI` volume

*Drafting note:* golden v2 draft (2026-11-07)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---
