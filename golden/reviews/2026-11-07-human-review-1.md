# Golden set review

For each question below:

1. Read the **question**: would a real user ask this? Is it clear and about Kubernetes v1.33?
2. Read the **documentation excerpts**: do they really answer the question? Is an obviously
   better section missing?
3. Read the **reference answer**: is it correct *according to the excerpts*?
4. Tick **exactly one** box (replace `[ ]` with `[x]`). If you pick *Needs changes*, write what
   to change under **Notes**.

Out-of-scope questions only need a check that they really are outside the Kubernetes docs.

When done, run: `uv run driftrag-golden apply --reviewer "Your Name"`

---

### `restart-deployment`

**Question** (en, command): How do I trigger a restart of all the pods in a Deployment?

**Reference answer:** Use `kubectl rollout restart deployment/<name>` (documented example: `kubectl rollout restart deployment/nginx`).

**Relevant documentation:**
- `reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart.md`, section: *(whole document)*
  > [kubectl rollout restart]
  > ##
  > Restart a resource.
  >         Resource rollout will be restarted.
  > ```
  > kubectl rollout restart RESOURCE
  > ```
  > ##
  > ```
  >   # Restart all deployments in the test-namespace namespace
  >   kubectl rollout restart deployment -n test-namespace
  >   # Restart a deployment
  >   kubectl rollout restart deployment/nginx
  >   # Restart a daemon set
  >   kubectl rollout restart daemonset/abc
  >   # Restart deployments with the app=nginx label
  >   kubectl rollout restart deployment --selector=app=nginx
  > ```
  > ##
  >    <table style="width: 100%; table-layout: fixed;">
  > <colgroup>
  > <col span="1" style="width: 10px;" />
  > <col span="1" />
  > </colgroup>
  > <tbody>
  > <tr>
  > <td colspan="2">--allow-missing-template-keys&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: true</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If true, ignore any errors in templates when a field or map key is missing in the template. Only applies to golang and jsonpath output formats.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--field-manager string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: "kubectl-rollout"</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Name of the manager used to track field ownership.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-f, --filename strings</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Filename, directory, or URL to files identifying the resource to get from a server.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-h, --help</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>help for restart</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-k, --kustomize string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Process the kustomization directory. This flag can't be used together with -f or -R.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-o, --output string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Output format. One of: (json, yaml, name, go-template, go-template-file, template, templatefile, jsonpath, jsonpath-as-json, jsonpath-file).</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-R, --recursive</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Process the directory used in -f, --filename recursively. Useful when you want to manage related manifests organized within the same directory.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">-l, --selector string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Selector (label query) to filter on, supports '=', '==', '!=', 'in', 'notin'.(e.g. -l key1=value1,key2=value2,key3 in (value3)). Matching objects must satisfy all of the specified label constraints.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--show-managed-fields</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>If true, keep the managedFields when printing objects in JSON or YAML format.</p></td>
  > </tr>
  > <tr>
  > <td colspan="2">--template string</td>
  > </tr>
  > <tr>
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Template string or path to template file to use when -o=go-template, -o=go-template-file. The template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].</p></td>
  > </tr>
  > </tbody>
  > </table>
  > ##
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
  > <td></td><td style="line-height: 130%; word-wrap: break-word;"><p>Indicates the tolerationSeconds of the toleration … (section continues)

*Drafting note:* Known hard case (E0): task wording vs command reference page. | LLM pre-review (ChatGPT, 2026-11-07): reworded question; removed claims about the spec and gradual replacement

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `resource-limits`

**Question** (en, task): How do I cap the CPU and memory a container is allowed to use?

**Reference answer:** Set `resources.limits.cpu` and `resources.limits.memory` on the container (and usually `resources.requests` for scheduling). CPU above the limit is throttled; a container that exceeds its memory limit can be OOM-killed.

**Relevant documentation:**
- `concepts/configuration/manage-resources-containers.md`, section: *Resource Management for Pods and Containers > Requests and limits*
  > [Resource Management for Pods and Containers > Requests and limits]
  > If the node where a Pod is running has enough of a resource available, it's possible (and
  > allowed) for a container to use more resource than its `request` for that resource specifies.
  > For example, if you set a `memory` request of 256 MiB for a container, and that container is in
  > a Pod scheduled to a Node with 8GiB of memory and no other Pods, then the container can try to use
  > more RAM.
  > Limits are a different story. Both `cpu` and `memory` limits are applied by the kubelet (and
  > container runtime),
  > and are ultimately enforced by the kernel. On Linux nodes, the Linux kernel
  > enforces limits with
  > cgroups.
  > The behavior of `cpu` and `memory` limit enforcement is slightly different.
  > `cpu` limits are enforced by CPU throttling. When a container approaches
  > its `cpu` limit, the kernel will restrict access to the CPU corresponding to the
  > container's limit. Thus, a `cpu` limit is a hard limit the kernel enforces.
  > Containers may not use more CPU than is specified in their `cpu` limit.
  > `memory` limits are enforced by the kernel with out of memory (OOM) kills. When
  > a container uses more than its `memory` limit, the kernel may terminate it. However,
  > terminations only happen when the kernel detects memory pressure. Thus, a
  > container that over allocates memory may not be immediately killed. This means
  > `memory` limits are enforced reactively. A container may use more memory than
  > its `memory` limit, but if it does, it may get killed.
  > There is an alpha feature `MemoryQoS` which attempts to add more preemptive
  > limit enforcement for memory (as opposed to reactive enforcement by the OOM
  > killer). However, this effort is
  > stalled
  > due to a potential livelock situation a memory hungry can cause.
  > If you specify a limit for a resource, but do not specify any request, and no admission-time
  > mechanism has applied a default request for that resource, then Kubernetes copies the limit
  > you specified and uses it as the requested value for the resource.
- `concepts/configuration/manage-resources-containers.md`, section: *Resource Management for Pods and Containers > Container resources example*
  > [Resource Management for Pods and Containers > Container resources example {#example-1}]
  > The following Pod has two containers. Both containers are defined with a request for
  > 0.25 CPU
  > and 64MiB (2<sup>26</sup> bytes) of memory. Each container has a limit of 0.5
  > CPU and 128MiB of memory. You can say the Pod has a request of 0.5 CPU and 128
  > MiB of memory, and a limit of 1 CPU and 256MiB of memory.
  > ```yaml
  > ---
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: frontend
  > spec:
  >   containers:
  >   - name: app
  >     image: images.my-company.example/app:v4
  >     resources:
  >       requests:
  >         memory: "64Mi"
  >         cpu: "250m"
  >       limits:
  >         memory: "128Mi"
  >         cpu: "500m"
  >   - name: log-aggregator
  >     image: images.my-company.example/log-aggregator:v6
  >     resources:
  >       requests:
  >         memory: "64Mi"
  >         cpu: "250m"
  >       limits:
  >         memory: "128Mi"
  >         cpu: "500m"
  > ```

*Drafting note:* Known partial answer in E0. | LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The CPU-throttling and memory-OOM statements are supported. However, the supplied excerpts do not say that `resources.requests` are used for scheduling. Add the scheduler explanation from the resource-management documentation or remove the phrase “for scheduling”.


---

### `probes-difference`

**Question** (en, concept): What's the difference between a liveness probe and a readiness probe?

**Reference answer:** A failing liveness probe makes the kubelet restart the container; a failing readiness probe removes the Pod from Service endpoints so it gets no traffic, without restarting it.

**Relevant documentation:**
- `concepts/configuration/liveness-readiness-startup-probes.md`, section: *(whole document)*
  > [Liveness, Readiness, and Startup Probes]
  > Kubernetes has various types of probes:
  > - Liveness probe
  > - Readiness probe
  > - Startup probe
  > [Liveness, Readiness, and Startup Probes > Liveness probe]
  > Liveness probes determine when to restart a container. For example, liveness probes could catch a deadlock when an application is running but unable to make progress.
  > If a container fails its liveness probe repeatedly, the kubelet restarts the container.
  > Liveness probes do not wait for readiness probes to succeed. If you want to wait before executing a liveness probe, you can either define `initialDelaySeconds` or use a
  > startup probe.
  > [Liveness, Readiness, and Startup Probes > Readiness probe]
  > Readiness probes determine when a container is ready to accept traffic. This is useful when waiting for an application to perform time-consuming initial tasks that depend on its backing services; for example: establishing network connections, loading files, and warming caches. Readiness probes can also be useful later in the container’s lifecycle, for example, when recovering from temporary faults or overloads.
  > If the readiness probe returns a failed state, Kubernetes removes the pod from all matching service endpoints.
  > Readiness probes run on the container during its whole lifecycle.
  > [Liveness, Readiness, and Startup Probes > Startup probe]
  > A startup probe verifies whether the application within a container is started. This can be used to adopt liveness checks on slow starting containers, avoiding them getting killed by the kubelet before they are up and running.
  > If such a probe is configured, it disables liveness and readiness checks until it succeeds.
  > This type of probe is only executed at startup, unlike liveness and readiness probes, which are run periodically.
  > * Read more about the Configure Liveness, Readiness and Startup Probes.
- `concepts/workloads/pods/pod-lifecycle.md`, section: *Pod Lifecycle > Container probes*
  > [Pod Lifecycle > Container probes]
  > A _probe_ is a diagnostic performed periodically by the kubelet
  > on a container. To perform a diagnostic, the kubelet either executes code within the container,
  > or makes a network request.
  > [Pod Lifecycle > Container probes > Check mechanisms {#probe-check-methods}]
  > There are four different ways to check a container using a probe.
  > Each probe must define exactly one of these four mechanisms:
  > `exec`
  > : Executes a specified command inside the container. The diagnostic
  >   is considered successful if the command exits with a status code of 0.
  > `grpc`
  > : Performs a remote procedure call using gRPC.
  >   The target should implement
  >   gRPC health checks.
  >   The diagnostic is considered successful if the `status`
  >   of the response is `SERVING`.
  > `httpGet`
  > : Performs an HTTP `GET` request against the Pod's IP
  >   address on a specified port and path. The diagnostic is
  >   considered successful if the response has a status code
  >   greater than or equal to 200 and less than 400.
  > `tcpSocket`
  > : Performs a TCP check against the Pod's IP address on
  >   a specified port. The diagnostic is considered successful if
  >   the port is open. If the remote system (the container) closes
  >   the connection immediately after it opens, this counts as healthy.
  > Unlike the other mechanisms, `exec` probe's implementation involves
  > the creation/forking of multiple processes each time when executed.
  > As a result, in case of the clusters having higher pod densities,
  > lower intervals of `initialDelaySeconds`, `periodSeconds`,
  > configuring any probe with exec mechanism might introduce an overhead on the cpu usage of the node.
  > In such scenarios, consider using the alternative probe mechanisms to avoid the overhead.
  > [Pod Lifecycle > Container probes > Probe outcome]
  > Each probe has one of three results:
  > `Success`
  > : The container passed the diagnostic.
  > `Failure`
  > : The container failed the diagnostic.
  > `Unknown`
  > : The diagnostic failed (no action should be taken, and the kubelet
  >   will make further checks).
  > [Pod Lifecycle > Container probes > Types of probe]
  > The kubelet can optionally perform and react to three kinds of probes on running
  > containers:
  > `livenessProbe`
  > : Indicates whether the container is running. If
  >   the liveness probe fails, the kubelet kills the container, and the container
  >   is subjected to its restart policy. If a container does not
  >   provide a liveness probe, the default state is `Success`.
  > `readinessProbe`
  > : Indicates whether the container is ready to respond to requests.
  >   If the readiness probe fails, the EndpointSlice controller removes the Pod's IP
  >   address from the EndpointSlices of all Services that match the Pod. The default
  >   state of readiness before the initial delay is `Failure`. If a container does
  >   not provide a readiness probe, the default state is `Success`.
  > `startupProbe`
  > : Indicates whether the application within the container is started.
  >   All other probes are disabled if a startup probe is provided, until it succeeds.
  >   If the startup probe fails, the kubelet kills the container, and the container
  >  is subjected to its restart policy. If a container does not
  >   provide a startup probe, the default state is `Success`.
  > For more information about how to set up a liveness, readiness, or startup probe,
  > see Configure Liveness, Readiness and Startup Probes.
  > [Pod Lifecycle > Container probes > Types of probe > When should you use a liveness probe?]
  > If the process in your container is able to crash on its own whenever it
  > encounters an issue or becomes unhealthy, you do not necessarily need a liveness
  > probe; the kubelet will automatically perform the correct action in accordance
  > with the Pod's `restartPolicy`.
  > If you'd like your container to be killed and restarted if a probe fails, then
  > specify a liveness probe, and specify a `restartPolicy` of Always or OnFailure.
  > [Pod Lifecycle > Container probes > Types of probe > When should you use a readiness probe?]
  > If you'd like to start sending traffic to a Pod only when a probe succeeds,
  > specify a readiness probe. In this case, the readiness probe might be the same
  > as the liveness probe, but the existence of the readiness probe in the spec means
  > that the Pod will start without receiving any traffic and only start receiving
  > traffic after the probe starts succeeding.
  > If you want your container to be able to take itself down for maintenance, you
  > can specify a readiness probe that checks an endpoint specific to readiness that
  > is different from the liveness probe.
  > If your app has a strict dependency on back-end services, you can implement both
  > a liveness and a readiness probe. The liveness probe passes when the app itself
  > is healthy, but the readiness probe additionally checks that each required
  > back-end service is available. This helps you avoid directing traffic to Pods
  > that can only respond with error messages.
  > If your container needs to work on loading large data, configuration files, or
  > migrations during startup, you can use a
  > startup probe. However, if you want to
  > detect the difference between an app that has failed and an app that is still
  > processing its startup data, you might prefer a readiness probe.
  > If you want to be able to drain requests when the Pod is deleted, you do not
  > necessarily need a readiness probe; when the Pod is deleted, the corresponding endpoint
  > in the `EndppointSlice` will update its conditions:
  > the endpoint `ready` condition will be set to `false`, so load balancers
  > will not use the Pod for regular traffic. See Pod termination
  > for more information about how the kubelet handles Pod deletion.
  > [Pod Lifecycle > Container probes > Types of probe > When should you use a startup probe?]
  > Startup probes are useful for Pods that have containers that take a long time to
  > come into service. Rather than set a long liveness interval, you can configure
  > a separate configuration for probing the container as it starts up, allowing
  > a time longer than the liveness interval would allow.
  > If your container usually starts in more … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `configmap-env`

**Question** (en, task): How can I turn every key of a ConfigMap into environment variables in my container?

**Reference answer:** Use `envFrom` in the container spec to define all of the ConfigMap's data as container environment variables.

**Relevant documentation:**
- `tasks/configure-pod-container/configure-pod-configmap.md`, section: *Configure a Pod to Use a ConfigMap > Configure all key-value pairs in a ConfigMap as container environment variables*
  > [Configure a Pod to Use a ConfigMap > Configure all key-value pairs in a ConfigMap as container environment variables]
  > * Create a ConfigMap containing multiple key-value pairs.
  >   Create the ConfigMap:
  >   ```shell
  >   kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml
  >   ```
  > * Use `envFrom` to define all of the ConfigMap's data as container environment variables. The
  >   key from the ConfigMap becomes the environment variable name in the Pod.
  >   Create the Pod:
  >   ```shell
  >   kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-envFrom.yaml
  >   ```
  >   Now, the Pod's output includes environment variables `SPECIAL_LEVEL=very` and
  >   `SPECIAL_TYPE=charm`.
  >   Once you're happy to move on, delete that Pod:
  >   ```shell
  >   kubectl delete pod dapi-test-pod --now
  >   ```

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): narrowed to the documented envFrom behaviour (the YAML example is not in the index)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `secret-encryption`

**Question** (en, concept): Are Kubernetes Secrets encrypted by default?

**Reference answer:** No. By default Secrets are stored unencrypted in etcd (values are only base64-encoded). Enable encryption at rest and restrict access with RBAC.

**Relevant documentation:**
- `concepts/configuration/secret.md`, section: *(whole document)*
  > [Secrets]
  > A Secret is an object that contains a small amount of sensitive data such as
  > a password, a token, or a key. Such information might otherwise be put in a
  >  specification or in a
  > container image. Using a
  > Secret means that you don't need to include confidential data in your
  > application code.
  > Because Secrets can be created independently of the Pods that use them, there
  > is less risk of the Secret (and its data) being exposed during the workflow of
  > creating, viewing, and editing Pods. Kubernetes, and applications that run in
  > your cluster, can also take additional precautions with Secrets, such as avoiding
  > writing sensitive data to nonvolatile storage.
  > Secrets are similar to ConfigMaps
  > but are specifically intended to hold confidential data.
  > Kubernetes Secrets are, by default, stored unencrypted in the API server's underlying data store
  > (etcd). Anyone with API access can retrieve or modify a Secret, and so can anyone with access to etcd.
  > Additionally, anyone who is authorized to create a Pod in a namespace can use that access to read
  > any Secret in that namespace; this includes indirect access such as the ability to create a
  > Deployment.
  > In order to safely use Secrets, take at least the following steps:
  > 1. Enable Encryption at Rest for Secrets.
  > 1. Enable or configure RBAC rules with
  >    least-privilege access to Secrets.
  > 1. Restrict Secret access to specific containers.
  > 1. Consider using external Secret store providers.
  > For more guidelines to manage and improve the security of your Secrets, refer to
  > Good practices for Kubernetes Secrets.
  > See Information security for Secrets for more details.
  > [Secrets > Uses for Secrets]
  > You can use Secrets for purposes such as the following:
  > - Set environment variables for a container.
  > - Provide credentials such as SSH keys or passwords to Pods.
  > - Allow the kubelet to pull container images from private registries.
  > The Kubernetes control plane also uses Secrets; for example,
  > bootstrap token Secrets are a mechanism to
  > help automate node registration.
  > [Secrets > Uses for Secrets > Use case: dotfiles in a secret volume]
  > You can make your data "hidden" by defining a key that begins with a dot.
  > This key represents a dotfile or "hidden" file. For example, when the following Secret
  > is mounted into a volume, `secret-volume`, the volume will contain a single file,
  > called `.secret-file`, and the `dotfile-test-container` will have this file
  > present at the path `/etc/secret-volume/.secret-file`.
  > Files beginning with dot characters are hidden from the output of `ls -l`;
  > you must use `ls -la` to see them when listing directory contents.
  > [Secrets > Uses for Secrets > Use case: Secret visible to one container in a Pod]
  > Consider a program that needs to handle HTTP requests, do some complex business
  > logic, and then sign some messages with an HMAC. Because it has complex
  > application logic, there might be an unnoticed remote file reading exploit in
  > the server, which could expose the private key to an attacker.
  > This could be divided into two processes in two containers: a frontend container
  > which handles user interaction and business logic, but which cannot see the
  > private key; and a signer container that can see the private key, and responds
  > to simple signing requests from the frontend (for example, over localhost networking).
  > With this partitioned approach, an attacker now has to trick the application
  > server into doing something rather arbitrary, which may be harder than getting
  > it to read a file.
  > [Secrets > Uses for Secrets > Alternatives to Secrets]
  > Rather than using a Secret to protect confidential data, you can pick from alternatives.
  > Here are some of your options:
  > - If your cloud-native component needs to authenticate to another application that you
  >   know is running within the same Kubernetes cluster, you can use a
  >   ServiceAccount
  >   and its tokens to identify your client.
  > - There are third-party tools that you can run, either within or outside your cluster,
  >   that manage sensitive data. For example, a service that Pods access over HTTPS,
  >   that reveals a Secret if the client correctly authenticates (for example, with a ServiceAccount
  >   token).
  > - For authentication, you can implement a custom signer for X.509 certificates, and use
  >   CertificateSigningRequests
  >   to let that custom signer issue certificates to Pods that need them.
  > - You can use a device plugin
  >   to expose node-local encryption hardware to a specific Pod. For example, you can schedule
  >   trusted Pods onto nodes that provide a Trusted Platform Module, configured out-of-band.
  > You can also combine two or more of those options, including the option to use Secret objects themselves.
  > You can also combine two or more of those options, including the option to use Secret objects themselves.
  > For example: implement (or deploy) an operator
  > that fetches short-lived session tokens from an external service, and then creates Secrets based
  > on those short-lived session tokens. Pods running in your cluster can make use of the session tokens,
  > and operator ensures they are valid. This separation means that you can run Pods that are unaware of
  > the exact mechanisms for issuing and refreshing those session tokens.
  > [Secrets > Types of Secret {#secret-types}]
  > When creating a Secret, you can specify its type using the `type` field of
  > the Secret
  > resource, or certain equivalent `kubectl` command line flags (if available).
  > The Secret type is used to facilitate programmatic handling of the Secret data.
  > Kubernetes provides several built-in types for some common usage scenarios.
  > These types vary in terms of the validations performed and the constraints
  > Kubernetes imposes on them.
  > Kubernetes provides several built-in types for some common usage scenarios.
  > These types vary in terms of the validations performed and the constraints
  > Kubernetes imposes on them.
  > | Built-in Type                         | Usage                                   |
  > | ------------------------------------- |---------------------------------------- … (section continues)

*Drafting note:* Common misconception; checks that the answer doesn't claim base64 is encryption. | LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The excerpt supports that Secrets are stored unencrypted in etcd by default and recommends encryption at rest and least-privilege RBAC. It does not say that the values are base64-encoded. Add the relevant excerpt about `data` values being base64-encoded, or remove that clause.


---

### `scale-deployment`

**Question** (en, command): How do I change the number of replicas of a Deployment from the command line?

**Reference answer:** `kubectl scale deployment/<name> --replicas=<n>`.

**Relevant documentation:**
- `concepts/workloads/controllers/deployment.md`, section: *Deployments > Scaling a Deployment*
  > [Deployments > Scaling a Deployment]
  > You can scale a Deployment by using the following command:
  > ```shell
  > kubectl scale deployment/nginx-deployment --replicas=10
  > ```
  > The output is similar to this:
  > ```
  > deployment.apps/nginx-deployment scaled
  > ```
  > Assuming horizontal Pod autoscaling is enabled
  > in your cluster, you can set up an autoscaler for your Deployment and choose the minimum and maximum number of
  > Pods you want to run based on the CPU utilization of your existing Pods.
  > ```shell
  > kubectl autoscale deployment/nginx-deployment --min=10 --max=15 --cpu-percent=80
  > ```
  > The output is similar to this:
  > ```
  > deployment.apps/nginx-deployment scaled
  > ```
  > [Deployments > Scaling a Deployment > Proportional scaling]
  > RollingUpdate Deployments support running multiple versions of an application at the same time. When you
  > or an autoscaler scales a RollingUpdate Deployment that is in the middle of a rollout (either in progress
  > or paused), the Deployment controller balances the additional replicas in the existing active
  > ReplicaSets (ReplicaSets with Pods) in order to mitigate risk. This is called *proportional scaling*.
  > For example, you are running a Deployment with 10 replicas, maxSurge=3, and maxUnavailable=2.
  > * Ensure that the 10 replicas in your Deployment are running.
  >   ```shell
  >   kubectl get deploy
  >   ```
  >   The output is similar to this:
  >   ```
  >   NAME                 DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
  >   nginx-deployment     10        10        10           10          50s
  >   ```
  > * You update to a new image which happens to be unresolvable from inside the cluster.
  >   ```shell
  >   kubectl set image deployment/nginx-deployment nginx=nginx:sometag
  >   ```
  >   The output is similar to this:
  >   ```
  >   deployment.apps/nginx-deployment image updated
  >   ```
  >   The output is similar to this:
  >   ```
  >   deployment.apps/nginx-deployment image updated
  >   ```
  > * The image update starts a new rollout with ReplicaSet nginx-deployment-1989198191, but it's blocked due to the
  > `maxUnavailable` requirement that you mentioned above. Check out the rollout status:
  >   ```shell
  >   kubectl get rs
  >   ```
  >   The output is similar to this:
  >   ```
  >   NAME                          DESIRED   CURRENT   READY     AGE
  >   nginx-deployment-1989198191   5         5         0         9s
  >   nginx-deployment-618515232    8         8         8         1m
  >   ```
  > * Then a new scaling request for the Deployment comes along. The autoscaler increments the Deployment replicas
  > to 15. The Deployment controller needs to decide where to add these new 5 replicas. If you weren't using
  > proportional scaling, all 5 of them would be added in the new ReplicaSet. With proportional scaling, you
  > spread the additional replicas across all ReplicaSets. Bigger proportions go to the ReplicaSets with the
  > most replicas and lower proportions go to ReplicaSets with less replicas. Any leftovers are added to the
  > ReplicaSet with the most replicas. ReplicaSets with zero replicas are not scaled up.
  > In our example above, 3 replicas are added to the old ReplicaSet and 2 replicas are added to the
  > new ReplicaSet. The rollout process should eventually move all replicas to the new ReplicaSet, assuming
  > the new replicas become healthy. To confirm this, run:
  > ```shell
  > kubectl get deploy
  > ```
  > The output is similar to this:
  > ```
  > NAME                 DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
  > nginx-deployment     15        18        7            8           7m
  > ```
  > The rollout status confirms how the replicas were added to each ReplicaSet.
  > ```shell
  > kubectl get rs
  > ```
  > The output is similar to this:
  > ```
  > NAME                          DESIRED   CURRENT   READY     AGE
  > nginx-deployment-1989198191   7         7         0         7m
  > nginx-deployment-618515232    11        11        11        7m
  > ```

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `rollback-deployment`

**Question** (en, task): I deployed a broken version of my app. How do I go back to the previous version?

**Reference answer:** `kubectl rollout undo deployment/<name>` (optionally `--to-revision=<n>`); `kubectl rollout history` lists revisions.

**Relevant documentation:**
- `concepts/workloads/controllers/deployment.md`, section: *Deployments > Rolling Back a Deployment*
  > [Deployments > Rolling Back a Deployment]
  > Sometimes, you may want to rollback a Deployment; for example, when the Deployment is not stable, such as crash looping.
  > By default, all of the Deployment's rollout history is kept in the system so that you can rollback anytime you want
  > (you can change that by modifying revision history limit).
  > A Deployment's revision is created when a Deployment's rollout is triggered. This means that the
  > new revision is created if and only if the Deployment's Pod template (`.spec.template`) is changed,
  > for example if you update the labels or container images of the template. Other updates, such as scaling the Deployment,
  > do not create a Deployment revision, so that you can facilitate simultaneous manual- or auto-scaling.
  > This means that when you roll back to an earlier revision, only the Deployment's Pod template part is
  > rolled back.
  > * Suppose that you made a typo while updating the Deployment, by putting the image name as `nginx:1.161` instead of `nginx:1.16.1`:
  >   ```shell
  >   kubectl set image deployment/nginx-deployment nginx=nginx:1.161
  >   ```
  >   The output is similar to this:
  >   ```
  >   deployment.apps/nginx-deployment image updated
  >   ```
  >   The output is similar to this:
  >   ```
  >   deployment.apps/nginx-deployment image updated
  >   ```
  > * The rollout gets stuck. You can verify it by checking the rollout status:
  >   ```shell
  >   kubectl rollout status deployment/nginx-deployment
  >   ```
  >   The output is similar to this:
  >   ```
  >   Waiting for rollout to finish: 1 out of 3 new replicas have been updated...
  >   ```
  > * Press Ctrl-C to stop the above rollout status watch. For more information on stuck rollouts,
  > read more here.
  > * You see that the number of old replicas (adding the replica count from
  >   `nginx-deployment-1564180365` and `nginx-deployment-2035384211`) is 3, and the number of
  >   new replicas (from `nginx-deployment-3066724191`) is 1.
  >   ```shell
  >   kubectl get rs
  >   ```
  >   The output is similar to this:
  >   ```
  >   NAME                          DESIRED   CURRENT   READY   AGE
  >   nginx-deployment-1564180365   3         3         3       25s
  >   nginx-deployment-2035384211   0         0         0       36s
  >   nginx-deployment-3066724191   1         1         0       6s
  >   ```
  > * Looking at the Pods created, you see that 1 Pod created by new ReplicaSet is stuck in an image pull loop.
  >   ```shell
  >   kubectl get pods
  >   ```
  >   ```shell
  >   kubectl get pods
  >   ```
  >   The output is similar to this:
  >   ```
  >   NAME                                READY     STATUS             RESTARTS   AGE
  >   nginx-deployment-1564180365-70iae   1/1       Running            0          25s
  >   nginx-deployment-1564180365-jbqqo   1/1       Running            0          25s
  >   nginx-deployment-1564180365-hysrc   1/1       Running            0          25s
  >   nginx-deployment-3066724191-08mng   0/1       ImagePullBackOff   0          6s
  >   ```
  >   The Deployment controller stops the bad rollout automatically, and stops scaling up the new ReplicaSet. This depends on the rollingUpdate parameters (`maxUnavailable` specifically) that you have specified. Kubernetes by default sets the value to 25%.
  > * Get the description of the Deployment:
  >   ```shell
  >   kubectl describe deployment
  >   ```
  > * Get the description of the Deployment:
  >   ```shell
  >   kubectl describe deployment
  >   ```
  >   The output is similar to this:
  >   ```
  >   Name:           nginx-deployment
  >   Namespace:      default
  >   CreationTimestamp:  Tue, 15 Mar 2016 14:48:04 -0700
  >   Labels:         app=nginx
  >   Selector:       app=nginx
  >   Replicas:       3 desired | 1 updated | 4 total | 3 available | 1 unavailable
  >   StrategyType:       RollingUpdate
  >   MinReadySeconds:    0
  >   RollingUpdateStrategy:  25% max unavailable, 25% max surge
  >   Pod Template:
  >     Labels:  app=nginx
  >     Containers:
  >      nginx:
  >       Image:        nginx:1.161
  >       Port:         80/TCP
  >       Host Port:    0/TCP
  >       Environment:  <none>
  >       Mounts:       <none>
  >     Volumes:        <none>
  >   Conditions:
  >     Type           Status  Reason
  >     ----           ------  ------
  >     Available      True    MinimumReplicasAvailable
  >     Progressing    True    ReplicaSetUpdated
  >   OldReplicaSets:     nginx-deployment-1564180365 (3/3 replicas created)
  >   NewReplicaSet:      nginx-deployment-3066724191 (1/1 replicas created)
  >   Events:
  >     FirstSeen LastSeen    Count   From                    SubObjectPath   Type        Reason              Message
  >     --------- --------    -----   ----                    -------------   --------    ------              -------
  >     1m        1m          1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-2035384211 to 3
  >     22s       22s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-1564180365 to 1
  >     22s       22s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled down replica set nginx-deployment-2035384211 to 2
  >     22s       22s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-1564180365 to 2
  >     21s       21s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled down replica set nginx-deployment-2035384211 to 1
  >     21s       21s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-1564180365 to 3
  >     13s       13s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled down replica set nginx-deployment-2035384211 to 0
  >     13s       13s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-3066724191 to 1
  >   ```
  >   To fix this, you need to rollback to a previous revision of Deployment that is stable.
  > [Deployments > Rolling Back a Deployment > Checking Rollout History of a Deployment]
  > Follow the steps given … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The excerpt explains why a Deployment may need rollback and introduces the rollout-history section, but the shown text does not include `kubectl rollout undo`, `--to-revision`, or `kubectl rollout history`. Add the actual “Checking Rollout History” and “Rolling Back to a Previous Revision” command excerpts, or remove those command claims.


---

### `service-types`

**Question** (en, concept): When should I use a NodePort Service instead of ClusterIP or LoadBalancer?

**Reference answer:** ClusterIP is reachable only inside the cluster (default). NodePort opens a static port on every node for external access. LoadBalancer provisions an external load balancer from the cloud provider.

**Relevant documentation:**
- `concepts/services-networking/service.md`, section: *Service > Service type*
  > [Service > Service type  {#publishing-services-service-types}]
  > For some parts of your application (for example, frontends) you may want to expose a
  > Service onto an external IP address, one that's accessible from outside of your
  > cluster.
  > Kubernetes Service types allow you to specify what kind of Service you want.
  > The available `type` values and their behaviors are:
  > `ClusterIP`
  > : Exposes the Service on a cluster-internal IP. Choosing this value
  >   makes the Service only reachable from within the cluster. This is the
  >   default that is used if you don't explicitly specify a `type` for a Service.
  >   You can expose the Service to the public internet using an
  >   Ingress or a
  >   Gateway.
  > `NodePort`
  > : Exposes the Service on each Node's IP at a static port (the `NodePort`).
  >   To make the node port available, Kubernetes sets up a cluster IP address,
  >   the same as if you had requested a Service of `type: ClusterIP`.
  > `LoadBalancer`
  > : Exposes the Service externally using an external load balancer. Kubernetes
  >   does not directly offer a load balancing component; you must provide one, or
  >   you can integrate your Kubernetes cluster with a cloud provider.
  > `ExternalName`
  > : Maps the Service to the contents of the `externalName` field (for example,
  >   to the hostname `api.foo.bar.example`). The mapping configures your cluster's
  >   DNS server to return a `CNAME` record with that external hostname value.
  >   No proxying of any kind is set up.
  > The `type` field in the Service API is designed as nested functionality - each level
  > adds to the previous. However there is an exception to this nested design. You can
  > define a `LoadBalancer` Service by
  > disabling the load balancer `NodePort` allocation.
  > [Service > Service type  {#publishing-services-service-types} > `type: ClusterIP` {#type-clusterip}]
  > This default Service type assigns an IP address from a pool of IP addresses that
  > your cluster has reserved for that purpose.
  > Several of the other types for Service build on the `ClusterIP` type as a
  > foundation.
  > If you define a Service that has the `.spec.clusterIP` set to `"None"` then
  > Kubernetes does not assign an IP address. See headless Services
  > for more information.
  > [Service > Service type  {#publishing-services-service-types} > `type: ClusterIP` {#type-clusterip} > Choosing your own IP address]
  > You can specify your own cluster IP address as part of a `Service` creation
  > request.  To do this, set the `.spec.clusterIP` field. For example, if you
  > already have an existing DNS entry that you wish to reuse, or legacy systems
  > that are configured for a specific IP address and difficult to re-configure.
  > The IP address that you choose must be a valid IPv4 or IPv6 address from within the
  > `service-cluster-ip-range` CIDR range that is configured for the API server.
  > If you try to create a Service with an invalid `clusterIP` address value, the API
  > server will return a 422 HTTP status code to indicate that there's a problem.
  > Read avoiding collisions
  > to learn how Kubernetes helps reduce the risk and impact of two different Services
  > both trying to use the same IP address.
  > [Service > Service type  {#publishing-services-service-types} > `type: NodePort` {#type-nodeport}]
  > If you set the `type` field to `NodePort`, the Kubernetes control plane
  > allocates a port from a range specified by `--service-node-port-range` flag (default: 30000-32767).
  > Each node proxies that port (the same port number on every Node) into your Service.
  > Your Service reports the allocated port in its `.spec.ports[*].nodePort` field.
  > Using a NodePort gives you the freedom to set up your own load balancing solution,
  > to configure environments that are not fully supported by Kubernetes, or even
  > to expose one or more nodes' IP addresses directly.
  > For a node port Service, Kubernetes additionally allocates a port (TCP, UDP or
  > SCTP to match the protocol of the Service). Every node in the cluster configures
  > itself to listen on that assigned port and to forward traffic to one of the ready
  > endpoints associated with that Service. You'll be able to contact the `type: NodePort`
  > Service, from outside the cluster, by connecting to any node using the appropriate
  > protocol (for example: TCP), and the appropriate port (as assigned to that Service).
  > [Service > Service type  {#publishing-services-service-types} > `type: NodePort` {#type-nodeport} > Choosing your own port {#nodeport-custom-port}]
  > If you want a specific port number, you can specify a value in the `nodePort`
  > field. The control plane will either allocate you that port or report that
  > the API transaction failed.
  > This means that you need to take care of possible port collisions yourself.
  > You also have to use a valid port number, one that's inside the range configured
  > for NodePort use.
  > Here is an example manifest for a Service of `type: NodePort` that specifies
  > a NodePort value (30007, in this example):
  > ```yaml
  > apiVersion: v1
  > kind: Service
  > metadata:
  >   name: my-service
  > spec:
  >   type: NodePort
  >   selector:
  >     app.kubernetes.io/name: MyApp
  >   ports:
  >     - port: 80
  >       # By default and for convenience, the `targetPort` is set to
  >       # the same value as the `port` field.
  >       targetPort: 80
  >       # Optional field
  >       # By default and for convenience, the Kubernetes control plane
  >       # will allocate a port from a range (default: 30000-32767)
  >       nodePort: 30007
  > ```
  > [Service > Service type  {#publishing-services-service-types} > `type: NodePort` {#type-nodeport} > Reserve Nodeport ranges to avoid collisions  {#avoid-nodeport-collisions}]
  > The policy for assigning ports to NodePort services applies to both the auto-assignment and
  > the manual assignment scenarios. When a user wants to create a NodePort service that
  > uses a specific port, the target port may conflict with another port that has already been assigned.
  > To avoid this problem, the port range for NodePort services is divided into two bands.
  > Dynamic port assignment uses the upper band by default, and it may use the lower band once the
  > upper band has been exhausted. Users … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The answer defines the Service types but does not state when NodePort is preferable. Include the documented NodePort use cases: providing your own load-balancing solution, supporting environments without a managed load balancer, or exposing node IPs directly. Also qualify LoadBalancer: Kubernetes does not itself provide the load-balancing component; one must be supplied or integrated through a cloud provider.


---

### `pod-pending`

**Question** (en, troubleshooting): My pod has been stuck in Pending for a long time. What can cause that?

**Reference answer:** The Pod can't be scheduled: usually not enough CPU or memory on any node, or a hostPort conflict. `kubectl describe pod` shows the scheduler's events explaining why.

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

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `crashloop`

**Question** (en, troubleshooting): My container keeps crashing and restarting in a loop. How do I find out why?

**Reference answer:** Read the logs of the previous (crashed) container instance with `kubectl logs <pod> --previous`, and inspect the Pod with `kubectl describe pod`. The kubelet restarts the failing container with an exponential backoff delay (CrashLoopBackOff).

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
- `concepts/workloads/pods/pod-lifecycle.md`, section: *Pod Lifecycle > How Pods handle problems with containers*
  > [Pod Lifecycle > How Pods handle problems with containers {#container-restarts}]
  > Kubernetes manages container failures within Pods using a `restartPolicy` defined in the Pod `spec`. This policy determines how Kubernetes reacts to containers exiting due to errors or other reasons, which falls in the following sequence:
  > 1. **Initial crash**: Kubernetes attempts an immediate restart based on the Pod `restartPolicy`.
  > 1. **Repeated crashes**: After the initial crash Kubernetes applies an exponential
  >    backoff delay for subsequent restarts, described in `restartPolicy`.
  >    This prevents rapid, repeated restart attempts from overloading the system.
  > 1. **CrashLoopBackOff state**: This indicates that the backoff delay mechanism is currently
  >    in effect for a given container that is in a crash loop, failing and restarting repeatedly.
  > 1. **Backoff reset**: If a container runs successfully for a certain duration
  >    (e.g., 10 minutes), Kubernetes resets the backoff delay, treating any new crash
  >    as the first one.
  > In practice, a `CrashLoopBackOff` is a condition or event that might be seen as output
  > from the `kubectl` command, while describing or listing Pods, when a container in the Pod
  > fails to start properly and then continually tries and fails in a loop.
  > In other words, when a container enters the crash loop, Kubernetes applies the
  > exponential backoff delay mentioned in the Container restart policy.
  > This mechanism prevents a faulty container from overwhelming the system with continuous
  > failed start attempts.
  > The `CrashLoopBackOff` can be caused by issues like the following:
  > * Application errors that cause the container to exit.
  > * Configuration errors, such as incorrect environment variables or missing
  >   configuration files.
  > * Resource constraints, where the container might not have enough memory or CPU
  >   to start properly.
  > * Health checks failing if the application doesn't start serving within the
  >   expected time.
  > * Container liveness probes or startup probes returning a `Failure` result
  >   as mentioned in the probes section.
  > To investigate the root cause of a `CrashLoopBackOff` issue, a user can:
  > To investigate the root cause of a `CrashLoopBackOff` issue, a user can:
  > 1. **Check logs**: Use `kubectl logs <name-of-pod>` to check the logs of the container.
  >    This is often the most direct way to diagnose the issue causing the crashes.
  > 1. **Inspect events**: Use `kubectl describe pod <name-of-pod>` to see events
  >    for the Pod, which can provide hints about configuration or resource issues.
  > 1. **Review configuration**: Ensure that the Pod configuration, including
  >    environment variables and mounted volumes, is correct and that all required
  >    external resources are available.
  > 1. **Check resource limits**: Make sure that the container has enough CPU
  >    and memory allocated. Sometimes, increasing the resources in the Pod definition
  >    can resolve the issue.
  > 1. **Debug application**: There might exist bugs or misconfigurations in the
  >    application code. Running this container image locally or in a development
  >    environment can help diagnose application specific issues.
  > [Pod Lifecycle > How Pods handle problems with containers {#container-restarts} > Container restart policy {#restart-policy}]
  > The `spec` of a Pod has a `restartPolicy` field with possible values Always, OnFailure,
  > and Never. The default value is Always.
  > The `restartPolicy` for a Pod applies to app containers
  > in the Pod and to regular init containers.
  > Sidecar containers
  > ignore the Pod-level `restartPolicy` field: in Kubernetes, a sidecar is defined as an
  > entry inside `initContainers` that has its container-level `restartPolicy` set to `Always`.
  > For init containers that exit with an error, the kubelet restarts the init container if
  > the Pod level `restartPolicy` is either `OnFailure` or `Always`:
  > * `Always`: Automatically restarts the container after any termination.
  > * `OnFailure`: Only restarts the container if it exits with an error (non-zero exit status).
  > * `Never`: Does not automatically restart the terminated container.
  > When the kubelet is handling container restarts according to the configured restart
  > policy, that only applies to restarts that make replacement containers inside the
  > same Pod and running on the same node. After containers in a Pod exit, the kubelet
  > restarts them with an exponential backoff delay (10s, 20s, 40s, …), that is capped at
  > 300 seconds (5 minutes). Once a container has executed for 10 minutes without any
  > problems, the kubelet resets the restart backoff timer for that container.
  > Sidecar containers and Pod lifecycle
  > explains the behaviour of `init containers` when specify `restartpolicy` field on it.
  > [Pod Lifecycle > How Pods handle problems with containers {#container-restarts} > Reduced container restart delay]
  > With the alpha feature gate `ReduceDefaultCrashLoopBackOffDecay` enabled,
  > container start retries across your cluster will be reduced to begin at 1s
  > (instead of 10s) and increase exponentially by 2x each restart until a maximum
  > delay of 60s (instead of 300s which is 5 minutes).
  > If you use this feature along with the alpha feature
  > `KubeletCrashLoopBackOffMax` (described below), individual nodes may have
  > different maximum delays.
  > [Pod Lifecycle > How Pods handle problems with containers {#container-restarts} > Configurable container restart delay]
  > With the alpha feature gate `KubeletCrashLoopBackOffMax` enabled, you can
  > reconfigure the maximum delay between container start retries from the default
  > of 300s (5 minutes). This configuration is set per node using kubelet
  > configuration. In your kubelet
  > configuration, under
  > `crashLoopBackOff` set the `maxContainerRestartPeriod` field between `"1s"` and
  > `"300s"`. As described above in Container restart policy,
  > delays on that node will still start at 10s and increase exponentially by 2x
  > each restart, but will now be capped at your configured maximum. If the
  > `maxContainerRestartPeriod` you configure is less than the default initial value
  > of 10s, the … (section continues)
- `tasks/debug/debug-application/debug-running-pod.md`, section: *Debug Running Pods > Examining pod logs*
  > [Debug Running Pods > Examining pod logs {#examine-pod-logs}]
  > First, look at the logs of the affected container:
  > ```shell
  > kubectl logs ${POD_NAME} ${CONTAINER_NAME}
  > ```
  > If your container has previously crashed, you can access the previous container's crash log with:
  > ```shell
  > kubectl logs --previous ${POD_NAME} ${CONTAINER_NAME}
  > ```

*Drafting note:* User says 'crashing in a loop'; docs say CrashLoopBackOff. | LLM pre-review (ChatGPT, 2026-11-07): removed the unsupported 'last state and exit code' claim

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `pvc-request-storage`

**Question** (en, concept): How does a pod ask for persistent storage that survives restarts?

**Reference answer:** Create a PersistentVolumeClaim (requested storage, access mode, optional storageClassName) and use it as a volume in the Pod spec; the claim is bound to a matching PersistentVolume.

**Relevant documentation:**
- `concepts/storage/persistent-volumes.md`, section: *Persistent Volumes > PersistentVolumeClaims*
  > [Persistent Volumes > PersistentVolumeClaims]
  > Each PVC contains a spec and status, which is the specification and status of the claim.
  > The name of a PersistentVolumeClaim object must be a valid
  > DNS subdomain name.
  > ```yaml
  > apiVersion: v1
  > kind: PersistentVolumeClaim
  > metadata:
  >   name: myclaim
  > spec:
  >   accessModes:
  >     - ReadWriteOnce
  >   volumeMode: Filesystem
  >   resources:
  >     requests:
  >       storage: 8Gi
  >   storageClassName: slow
  >   selector:
  >     matchLabels:
  >       release: "stable"
  >     matchExpressions:
  >       - {key: environment, operator: In, values: [dev]}
  > ```
  > [Persistent Volumes > PersistentVolumeClaims > Access Modes]
  > Claims use the same conventions as volumes when requesting
  > storage with specific access modes.
  > [Persistent Volumes > PersistentVolumeClaims > Volume Modes]
  > Claims use the same convention as volumes to indicate the
  > consumption of the volume as either a filesystem or block device.
  > [Persistent Volumes > PersistentVolumeClaims > Volume Name]
  > Claims can use the `volumeName` field to explicitly bind to a specific PersistentVolume. You can also leave
  > `volumeName` unset, indicating that you'd like Kubernetes to set up a new PersistentVolume
  > that matches the claim.
  > If the specified PV is already bound to another PVC, the binding will be stuck
  > in a pending state.
  > [Persistent Volumes > PersistentVolumeClaims > Resources]
  > Claims, like Pods, can request specific quantities of a resource. In this case,
  > the request is for storage. The same
  > resource model
  > applies to both volumes and claims.
  > For `Filesystem` volumes, the storage request refers to the "outer" volume size
  > (i.e. the allocated size from the storage backend).
  > This means that the writeable size may be slightly lower for providers that
  > build a filesystem on top of a block device, due to filesystem overhead.
  > This is especially visible with XFS, where many metadata features are enabled by default.
  > [Persistent Volumes > PersistentVolumeClaims > Selector]
  > Claims can specify a
  > label selector
  > to further filter the set of volumes.
  > Only the volumes whose labels match the selector can be bound to the claim.
  > The selector can consist of two fields:
  > * `matchLabels` - the volume must have a label with this value
  > * `matchExpressions` - a list of requirements made by specifying key, list of values,
  >   and operator that relates the key and values.
  >   Valid operators include `In`, `NotIn`, `Exists`, and `DoesNotExist`.
  > All of the requirements, from both `matchLabels` and `matchExpressions`, are
  > ANDed together – they must all be satisfied in order to match.
  > [Persistent Volumes > PersistentVolumeClaims > Class]
  > A claim can request a particular class by specifying the name of a
  > StorageClass
  > using the attribute `storageClassName`.
  > Only PVs of the requested class, ones with the same `storageClassName` as the PVC,
  > can be bound to the PVC.
  > PVCs don't necessarily have to request a class. A PVC with its `storageClassName` set
  > equal to `""` is always interpreted to be requesting a PV with no class, so it
  > can only be bound to PVs with no class (no annotation or one set equal to `""`).
  > A PVC with no `storageClassName` is not quite the same and is treated differently
  > by the cluster, depending on whether the
  > `DefaultStorageClass` admission plugin
  > is turned on.
  > * If the admission plugin is turned on, the administrator may specify a default StorageClass.
  >   All PVCs that have no `storageClassName` can be bound only to PVs of that default.
  >   Specifying a default StorageClass is done by setting the annotation
  >   `storageclass.kubernetes.io/is-default-class` equal to `true` in a StorageClass object.
  >   If the administrator does not specify a default, the cluster responds to PVC creation
  >   as if the admission plugin were turned off.
  >   If more than one default StorageClass is specified, the newest default is used when
  >   the PVC is dynamically provisioned.
  > * If the admission plugin is turned off, there is no notion of a default StorageClass.
  >   All PVCs that have `storageClassName` set to `""` can be bound only to PVs
  >   that have `storageClassName` also set to `""`.
  >   However, PVCs with missing `storageClassName` can be updated later once default StorageClass becomes available.
  >   If the PVC gets updated it will no longer bind to PVs that have `storageClassName` also set to `""`.
  > See retroactive default StorageClass assignment for more details.
  > See retroactive default StorageClass assignment for more details.
  > Depending on installation method, a default StorageClass may be deployed
  > to a Kubernetes cluster by addon manager during installation.
  > When a PVC specifies a `selector` in addition to requesting a StorageClass,
  > the requirements are ANDed together: only a PV of the requested class and with
  > the requested labels may be bound to the PVC.
  > Currently, a PVC with a non-empty `selector` can't have a PV dynamically provisioned for it.
  > In the past, the annotation `volume.beta.kubernetes.io/storage-class` was used instead
  > of `storageClassName` attribute. This annotation is still working; however,
  > it won't be supported in a future Kubernetes release.
  > [Persistent Volumes > PersistentVolumeClaims > Class > Retroactive default StorageClass assignment]
  > You can create a PersistentVolumeClaim without specifying a `storageClassName`
  > for the new PVC, and you can do so even when no default StorageClass exists
  > in your cluster. In this case, the new PVC creates as you defined it, and the
  > `storageClassName` of that PVC remains unset until default becomes available.
  > When a default StorageClass becomes available, the control plane identifies any
  > existing PVCs without `storageClassName`. For the PVCs that either have an empty
  > value for `storageClassName` or do not have this key, the control plane then
  > updates those PVCs to set `storageClassName` to match the new default StorageClass.
  > If you have an existing PVC where the `storageClassName` is `""`, and you configure
  > a default StorageClass, then this PVC will not get updated.
  > In order to keep binding to PVs with `storageClassName` set to … (section continues)
- `concepts/storage/persistent-volumes.md`, section: *Persistent Volumes > Claims As Volumes*
  > [Persistent Volumes > Claims As Volumes]
  > Pods access storage by using the claim as a volume. Claims must exist in the
  > same namespace as the Pod using the claim. The cluster finds the claim in the
  > Pod's namespace and uses it to get the PersistentVolume backing the claim.
  > The volume is then mounted to the host and into the Pod.
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: mypod
  > spec:
  >   containers:
  >     - name: myfrontend
  >       image: nginx
  >       volumeMounts:
  >       - mountPath: "/var/www/html"
  >         name: mypd
  >   volumes:
  >     - name: mypd
  >       persistentVolumeClaim:
  >         claimName: myclaim
  > ```
  > [Persistent Volumes > Claims As Volumes > A Note on Namespaces]
  > PersistentVolumes binds are exclusive, and since PersistentVolumeClaims are
  > namespaced objects, mounting claims with "Many" modes (`ROX`, `RWX`) is only
  > possible within one namespace.
  > [Persistent Volumes > Claims As Volumes > PersistentVolumes typed `hostPath`]
  > A `hostPath` PersistentVolume uses a file or directory on the Node to emulate
  > network-attached storage. See
  > an example of `hostPath` typed volume.
- `concepts/storage/persistent-volumes.md`, section: *Persistent Volumes > Lifecycle of a volume and claim*
  > [Persistent Volumes > Lifecycle of a volume and claim]
  > PVs are resources in the cluster. PVCs are requests for those resources and also act
  > as claim checks to the resource. The interaction between PVs and PVCs follows this lifecycle:
  > [Persistent Volumes > Lifecycle of a volume and claim > Provisioning]
  > There are two ways PVs may be provisioned: statically or dynamically.
  > [Persistent Volumes > Lifecycle of a volume and claim > Provisioning > Static]
  > A cluster administrator creates a number of PVs. They carry the details of the
  > real storage, which is available for use by cluster users. They exist in the
  > Kubernetes API and are available for consumption.
  > [Persistent Volumes > Lifecycle of a volume and claim > Provisioning > Dynamic]
  > When none of the static PVs the administrator created match a user's PersistentVolumeClaim,
  > the cluster may try to dynamically provision a volume specially for the PVC.
  > This provisioning is based on StorageClasses: the PVC must request a
  > storage class and
  > the administrator must have created and configured that class for dynamic
  > provisioning to occur. Claims that request the class `""` effectively disable
  > dynamic provisioning for themselves.
  > To enable dynamic storage provisioning based on storage class, the cluster administrator
  > needs to enable the `DefaultStorageClass`
  > admission controller
  > on the API server. This can be done, for example, by ensuring that `DefaultStorageClass` is
  > among the comma-delimited, ordered list of values for the `--enable-admission-plugins` flag of
  > the API server component. For more information on API server command-line flags,
  > check kube-apiserver documentation.
  > [Persistent Volumes > Lifecycle of a volume and claim > Binding]
  > A user creates, or in the case of dynamic provisioning, has already created,
  > a PersistentVolumeClaim with a specific amount of storage requested and with
  > certain access modes. A control loop in the control plane watches for new PVCs, finds
  > a matching PV (if possible), and binds them together. If a PV was dynamically
  > provisioned for a new PVC, the loop will always bind that PV to the PVC. Otherwise,
  > the user will always get at least what they asked for, but the volume may be in
  > excess of what was requested. Once bound, PersistentVolumeClaim binds are exclusive,
  > regardless of how they were bound. A PVC to PV binding is a one-to-one mapping,
  > using a ClaimRef which is a bi-directional binding between the PersistentVolume
  > and the PersistentVolumeClaim.
  > Claims will remain unbound indefinitely if a matching volume does not exist.
  > Claims will be bound as matching volumes become available. For example, a
  > cluster provisioned with many 50Gi PVs would not match a PVC requesting 100Gi.
  > The PVC can be bound when a 100Gi PV is added to the cluster.
  > [Persistent Volumes > Lifecycle of a volume and claim > Using]
  > Pods use claims as volumes. The cluster inspects the claim to find the bound
  > volume and mounts that volume for a Pod. For volumes that support multiple
  > access modes, the user specifies which mode is desired when using their claim
  > as a volume in a Pod.
  > Once a user has a claim and that claim is bound, the bound PV belongs to the
  > user for as long as they need it. Users schedule Pods and access their claimed
  > PVs by including a `persistentVolumeClaim` section in a Pod's `volumes` block.
  > See Claims As Volumes for more details on this.
  > [Persistent Volumes > Lifecycle of a volume and claim > Storage Object in Use Protection]
  > The purpose of the Storage Object in Use Protection feature is to ensure that
  > PersistentVolumeClaims (PVCs) in active use by a Pod and PersistentVolume (PVs)
  > that are bound to PVCs are not removed from the system, as this may result in data loss.
  > PVC is in active use by a Pod when a Pod object exists that is using the PVC.
  > If a user deletes a PVC in active use by a Pod, the PVC is not removed immediately.
  > PVC removal is postponed until the PVC is no longer actively used by any Pods. Also,
  > if an admin deletes a PV that is bound to a PVC, the PV is not removed immediately.
  > PV removal is postponed until the PV is no longer bound to a PVC.
  > You can see that a PVC is protected when the PVC's status is `Terminating` and the
  > `Finalizers` list includes `kubernetes.io/pvc-protection`:
  > ```shell
  > kubectl describe pvc hostpath
  > Name:          hostpath
  > Namespace:     default
  > StorageClass:  example-hostpath
  > Status:        Terminating
  > Volume:
  > Labels:        <none>
  > Annotations:   volume.beta.kubernetes.io/storage-class=example-hostpath
  >                volume.beta.kubernetes.io/storage-provisioner=example.com/hostpath
  > Finalizers:    [kubernetes.io/pvc-protection]
  > ...
  > ```
  > You can see that a PV is protected when the PV's status is `Terminating` and
  > the `Finalizers` list includes `kubernetes.io/pv-protection` too:
  > ```shell
  > kubectl describe pv task-pv-volume
  > Name:            task-pv-volume
  > Labels:          type=local
  > Annotations:     <none>
  > Finalizers:      [kubernetes.io/pv-protection]
  > StorageClass:    standard
  > Status:          Terminating
  > Claim:
  > Reclaim Policy:  Delete
  > Access Modes:    RWO
  > Capacity:        1Gi
  > Message:
  > Source:
  >     Type:          HostPath (bare host directory volume)
  >     Path:          /tmp/data
  >     HostPathType:
  > Events:            <none>
  > ```
  > [Persistent Volumes > Lifecycle of a volume and claim > Reclaiming]
  > When a user is done with their volume, they can delete the PVC objects from the
  > API that allows reclamation of the resource. The reclaim policy for a PersistentVolume
  > tells the cluster what to do with the volume after it has been released of its claim.
  > Currently, volumes can either be Retained, Recycled, or Deleted.
  > [Persistent Volumes > Lifecycle of a volume and claim > Reclaiming > Retain]
  > The `Retain` reclaim policy allows for manual reclamation of the resource.
  > When the PersistentVolumeClaim is deleted, the PersistentVolume still exists
  > and the volume is considered "released". But it is not yet available for
  > another claim because the previous claimant's data remains on the volume.
  > An administrator can … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): added the lifecycle section that documents binding; removed 'survives restarts'

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `namespaces-when`

**Question** (en, concept): When does it make sense to split a cluster into multiple namespaces?

**Reference answer:** When many users spread across multiple teams or projects share a cluster: namespaces scope names and let you divide cluster resources with resource quotas. They aren't needed to separate slightly different versions of the same software.

**Relevant documentation:**
- `concepts/overview/working-with-objects/namespaces.md`, section: *Namespaces > When to Use Multiple Namespaces*
  > [Namespaces > When to Use Multiple Namespaces]
  > Namespaces are intended for use in environments with many users spread across multiple
  > teams, or projects.  For clusters with a few to tens of users, you should not
  > need to create or think about namespaces at all.  Start using namespaces when you
  > need the features they provide.
  > Namespaces provide a scope for names.  Names of resources need to be unique within a namespace,
  > but not across namespaces. Namespaces cannot be nested inside one another and each Kubernetes
  > resource can only be in one namespace.
  > Namespaces are a way to divide cluster resources between multiple users (via resource quota).
  > It is not necessary to use multiple namespaces to separate slightly different
  > resources, such as different versions of the same software: use
  > labels to distinguish
  > resources within the same namespace.
  > For a production cluster, consider _not_ using the `default` namespace. Instead, make other namespaces and use those.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): removed 'access policies' (not in the section)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `taint-dedicated-node`

**Question** (en, concept): How can I keep ordinary pods from being scheduled on a particular node?

**Reference answer:** Taint the node, e.g. `kubectl taint nodes <node> key1=value1:NoSchedule`. Pods without a matching toleration won't be scheduled there. A toleration allows scheduling on the node but doesn't guarantee it.

**Relevant documentation:**
- `concepts/scheduling-eviction/taint-and-toleration.md`, section: *(whole document)*
  > [Taints and Tolerations]
  > _Node affinity_
  > is a property of Pods that *attracts* them to
  > a set of nodes (either as a preference or a
  > hard requirement). _Taints_ are the opposite -- they allow a node to repel a set of pods.
  > _Tolerations_ are applied to pods. Tolerations allow the scheduler to schedule pods with matching
  > taints. Tolerations allow scheduling but don't guarantee scheduling: the scheduler also
  > evaluates other parameters
  > as part of its function.
  > Taints and tolerations work together to ensure that pods are not scheduled
  > onto inappropriate nodes. One or more taints are applied to a node; this
  > marks that the node should not accept any pods that do not tolerate the taints.
  > [Taints and Tolerations > Concepts]
  > You add a taint to a node using kubectl taint.
  > For example,
  > ```shell
  > kubectl taint nodes node1 key1=value1:NoSchedule
  > ```
  > places a taint on node `node1`. The taint has key `key1`, value `value1`, and taint effect `NoSchedule`.
  > This means that no pod will be able to schedule onto `node1` unless it has a matching toleration.
  > To remove the taint added by the command above, you can run:
  > ```shell
  > kubectl taint nodes node1 key1=value1:NoSchedule-
  > ```
  > You specify a toleration for a pod in the PodSpec. Both of the following tolerations "match" the
  > taint created by the `kubectl taint` line above, and thus a pod with either toleration would be able
  > to schedule onto `node1`:
  > ```yaml
  > tolerations:
  > - key: "key1"
  >   operator: "Equal"
  >   value: "value1"
  >   effect: "NoSchedule"
  > ```
  > ```yaml
  > tolerations:
  > - key: "key1"
  >   operator: "Exists"
  >   effect: "NoSchedule"
  > ```
  > ```yaml
  > tolerations:
  > - key: "key1"
  >   operator: "Exists"
  >   effect: "NoSchedule"
  > ```
  > The default Kubernetes scheduler takes taints and tolerations into account when
  > selecting a node to run a particular Pod. However, if you manually specify the
  > `.spec.nodeName` for a Pod, that action bypasses the scheduler; the Pod is then
  > bound onto the node where you assigned it, even if there are `NoSchedule`
  > taints on that node that you selected.
  > If this happens and the node also has a `NoExecute` taint set, the kubelet will
  > eject the Pod unless there is an appropriate tolerance set.
  > Here's an example of a pod that has some tolerations defined:
  > The default value for `operator` is `Equal`.
  > A toleration "matches" a taint if the keys are the same and the effects are the same, and:
  > * the `operator` is `Exists` (in which case no `value` should be specified), or
  > * the `operator` is `Equal` and the values should be equal.
  > There are two special cases:
  > If the `key` is empty, then the `operator` must be `Exists`, which matches all keys and values. Note that the `effect` still needs to be matched at the same time.
  > An empty `effect` matches all effects with key `key1`.
  > An empty `effect` matches all effects with key `key1`.
  > The above example used the `effect` of `NoSchedule`. Alternatively, you can use the `effect` of `PreferNoSchedule`.
  > The allowed values for the `effect` field are:
  > `NoExecute`
  > : This affects pods that are already running on the node as follows:
  >   * Pods that do not tolerate the taint are evicted immediately
  >   * Pods that tolerate the taint without specifying `tolerationSeconds` in
  >     their toleration specification remain bound forever
  >   * Pods that tolerate the taint with a specified `tolerationSeconds` remain
  >     bound for the specified amount of time. After that time elapses, the node
  >     lifecycle controller evicts the Pods from the node.
  > `NoSchedule`
  > : No new Pods will be scheduled on the tainted node unless they have a matching
  >   toleration. Pods currently running on the node are **not** evicted.
  > `PreferNoSchedule`
  > : `PreferNoSchedule` is a "preference" or "soft" version of `NoSchedule`.
  >   The control plane will *try* to avoid placing a Pod that does not tolerate
  >   the taint on the node, but it is not guaranteed.
  > You can put multiple taints on the same node and multiple tolerations on the same pod.
  > The way Kubernetes processes multiple taints and tolerations is like a filter: start
  > with all of a node's taints, then ignore the ones for which the pod has a matching toleration; the
  > remaining un-ignored taints have the indicated effects on the pod. In particular,
  > * if there is at least one un-ignored taint with effect `NoSchedule` then Kubernetes will not schedule
  > the pod onto that node
  > * if there is no un-ignored taint with effect `NoSchedule` but there is at least one un-ignored taint with
  > effect `PreferNoSchedule` then Kubernetes will *try* to not schedule the pod onto the node
  > * if there is at least one un-ignored taint with effect `NoExecute` then the pod will be evicted from
  > the node (if it is already running on the node), and will not be
  > scheduled onto the node (if it is not yet running on the node).
  > For example, imagine you taint a node like this
  > ```shell
  > kubectl taint nodes node1 key1=value1:NoSchedule
  > kubectl taint nodes node1 key1=value1:NoExecute
  > kubectl taint nodes node1 key2=value2:NoSchedule
  > ```
  > And a pod has two tolerations:
  > And a pod has two tolerations:
  > ```yaml
  > tolerations:
  > - key: "key1"
  >   operator: "Equal"
  >   value: "value1"
  >   effect: "NoSchedule"
  > - key: "key1"
  >   operator: "Equal"
  >   value: "value1"
  >   effect: "NoExecute"
  > ```
  > In this case, the pod will not be able to schedule onto the node, because there is no
  > toleration matching the third taint. But it will be able to continue running if it is
  > already running on the node when the taint is added, because the third taint is the only
  > one of the three that is not tolerated by the pod.
  > Normally, if a taint with effect `NoExecute` is added to a node, then any pods that do
  > not tolerate the taint will be evicted immediately, and pods that do tolerate the
  > taint will never be evicted. However, a toleration with `NoExecute` effect can specify
  > an optional `tolerationSeconds` field that dictates how long the pod will stay bound
  > to the node after the taint is added. For example,
  > ```yaml
  > tolerations:
  > - key: "key1"
  >   operator: "Equal"
  >   value: "value1"
  >   effect: … (section continues)

*Drafting note:* Vocabulary gap: user doesn't say 'taint'. | LLM pre-review (ChatGPT, 2026-11-07): added the documented command; clarified that a toleration doesn't guarantee placement

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `node-selector-ssd`

**Question** (en, task): How do I make a pod run only on nodes that have an SSD?

**Reference answer:** Label the SSD nodes (e.g. `disktype=ssd`) and set `nodeSelector` (or node affinity) in the Pod spec to that label.

**Relevant documentation:**
- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > nodeSelector*
  > [Assigning Pods to Nodes > nodeSelector]
  > `nodeSelector` is the simplest recommended form of node selection constraint.
  > You can add the `nodeSelector` field to your Pod specification and specify the
  > node labels you want the target node to have.
  > Kubernetes only schedules the Pod onto nodes that have each of the labels you
  > specify.
  > See Assign Pods to Nodes for more
  > information.
- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > Affinity and anti-affinity*
  > [Assigning Pods to Nodes > Affinity and anti-affinity]
  > `nodeSelector` is the simplest way to constrain Pods to nodes with specific
  > labels. Affinity and anti-affinity expand the types of constraints you can
  > define. Some of the benefits of affinity and anti-affinity include:
  > - The affinity/anti-affinity language is more expressive. `nodeSelector` only
  >   selects nodes with all the specified labels. Affinity/anti-affinity gives you
  >   more control over the selection logic.
  > - You can indicate that a rule is *soft* or *preferred*, so that the scheduler
  >   still schedules the Pod even if it can't find a matching node.
  > - You can constrain a Pod using labels on other Pods running on the node (or other topological domain),
  >   instead of just node labels, which allows you to define rules for which Pods
  >   can be co-located on a node.
  > The affinity feature consists of two types of affinity:
  > - *Node affinity* functions like the `nodeSelector` field but is more expressive and
  >   allows you to specify soft rules.
  > - *Inter-pod affinity/anti-affinity* allows you to constrain Pods against labels
  >   on other Pods.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity]
  > Node affinity is conceptually similar to `nodeSelector`, allowing you to constrain which nodes your
  > Pod can be scheduled on based on node labels. There are two types of node
  > affinity:
  > - `requiredDuringSchedulingIgnoredDuringExecution`: The scheduler can't
  >   schedule the Pod unless the rule is met. This functions like `nodeSelector`,
  >   but with a more expressive syntax.
  > - `preferredDuringSchedulingIgnoredDuringExecution`: The scheduler tries to
  >   find a node that meets the rule. If a matching node is not available, the
  >   scheduler still schedules the Pod.
  > In the preceding types, `IgnoredDuringExecution` means that if the node labels
  > change after Kubernetes schedules the Pod, the Pod continues to run.
  > You can specify node affinities using the `.spec.affinity.nodeAffinity` field in
  > your Pod spec.
  > For example, consider the following Pod spec:
  > In this example, the following rules apply:
  > - The node *must* have a label with the key `topology.kubernetes.io/zone` and
  >   the value of that label *must* be either `antarctica-east1` or `antarctica-west1`.
  > - The node *preferably* has a label with the key `another-node-label-key` and
  >   the value `another-node-label-value`.
  > You can use the `operator` field to specify a logical operator for Kubernetes to use when
  > interpreting the rules. You can use `In`, `NotIn`, `Exists`, `DoesNotExist`,
  > `Gt` and `Lt`.
  > Read Operators
  > to learn more about how these work.
  > `NotIn` and `DoesNotExist` allow you to define node anti-affinity behavior.
  > Alternatively, you can use node taints
  > to repel Pods from specific nodes.
  > If you specify both `nodeSelector` and `nodeAffinity`, *both* must be satisfied
  > for the Pod to be scheduled onto a node.
  > If you specify multiple terms in `nodeSelectorTerms` associated with `nodeAffinity`
  > types, then the Pod can be scheduled onto a node if one of the specified terms
  > can be satisfied (terms are ORed).
  > If you specify multiple expressions in a single `matchExpressions` field associated with a
  > term in `nodeSelectorTerms`, then the Pod can be scheduled onto a node only
  > if all the expressions are satisfied (expressions are ANDed).
  > See Assign Pods to Nodes using Node Affinity
  > for more information.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity > Node affinity weight]
  > You can specify a `weight` between 1 and 100 for each instance of the
  > `preferredDuringSchedulingIgnoredDuringExecution` affinity type. When the
  > scheduler finds nodes that meet all the other scheduling requirements of the Pod, the
  > scheduler iterates through every preferred rule that the node satisfies and adds the
  > value of the `weight` for that expression to a sum.
  > The final sum is added to the score of other priority functions for the node.
  > Nodes with the highest total score are prioritized when the scheduler makes a
  > scheduling decision for the Pod.
  > For example, consider the following Pod spec:
  > If there are two possible nodes that match the
  > `preferredDuringSchedulingIgnoredDuringExecution` rule, one with the
  > `label-1:key-1` label and another with the `label-2:key-2` label, the scheduler
  > considers the `weight` of each node and adds the weight to the other scores for
  > that node, and schedules the Pod onto the node with the highest final score.
  > If you want Kubernetes to successfully schedule the Pods in this example, you
  > must have existing nodes with the `kubernetes.io/os=linux` label.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity > Node affinity per scheduling profile]
  > When configuring multiple scheduling profiles, you can associate
  > a profile with a node affinity, which is useful if a profile only applies to a specific set of nodes.
  > To do so, add an `addedAffinity` to the `args` field of the `NodeAffinity` plugin
  > in the scheduler configuration. For example:
  > ```yaml
  > apiVersion: kubescheduler.config.k8s.io/v1
  > kind: KubeSchedulerConfiguration
  > profiles:
  >   - schedulerName: default-scheduler
  >   - schedulerName: foo-scheduler
  >     pluginConfig:
  >       - name: NodeAffinity
  >         args:
  >           addedAffinity:
  >             requiredDuringSchedulingIgnoredDuringExecution:
  >               nodeSelectorTerms:
  >               - matchExpressions:
  >                 - key: scheduler-profile
  >                   operator: In
  >                   values:
  >                   - foo
  > ```
  > The `addedAffinity` is applied to all Pods that set `.spec.schedulerName` to `foo-scheduler`, in addition to the
  > NodeAffinity specified in the PodSpec.
  > That is, in order to match the Pod, nodes need to satisfy `addedAffinity` and
  > the Pod's `.spec.NodeAffinity`.
  > Since the `addedAffinity` is not visible to end users, its behavior might be
  > unexpected to them. Use node labels that have a clear correlation to the
  > scheduler profile name.
  > The DaemonSet controller, which creates Pods for DaemonSets,
  > does not support scheduling … (section continues)

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The excerpts explain how `nodeSelector` and node affinity match node labels, but do not show how to attach the SSD label to nodes. Add the “Node labels” excerpt (which explains manual labeling) or a documented `kubectl label nodes ...` example. The SSD-specific use case is also a better fit for the introductory “Assigning Pods to Nodes” text.


---

### `hpa-cpu`

**Question** (en, concept): How can Kubernetes add more pods automatically when CPU usage goes up?

**Reference answer:** A HorizontalPodAutoscaler: a control loop that runs intermittently, compares observed metrics such as average CPU utilization with the target you set, and adjusts the number of replicas.

**Relevant documentation:**
- `tasks/run-application/horizontal-pod-autoscale.md`, section: *(whole document)*
  > [Horizontal Pod Autoscaling]
  > In Kubernetes, a _HorizontalPodAutoscaler_ automatically updates a workload resource (such as
  > a Deployment or
  > StatefulSet), with the
  > aim of automatically scaling the workload to match demand.
  > Horizontal scaling means that the response to increased load is to deploy more
  > Pods.
  > This is different from _vertical_ scaling, which for Kubernetes would mean
  > assigning more resources (for example: memory or CPU) to the Pods that are already
  > running for the workload.
  > If the load decreases, and the number of Pods is above the configured minimum,
  > the HorizontalPodAutoscaler instructs the workload resource (the Deployment, StatefulSet,
  > or other similar resource) to scale back down.
  > Horizontal pod autoscaling does not apply to objects that can't be scaled (for example:
  > a DaemonSet.)
  > Horizontal pod autoscaling does not apply to objects that can't be scaled (for example:
  > a DaemonSet.)
  > The HorizontalPodAutoscaler is implemented as a Kubernetes API resource and a
  > controller.
  > The resource determines the behavior of the controller.
  > The horizontal pod autoscaling controller, running within the Kubernetes
  > control plane, periodically adjusts the
  > desired scale of its target (for example, a Deployment) to match observed metrics such as average
  > CPU utilization, average memory utilization, or any other custom metric you specify.
  > There is walkthrough example of using
  > horizontal pod autoscaling.
  > [Horizontal Pod Autoscaling > How does a HorizontalPodAutoscaler work?]
  > graph BT
  > hpa[Horizontal Pod Autoscaler] --> scale[Scale]
  > subgraph rc[RC / Deployment]
  >     scale
  > end
  > scale -.-> pod1[Pod 1]
  > scale -.-> pod2[Pod 2]
  > scale -.-> pod3[Pod N]
  > classDef hpa fill:#D5A6BD,stroke:#1E1E1D,stroke-width:1px,color:#1E1E1D;
  > classDef rc fill:#F9CB9C,stroke:#1E1E1D,stroke-width:1px,color:#1E1E1D;
  > classDef scale fill:#B6D7A8,stroke:#1E1E1D,stroke-width:1px,color:#1E1E1D;
  > classDef pod fill:#9FC5E8,stroke:#1E1E1D,stroke-width:1px,color:#1E1E1D;
  > class hpa hpa;
  > class rc rc;
  > class scale scale;
  > class pod1,pod2,pod3 pod
  > Figure 1. HorizontalPodAutoscaler controls the scale of a Deployment and its ReplicaSet
  > Kubernetes implements horizontal pod autoscaling as a control loop that runs intermittently
  > (it is not a continuous process). The interval is set by the
  > `--horizontal-pod-autoscaler-sync-period` parameter to the
  > `kube-controller-manager`
  > (and the default interval is 15 seconds).
  > Once during each period, the controller manager queries the resource utilization against the
  > metrics specified in each HorizontalPodAutoscaler definition. The controller manager
  > finds the target resource defined by the `scaleTargetRef`,
  > then selects the pods based on the target resource's `.spec.selector` labels,
  > and obtains the metrics from either the resource metrics API (for per-pod resource metrics),
  > or the custom metrics API (for all other metrics).
  > - For per-pod resource metrics (like CPU), the controller fetches the metrics
  >   from the resource metrics API for each Pod targeted by the HorizontalPodAutoscaler.
  >   Then, if a target utilization value is set, the controller calculates the utilization
  >   value as a percentage of the equivalent
  >   resource request
  >   on the containers in each Pod. If a target raw value is set, the raw metric values are used directly.
  >   The controller then takes the mean of the utilization or the raw value (depending on the type
  >   of target specified) across all targeted Pods, and produces a ratio used to scale
  >   the number of desired replicas.
  >   Please note that if some of the Pod's containers do not have the relevant resource request set,
  >   CPU utilization for the Pod will not be defined and the autoscaler will
  >   not take any action for that metric. See the algorithm details section below
  >   for more information about how the autoscaling algorithm works.
  > - For per-pod custom metrics, the controller functions similarly to per-pod resource metrics,
  >   except that it works with raw values, not utilization values.
  > - For object metrics and external metrics, a single metric is fetched, which describes
  >   the object in question. This metric is compared to the target
  >   value, to produce a ratio as above. In the `autoscaling/v2` API
  >   version, this value can optionally be divided by the number of Pods before the
  >   comparison is made.
  > The common use for HorizontalPodAutoscaler is to configure it to fetch metrics from
  > aggregated APIs
  > (`metrics.k8s.io`, `custom.metrics.k8s.io`, or `external.metrics.k8s.io`). The `metrics.k8s.io` API is
  > usually provided by an add-on named Metrics Server, which needs to be launched separately.
  > For more information about resource metrics, see
  > Metrics Server.
  > Support for metrics APIs explains the stability guarantees and support status for these
  > different APIs.
  > The HorizontalPodAutoscaler controller accesses corresponding workload resources that support scaling (such as Deployments
  > and StatefulSet). These resources each have a subresource named `scale`, an interface that allows you to dynamically set the
  > number of replicas and examine each of their current states.
  > For general information about subresources in the Kubernetes API, see
  > Kubernetes API Concepts.
  > [Horizontal Pod Autoscaling > How does a HorizontalPodAutoscaler work? > Algorithm details]
  > From the most basic perspective, the HorizontalPodAutoscaler controller
  > operates on the ratio between desired metric value and current metric
  > value:
  > ```math
  > \begin{equation*}
  > desiredReplicas = ceil\left\lceil currentReplicas \times \frac{currentMetricValue}{desiredMetricValue} \right\rceil
  > \end{equation*}
  > ```
  > For example, if the current metric value is `200m`, and the desired value
  > is `100m`, the number of replicas will be doubled, since
  > \\( { 200.0 \div 100.0 } = 2.0 \\).
  > If the current value is instead `50m`, you'll halve the number of
  > replicas, since \\( { 50.0 \div 100.0 } = 0.5 \\). The control plane skips any scaling
  > action if the ratio is sufficiently close to 1.0 (within a
  > configurable tolerance, 0.1 by default).
  > When a … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): aligned wording with the source ('intermittently', not 'periodically')

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `ingress-vs-service`

**Question** (en, concept): What is an Ingress and how is it different from a Service?

**Reference answer:** An Ingress exposes HTTP and HTTPS routes from outside the cluster to Services, using rules that match host and path, and can terminate TLS; it needs an Ingress controller. A Service exposes a set of Pods as a network service behind one endpoint.

**Relevant documentation:**
- `concepts/services-networking/ingress.md`, section: *Ingress > What is Ingress?*
  > [Ingress > What is Ingress?]
  > Ingress
  > exposes HTTP and HTTPS routes from outside the cluster to
  >  within the cluster.
  > Traffic routing is controlled by rules defined on the Ingress resource.
  > Here is a simple example where an Ingress sends all its traffic to one Service:
  > An Ingress may be configured to give Services externally-reachable URLs,
  > load balance traffic, terminate SSL / TLS, and offer name-based virtual hosting.
  > An Ingress controller
  > is responsible for fulfilling the Ingress, usually with a load balancer, though
  > it may also configure your edge router or additional frontends to help handle the traffic.
  > An Ingress does not expose arbitrary ports or protocols. Exposing services other than HTTP and HTTPS to the internet typically
  > uses a service of type Service.Type=NodePort or
  > Service.Type=LoadBalancer.
- `concepts/services-networking/ingress.md`, section: *Ingress > The Ingress resource*
  > [Ingress > The Ingress resource]
  > A minimal Ingress resource example:
  > An Ingress needs `apiVersion`, `kind`, `metadata` and `spec` fields.
  > The name of an Ingress object must be a valid
  > DNS subdomain name.
  > For general information about working with config files, see
  > deploying applications,
  > configuring containers,
  > managing resources.
  > Ingress frequently uses annotations to configure some options depending on the Ingress controller, an example of which
  > is the rewrite-target annotation.
  > Different Ingress controllers support different annotations.
  > Review the documentation for your choice of Ingress controller to learn which annotations are supported.
  > The Ingress spec
  > has all the information needed to configure a load balancer or proxy server. Most importantly, it
  > contains a list of rules matched against all incoming requests. Ingress resource only supports rules
  > for directing HTTP(S) traffic.
  > If the `ingressClassName` is omitted, a default Ingress class
  > should be defined.
  > If the `ingressClassName` is omitted, a default Ingress class
  > should be defined.
  > There are some ingress controllers, that work without the definition of a
  > default `IngressClass`. For example, the Ingress-NGINX controller can be
  > configured with a flag
  > `--watch-ingress-without-class`. It is recommended though, to specify the
  > default `IngressClass` as shown below.
  > [Ingress > The Ingress resource > Ingress rules]
  > Each HTTP rule contains the following information:
  > * An optional host. In this example, no host is specified, so the rule applies to all inbound
  >   HTTP traffic through the IP address specified. If a host is provided (for example,
  >   foo.bar.com), the rules apply to that host.
  > * A list of paths (for example, `/testpath`), each of which has an associated
  >   backend defined with a `service.name` and a `service.port.name` or
  >   `service.port.number`. Both the host and path must match the content of an
  >   incoming request before the load balancer directs traffic to the referenced
  >   Service.
  > * A backend is a combination of Service and port names as described in the
  >   Service doc or a custom resource backend
  >   by way of a CRD. HTTP (and HTTPS) requests to the
  >   Ingress that match the host and path of the rule are sent to the listed backend.
  > A `defaultBackend` is often configured in an Ingress controller to service any requests that do not
  > match a path in the spec.
  > [Ingress > The Ingress resource > DefaultBackend {#default-backend}]
  > An Ingress with no rules sends all traffic to a single default backend and `.spec.defaultBackend`
  > is the backend that should handle requests in that case.
  > The `defaultBackend` is conventionally a configuration option of the
  > Ingress controller and
  > is not specified in your Ingress resources.
  > If no `.spec.rules` are specified, `.spec.defaultBackend` must be specified.
  > If `defaultBackend` is not set, the handling of requests that do not match any of the rules will be up to the
  > ingress controller (consult the documentation for your ingress controller to find out how it handles this case).
  > If none of the hosts or paths match the HTTP request in the Ingress objects, the traffic is
  > routed to your default backend.
  > [Ingress > The Ingress resource > Resource backends {#resource-backend}]
  > A `Resource` backend is an ObjectRef to another Kubernetes resource within the
  > same namespace as the Ingress object. A `Resource` is a mutually exclusive
  > setting with Service, and will fail validation if both are specified. A common
  > usage for a `Resource` backend is to ingress data to an object storage backend
  > with static assets.
  > After creating the Ingress above, you can view it with the following command:
  > ```bash
  > kubectl describe ingress ingress-resource-backend
  > ```
  > ```
  > Name:             ingress-resource-backend
  > Namespace:        default
  > Address:
  > Default backend:  APIGroup: k8s.example.com, Kind: StorageBucket, Name: static-assets
  > Rules:
  >   Host        Path  Backends
  >   ----        ----  --------
  >   *
  >               /icons   APIGroup: k8s.example.com, Kind: StorageBucket, Name: icon-assets
  > Annotations:  <none>
  > Events:       <none>
  > ```
  > [Ingress > The Ingress resource > Path types]
  > Each path in an Ingress is required to have a corresponding path type. Paths
  > that do not include an explicit `pathType` will fail validation. There are three
  > supported path types:
  > * `ImplementationSpecific`: With this path type, matching is up to the
  >   IngressClass. Implementations can treat this as a separate `pathType` or treat
  >   it identically to `Prefix` or `Exact` path types.
  > * `Exact`: Matches the URL path exactly and with case sensitivity.
  > * `Prefix`: Matches based on a URL path prefix split by `/`. Matching is case
  >   sensitive and done on a path element by element basis. A path element refers
  >   to the list of labels in the path split by the `/` separator. A request is a
  >   match for path _p_ if every _p_ is an element-wise prefix of _p_ of the
  >   request path.
  >   If the last element of the path is a substring of the last
  >   element in request path, it is not a match (for example: `/foo/bar`
  >   matches `/foo/bar/baz`, but does not match `/foo/barbaz`).
  > [Ingress > The Ingress resource > Examples]
  > | Kind   | Path(s)                         | Request path(s)               | Matches?                           |
  > |--------|---------------------------------|-------------------------------|------------------------------------|
  > | Prefix | `/`                             | (all paths)                   | Yes                                |
  > | Exact  | `/foo`                          | `/foo`                        | Yes                                |
  > | Exact  | `/foo`                          | `/bar`                        | No                                 |
  > | Exact  | `/foo`                          | `/foo/`                       | No                                 |
  > | Exact  | `/foo/`                         | `/foo`                        | No                                 |
  > | Prefix | `/foo`                          | `/foo`, `/foo/`       … (section continues)
- `concepts/services-networking/service.md`, section: *Service > Services in Kubernetes*
  > [Service > Services in Kubernetes]
  > The Service API, part of Kubernetes, is an abstraction to help you expose groups of
  > Pods over a network. Each Service object defines a logical set of endpoints (usually
  > these endpoints are Pods) along with a policy about how to make those pods accessible.
  > For example, consider a stateless image-processing backend which is running with
  > 3 replicas.  Those replicas are fungible&mdash;frontends do not care which backend
  > they use.  While the actual Pods that compose the backend set may change, the
  > frontend clients should not need to be aware of that, nor should they need to keep
  > track of the set of backends themselves.
  > The Service abstraction enables this decoupling.
  > The set of Pods targeted by a Service is usually determined
  > by a selector that you
  > define.
  > To learn about other ways to define Service endpoints,
  > see Services _without_ selectors.
  > The set of Pods targeted by a Service is usually determined
  > by a selector that you
  > define.
  > To learn about other ways to define Service endpoints,
  > see Services _without_ selectors.
  > If your workload speaks HTTP, you might choose to use an
  > Ingress to control how web traffic
  > reaches that workload.
  > Ingress is not a Service type, but it acts as the entry point for your
  > cluster. An Ingress lets you consolidate your routing rules into a single resource, so
  > that you can expose multiple components of your workload, running separately in your
  > cluster, behind a single listener.
  > The Gateway API for Kubernetes
  > provides extra capabilities beyond Ingress and Service. You can add Gateway to your cluster -
  > it is a family of extension APIs, implemented using
  > CustomResourceDefinitions -
  > and then use these to configure access to network services that are running in your cluster.
  > [Service > Services in Kubernetes > Cloud-native service discovery]
  > If you're able to use Kubernetes APIs for service discovery in your application,
  > you can query the API server
  > for matching EndpointSlices. Kubernetes updates the EndpointSlices for a Service
  > whenever the set of Pods in a Service changes.
  > For non-native applications, Kubernetes offers ways to place a network port or load
  > balancer in between your application and the backend Pods.
  > Either way, your workload can use these service discovery
  > mechanisms to find the target it wants to connect to.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): added the Ingress-rules and Service-definition sections

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `netpol-default-deny`

**Question** (en, task): How do I block all incoming traffic to the pods in a namespace by default?

**Reference answer:** By default all traffic is allowed. Create a NetworkPolicy that selects all Pods in the namespace and allows no ingress ("default deny all ingress traffic"). It only has an effect if the cluster's network plugin supports NetworkPolicy.

**Relevant documentation:**
- `concepts/services-networking/network-policies.md`, section: *Network Policies > Default policies*
  > [Network Policies > Default policies]
  > By default, if no policies exist in a namespace, then all ingress and egress traffic is allowed to
  > and from pods in that namespace. The following examples let you change the default behavior
  > in that namespace.
  > [Network Policies > Default policies > Default deny all ingress traffic]
  > You can create a "default" ingress isolation policy for a namespace by creating a NetworkPolicy
  > that selects all pods but does not allow any ingress traffic to those pods.
  > This ensures that even pods that aren't selected by any other NetworkPolicy will still be isolated
  > for ingress. This policy does not affect isolation for egress from any pod.
  > [Network Policies > Default policies > Allow all ingress traffic]
  > If you want to allow all incoming connections to all pods in a namespace, you can create a policy
  > that explicitly allows that.
  > With this policy in place, no additional policy or policies can cause any incoming connection to
  > those pods to be denied. This policy has no effect on isolation for egress from any pod.
  > [Network Policies > Default policies > Default deny all egress traffic]
  > You can create a "default" egress isolation policy for a namespace by creating a NetworkPolicy
  > that selects all pods but does not allow any egress traffic from those pods.
  > This ensures that even pods that aren't selected by any other NetworkPolicy will not be allowed
  > egress traffic. This policy does not change the ingress isolation behavior of any pod.
  > [Network Policies > Default policies > Allow all egress traffic]
  > If you want to allow all connections from all pods in a namespace, you can create a policy that
  > explicitly allows all outgoing connections from pods in that namespace.
  > With this policy in place, no additional policy or policies can cause any outgoing connection from
  > those pods to be denied. This policy has no effect on isolation for ingress to any pod.
  > [Network Policies > Default policies > Default deny all ingress and all egress traffic]
  > You can create a "default" policy for a namespace which prevents all ingress AND egress traffic by
  > creating the following NetworkPolicy in that namespace.
  > This ensures that even pods that aren't selected by any other NetworkPolicy will not be allowed
  > ingress or egress traffic.
- `concepts/services-networking/network-policies.md`, section: *Network Policies > Prerequisites*
  > [Network Policies > Prerequisites]
  > Network policies are implemented by the network plugin.
  > To use network policies, you must be using a networking solution which supports NetworkPolicy.
  > Creating a NetworkPolicy resource without a controller that implements it will have no effect.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): narrowed (the YAML example is not in the index); added the prerequisites section

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `daemonset-agent`

**Question** (en, concept): How do I run exactly one copy of a log collector on every node of the cluster?

**Reference answer:** Use a DaemonSet: it runs one Pod per (matching) node and adds Pods to new nodes automatically.

**Relevant documentation:**
- `concepts/workloads/controllers/daemonset.md`, section: *(whole document)*
  > [DaemonSet]
  > A _DaemonSet_ ensures that all (or some) Nodes run a copy of a Pod.  As nodes are added to the
  > cluster, Pods are added to them.  As nodes are removed from the cluster, those Pods are garbage
  > collected.  Deleting a DaemonSet will clean up the Pods it created.
  > Some typical uses of a DaemonSet are:
  > - running a cluster storage daemon on every node
  > - running a logs collection daemon on every node
  > - running a node monitoring daemon on every node
  > In a simple case, one DaemonSet, covering all nodes, would be used for each type of daemon.
  > A more complex setup might use multiple DaemonSets for a single type of daemon, but with
  > different flags and/or different memory and cpu requests for different hardware types.
  > [DaemonSet > Writing a DaemonSet Spec > Create a DaemonSet]
  > You can describe a DaemonSet in a YAML file. For example, the `daemonset.yaml` file below
  > describes a DaemonSet that runs the fluentd-elasticsearch Docker image:
  > Create a DaemonSet based on the YAML file:
  > ```
  > kubectl apply -f https://k8s.io/examples/controllers/daemonset.yaml
  > ```
  > [DaemonSet > Writing a DaemonSet Spec > Required Fields]
  > As with all other Kubernetes config, a DaemonSet needs `apiVersion`, `kind`, and `metadata` fields.  For
  > general information about working with config files, see
  > running stateless applications
  > and object management using kubectl.
  > The name of a DaemonSet object must be a valid
  > DNS subdomain name.
  > A DaemonSet also needs a
  > `.spec`
  > section.
  > [DaemonSet > Writing a DaemonSet Spec > Pod Template]
  > The `.spec.template` is one of the required fields in `.spec`.
  > The `.spec.template` is a pod template.
  > It has exactly the same schema as a Pod,
  > except it is nested and does not have an `apiVersion` or `kind`.
  > In addition to required fields for a Pod, a Pod template in a DaemonSet has to specify appropriate
  > labels (see pod selector).
  > A Pod Template in a DaemonSet must have a `RestartPolicy`
  >  equal to `Always`, or be unspecified, which defaults to `Always`.
  > [DaemonSet > Writing a DaemonSet Spec > Pod Selector]
  > The `.spec.selector` field is a pod selector.  It works the same as the `.spec.selector` of
  > a Job.
  > You must specify a pod selector that matches the labels of the
  > `.spec.template`.
  > Also, once a DaemonSet is created,
  > its `.spec.selector` can not be mutated. Mutating the pod selector can lead to the
  > unintentional orphaning of Pods, and it was found to be confusing to users.
  > The `.spec.selector` is an object consisting of two fields:
  > * `matchLabels` - works the same as the `.spec.selector` of a
  >   ReplicationController.
  > * `matchExpressions` - allows to build more sophisticated selectors by specifying key,
  >   list of values and an operator that relates the key and values.
  > When the two are specified the result is ANDed.
  > The `.spec.selector` must match the `.spec.template.metadata.labels`.
  > Config with these two not matching will be rejected by the API.
  > [DaemonSet > Writing a DaemonSet Spec > Running Pods on select Nodes]
  > If you specify a `.spec.template.spec.nodeSelector`, then the DaemonSet controller will
  > create Pods on nodes which match that node selector.
  > Likewise if you specify a `.spec.template.spec.affinity`,
  > then DaemonSet controller will create Pods on nodes which match that
  > node affinity.
  > If you do not specify either, then the DaemonSet controller will create Pods on all nodes.
  > [DaemonSet > How Daemon Pods are scheduled]
  > A DaemonSet can be used to ensure that all eligible nodes run a copy of a Pod.
  > The DaemonSet controller creates a Pod for each eligible node and adds the
  > `spec.affinity.nodeAffinity` field of the Pod to match the target host. After
  > the Pod is created, the default scheduler typically takes over and then binds
  > the Pod to the target host by setting the `.spec.nodeName` field.  If the new
  > Pod cannot fit on the node, the default scheduler may preempt (evict) some of
  > the existing Pods based on the
  > priority
  > of the new Pod.
  > If it's important that the DaemonSet pod run on each node, it's often desirable
  > to set the `.spec.template.spec.priorityClassName` of the DaemonSet to a
  > PriorityClass
  > with a higher priority to ensure that this eviction occurs.
  > The user can specify a different scheduler for the Pods of the DaemonSet, by
  > setting the `.spec.template.spec.schedulerName` field of the DaemonSet.
  > The user can specify a different scheduler for the Pods of the DaemonSet, by
  > setting the `.spec.template.spec.schedulerName` field of the DaemonSet.
  > The original node affinity specified at the
  > `.spec.template.spec.affinity.nodeAffinity` field (if specified) is taken into
  > consideration by the DaemonSet controller when evaluating the eligible nodes,
  > but is replaced on the created Pod with the node affinity that matches the name
  > of the eligible node.
  > ```yaml
  > nodeAffinity:
  >   requiredDuringSchedulingIgnoredDuringExecution:
  >     nodeSelectorTerms:
  >     - matchFields:
  >       - key: metadata.name
  >         operator: In
  >         values:
  >         - target-host-name
  > ```
  > [DaemonSet > How Daemon Pods are scheduled > Taints and tolerations]
  > The DaemonSet controller automatically adds a set of tolerations to DaemonSet Pods:
  > | Toleration key                                                                                                        | Effect       | Details                                                                                                                                       |
  > | --------------------------------------------------------------------------------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
  > | `node.kubernetes.io/not-ready`             | `NoExecute`  | DaemonSet Pods can be scheduled onto nodes that are not healthy or ready to accept Pods. Any DaemonSet Pods running on such nodes will not be evicted. |
  > | `node.kubernetes.io/unreachable`         | `NoExecute`  | DaemonSet Pods can be scheduled onto nodes that are … (section continues)

*Drafting note:* Vocabulary gap: user doesn't say 'DaemonSet'.

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `statefulset-database`

**Question** (en, concept): Why would I use a StatefulSet instead of a Deployment for a database?

**Reference answer:** A StatefulSet gives each Pod a stable network identity and its own stable persistent storage, with ordered, graceful deployment and scaling, which databases rely on.

**Relevant documentation:**
- `concepts/workloads/controllers/statefulset.md`, section: *StatefulSets > Using StatefulSets*
  > [StatefulSets > Using StatefulSets]
  > StatefulSets are valuable for applications that require one or more of the
  > following.
  > * Stable, unique network identifiers.
  > * Stable, persistent storage.
  > * Ordered, graceful deployment and scaling.
  > * Ordered, automated rolling updates.
  > In the above, stable is synonymous with persistence across Pod (re)scheduling.
  > If an application doesn't require any stable identifiers or ordered deployment,
  > deletion, or scaling, you should deploy your application using a workload object
  > that provides a set of stateless replicas.
  > Deployment or
  > ReplicaSet may be better suited to your stateless needs.
- `concepts/workloads/controllers/statefulset.md`, section: *StatefulSets > Pod Identity*
  > [StatefulSets > Pod Identity]
  > StatefulSet Pods have a unique identity that consists of an ordinal, a
  > stable network identity, and stable storage. The identity sticks to the Pod,
  > regardless of which node it's (re)scheduled on.
  > [StatefulSets > Pod Identity > Ordinal Index]
  > For a StatefulSet with N replicas, each Pod in the StatefulSet
  > will be assigned an integer ordinal, that is unique over the Set. By default,
  > pods will be assigned ordinals from 0 up through N-1. The StatefulSet controller
  > will also add a pod label with this index: `apps.kubernetes.io/pod-index`.
  > [StatefulSets > Pod Identity > Start ordinal]
  > `.spec.ordinals` is an optional field that allows you to configure the integer
  > ordinals assigned to each Pod. It defaults to nil. Within the field, you can
  > configure the following options:
  > * `.spec.ordinals.start`: If the `.spec.ordinals.start` field is set, Pods will
  >   be assigned ordinals from `.spec.ordinals.start` up through
  >   `.spec.ordinals.start + .spec.replicas - 1`.
  > [StatefulSets > Pod Identity > Stable Network ID]
  > Each Pod in a StatefulSet derives its hostname from the name of the StatefulSet
  > and the ordinal of the Pod. The pattern for the constructed hostname
  > is `$(statefulset name)-$(ordinal)`. The example above will create three Pods
  > named `web-0,web-1,web-2`.
  > A StatefulSet can use a Headless Service
  > to control the domain of its Pods. The domain managed by this Service takes the form:
  > `$(service name).$(namespace).svc.cluster.local`, where "cluster.local" is the
  > cluster domain.
  > As each Pod is created, it gets a matching DNS subdomain, taking the form:
  > `$(podname).$(governing service domain)`, where the governing service is defined
  > by the `serviceName` field on the StatefulSet.
  > Depending on how DNS is configured in your cluster, you may not be able to look up the DNS
  > name for a newly-run Pod immediately. This behavior can occur when other clients in the
  > cluster have already sent queries for the hostname of the Pod before it was created.
  > Negative caching (normal in DNS) means that the results of previous failed lookups are
  > remembered and reused, even after the Pod is running, for at least a few seconds.
  > If you need to discover Pods promptly after they are created, you have a few options:
  > If you need to discover Pods promptly after they are created, you have a few options:
  > - Query the Kubernetes API directly (for example, using a watch) rather than relying on DNS lookups.
  > - Decrease the time of caching in your Kubernetes DNS provider (typically this means editing the
  >   config map for CoreDNS, which currently caches for 30 seconds).
  > As mentioned in the limitations section, you are responsible for
  > creating the Headless Service
  > responsible for the network identity of the pods.
  > Here are some examples of choices for Cluster Domain, Service name,
  > StatefulSet name, and how that affects the DNS names for the StatefulSet's Pods.
  > Here are some examples of choices for Cluster Domain, Service name,
  > StatefulSet name, and how that affects the DNS names for the StatefulSet's Pods.
  > Cluster Domain | Service (ns/name) | StatefulSet (ns/name)  | StatefulSet Domain  | Pod DNS | Pod Hostname |
  > -------------- | ----------------- | ----------------- | -------------- | ------- | ------------ |
  >  cluster.local | default/nginx     | default/web       | nginx.default.svc.cluster.local | web-{0..N-1}.nginx.default.svc.cluster.local | web-{0..N-1} |
  >  cluster.local | foo/nginx         | foo/web           | nginx.foo.svc.cluster.local     | web-{0..N-1}.nginx.foo.svc.cluster.local     | web-{0..N-1} |
  >  kube.local    | foo/nginx         | foo/web           | nginx.foo.svc.kube.local        | web-{0..N-1}.nginx.foo.svc.kube.local        | web-{0..N-1} |
  > Cluster Domain will be set to `cluster.local` unless
  > otherwise configured.
  > [StatefulSets > Pod Identity > Stable Storage]
  > For each VolumeClaimTemplate entry defined in a StatefulSet, each Pod receives one
  > PersistentVolumeClaim. In the nginx example above, each Pod receives a single PersistentVolume
  > with a StorageClass of `my-storage-class` and 1 GiB of provisioned storage. If no StorageClass
  > is specified, then the default StorageClass will be used. When a Pod is (re)scheduled
  > onto a node, its `volumeMounts` mount the PersistentVolumes associated with its
  > PersistentVolume Claims. Note that, the PersistentVolumes associated with the
  > Pods' PersistentVolume Claims are not deleted when the Pods, or StatefulSet are deleted.
  > This must be done manually.
  > [StatefulSets > Pod Identity > Pod Name Label]
  > When the StatefulSet controller creates a Pod,
  > it adds a label, `statefulset.kubernetes.io/pod-name`, that is set to the name of
  > the Pod. This label allows you to attach a Service to a specific Pod in
  > the StatefulSet.
  > [StatefulSets > Pod Identity > Pod index label]
  > When the StatefulSet controller creates a Pod,
  > the new Pod is labelled with `apps.kubernetes.io/pod-index`. The value of this label is the ordinal index of
  > the Pod. This label allows you to route traffic to a particular pod index, filter logs/metrics
  > using the pod index label, and more. Note the feature gate `PodIndexLabel` is enabled and locked by default for this
  > feature, in order to disable it, users will have to use server emulated version v1.31.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): removed the unsupported comparison with Deployments

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The excerpts support using StatefulSets for workloads that need stable network identities, persistent storage, and ordered deployment/scaling. They do not say that databases as a class necessarily rely on all these properties. Qualify the answer: use a StatefulSet for a database when it needs those guarantees.


---

### `cronjob-nightly`

**Question** (en, task): How do I run a job every night at 2 am?

**Reference answer:** Create a CronJob with `schedule: "0 2 * * *"` (cron syntax; `timeZone` can set the time zone).

**Relevant documentation:**
- `concepts/workloads/controllers/cron-jobs.md`, section: *CronJob > Writing a CronJob spec*
  > [CronJob > Writing a CronJob spec > Schedule syntax]
  > The `.spec.schedule` field is required. The value of that field follows the Cron syntax:
  > ```
  > # ┌───────────── minute (0 - 59)
  > # │ ┌───────────── hour (0 - 23)
  > # │ │ ┌───────────── day of the month (1 - 31)
  > # │ │ │ ┌───────────── month (1 - 12)
  > # │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
  > # │ │ │ │ │                                   OR sun, mon, tue, wed, thu, fri, sat
  > # │ │ │ │ │
  > # │ │ │ │ │
  > # * * * * *
  > ```
  > For example, `0 3 * * 1` means this task is scheduled to run weekly on a Monday at 3 AM.
  > The format also includes extended "Vixie cron" step values. As explained in the
  > FreeBSD manual:
  > > Step values can be used in conjunction with ranges. Following a range
  > > with `/<number>` specifies skips of the number's value through the
  > > range. For example, `0-23/2` can be used in the hours field to specify
  > > command execution every other hour (the alternative in the V7 standard is
  > > `0,2,4,6,8,10,12,14,16,18,20,22`). Steps are also permitted after an
  > > asterisk, so if you want to say "every two hours", just use `*/2`.
  > A question mark (`?`) in the schedule has the same meaning as an asterisk `*`, that is,
  > it stands for any of available value for a given field.
  > A question mark (`?`) in the schedule has the same meaning as an asterisk `*`, that is,
  > it stands for any of available value for a given field.
  > Other than the standard syntax, some macros like `@monthly` can also be used:
  > | Entry 										| Description																									| Equivalent to |
  > | ------------- 						| ------------- 																							|-------------  |
  > | @yearly (or @annually)		| Run once a year at midnight of 1 January										| 0 0 1 1 * 		|
  > | @monthly 									| Run once a month at midnight of the first day of the month	| 0 0 1 * * 		|
  > | @weekly 									| Run once a week at midnight on Sunday morning								| 0 0 * * 0 		|
  > | @daily (or @midnight)			| Run once a day at midnight																	| 0 0 * * * 		|
  > | @hourly 									| Run once an hour at the beginning of the hour								| 0 * * * * 		|
  > To generate CronJob schedule expressions, you can also use web tools like crontab.guru.
  > [CronJob > Writing a CronJob spec > Job template]
  > The `.spec.jobTemplate` defines a template for the Jobs that the CronJob creates, and it is required.
  > It has exactly the same schema as a Job, except that
  > it is nested and does not have an `apiVersion` or `kind`.
  > You can specify common metadata for the templated Jobs, such as
  > labels or
  > annotations.
  > For information about writing a Job `.spec`, see Writing a Job Spec.
  > [CronJob > Writing a CronJob spec > Deadline for delayed Job start {#starting-deadline}]
  > The `.spec.startingDeadlineSeconds` field is optional.
  > This field defines a deadline (in whole seconds) for starting the Job, if that Job misses its scheduled time
  > for any reason.
  > After missing the deadline, the CronJob skips that instance of the Job (future occurrences are still scheduled).
  > For example, if you have a backup Job that runs twice a day, you might allow it to start up to 8 hours late,
  > but no later, because a backup taken any later wouldn't be useful: you would instead prefer to wait for
  > the next scheduled run.
  > For Jobs that miss their configured deadline, Kubernetes treats them as failed Jobs.
  > If you don't specify `startingDeadlineSeconds` for a CronJob, the Job occurrences have no deadline.
  > If the `.spec.startingDeadlineSeconds` field is set (not null), the CronJob
  > controller measures the time between when a Job is expected to be created and
  > now. If the difference is higher than that limit, it will skip this execution.
  > For example, if it is set to `200`, it allows a Job to be created for up to 200
  > seconds after the actual schedule.
  > [CronJob > Writing a CronJob spec > Concurrency policy]
  > The `.spec.concurrencyPolicy` field is also optional.
  > It specifies how to treat concurrent executions of a Job that is created by this CronJob.
  > The spec may specify only one of the following concurrency policies:
  > * `Allow` (default): The CronJob allows concurrently running Jobs
  > * `Forbid`: The CronJob does not allow concurrent runs; if it is time for a new Job run and the
  >   previous Job run hasn't finished yet, the CronJob skips the new Job run. Also note that when the
  >   previous Job run finishes, `.spec.startingDeadlineSeconds` is still taken into account and may
  >   result in a new Job run.
  > * `Replace`: If it is time for a new Job run and the previous Job run hasn't finished yet, the
  >   CronJob replaces the currently running Job run with a new Job run
  > Note that concurrency policy only applies to the Jobs created by the same CronJob.
  > If there are multiple CronJobs, their respective Jobs are always allowed to run concurrently.
  > [CronJob > Writing a CronJob spec > Schedule suspension]
  > You can suspend execution of Jobs for a CronJob, by setting the optional `.spec.suspend` field
  > to true. The field defaults to false.
  > This setting does _not_ affect Jobs that the CronJob has already started.
  > If you do set that field to true, all subsequent executions are suspended (they remain
  > scheduled, but the CronJob controller does not start the Jobs to run the tasks) until
  > you unsuspend the CronJob.
  > Executions that are suspended during their scheduled time count as missed Jobs.
  > When `.spec.suspend` changes from `true` to `false` on an existing CronJob without a
  > starting deadline, the missed Jobs are scheduled immediately.
  > [CronJob > Writing a CronJob spec > Jobs history limits]
  > The `.spec.successfulJobsHistoryLimit` and `.spec.failedJobsHistoryLimit` fields specify
  > how many completed and failed Jobs should be kept. Both fields are optional.
  > * `.spec.successfulJobsHistoryLimit`: This field specifies the number of successful finished
  > jobs to keep. The default value is `3`. Setting this field to `0` will not keep any successful jobs.
  > * `.spec.failedJobsHistoryLimit`: This field specifies the number of failed finished jobs to keep.
  > The default value is `1`. Setting this … (section continues)
- `concepts/workloads/controllers/cron-jobs.md`, section: *CronJob > Example*
  > [CronJob > Example]
  > This example CronJob manifest prints the current time and a hello message every minute:
  > (Running Automated Tasks with a CronJob
  > takes you through this example in more detail).

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The cron field layout supports `0 2 * * *`, but the supplied excerpts do not mention `.spec.timeZone`. Remove the time-zone clause or add the “Time zones” documentation excerpt.


---

### `rbac-role-clusterrole`

**Question** (en, concept): What is the difference between a Role and a ClusterRole?

**Reference answer:** A Role grants permissions within one namespace; a ClusterRole is cluster-wide and can cover cluster-scoped resources or be reused across namespaces via RoleBindings.

**Relevant documentation:**
- `reference/access-authn-authz/rbac.md`, section: *Using RBAC Authorization > API objects*
  > [Using RBAC Authorization > API objects {#api-overview}]
  > The RBAC API declares four kinds of Kubernetes object: _Role_, _ClusterRole_,
  > _RoleBinding_ and _ClusterRoleBinding_. You can describe or amend the RBAC
  > objects
  > using tools such as `kubectl`, just like any other Kubernetes object.
  > These objects, by design, impose access restrictions. If you are making changes
  > to a cluster as you learn, see
  > privilege escalation prevention and bootstrapping
  > to understand how those restrictions can prevent you making some changes.
  > [Using RBAC Authorization > API objects {#api-overview} > Role and ClusterRole]
  > An RBAC _Role_ or _ClusterRole_ contains rules that represent a set of permissions.
  > Permissions are purely additive (there are no "deny" rules).
  > A Role always sets permissions within a particular namespace;
  > when you create a Role, you have to specify the namespace it belongs in.
  > ClusterRole, by contrast, is a non-namespaced resource. The resources have different names (Role
  > and ClusterRole) because a Kubernetes object always has to be either namespaced or not namespaced;
  > it can't be both.
  > ClusterRoles have several uses. You can use a ClusterRole to:
  > 1. define permissions on namespaced resources and be granted access within individual namespace(s)
  > 1. define permissions on namespaced resources and be granted access across all namespaces
  > 1. define permissions on cluster-scoped resources
  > If you want to define a role within a namespace, use a Role; if you want to define
  > a role cluster-wide, use a ClusterRole.
  > [Using RBAC Authorization > API objects {#api-overview} > Role and ClusterRole > Role example]
  > Here's an example Role in the "default" namespace that can be used to grant read access to
  > pods:
  > [Using RBAC Authorization > API objects {#api-overview} > Role and ClusterRole > ClusterRole example]
  > A ClusterRole can be used to grant the same permissions as a Role.
  > Because ClusterRoles are cluster-scoped, you can also use them to grant access to:
  > * cluster-scoped resources (like nodes)
  > * non-resource endpoints (like `/healthz`)
  > * namespaced resources (like Pods), across all namespaces
  >   For example: you can use a ClusterRole to allow a particular user to run
  >   `kubectl get pods --all-namespaces`
  > Here is an example of a ClusterRole that can be used to grant read access to
  > secrets in any particular namespace,
  > or across all namespaces (depending on how it is bound):
  > The name of a Role or a ClusterRole object must be a valid
  > path segment name.
  > [Using RBAC Authorization > API objects {#api-overview} > RoleBinding and ClusterRoleBinding]
  > A role binding grants the permissions defined in a role to a user or set of users.
  > It holds a list of *subjects* (users, groups, or service accounts), and a reference to the
  > role being granted.
  > A RoleBinding grants permissions within a specific namespace whereas a ClusterRoleBinding
  > grants that access cluster-wide.
  > A RoleBinding may reference any Role in the same namespace. Alternatively, a RoleBinding
  > can reference a ClusterRole and bind that ClusterRole to the namespace of the RoleBinding.
  > If you want to bind a ClusterRole to all the namespaces in your cluster, you use a
  > ClusterRoleBinding.
  > The name of a RoleBinding or ClusterRoleBinding object must be a valid
  > path segment name.
  > [Using RBAC Authorization > API objects {#api-overview} > RoleBinding and ClusterRoleBinding > RoleBinding examples {#rolebinding-example}]
  > Here is an example of a RoleBinding that grants the "pod-reader" Role to the user "jane"
  > within the "default" namespace.
  > This allows "jane" to read pods in the "default" namespace.
  > A RoleBinding can also reference a ClusterRole to grant the permissions defined in that
  > ClusterRole to resources inside the RoleBinding's namespace. This kind of reference
  > lets you define a set of common roles across your cluster, then reuse them within
  > multiple namespaces.
  > For instance, even though the following RoleBinding refers to a ClusterRole,
  > "dave" (the subject, case sensitive) will only be able to read Secrets in the "development"
  > namespace, because the RoleBinding's namespace (in its metadata) is "development".
  > [Using RBAC Authorization > API objects {#api-overview} > RoleBinding and ClusterRoleBinding > ClusterRoleBinding example]
  > To grant permissions across a whole cluster, you can use a ClusterRoleBinding.
  > The following ClusterRoleBinding allows any user in the group "manager" to read
  > secrets in any namespace.
  > After you create a binding, you cannot change the Role or ClusterRole that it refers to.
  > If you try to change a binding's `roleRef`, you get a validation error. If you do want
  > to change the `roleRef` for a binding, you need to remove the binding object and create
  > a replacement.
  > There are two reasons for this restriction:
  > 1. Making `roleRef` immutable allows granting someone `update` permission on an existing binding
  >    object, so that they can manage the list of subjects, without being able to change
  >    the role that is granted to those subjects.
  > 1. A binding to a different role is a fundamentally different binding.
  >    Requiring a binding to be deleted/recreated in order to change the `roleRef`
  >    ensures the full list of subjects in the binding is intended to be granted
  >    the new role (as opposed to enabling or accidentally modifying only the roleRef
  >    without verifying all of the existing subjects should be given the new role's
  >    permissions).
  > The `kubectl auth reconcile` command-line utility creates or updates a manifest file containing RBAC objects,
  > and handles deleting and recreating binding objects if required to change the role they refer to.
  > See command usage and examples for more information.
  > [Using RBAC Authorization > API objects {#api-overview} > Referring to resources]
  > In the Kubernetes API, most resources are represented and accessed using a string representation of
  > their object name, such as `pods` for a Pod. RBAC refers to resources using exactly the same
  > name that appears in the URL for the relevant API endpoint.
  > Some Kubernetes … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `drain-node`

**Question** (en, command): How do I safely take a node offline for maintenance?

**Reference answer:** `kubectl drain <node> --ignore-daemonsets` evicts Pods (respecting PodDisruptionBudgets) and cordons the node; `kubectl uncordon <node>` afterwards.

**Relevant documentation:**
- `tasks/administer-cluster/safely-drain-node.md`, section: *Safely Drain a Node > Use `kubectl drain` to remove a node from service*
  > [Safely Drain a Node > Use `kubectl drain` to remove a node from service]
  > You can use `kubectl drain` to safely evict all of your pods from a
  > node before you perform maintenance on the node (e.g. kernel upgrade,
  > hardware maintenance, etc.). Safe evictions allow the pod's containers
  > to gracefully terminate
  > and will respect the PodDisruptionBudgets you have specified.
  > By default `kubectl drain` ignores certain system pods on the node
  > that cannot be killed; see
  > the kubectl drain
  > documentation for more details.
  > When `kubectl drain` returns successfully, that indicates that all of
  > the pods (except the ones excluded as described in the previous paragraph)
  > have been safely evicted (respecting the desired graceful termination period,
  > and respecting the PodDisruptionBudget you have defined). It is then safe to
  > bring down the node by powering down its physical machine or, if running on a
  > cloud platform, deleting its virtual machine.
  > If any new Pods tolerate the `node.kubernetes.io/unschedulable` taint, then those Pods
  > might be scheduled to the node you have drained. Avoid tolerating that taint other than
  > for DaemonSets.
  > If any new Pods tolerate the `node.kubernetes.io/unschedulable` taint, then those Pods
  > might be scheduled to the node you have drained. Avoid tolerating that taint other than
  > for DaemonSets.
  > If you or another API user directly set the `nodeName`
  > field for a Pod (bypassing the scheduler), then the Pod is bound to the specified node
  > and will run there, even though you have drained that node and marked it unschedulable.
  > First, identify the name of the node you wish to drain. You can list all of the nodes in your cluster with
  > ```shell
  > kubectl get nodes
  > ```
  > Next, tell Kubernetes to drain the node:
  > ```shell
  > kubectl drain --ignore-daemonsets <node name>
  > ```
  > If there are pods managed by a DaemonSet, you will need to specify
  > `--ignore-daemonsets` with `kubectl` to successfully drain the node. The `kubectl drain` subcommand on its own does not actually drain
  > a node of its DaemonSet pods:
  > the DaemonSet controller (part of the control plane) immediately replaces missing Pods with
  > new equivalent Pods. The DaemonSet controller also creates Pods that ignore unschedulable
  > taints, which allows the new Pods to launch onto a node that you are draining.
  > Once it returns (without giving an error), you can power down the node
  > (or equivalently, if on a cloud platform, delete the virtual machine backing the node).
  > If you leave the node in the cluster during the maintenance operation, you need to run
  > ```shell
  > kubectl uncordon <node name>
  > ```
  > afterwards to tell Kubernetes that it can resume scheduling new pods onto the node.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `init-container-setup`

**Question** (en, concept): How can I make sure a setup step finishes before my app container starts?

**Reference answer:** Use init containers: they run to completion, one after another, before the app containers start.

**Relevant documentation:**
- `concepts/workloads/pods/init-containers.md`, section: *(whole document)*
  > [Init Containers]
  > This page provides an overview of init containers: specialized containers that run
  > before app containers in a Pod.
  > Init containers can contain utilities or setup scripts not present in an app image.
  > You can specify init containers in the Pod specification alongside the `containers`
  > array (which describes app containers).
  > In Kubernetes, a sidecar container is a container that
  > starts before the main application container and _continues to run_. This document is about init containers:
  > containers that run to completion during Pod initialization.
  > [Init Containers > Understanding init containers]
  > A Pod can have multiple containers
  > running apps within it, but it can also have one or more init containers, which are run
  > before the app containers are started.
  > Init containers are exactly like regular containers, except:
  > * Init containers always run to completion.
  > * Each init container must complete successfully before the next one starts.
  > If a Pod's init container fails, the kubelet repeatedly restarts that init container until it succeeds.
  > However, if the Pod has a `restartPolicy` of Never, and an init container fails during startup of that Pod, Kubernetes treats the overall Pod as failed.
  > To specify an init container for a Pod, add the `initContainers` field into
  > the Pod specification,
  > as an array of `container` items (similar to the app `containers` field and its contents).
  > See Container in the
  > API reference for more details.
  > The status of the init containers is returned in `.status.initContainerStatuses`
  > field as an array of the container statuses (similar to the `.status.containerStatuses`
  > field).
  > [Init Containers > Understanding init containers > Differences from regular containers]
  > Init containers support all the fields and features of app containers,
  > including resource limits, volumes, and security settings. However, the
  > resource requests and limits for an init container are handled differently,
  > as documented in Resource sharing within containers.
  > Regular init containers (in other words: excluding sidecar containers) do not support the
  > `lifecycle`, `livenessProbe`, `readinessProbe`, or `startupProbe` fields. Init containers
  > must run to completion before the Pod can be ready; sidecar containers continue running
  > during a Pod's lifetime, and _do_ support some probes. See sidecar container
  > for further details about sidecar containers.
  > If you specify multiple init containers for a Pod, kubelet runs each init
  > container sequentially. Each init container must succeed before the next can run.
  > When all of the init containers have run to completion, kubelet initializes
  > the application containers for the Pod and runs them as usual.
  > [Init Containers > Understanding init containers > Differences from sidecar containers]
  > Init containers run and complete their tasks before the main application container starts.
  > Unlike sidecar containers,
  > init containers are not continuously running alongside the main containers.
  > Init containers run to completion sequentially, and the main container does not start
  > until all the init containers have successfully completed.
  > init containers do not support `lifecycle`, `livenessProbe`, `readinessProbe`, or
  > `startupProbe` whereas sidecar containers support all these probes to control their lifecycle.
  > Init containers share the same resources (CPU, memory, network) with the main application
  > containers but do not interact directly with them. They can, however, use shared volumes
  > for data exchange.
  > [Init Containers > Using init containers]
  > Because init containers have separate images from app containers, they
  > have some advantages for start-up related code:
  > * Init containers can contain utilities or custom code for setup that are not present in an app
  >   image. For example, there is no need to make an image `FROM` another image just to use a tool like
  >   `sed`, `awk`, `python`, or `dig` during setup.
  > * The application image builder and deployer roles can work independently without
  >   the need to jointly build a single app image.
  > * Init containers can run with a different view of the filesystem than app containers in the
  >   same Pod. Consequently, they can be given access to
  >   Secrets that app containers cannot access.
  > * Because init containers run to completion before any app containers start, init containers offer
  >   a mechanism to block or delay app container startup until a set of preconditions are met. Once
  >   preconditions are met, all of the app containers in a Pod can start in parallel.
  > * Init containers can securely run utilities or custom code that would otherwise make an app
  >   container image less secure. By keeping unnecessary tools separate you can limit the attack
  >   surface of your app container image.
  > [Init Containers > Using init containers > Examples]
  > Here are some ideas for how to use init containers:
  > * Wait for a Service to
  >   be created, using a shell one-line command like:
  >   ```shell
  >   for i in {1..100}; do sleep 1; if nslookup myservice; then exit 0; fi; done; exit 1
  >   ```
  > * Register this Pod with a remote server from the downward API with a command like:
  >   ```shell
  >   curl -X POST http://$MANAGEMENT_SERVICE_HOST:$MANAGEMENT_SERVICE_PORT/register -d 'instance=$(<POD_NAME>)&ip=$(<POD_IP>)'
  >   ```
  > * Wait for some time before starting the app container with a command like
  >   ```shell
  >   sleep 60
  >   ```
  > * Clone a Git repository into a Volume
  > * Place values into a configuration file and run a template tool to dynamically
  >   generate a configuration file for the main app container. For example,
  >   place the `POD_IP` value in a configuration and generate the main app
  >   configuration file using Jinja.
  > [Init Containers > Using init containers > Examples > Init containers in use]
  > This example defines a simple Pod that has two init containers.
  > The first waits for `myservice`, and the second waits for `mydb`. Once both
  > init containers complete, the Pod runs the app container from its `spec` section.
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: … (section continues)

*Drafting note:* Vocabulary gap: user doesn't say 'init container'. | LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `image-pull-policy`

**Question** (en, concept): When does the kubelet pull an image again instead of using the cached one?

**Reference answer:** It depends on `imagePullPolicy`: `Always` pulls each time, `IfNotPresent` uses the local copy, `Never` never pulls. With the `:latest` tag or no tag the default is `Always`.

**Relevant documentation:**
- `concepts/containers/images.md`, section: *Images > Updating images*
  > [Images > Updating images]
  > When you first create a Deployment,
  > StatefulSet, Pod, or other
  > object that includes a PodTemplate, and a pull policy was not explicitly specified,
  > then by default the pull policy of all containers in that Pod will be set to
  > `IfNotPresent`. This policy causes the
  > kubelet to skip pulling an
  > image if it already exists.
  > [Images > Updating images > Image pull policy]
  > The `imagePullPolicy` for a container and the tag of the image both affect _when_ the
  > kubelet attempts to pull
  > (download) the specified image.
  > Here's a list of the values you can set for `imagePullPolicy` and the effects
  > these values have:
  > `IfNotPresent`
  > : the image is pulled only if it is not already present locally.
  > `Always`
  > : every time the kubelet launches a container, the kubelet queries the container
  >   image registry to resolve the name to an image
  >   digest.
  >   If the kubelet has a container image with that exact digest cached locally, the kubelet uses its
  >   cached image; otherwise, the kubelet pulls the image with the resolved digest, and uses that image
  >   to launch the container.
  > `Never`
  > : the kubelet does not try fetching the image. If the image is somehow already present
  >   locally, the kubelet attempts to start the container; otherwise, startup fails.
  >   See pre-pulled images for more details.
  > The caching semantics of the underlying image provider make even
  > `imagePullPolicy: Always` efficient, as long as the registry is reliably accessible.
  > Your container runtime can notice that the image layers already exist on the node
  > so that they don't need to be downloaded again.
  > You should avoid using the `:latest` tag when deploying containers in production as
  > it is harder to track which version of the image is running and more difficult to
  > roll back properly.
  > Instead, specify a meaningful tag such as `v1.42.0` and/or a digest.
  > To make sure the Pod always uses the same version of a container image, you can specify
  > the image's digest;
  > replace `<image-name>:<tag>` with `<image-name>@<digest>`
  > (for example, `image@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2`).
  > When using image tags, if the image registry were to change the code that the tag on that image
  > represents, you might end up with a mix of Pods running the old and new code. An image digest
  > uniquely identifies a specific version of the image, so Kubernetes runs the same code every time
  > it starts a container with that image name and digest specified. Specifying an image by digest
  > pins the code that you run so that a change at the registry cannot lead to that mix of versions.
  > There are third-party admission controllers
  > that mutate Pods (and PodTemplates) when they are created, so that the
  > running workload is defined based on an image digest rather than a tag.
  > That might be useful if you want to make sure that your entire workload is
  > running the same code no matter what tag changes happen at the registry.
  > [Images > Updating images > Image pull policy > Default image pull policy {#imagepullpolicy-defaulting}]
  > When you (or a controller) submit a new Pod to the API server, your cluster sets the
  > `imagePullPolicy` field when specific conditions are met:
  > - if you omit the `imagePullPolicy` field, and you specify the digest for the
  >   container image, the `imagePullPolicy` is automatically set to `IfNotPresent`.
  > - if you omit the `imagePullPolicy` field, and the tag for the container image is
  >   `:latest`, `imagePullPolicy` is automatically set to `Always`.
  > - if you omit the `imagePullPolicy` field, and you don't specify the tag for the
  >   container image, `imagePullPolicy` is automatically set to `Always`.
  > - if you omit the `imagePullPolicy` field, and you specify a tag for the container
  >   image that isn't `:latest`, the `imagePullPolicy` is automatically set to
  >   `IfNotPresent`.
  > The value of `imagePullPolicy` of the container is always set when the object is
  > first _created_, and is not updated if the image's tag or digest later changes.
  > The value of `imagePullPolicy` of the container is always set when the object is
  > first _created_, and is not updated if the image's tag or digest later changes.
  > For example, if you create a Deployment with an image whose tag is _not_
  > `:latest`, and later update that Deployment's image to a `:latest` tag, the
  > `imagePullPolicy` field will _not_ change to `Always`. You must manually change
  > the pull policy of any object after its initial creation.
  > [Images > Updating images > Image pull policy > Required image pull]
  > If you would like to always force a pull, you can do one of the following:
  > - Set the `imagePullPolicy` of the container to `Always`.
  > - Omit the `imagePullPolicy` and use `:latest` as the tag for the image to use;
  >   Kubernetes will set the policy to `Always` when you submit the Pod.
  > - Omit the `imagePullPolicy` and the tag for the image to use;
  >   Kubernetes will set the policy to `Always` when you submit the Pod.
  > - Enable the AlwaysPullImages
  >   admission controller.
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
  > [Images > Updating images > Image pull per runtime class]
  > Kubernetes includes alpha support for performing image pulls based on the RuntimeClass of a Pod.
  > If you enable the `RuntimeClassInImageCriApi` feature gate,
  > the kubelet references container images by a tuple of image name and runtime handler
  > rather than just the image name or digest. Your
  > container … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
`Always` does not necessarily download the image on every launch. The excerpt says the kubelet queries the registry each time to resolve the image digest, then reuses the locally cached image when that exact digest is present; it pulls only when needed. Change “Always pulls each time” to that distinction. The `IfNotPresent`, `Never`, and `:latest`/untagged default statements are supported.


---

### `pdb-keep-replicas`

**Question** (en, task): How do I make sure at least two replicas stay up while nodes are being drained?

**Reference answer:** Create a PodDisruptionBudget for those Pods that limits how many can be down at the same time (e.g. requiring at least two available). Voluntary disruptions such as draining a node respect it.

**Relevant documentation:**
- `concepts/workloads/pods/disruptions.md`, section: *Disruptions > Pod disruption budgets*
  > [Disruptions > Pod disruption budgets]
  > Kubernetes offers features to help you run highly available applications even when you
  > introduce frequent voluntary disruptions.
  > As an application owner, you can create a PodDisruptionBudget (PDB) for each application.
  > A PDB limits the number of Pods of a replicated application that are down simultaneously from
  > voluntary disruptions. For example, a quorum-based application would
  > like to ensure that the number of replicas running is never brought below the
  > number needed for a quorum. A web front end might want to
  > ensure that the number of replicas serving load never falls below a certain
  > percentage of the total.
  > Cluster managers and hosting providers should use tools which
  > respect PodDisruptionBudgets by calling the Eviction API
  > instead of directly deleting pods or deployments.
  > Cluster managers and hosting providers should use tools which
  > respect PodDisruptionBudgets by calling the Eviction API
  > instead of directly deleting pods or deployments.
  > For example, the `kubectl drain` subcommand lets you mark a node as going out of
  > service. When you run `kubectl drain`, the tool tries to evict all of the Pods on
  > the Node you're taking out of service. The eviction request that `kubectl` submits on
  > your behalf may be temporarily rejected, so the tool periodically retries all failed
  > requests until all Pods on the target node are terminated, or until a configurable timeout
  > is reached.
  > A PDB specifies the number of replicas that an application can tolerate having, relative to how
  > many it is intended to have.  For example, a Deployment which has a `.spec.replicas: 5` is
  > supposed to have 5 pods at any given time.  If its PDB allows for there to be 4 at a time,
  > then the Eviction API will allow voluntary disruption of one (but not two) pods at a time.
  > The group of pods that comprise the application is specified using a label selector, the same
  > as the one used by the application's controller (deployment, stateful-set, etc).
  > The group of pods that comprise the application is specified using a label selector, the same
  > as the one used by the application's controller (deployment, stateful-set, etc).
  > The "intended" number of pods is computed from the `.spec.replicas` of the workload resource
  > that is managing those pods. The control plane discovers the owning workload resource by
  > examining the `.metadata.ownerReferences` of the Pod.
  > Involuntary disruptions cannot be prevented by PDBs; however they
  > do count against the budget.
  > Pods which are deleted or unavailable due to a rolling upgrade to an application do count
  > against the disruption budget, but workload resources (such as Deployment and StatefulSet)
  > are not limited by PDBs when doing rolling upgrades. Instead, the handling of failures
  > during application updates is configured in the spec for the specific workload resource.
  > It is recommended to set `AlwaysAllow` Unhealthy Pod Eviction Policy
  > to your PodDisruptionBudgets to support eviction of misbehaving applications during a node drain.
  > The default behavior is to wait for the application pods to become healthy
  > before the drain can proceed.
  > When a pod is evicted using the eviction API, it is gracefully
  > terminated, honoring the
  > `terminationGracePeriodSeconds` setting in its PodSpec.
- `tasks/administer-cluster/safely-drain-node.md`, section: *Safely Drain a Node > (Optional) Configure a disruption budget*
  > [Safely Drain a Node > (Optional) Configure a disruption budget {#configure-poddisruptionbudget}]
  > To ensure that your workloads remain available during maintenance, you can
  > configure a PodDisruptionBudget.
  > If availability is important for any applications that run or could run on the node(s)
  > that you are draining, configure a PodDisruptionBudgets
  > first and then continue following this guide.
  > It is recommended to set `AlwaysAllow` Unhealthy Pod Eviction Policy
  > to your PodDisruptionBudgets to support eviction of misbehaving applications during a node drain.
  > The default behavior is to wait for the application pods to become healthy
  > before the drain can proceed.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): narrowed (the PDB YAML example is not in the index)

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-pod-multi-container`

**Question** (fr, concept): Qu'est-ce qu'un Pod et pourquoi peut-il contenir plusieurs conteneurs ?

**Reference answer:** Un Pod est la plus petite unité déployable ; il regroupe un ou plusieurs conteneurs qui partagent le réseau et le stockage, pour des conteneurs étroitement liés.

**Relevant documentation:**
- `concepts/workloads/pods/pod-overview.md`, section: *Aperçu du Pod > Comprendre les Pods*
  > [Aperçu du Pod > Comprendre les Pods]
  > Un *Pod* est l'unité d'exécution de base d'une application Kubernetes--l'unité la plus petite et la plus simple dans le modèle d'objets de Kubernetes--que vous créez ou déployez. Un Pod représente des process en cours d'exécution dans votre cluster.
  > Un Pod encapsule un conteneur applicatif (ou, dans certains cas, plusieurs conteneurs), des ressources de stockage, une identité réseau (adresse IP) unique, ainsi que des options qui contrôlent comment le ou les conteneurs doivent s'exécuter. Un Pod représente une unité de déploiement : *une instance unique d'une application dans Kubernetes*, qui peut consister soit en un unique container soit en un petit nombre de conteneurs qui sont étroitement liés et qui partagent des ressources.
  > > Docker est le runtime de conteneurs le plus courant utilisé dans un Pod Kubernetes, mais les Pods prennent également en charge d'autres runtimes de conteneurs.
  > Les Pods dans un cluster Kubernetes peuvent être utilisés de deux manières différentes :
  > Les Pods dans un cluster Kubernetes peuvent être utilisés de deux manières différentes :
  > * **les Pods exécutant un conteneur unique**. Le modèle "un-conteneur-par-Pod" est le cas d'utilisation Kubernetes le plus courant ; dans ce cas, vous pouvez voir un Pod comme un wrapper autour d'un conteneur unique, et Kubernetes gère les Pods plutôt que directement les conteneurs.
  > * **les Pods exécutant plusieurs conteneurs devant travailler ensemble**. Un Pod peut encapsuler une application composée de plusieurs conteneurs co-localisés qui sont étroitement liés et qui doivent partager des ressources. Ces conteneurs co-localisés pourraient former une unique unité de service cohésive--un conteneur servant des fichiers d'un volume partagé au public, alors qu'un conteneur "sidecar" séparé rafraîchit ou met à jour ces fichiers. Le Pod enveloppe ensemble ces conteneurs et ressources de stockage en une entité maniable de base.
  > Chaque Pod est destiné à exécuter une instance unique d'une application donnée. Si vous désirez mettre à l'échelle votre application horizontalement, (pour fournir plus de ressources au global en exécutant plus d'instances), vous devez utiliser plusieurs Pods, un pour chaque instance. Dans Kubernetes, on parle typiquement de _réplication_. Des Pods répliqués sont en général créés et gérés en tant que groupe par une ressource de charge de travail et son _contrôleur_. Voir Pods et contrôleurs pour plus d'informations.
  > [Aperçu du Pod > Comprendre les Pods > Comment les Pods gèrent plusieurs conteneurs]
  > Les Pods sont conçus pour supporter plusieurs process coopérants (sous forme de conteneurs) qui forment une unité de service cohésive. Les conteneurs d'un même Pod sont automatiquement co-localisés et co-programmés sur la même machine physique ou virtuelle dans le cluster. Ces conteneurs peuvent partager des ressources et dépendances, communiquer entre eux, et coordonner quand et comment ils sont arrêtés.
  > Notez que grouper plusieurs conteneurs co-localisés et co-gérés dans un unique Pod est un cas d'utilisation relativement avancé. Vous devez utiliser ce pattern seulement dans des instances spécifiques dans lesquelles vos conteneurs sont étroitement liés. Par exemple, vous pourriez avoir un conteneur qui agit comme un serveur web pour des fichiers contenus dans un volume partagé, et un conteneur "sidecar" séparé qui met à jour ces fichiers depuis une source externe, comme dans le diagramme suivant :
  > Certains Pods ont des init containers en plus d'app containers. Les Init containers s'exécutent et terminent avant que les conteneurs d'application soient démarrés.
  > Les Pods fournissent deux types de ressources partagées pour leurs conteneurs : *réseau* et *stockage*.
  > [Aperçu du Pod > Comprendre les Pods > Comment les Pods gèrent plusieurs conteneurs > Réseau]
  > Chaque Pod se voit assigner une adresse IP unique pour chaque famille d'adresses. Tous les conteneurs d'un Pod partagent le même namespace réseau, y compris l'adresse IP et les ports réseau. Les conteneurs *à l'intérieur d'un Pod* peuvent communiquer entre eux en utilisant `localhost`. Lorsque les conteneurs dans un Pod communiquent avec des entités *en dehors du Pod*, ils doivent coordonner comment ils utilisent les ressources réseau partagées (comme les ports).
  > [Aperçu du Pod > Comprendre les Pods > Comment les Pods gèrent plusieurs conteneurs > Stockage]
  > Un Pod peut spécifier un jeu de volumes de stockage partagés. Tous les conteneurs dans le Pod peuvent accéder aux volumes partagés, permettant à ces conteneurs de partager des données. Les volumes permettent aussi les données persistantes d'un Pod de survivre au cas où un des conteneurs doit être redémarré. Voir Volumes pour plus d'informations sur la façon dont Kubernetes implémente le stockage partagé dans un Pod.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-rollback`

**Question** (fr, task): Comment revenir à la version précédente d'un déploiement ?

**Reference answer:** `kubectl rollout undo deployment/<nom>` (option `--to-revision`).

**Relevant documentation:**
- `concepts/workloads/controllers/deployment.md`, section: *Déploiements > Annulation d'un déploiement*
  > [Déploiements > Annulation d'un déploiement]
  > Parfois, vous souhaiterez peut-être annuler un déploiement; par exemple, lorsque le déploiement n'est pas stable, comme en cas d'échecs à répétition (CrashLoopBackOff).
  > Par défaut, tout l'historique des déploiements d'un déploiement est conservé dans le système afin que vous puissiez le restaurer à tout moment (vous pouvez le modifier en modifiant la limite de l'historique des révisions).
  > La révision d'un déploiement est créée lorsque le déploiement d'un déploiement est déclenché.
  > Cela signifie qu'une nouvelle révision est créée si et seulement si le template de pod de déploiement (`.spec.template`) est modifié, par exemple si vous mettez à jour les labels ou les images de conteneur du template.
  > D'autres mises à jour, telles que la mise à l'échelle du déploiement, ne créent pas de révision de déploiement, de sorte que vous puissiez faciliter la mise à l'échelle manuelle ou automatique simultanée.
  > Cela signifie que lorsque vous revenez à une révision antérieure, seule la partie du template de pod de déploiement est annulée.
  > * Supposons que vous ayez fait une faute de frappe lors de la mise à jour du déploiement, en mettant le nom de l'image sous la forme `nginx:1.91` au lieu de `nginx: 1.9.1`:
  >     ```shell
  >     kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.91 --record=true
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     deployment.apps/nginx-deployment image updated
  >     ```
  > * Le déploiement est bloqué.
  >   Vous pouvez le vérifier en vérifiant l'état du déploiement:
  >     ```shell
  >     kubectl rollout status deployment.v1.apps/nginx-deployment
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     Waiting for rollout to finish: 1 out of 3 new replicas have been updated...
  >     ```
  > * Appuyez sur Ctrl-C pour arrêter la surveillance d'état de déploiement ci-dessus.
  >   Pour plus d'informations sur les déploiements bloqués, en savoir plus ici.
  > * Vous voyez que le nombre d'anciens réplicas (`nginx-deployment-1564180365` et `nginx-deployment-2035384211`) est 2, et les nouveaux réplicas (`nginx-deployment-3066724191`) est 1.
  >     ```shell
  >     kubectl get rs
  >     ```
  >     La sortie est similaire à ceci:
  >     La sortie est similaire à ceci:
  >     ```text
  >     NAME                          DESIRED   CURRENT   READY   AGE
  >     nginx-deployment-1564180365   3         3         3       25s
  >     nginx-deployment-2035384211   0         0         0       36s
  >     nginx-deployment-3066724191   1         1         0       6s
  >     ```
  > * En regardant les pods créés, vous voyez que 1 pod créé par le nouveau ReplicaSet est coincé dans une boucle pour récupérer son image:
  >     ```shell
  >     kubectl get pods
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     NAME                                READY     STATUS             RESTARTS   AGE
  >     nginx-deployment-1564180365-70iae   1/1       Running            0          25s
  >     nginx-deployment-1564180365-jbqqo   1/1       Running            0          25s
  >     nginx-deployment-1564180365-hysrc   1/1       Running            0          25s
  >     nginx-deployment-3066724191-08mng   0/1       ImagePullBackOff   0          6s
  >     ```
  >     Le contrôleur de déploiement arrête automatiquement le mauvais déploiement et arrête la mise à l'échelle du nouveau ReplicaSet.
  >     Cela dépend des paramètres rollingUpdate (`maxUnavailable` spécifiquement) que vous avez spécifiés.
  >     Kubernetes définit par défaut la valeur à 25%.
  > * Obtenez la description du déploiement:
  >     ```shell
  >     kubectl describe deployment
  >     ```
  >     La sortie est similaire à ceci:
  >     La sortie est similaire à ceci:
  >     ```text
  >     Name:           nginx-deployment
  >     Namespace:      default
  >     CreationTimestamp:  Tue, 15 Mar 2016 14:48:04 -0700
  >     Labels:         app=nginx
  >     Selector:       app=nginx
  >     Replicas:       3 desired | 1 updated | 4 total | 3 available | 1 unavailable
  >     StrategyType:       RollingUpdate
  >     MinReadySeconds:    0
  >     RollingUpdateStrategy:  25% max unavailable, 25% max surge
  >     Pod Template:
  >       Labels:  app=nginx
  >       Containers:
  >        nginx:
  >         Image:        nginx:1.91
  >         Port:         80/TCP
  >         Host Port:    0/TCP
  >         Environment:  <none>
  >         Mounts:       <none>
  >       Volumes:        <none>
  >     Conditions:
  >       Type           Status  Reason
  >       ----           ------  ------
  >       Available      True    MinimumReplicasAvailable
  >       Progressing    True    ReplicaSetUpdated
  >     OldReplicaSets:     nginx-deployment-1564180365 (3/3 replicas created)
  >     NewReplicaSet:      nginx-deployment-3066724191 (1/1 replicas created)
  >     Events:
  >       FirstSeen LastSeen    Count   From                    SubObjectPath   Type        Reason              Message
  >       --------- --------    -----   ----                    -------------   --------    ------              -------
  >       1m        1m          1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-2035384211 to 3
  >       22s       22s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-1564180365 to 1
  >       22s       22s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled down replica set nginx-deployment-2035384211 to 2
  >       22s       22s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-1564180365 to 2
  >       21s       21s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled down replica set nginx-deployment-2035384211 to 1
  >       21s       21s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled up replica set nginx-deployment-1564180365 to 3
  >       13s       13s         1       {deployment-controller }                Normal      ScalingReplicaSet   Scaled down replica set … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
L’extrait explique le principe du retour arrière et l’historique des révisions, mais le texte fourni ne montre pas les commandes `kubectl rollout undo` ni l’option `--to-revision`. Ajouter les commandes de la section « Vérification de l’historique » et « Annulation à une révision précédente », ou retirer ces éléments de la réponse.


---

### `fr-scale`

**Question** (fr, command): Comment changer le nombre de réplicas d'un déploiement ?

**Reference answer:** `kubectl scale deployment.v1.apps/<nom> --replicas=<n>`.

**Relevant documentation:**
- `concepts/workloads/controllers/deployment.md`, section: *Déploiements > Mise à l'échelle d'un déploiement*
  > [Déploiements > Mise à l'échelle d'un déploiement]
  > Vous pouvez mettre à l'échelle un déploiement à l'aide de la commande suivante:
  > ```shell
  > kubectl scale deployment.v1.apps/nginx-deployment --replicas=10
  > ```
  > La sortie est similaire à ceci:
  > ```text
  > deployment.apps/nginx-deployment scaled
  > ```
  > En supposant que l'horizontal Pod autoscaling est activé dans votre cluster, vous pouvez configurer une mise à l'échelle automatique pour votre déploiement et choisir le nombre minimum et maximum de pods que vous souhaitez exécuter en fonction de l'utilisation du processeur de vos pods existants.
  > ```shell
  > kubectl autoscale deployment.v1.apps/nginx-deployment --min=10 --max=15 --cpu-percent=80
  > ```
  > La sortie est similaire à ceci:
  > ```text
  > deployment.apps/nginx-deployment scaled
  > ```
  > [Déploiements > Mise à l'échelle d'un déploiement > Mise à l'échelle proportionnelle]
  > Les déploiements RollingUpdate prennent en charge l'exécution simultanée de plusieurs versions d'une application.
  > Lorsque vous ou un autoscaler mettez à l'échelle un déploiement RollingUpdate qui se trouve au milieu d'un déploiement (en cours ou en pause), le contrôleur de déploiement équilibre les réplicas supplémentaires dans les ReplicaSets actifs existants (ReplicaSets avec pods) afin d'atténuer le risque.
  > Ceci est appelé *mise à l'échelle proportionnelle*.
  > Par exemple, vous exécutez un déploiement avec 10 réplicas, maxSurge=3, et maxUnavailable=2.
  > * Assurez-vous que les 10 réplicas de votre déploiement sont en cours d'exécution.
  >     ```shell
  >     kubectl get deploy
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     NAME                 DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
  >     nginx-deployment     10        10        10           10          50s
  >     ```
  > * Vous effectuez une mise à jour vers une nouvelle image qui s'avère impossible à résoudre depuis l'intérieur du cluster.
  >     ```shell
  >     kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:sometag
  >     ```
  >     La sortie est similaire à ceci:
  >     La sortie est similaire à ceci:
  >     ```text
  >     deployment.apps/nginx-deployment image updated
  >     ```
  > * La mise à jour de l'image démarre un nouveau déploiement avec ReplicaSet `nginx-deployment-1989198191`, mais elle est bloquée en raison de l'exigence `maxUnavailable` que vous avez mentionnée ci-dessus.
  >   Découvrez l'état du déploiement:
  >     ```shell
  >     kubectl get rs
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     NAME                          DESIRED   CURRENT   READY     AGE
  >     nginx-deployment-1989198191   5         5         0         9s
  >     nginx-deployment-618515232    8         8         8         1m
  >     ```
  > * Ensuite, une nouvelle demande de mise à l'échelle pour le déploiement arrive.
  >   La mise à l'échelle automatique incrémente les réplicas de déploiement à 15.
  >   Le contrôleur de déploiement doit décider où ajouter ces 5 nouvelles répliques.
  >   Si vous n'utilisiez pas la mise à l'échelle proportionnelle, les 5 seraient ajoutés dans le nouveau ReplicaSet.
  >   Avec une mise à l'échelle proportionnelle, vous répartissez les répliques supplémentaires sur tous les ReplicaSets.
  >   Des proportions plus importantes vont aux ReplicaSets avec le plus de répliques et des proportions plus faibles vont aux ReplicaSets avec moins de replicas.
  >   Tous les restes sont ajoutés au ReplicaSet avec le plus de répliques.
  >   Les ReplicaSets avec zéro réplicas ne sont pas mis à l'échelle.
  > Dans notre exemple ci-dessus, 3 répliques sont ajoutées à l'ancien ReplicaSet et 2 répliques sont ajoutées au nouveau ReplicaSet.
  > Le processus de déploiement devrait éventuellement déplacer toutes les répliques vers le nouveau ReplicaSet, en supposant que les nouvelles répliques deviennent saines.
  > Pour confirmer cela, exécutez:
  > ```shell
  > kubectl get deploy
  > ```
  > La sortie est similaire à ceci:
  > La sortie est similaire à ceci:
  > ```text
  > NAME                 DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
  > nginx-deployment     15        18        7            8           7m
  > ```
  > Le statut de déploiement confirme la façon dont les réplicas ont été ajoutés à chaque ReplicaSet.
  > ```shell
  > kubectl get rs
  > ```
  > La sortie est similaire à ceci:
  > ```text
  > NAME                          DESIRED   CURRENT   READY     AGE
  > nginx-deployment-1989198191   7         7         0         7m
  > nginx-deployment-618515232    11        11        11        7m
  > ```

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): used the exact documented syntax

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-service-types`

**Question** (fr, concept): Quels types de Service permettent d'exposer une application en dehors du cluster ?

**Reference answer:** NodePort, LoadBalancer et ExternalName ; ClusterIP (par défaut) reste interne au cluster.

**Relevant documentation:**
- `concepts/services-networking/service.md`, section: *Service > Services de publication (ServiceTypes)*
  > [Service > Services de publication (ServiceTypes) {#publishing-services-service-types}]
  > Pour certaines parties de votre application (par exemple, les frontaux), vous souhaiterez peut-être exposer un service sur une adresse IP externe, qui est en dehors de votre cluster.
  > Les «ServiceTypes» de Kubernetes vous permettent de spécifier le type de service que vous souhaitez.
  > La valeur par défaut est «ClusterIP».
  > Les valeurs de `Type` et leurs comportements sont:
  > Les valeurs de `Type` et leurs comportements sont:
  >    * `ClusterIP`: Expose le service sur une IP interne au cluster.
  >      Le choix de cette valeur rend le service uniquement accessible à partir du cluster.
  >      Il s'agit du `ServiceType` par défaut.
  >    * `NodePort`: Expose le service sur l'IP de chaque nœud sur un port statique (le `NodePort`).
  >      Un service `ClusterIP`, vers lequel le service `NodePort` est automatiquement créé.
  >      Vous pourrez contacter le service `NodePort`, depuis l'extérieur du cluster, en demandant `<NodeIP>: <NodePort>`.
  >    * `LoadBalancer`: Expose le service en externe à l'aide de l'équilibreur de charge d'un fournisseur de cloud.
  >      Les services `NodePort` et `ClusterIP`, vers lesquels les itinéraires de l'équilibreur de charge externe, sont automatiquement créés.
  >    * `ExternalName`: Mappe le service au contenu du champ `externalName` (par exemple `foo.bar.example.com`), en renvoyant un enregistrement `CNAME` avec sa valeur.
  >      Aucun proxy d'aucune sorte n'est mis en place.
  >      Vous avez besoin de CoreDNS version 1.7 ou supérieure pour utiliser le type `ExternalName`.
  >      Vous avez besoin de CoreDNS version 1.7 ou supérieure pour utiliser le type `ExternalName`.
  > Vous pouvez également utiliser Ingress pour exposer votre service.
  > Ingress n'est pas un type de service, mais il sert de point d'entrée pour votre cluster.
  > Il vous permet de consolider vos règles de routage en une seule ressource car il peut exposer plusieurs services sous la même adresse IP.
  > [Service > Services de publication (ServiceTypes) {#publishing-services-service-types} > Type NodePort {#type-nodeport}]
  > Si vous définissez le champ `type` sur` NodePort`, le plan de contrôle Kubernetes alloue un port à partir d'une plage spécifiée par l'indicateur `--service-node-port-range` (par défaut: 30000-32767).
  > Chaque nœud assure le proxy de ce port (le même numéro de port sur chaque nœud) vers votre service.
  > Votre service signale le port alloué dans son champ `.spec.ports[*].nodePort`.
  > Si vous souhaitez spécifier une ou des adresses IP particulières pour proxyfier le port, vous pouvez définir l'indicateur `--nodeport-addresses` dans kube-proxy sur des blocs IP particuliers; cela est pris en charge depuis Kubernetes v1.10.
  > Cet indicateur prend une liste délimitée par des virgules de blocs IP (par exemple 10.0.0.0/8, 192.0.2.0/25) pour spécifier les plages d'adresses IP que kube-proxy doit considérer comme locales pour ce nœud.
  > Par exemple, si vous démarrez kube-proxy avec l'indicateur `--nodeport-addresses=127.0.0.0/8`, kube-proxy sélectionne uniquement l'interface de boucle locale pour les services NodePort.
  > La valeur par défaut pour `--nodeport-addresses` est une liste vide.
  > Cela signifie que kube-proxy doit prendre en compte toutes les interfaces réseau disponibles pour NodePort (qui est également compatible avec les versions antérieures de Kubernetes).
  > Si vous voulez un numéro de port spécifique, vous pouvez spécifier une valeur dans le champ `nodePort`.
  > Le plan de contrôle vous attribuera ce port ou signalera l'échec de la transaction API.
  > Cela signifie que vous devez vous occuper vous-même des éventuelles collisions de ports.
  > Vous devez également utiliser un numéro de port valide, celui qui se trouve dans la plage configurée pour l'utilisation de NodePort.
  > L'utilisation d'un NodePort vous donne la liberté de configurer votre propre solution d'équilibrage de charge, de configurer des environnements qui ne sont pas entièrement pris en charge par Kubernetes, ou même d'exposer directement les adresses IP d'un ou plusieurs nœuds.
  > Notez que ce service est visible en tant que `<NodeIP>: spec.ports[*].nodePort` et `.spec.clusterIP: spec.ports[*].Port`.
  > (Si l'indicateur `--nodeport-addresses` dans kube-proxy est défini, <NodeIP> serait filtré NodeIP(s).)
  > [Service > Services de publication (ServiceTypes) {#publishing-services-service-types} > Type LoadBalancer {#loadbalancer}]
  > Sur les fournisseurs de cloud qui prennent en charge les load balancers externes, la définition du champ `type` sur` LoadBalancer` provisionne un load balancer pour votre service.
  > La création réelle du load balancer se produit de manière asynchrone et les informations sur le load balancer provisionné sont publiées dans le champ `.status.loadBalancer`.
  > Par exemple:
  > ```yaml
  > apiVersion: v1
  > kind: Service
  > metadata:
  >   name: my-service
  > spec:
  >   selector:
  >     app.kubernetes.io/name: MyApp
  >   ports:
  >     - protocol: TCP
  >       port: 80
  >       targetPort: 9376
  >   clusterIP: 10.0.171.239
  >   type: LoadBalancer
  > status:
  >   loadBalancer:
  >     ingress:
  >     - ip: 192.0.2.127
  > ```
  > Le trafic provenant du load balancer externe est dirigé vers les Pods backend.
  > Le fournisseur de cloud décide de la répartition de la charge.
  > Le trafic provenant du load balancer externe est dirigé vers les Pods backend.
  > Le fournisseur de cloud décide de la répartition de la charge.
  > Certains fournisseurs de cloud vous permettent de spécifier le `loadBalancerIP`.
  > Dans ces cas, le load balancer est créé avec le `loadBalancerIP` spécifié par l'utilisateur.
  > Si le champ `loadBalancerIP` n'est pas spécifié, le loadBalancer est configuré avec une adresse IP éphémère.
  > Si vous spécifiez un `loadBalancerIP` mais que votre fournisseur de cloud ne prend pas en charge la fonctionnalité, le champ `loadBalancerIP` que vous définissez est ignoré.
  > Si vous utilisez SCTP, voir le caveat ci-dessous sur le type de service `LoadBalancer`.
  > Sur **Azure**, si vous souhaitez utiliser un type public spécifié par l'utilisateur … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
`ExternalName` ne publie pas l’application hors du cluster : l’extrait indique qu’il associe le Service à un nom DNS/CNAME et qu’aucun proxy n’est configuré. Limiter les types qui exposent le service à l’extérieur à `NodePort` et `LoadBalancer`; expliquer `ExternalName` séparément comme alias DNS.


---

### `fr-labels-selectors`

**Question** (fr, concept): À quoi servent les labels et les sélecteurs dans Kubernetes ?

**Reference answer:** Les labels sont des paires clé/valeur attachées aux objets pour les organiser ; les sélecteurs permettent de choisir un ensemble d'objets par leurs labels.

**Relevant documentation:**
- `concepts/overview/working-with-objects/labels.md`, section: *Labels et sélecteurs > Motivation*
  > [Labels et sélecteurs > Motivation]
  > Les labels permettent aux utilisateurs de mapper leurs propres structures organisationnelles sur les objets système de manière lâchement couplée, sans nécessiter aux clients de stocker ces mappings.
  > Les déploiements de services et les pipelines de traitement par lots sont souvent des entités multidimensionnelles (par exemple, plusieurs partitions ou déploiements, plusieurs pistes de version, plusieurs niveaux, plusieurs micro-services par niveau). La gestion nécessite souvent des opérations transversales, ce qui rompt l'encapsulation des représentations strictement hiérarchiques, en particulier les hiérarchies rigides déterminées par l'infrastructure plutôt que par les utilisateurs.
  > Exemples de labels :
  > * `"release" : "stable"`, `"release" : "canary"`
  > * `"environment" : "dev"`, `"environment" : "qa"`, `"environment" : "production"`
  > * `"tier" : "frontend"`, `"tier" : "backend"`, `"tier" : "cache"`
  > * `"partition" : "customerA"`, `"partition" : "customerB"`
  > * `"track" : "daily"`, `"track" : "weekly"`
  > Voici des exemples de _label_ couramment utilisées; vous êtes libre de développer vos propres conventions. Gardez à l'esprit que la clé du _label_ doit être unique pour un objet donné.
- `concepts/overview/working-with-objects/labels.md`, section: *Labels et sélecteurs > Sélecteurs de labels*
  > [Labels et sélecteurs > Sélecteurs de labels]
  > Contrairement aux noms et UIDs, les labels ne garantissent pas l'unicité. En général, nous nous attendons à ce que de nombreux objets portent les mêmes label(s).
  > Via un _sélecteur de label_, le client/utilisateur peut identifier un ensemble d'objets.
  > Le sélecteur de label est le principe de regroupement central dans Kubernetes.
  > L'API prend actuellement en charge deux types de sélecteurs : _basés sur l'égalité_ et _basés sur un ensemble_.
  > Un sélecteur de label peut être composé de plusieurs _exigences_ séparées par des virgules.
  > Dans le cas de plusieurs exigences, toutes doivent être satisfaites, donc le séparateur de virgule
  > agit comme un opérateur logique _ET_ (`&&`).
  > La signification des sélecteurs vides ou non spécifiés dépend du contexte,
  > et les types d'API qui utilisent des sélecteurs doivent documenter leur validité et leur signification.
  > Pour certains types d'API, tels que les ReplicaSets, les sélecteurs de labels de deux instances ne doivent pas se chevaucher dans un namespace, sinon le contrôleur peut considérer cela comme des instructions contradictoires et échouer à déterminer combien de répliques doivent être présentes.
  > Pour les conditions basées sur l'égalité et les conditions basées sur un ensemble, il n'y a pas d'opérateur logique _OU_ (`||`).
  > Assurez-vous que vos déclarations de filtre sont structurées en conséquence.
  > [Labels et sélecteurs > Sélecteurs de labels > Exigence basée sur l'égalité]
  > Les exigences basées sur l'égalité ou l'inégalité permettent de filtrer par clés et valeurs de label.
  > Les objets correspondants doivent satisfaire toutes les contraintes de label spécifiées, bien qu'ils puissent également avoir des labels supplémentaires. Trois types d'opérateurs sont admis : `=`, `==`, `!=`.
  > Les deux premiers représentent l'égalité (et sont synonymes), tandis que le dernier représente l'inégalité.
  > Par exemple :
  > ```
  > environment = production
  > tier != frontend
  > ```
  > Le premier sélectionne toutes les ressources avec une clé égale à `environment` et une valeur égale à `production`.
  > Le second sélectionne toutes les ressources avec une clé égale à `tier` et une valeur différente de `frontend`,
  > ainsi que toutes les ressources sans labels avec la clé `tier`. On peut filtrer les ressources en `production`
  > en excluant `frontend` en utilisant l'opérateur virgule : `environment=production,tier!=frontend`
  > Un scénario d'utilisation pour une exigence de label basée sur l'égalité est de spécifier des critères de sélection de nœud pour les Pods. Par exemple, le Pod d'exemple ci-dessous sélectionne les nœuds où le label "accelerator" existe et est définie sur "nvidia-tesla-p100".
  > ```yaml
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: cuda-test
  > spec:
  >   containers:
  >     - name: cuda-test
  >       image: "registry.k8s.io/cuda-vector-add:v0.1"
  >       resources:
  >         limits:
  >           nvidia.com/gpu: 1
  >   nodeSelector:
  >     accelerator: nvidia-tesla-p100
  > ```
  > [Labels et sélecteurs > Sélecteurs de labels > Exigence basée sur un ensemble]
  > Les exigences basées sur un ensemble permettent de filtrer les clés en fonction d'un ensemble de valeurs.
  > Trois types d'opérateurs sont pris en charge : `in`, `notin` et `exists` (uniquement l'identifiant de clé).
  > Par exemple :
  > ```
  > environment in (production, qa)
  > tier notin (frontend, backend)
  > partition
  > !partition
  > ```
  > - Le premier exemple sélectionne toutes les ressources avec une clé égale à `environment` et une valeur égale à `production` ou `qa`.
  > - Le deuxième exemple sélectionne toutes les ressources avec une clé égale à `tier` et des valeurs autres que `frontend` et `backend`, ainsi que toutes les ressources sans labels avec la clé `tier`.
  > - Le troisième exemple sélectionne toutes les ressources incluant un label avec la clé `partition`; aucune valeur n'est vérifiée.
  > - Le quatrième exemple sélectionne toutes les ressources sans un label avec la clé `partition`; aucune valeur n'est vérifiée.
  > De même, le séparateur virgule agit comme un opérateur _ET_. Ainsi, pour filtrer les ressources avec une clé `partition` (peu importe la valeur) et avec `environment` différent de `qa`, vous pouvez utiliser `partition,environment notin (qa)`. Le sélecteur de label basé sur un ensemble est une forme générale d'égalité, car `environment=production` est équivalent à `environment in (production)`; de même pour `!=` et `notin`.
  > Les exigences basées sur un ensemble peuvent être mélangées avec des exigences basées sur l'égalité. Par exemple: `partition in (customerA, customerB),environment!=qa`.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged

**Decision** (tick one):
- [x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `oos-capital`

**Question** (en, out-of-scope): What is the capital of France?

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [x] ❌ Reject

**Notes:**
Confirmed out of scope: this is a geography question, not a Kubernetes question.


---

### `oos-python`

**Question** (en, out-of-scope): Write a Python function that reverses a string.

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [x] ❌ Reject

**Notes:**
Confirmed out of scope: this is a general Python programming task, not a Kubernetes question.


---

### `oos-docker-swarm`

**Question** (en, out-of-scope): How do I create an overlay network in Docker Swarm?

*Drafting note:* Adjacent domain: containers, but not Kubernetes.

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [x] ❌ Reject

**Notes:**
Confirmed out of scope: this concerns Docker Swarm networking, not Kubernetes.


---

### `oos-meteo`

**Question** (fr, out-of-scope): Quel temps fera-t-il à Paris demain ?

**Decision** (tick one):
- [ ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [x] ❌ Reject

**Notes:**
Confirmé hors périmètre : il s’agit d’une question de météo, pas d’une question Kubernetes.


---
